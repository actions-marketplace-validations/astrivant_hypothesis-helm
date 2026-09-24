package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"flag"
	"io"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

// TestHelmCommand dispatches function extraction through the shared entry point.
//
// Args:
//
//	t (*testing.T): Test assertions and isolated source fixtures.
func TestHelmCommand(t *testing.T) {
	src := fixture(t, `package fixture
var genericMap = map[string]any{"hello": hello}
func hello() string { return "world" }
`)
	config := filepath.Join(t.TempDir(), "sources.json")
	data, err := json.Marshal([]source{src})
	if err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(config, data, 0600); err != nil {
		t.Fatal(err)
	}
	var output bytes.Buffer
	if err := run([]string{"--config", config}, strings.NewReader(""), &output, io.Discard); err != nil {
		t.Fatal(err)
	}
	var result struct {
		Functions map[string]facts `json:"functions"`
	}
	if err := json.Unmarshal(output.Bytes(), &result); err != nil {
		t.Fatal(err)
	}
	if result.Functions["hello"].Shape != "scalar" {
		t.Fatal(result)
	}
}

// TestOracleCommand preserves JSON Lines validation across repeated invocations.
//
// Args:
//
//	t (*testing.T): Test assertions and input/output buffers.
func TestOracleCommand(t *testing.T) {
	for _, test := range []struct{ input, expected string }{
		{`{"profile":"port-number","value":0}
{"profile":"port-number","value":1}
{"profile":"port-number","value":65536}
`, "false\ntrue\nfalse\n"},
		{`{"profile":"dns1123-subdomain","value":"my-config"}
{"profile":"dns1123-subdomain","value":"I\n&"}
`, "true\nfalse\n"},
		{`{"profile":"pdb-count-or-percent","value":"100%"}
{"profile":"pdb-count-or-percent","value":"101%"}
`, "true\nfalse\n"},
		{`{"profile":"port-number-or-name","value":"http"}
{"profile":"port-number-or-name","value":"I\n&"}
{"profile":"port-number-or-name","value":1}
{"profile":"port-number-or-name","value":65536}
{"profile":"port-number-or-name","value":"http--api"}
{"profile":"port-number-or-name","value":null}
{"profile":"port-number-or-name","value":true}
{"profile":"port-number-or-name","value":"123"}
`, "true\nfalse\ntrue\nfalse\nfalse\nfalse\nfalse\nfalse\n"},
	} {
		var output bytes.Buffer
		if err := run([]string{"--oracle"}, strings.NewReader(test.input), &output, io.Discard); err != nil {
			t.Fatal(err)
		}
		if output.String() != test.expected {
			t.Fatalf("unexpected oracle results: %q", output.String())
		}
	}
}

// TestInvalidCommandSelection rejects ambiguous operations before inspecting sources.
//
// Args:
//
//	t (*testing.T): Test assertions for argument errors.
func TestInvalidCommandSelection(t *testing.T) {
	for _, args := range [][]string{
		{}, {"--source", "missing", "--config", "missing"},
		{"--oracle", "--source", "missing"}, {"--oracle", "--config", "missing"},
		{"--oracle", "unexpected"}, {"--unknown"},
	} {
		var output bytes.Buffer
		if err := run(args, strings.NewReader(""), &output, io.Discard); err == nil {
			t.Fatalf("accepted invalid flags: %v", args)
		}
		if output.Len() != 0 {
			t.Fatalf("invalid command emitted catalog data: %v", args)
		}
	}
	if err := run([]string{"--help"}, strings.NewReader(""), io.Discard, io.Discard); !errors.Is(err, flag.ErrHelp) {
		t.Fatalf("help must remain a successful CLI request: %v", err)
	}
}

// TestOracleRejectsMalformedInput reports incomplete JSON instead of accepting partial cases.
//
// Args:
//
//	t (*testing.T): Test assertions for input errors.
func TestOracleRejectsMalformedInput(t *testing.T) {
	if err := run([]string{"--oracle"}, strings.NewReader(`{"profile":`), io.Discard, io.Discard); err == nil {
		t.Fatal("malformed input did not fail")
	}
}
