"""
Describe randAlphaNum's output domain without treating sampled values as equality proofs.
"""

from collections.abc import Callable
from contextvars import ContextVar, Token
from types import TracebackType

from hypothesis import strategies as st
from hypothesis.strategies import SearchStrategy

from hypothesis_helm.exceptions.rendering import RandomInputUnavailable
from hypothesis_helm.schemas.contracts import mapping, sequence

__all__ = ("ALPHABET", "CURRENT", "RandomInputs", "RandomOutput", "domain")

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
CURRENT: ContextVar["RandomInputs | None"] = ContextVar("renderer_random_inputs", default=None)


def domain(length: int) -> SearchStrategy[str]:
    """
    Generate only strings the pinned Sprig randAlphaNum implementation can return.

    Args:
        length (int): Evaluated native integer argument, already checked against the execution budget.

    Returns:
        SearchStrategy[str]: Fixed-length ASCII alphanumerics, or the native empty result for nonpositive counts.
    """
    return st.text(alphabet=ALPHABET, min_size=max(0, length), max_size=max(0, length))


class RandomInputs:
    """
    Own one property example's draws, retaining an exact tape for failure replay.

    Attributes:
        draw (Callable[[SearchStrategy[str], str], str] | None): Hypothesis draw callback; absent for deterministic baseline renders.
        replay (list[dict[str, object]] | None): Exact saved tape; missing or unused entries are errors.
        records (list[dict[str, object]]): Actual call identities, lengths and values from the latest render.
        context (dict[str, object]): Source, overrides and renderer identities for portable replay verification.
        expected_context (dict[str, object] | None): Frozen context required by an imported replay artifact.
    """

    draw: Callable[[SearchStrategy[str], str], str] | None
    replay: list[dict[str, object]] | None
    records: list[dict[str, object]]
    context: dict[str, object]
    expected_context: dict[str, object] | None

    def __init__(
        self, draw: Callable[[SearchStrategy[str], str], str] | None = None, *, replay: list[dict[str, object]] | None = None
    ) -> None:
        """
        Retain a draw context or a strict replay tape independently of chart values.

        Args:
            draw (Callable[[SearchStrategy[str], str], str] | None): Seeded Hypothesis draw callback.
            replay (list[dict[str, object]] | None): Saved ordered draw records, including source paths.
        """
        self.draw = draw
        self.replay = replay
        self.records: list[dict[str, object]] = []
        self.context: dict[str, object] = {}
        self.expected_context: dict[str, object] | None = None
        self._token: Token[RandomInputs | None] | None = None

    def __enter__(self) -> "RandomInputs":
        """
        Expose this example's random domain to its native render invocations.

        Returns:
            RandomInputs: The active tape owner.
        """
        self._token = CURRENT.set(self)
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None) -> None:
        """
        Restore the parent example after success, failure, shrinking or cancellation.

        Args:
            exc_type (type[BaseException] | None): Propagating exception type.
            exc (BaseException | None): Propagating exception instance.
            traceback (TracebackType | None): Propagating exception traceback.

        Returns:
            None: Context is restored without suppressing the exception.
        """
        from hypothesis_helm.exceptions.rendering import RenderFailure

        if isinstance(exc, RenderFailure) and (self.records or exc.random_inputs is None):
            exc.random_inputs = self.document()
        if self._token is not None:
            CURRENT.reset(self._token)
            self._token = None

    def next(self, request: dict[str, object]) -> dict[str, object]:
        """
        Draw or replay the next call, preserving its exact native length and source identity.

        Args:
            request (dict[str, object]): The native renderer's next requested call.

        Returns:
            dict[str, object]: Validated draw metadata and selected value.

        Raises:
            ValueError: Replay is incomplete, diverges from native control flow, or violates the source function's domain.
        """
        length = int(str(request["length"]))
        path = str(request["path"])
        if self.replay is not None:
            if len(self.records) >= len(self.replay):
                raise RandomInputUnavailable(f"Random replay has no draw for {path}")
            record = self.replay[len(self.records)]
            if record.get("path") != path or record.get("length") != length:
                raise RandomInputUnavailable(f"Random replay diverged at {path}")
            value = record.get("value")
        else:
            # Defaults/finite plans use a documented representative, not claimed random coverage.
            value = self.draw(domain(length), path) if self.draw is not None else "0" * length
        if not isinstance(value, str) or len(value) != length or any(character not in ALPHABET for character in value):
            raise RandomInputUnavailable(f"Random input violates randAlphaNum's domain at {path}")
        record = {"path": path, "length": length, "value": value}
        self.records.append(record)
        return record

    @classmethod
    def from_document(cls, document: object) -> "RandomInputs":
        """
        Load the versioned replay artifact rather than accepting arbitrary values overrides.

        Args:
            document (object): Parsed JSON replay artifact.

        Returns:
            RandomInputs: Strict replay owner.
        """
        data = mapping(document)
        if data.get("format") != "helm-random-inputs-v1" or data.get("renderer") != "helm-4.3.0":
            raise ValueError("Unsupported random-input replay format or renderer version")
        case = cls(replay=[mapping(record) for record in sequence(data["draws"])])
        case.expected_context = mapping(data["context"])
        return case

    def document(self) -> dict[str, object]:
        """
        Export source positions and exact draws without claiming exhaustive stochastic coverage.

        Returns:
            dict[str, object]: JSON-compatible replay document with the renderer contract version.
        """
        return {"format": "helm-random-inputs-v1", "renderer": "helm-4.3.0", "context": dict(self.context), "draws": list(self.records)}


class RandomOutput(str):
    """
    Carry a render's input tape across worker boundaries alongside its ordinary YAML text.

    Attributes:
        random_inputs (dict[str, object]): Draws that produced this particular output.
    """

    random_inputs: dict[str, object]

    def __new__(cls, output: str, random_inputs: dict[str, object]) -> "RandomOutput":
        """
        Preserve the string interface used by parsers and attach replay provenance.

        Args:
            output (str): Native Helm YAML.
            random_inputs (dict[str, object]): Source identities and draw tape.

        Returns:
            RandomOutput: YAML with its matching synthetic inputs.
        """
        result = super().__new__(cls, output)
        result.random_inputs = random_inputs
        return result
