package main

import (
	"os"
	"path/filepath"
	"slices"
	"testing"
)

func fixture(t *testing.T, code string) source {
	t.Helper()
	root := t.TempDir()
	if err := os.WriteFile(filepath.Join(root, "functions.go"), []byte(code), 0600); err != nil {
		t.Fatal(err)
	}
	return source{Provider: "fixture", Directory: root, Map: "genericMap"}
}

func TestNewFunctionsAndAliasesFollowSources(t *testing.T) {
	src := fixture(t, `package fixture
import "crypto/rand"
var genericMap = map[string]any{"newName": wrapper, "alias": wrapper, "newShape": object}
func wrapper(values map[string]any) string { change(values); return "ok" }
func change(values map[string]any) { values["secret"] = rand.Reader }
type result struct { Name string; hidden bool }
func object() result { return result{} }
`)
	result, _, err := extract([]source{src})
	if err != nil {
		t.Fatal(err)
	}
	for _, name := range []string{"newName", "alias"} {
		f := result[name]
		if !slices.Contains(f.Effects, "mutation") || !slices.Contains(f.Effects, "randomness") {
			t.Fatalf("effects not propagated: %+v", f)
		}
		if f.Shape != "scalar" || f.Signature == "" || f.SHA256 == "" || len(f.Evidence) == 0 {
			t.Fatalf("missing source facts: %+v", f)
		}
	}
	if f := result["newShape"]; f.Shape != "record" || !slices.Equal(f.Fields, []string{"Name"}) {
		t.Fatalf("record fields: %+v", f)
	}
}

func TestUnknownCallNeverBecomesPurityEvidence(t *testing.T) {
	src := fixture(t, `package fixture
import "example.com/unknown"
var genericMap = map[string]any{"wrapper": wrapper}
func wrapper(x any) string { return unknown.Execute(x) }
`)
	result, _, err := extract([]source{src})
	if err != nil {
		t.Fatal(err)
	}
	if !slices.Contains(result["wrapper"].Unresolved, "example.com/unknown.Execute") {
		t.Fatal(result)
	}
}

func TestSourceChangeChangesShapeAndFingerprint(t *testing.T) {
	before := fixture(t, `package fixture
var genericMap = map[string]any{"value": value}
func value() string { return "one" }
`)
	a, _, err := extract([]source{before})
	if err != nil {
		t.Fatal(err)
	}
	after := fixture(t, `package fixture
var genericMap = map[string]any{"value": value}
func value() []string { return []string{"one"} }
`)
	b, _, err := extract([]source{after})
	if err != nil {
		t.Fatal(err)
	}
	if a["value"].Shape != "scalar" || b["value"].Shape != "sequence" || a["value"].SHA256 == b["value"].SHA256 {
		t.Fatal(a, b)
	}
}

func TestRendererOverrideRetainsEnabledImplementation(t *testing.T) {
	base := fixture(t, `package fixture
import "net"
var genericMap = map[string]any{"getHostByName": lookup, "env": lookup}
func lookup(name string) string { net.LookupHost(name); return name }
`)
	override := fixture(t, `package fixture
var genericMap = map[string]any{"other": func() bool { return true }}
func funcMap() { f:=map[string]any{}; delete(f,"env") }
type Engine struct { DNS bool }
func (e Engine) initFunMap() {
 funcMap:=map[string]any{}
 if !e.DNS { funcMap["getHostByName"] = func(_ string) string { return "" } }
}
`)
	result, removed, err := extract([]source{base, override})
	if err != nil {
		t.Fatal(err)
	}
	if _, exists := result["env"]; exists || !slices.Contains(removed, "env") {
		t.Fatal(result, removed)
	}
	if !slices.Contains(result["getHostByName"].Effects, "external-state") {
		t.Fatal("lost conditional renderer effect", result)
	}
}

func TestDynamicMapDefinitionFailsRebuild(t *testing.T) {
	src := fixture(t, `package fixture; var genericMap = createMap()`)
	if _, _, err := extract([]source{src}); err == nil {
		t.Fatal("silently accepted changed upstream registration syntax")
	}
}

func TestRecursiveCallsTerminateAndRetainEffects(t *testing.T) {
	src := fixture(t, `package fixture
import "time"
var genericMap = map[string]any{"a": a}
func a() string { return b() }
func b() string { time.Now(); return a() }
`)
	result, _, err := extract([]source{src})
	if err != nil {
		t.Fatal(err)
	}
	if !slices.Contains(result["a"].Effects, "clock-or-timezone") {
		t.Fatal(result)
	}
}

func TestMapProjectionDiffersFromOrderDependentSelection(t *testing.T) {
	src := fixture(t, `package fixture
var genericMap = map[string]any{"project": project, "first": first}
func project(input map[string]any, excluded map[string]bool) map[string]any {
 result := map[string]any{}
 for key, value := range input { if !excluded[key] { result[key] = value } }
 return result
}
func first(input map[string]any) map[string]any {
 result := map[string]any{}
 for key, value := range input { result[key] = value; break }
 return result
}
`)
	result, _, err := extract([]source{src})
	if err != nil {
		t.Fatal(err)
	}
	if slices.Contains(result["project"].Effects, "unordered") {
		t.Fatal(result["project"])
	}
	if !slices.Contains(result["first"].Effects, "unordered") {
		t.Fatal(result["first"])
	}
}
