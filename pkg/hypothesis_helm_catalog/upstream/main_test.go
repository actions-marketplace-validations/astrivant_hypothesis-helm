package main

import (
	"os"
	"path/filepath"
	"testing"
)

func TestIndependentFieldAnnotations(t *testing.T) {
	root := t.TempDir()
	relative := "staging/src/k8s.io/api/example/v1/types.go"
	file := filepath.Join(root, relative)
	if err := os.MkdirAll(filepath.Dir(file), 0755); err != nil {
		t.Fatal(err)
	}
	source := `package v1
 type Settings struct {
    // +k8s:minimum=1
    Count *int32 ` + "`json:\"count,omitempty\"`" + `
    // +k8s:maxLength=63
    Name string ` + "`json:\"name\"`" + `
    // +k8s:ifEnabled(Feature):minimum=2
    Conditional int32 ` + "`json:\"conditional\"`" + `
    // +k8s:minimum=1
    Duration Duration ` + "`json:\"duration\"`" + `
    // +k8s:minimum=2
    Items []int32 ` + "`json:\"items\"`" + `
    // +k8s:maximum=3
    Private int32
 }
`
	if err := os.WriteFile(file, []byte(source), 0600); err != nil {
		t.Fatal(err)
	}
	rules, unresolved, hashes := fields(root)
	if len(rules) != 2 || len(unresolved) != 4 {
		t.Fatalf("unexpected extraction: %v, %v", rules, unresolved)
	}
	count := rules["io.k8s.api.example.v1.Settings/count"].([]Record)[0]
	if count["schema"].(Record)["minimum"] != 1 || count["file"] != relative {
		t.Fatalf("missing bound or provenance: %v", count)
	}
	name := rules["io.k8s.api.example.v1.Settings/name"].([]Record)[0]
	if name["schema"].(Record)["maxLength"] != 63 {
		t.Fatalf("missing length bound: %v", name)
	}
	if hashes[relative] != hash([]byte(source)) {
		t.Fatal("source digest mismatch")
	}
	for _, row := range unresolved {
		if row["reason"] == nil || row["line"] == nil {
			t.Fatalf("unexplained omission: %v", row)
		}
	}
}

func TestChangedValidatorChangesCanonicalIdentity(t *testing.T) {
	file := filepath.Join(t.TempDir(), "validation.go")
	write := func(source string) string {
		t.Helper()
		if err := os.WriteFile(file, []byte(source), 0600); err != nil {
			t.Fatal(err)
		}
		_, functions := declarations(file)
		return canonical(functions["valid"])
	}
	first := write("package validation; func valid(port int) bool { return 1 <= port && port <= 65535 }")
	formatted := write("package validation\nfunc valid(port int) bool {\nreturn 1 <= port && port <= 65535\n}")
	changed := write("package validation; func valid(port int) bool { return 0 <= port && port <= 65535 }")
	if first != formatted || first == changed {
		t.Fatal("validator identities must ignore formatting and detect changed bounds")
	}
}
