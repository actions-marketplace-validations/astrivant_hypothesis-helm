"""
Exchange bounded-time JSON frames with an owned renderer without restarting Helm for each draw.
"""

import json
import os
import selectors
import subprocess
import time
from collections.abc import Callable

from hypothesis_helm.exceptions.rendering import RandomInputUnavailable
from hypothesis_helm.schemas.contracts import mapping

__all__ = ("exchange",)


def exchange(
    child: subprocess.Popen[str],
    payload: dict[str, object],
    receive: Callable[[dict[str, object]], dict[str, object] | None],
    deadline: float,
) -> tuple[str, str]:
    """
    Feed draw replies on the calling thread while draining both child output pipes.

    Args:
        child (subprocess.Popen[str]): Child registered with the caller's process owner.
        payload (dict[str, object]): Initial chart render request.
        receive (Callable[[dict[str, object]], dict[str, object] | None]): Frame handler returning a draw reply when needed.
        deadline (float): Shared monotonic deadline, including all draws and any fallback.

    Returns:
        tuple[str, str]: Last JSON frame and captured native diagnostics.

    Raises:
        RandomInputUnavailable: A child exits without a result or emits an invalid protocol frame.
        subprocess.TimeoutExpired: The complete render's deadline expires.
    """
    assert child.stdin is not None and child.stdout is not None and child.stderr is not None
    incoming = bytearray()
    outgoing = bytearray((json.dumps(payload) + "\n").encode())
    errors = bytearray()
    terminal = ""
    with selectors.DefaultSelector() as selector:
        for stream in (child.stdin, child.stdout, child.stderr):
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_WRITE if stream is child.stdin else selectors.EVENT_READ)
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise subprocess.TimeoutExpired(child.args, 0)
            for key, _ in selector.select(remaining):
                ready_stream = key.fileobj
                if ready_stream is child.stdin:
                    written = os.write(key.fd, outgoing)
                    del outgoing[:written]
                    if not outgoing:
                        selector.unregister(ready_stream)
                    continue
                data = os.read(key.fd, 65536)
                if not data:
                    selector.unregister(ready_stream)
                    continue
                if ready_stream is child.stderr:
                    # Diagnostics must not block a renderer with a full stderr pipe.
                    errors.extend(data)
                    continue
                incoming.extend(data)
                while b"\n" in incoming:
                    frame, _, rest = incoming.partition(b"\n")
                    incoming = bytearray(rest)
                    try:
                        message = mapping(json.loads(frame))
                    except (ValueError, UnicodeError) as exc:
                        raise RandomInputUnavailable("Invalid controlled renderer response") from exc
                    reply = receive(message)
                    if reply is not None:
                        outgoing.extend((json.dumps(reply) + "\n").encode())
                        selector.register(child.stdin, selectors.EVENT_WRITE)
                    elif not message.get("ready"):
                        terminal = frame.decode()
        if incoming or not terminal:
            raise RandomInputUnavailable("Controlled renderer closed without a complete result")
    return terminal, errors.decode(errors="replace")
