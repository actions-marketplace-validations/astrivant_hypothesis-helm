// Command random-renderer renders charts with replayable synthetic random inputs.
package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"sort"
	"strings"
	"text/template"
	"text/template/parse"

	"helm.sh/helm/v4/pkg/chart/common"
	commonutil "helm.sh/helm/v4/pkg/chart/common/util"
	chart "helm.sh/helm/v4/pkg/chart/v2"
	"helm.sh/helm/v4/pkg/chart/v2/loader"
	chartutil "helm.sh/helm/v4/pkg/chart/v2/util"
	"helm.sh/helm/v4/pkg/engine"
	releaseutil "helm.sh/helm/v4/pkg/release/v1/util"
)

const alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

// Draw describes one evaluated random call, separately from chart values.
type Draw struct {
	Path   string `json:"path"`
	Length int    `json:"length"`
	Value  string `json:"value"`
}

// Request supplies a chart, renderer context, and an exact prefix of random draws.
type Request struct {
	Chart       string          `json:"chart"`
	Values      json.RawMessage `json:"values"`
	Release     string          `json:"release"`
	Namespace   string          `json:"namespace"`
	KubeVersion string          `json:"kube_version"`
	Draws       []Draw          `json:"draws"`
	MaxChars    int             `json:"max_chars"`
	MaxCalls    int             `json:"max_calls"`
	Unsupported []string        `json:"unsupported"`
}

// Response distinguishes another requested input from a rendered result or chart error.
type Response struct {
	ChartDigest string `json:"chart_digest,omitempty"`
	Output      string `json:"output,omitempty"`
	Error       string `json:"error,omitempty"`
	Invalid     string `json:"invalid,omitempty"`
	Request     *Draw  `json:"request,omitempty"`
}

// Tape consumes values in execution order while retaining independent call-site identities.
type Tape struct {
	request   Request
	position  int
	counts    map[string]int
	next      *Draw
	invalid   string
	functions template.FuncMap
}

// function creates an override for one source call or an uninstrumented dynamic tpl call.
//
// Args:
//
//	site (string): Stable template source position, or the explicit dynamic-call namespace.
//
// Returns:
//
//	func(int) (string, error): A Helm-compatible function consuming one independent draw.
func (t *Tape) function(site string) func(int) (string, error) {
	return func(count int) (string, error) {
		// Sprig discards the error returned for negative counts and returns an empty string.
		if count <= 0 {
			return "", nil
		}
		if count > t.request.MaxChars || t.position >= t.request.MaxCalls {
			t.invalid = "random input exceeds configured character or invocation budget"
			return "", fmt.Errorf("%s", t.invalid)
		}
		occurrence := t.counts[site]
		t.counts[site]++
		path := fmt.Sprintf("$render.random[%q][%d]", site, occurrence)
		if t.position == len(t.request.Draws) {
			t.next = &Draw{Path: path, Length: count}
			return "", fmt.Errorf("synthetic random input requested")
		}
		draw := t.request.Draws[t.position]
		t.position++
		valid := draw.Path == path && draw.Length == count && len(draw.Value) == count
		for _, character := range draw.Value {
			valid = valid && strings.ContainsRune(alphabet, character)
		}
		if !valid {
			t.invalid = "random replay does not match this chart execution or randAlphaNum domain"
			return "", fmt.Errorf("%s", t.invalid)
		}
		return draw.Value, nil
	}
}

// instrument assigns a separate function closure to each random call using Go's syntax tree.
//
// Args:
//
//	c (*chart.Chart): Loaded chart, including prepared dependency archives.
//
// Returns:
//
//	error: Native parse error; nil when every original template is preserved or instrumented.
func (t *Tape) instrument(c *chart.Chart) error {
	for _, file := range c.Templates {
		if !bytes.Contains(file.Data, []byte("randAlphaNum")) {
			continue
		}
		name := c.ChartFullPath() + "/" + file.Name
		tree := parse.New(name)
		tree.Mode = parse.SkipFuncCheck
		trees := map[string]*parse.Tree{}
		if _, err := tree.Parse(string(file.Data), "{{", "}}", trees); err != nil {
			return err
		}
		// Locate calls with the native AST, then replace only their identifier tokens.
		// Keeping the surrounding bytes preserves whitespace, definitions and source lines.
		replacements := map[int]string{}
		var walk func(parse.Node, *parse.Tree)
		walk = func(node parse.Node, tree *parse.Tree) {
			if node == nil {
				return
			}
			switch n := node.(type) {
			case *parse.ListNode:
				if n != nil {
					for _, child := range n.Nodes {
						walk(child, tree)
					}
				}
			case *parse.ActionNode:
				walk(n.Pipe, tree)
			case *parse.IfNode:
				walk(n.Pipe, tree)
				walk(n.List, tree)
				walk(n.ElseList, tree)
			case *parse.WithNode:
				walk(n.Pipe, tree)
				walk(n.List, tree)
				walk(n.ElseList, tree)
			case *parse.RangeNode:
				walk(n.Pipe, tree)
				walk(n.List, tree)
				walk(n.ElseList, tree)
			case *parse.TemplateNode:
				if n.Pipe != nil {
					walk(n.Pipe, tree)
				}
			case *parse.PipeNode:
				for _, command := range n.Cmds {
					walk(command, tree)
				}
			case *parse.CommandNode:
				for _, argument := range n.Args {
					walk(argument, tree)
				}
			case *parse.ChainNode:
				walk(n.Node, tree)
			case *parse.IdentifierNode:
				if n.Ident == "randAlphaNum" {
					location, _ := tree.ErrorContext(n)
					site := name + "@" + location
					digest := sha256.Sum256([]byte(site))
					identifier := "hhRandom_" + hex.EncodeToString(digest[:])
					t.functions[identifier] = t.function(site)
					replacements[int(n.Position())] = identifier
				}
			}
		}
		for _, parsed := range trees {
			walk(parsed.Root, parsed)
		}
		if len(replacements) == 0 {
			continue
		}
		var offsets []int
		for offset := range replacements {
			offsets = append(offsets, offset)
		}
		sort.Sort(sort.Reverse(sort.IntSlice(offsets)))
		source := string(file.Data)
		for _, offset := range offsets {
			end := offset + len("randAlphaNum")
			if offset < 0 || end > len(source) || source[offset:end] != "randAlphaNum" {
				return fmt.Errorf("native parser returned an invalid random call position in %s", name)
			}
			source = source[:offset] + replacements[offset] + source[end:]
		}
		file.Data = []byte(source)
	}
	for _, dependency := range c.Dependencies() {
		if err := t.instrument(dependency); err != nil {
			return err
		}
	}
	return nil
}

// render evaluates one exact draw prefix with Helm's native loader, coalescer, schema checks and engine.
//
// Args:
//
//	request (Request): Chart inputs and configured analysis budgets.
//
// Returns:
//
//	Response: Complete manifests, the next synthetic draw, or an explicitly classified failure.
func render(request Request) (response Response) {
	c, err := loader.Load(request.Chart)
	if err != nil {
		return Response{Error: err.Error()}
	}
	digest := sha256.New()
	var hashChart func(*chart.Chart)
	hashChart = func(current *chart.Chart) {
		name := current.ChartFullPath()
		fmt.Fprintf(digest, "chart:%d:%s:", len(name), name)
		raw := append([]*common.File(nil), current.Raw...)
		sort.Slice(raw, func(i, j int) bool { return raw[i].Name < raw[j].Name })
		fmt.Fprintf(digest, "files:%d:", len(raw))
		for _, file := range raw {
			fmt.Fprintf(digest, "%d:%s:%d:", len(file.Name), file.Name, len(file.Data))
			digest.Write(file.Data)
		}
		// The loader collects dependencies through maps; execution order is not source identity.
		children := append([]*chart.Chart(nil), current.Dependencies()...)
		sort.Slice(children, func(i, j int) bool { return children[i].ChartFullPath() < children[j].ChartFullPath() })
		fmt.Fprintf(digest, "children:%d:", len(children))
		for _, child := range children {
			hashChart(child)
		}
	}
	hashChart(c)
	chartDigest := hex.EncodeToString(digest.Sum(nil))
	defer func() { response.ChartDigest = chartDigest }()
	values, err := loader.LoadValues(bytes.NewReader(request.Values))
	if err != nil {
		return Response{Error: err.Error()}
	}
	if err = chartutil.ProcessDependencies(c, values); err != nil {
		return Response{Error: err.Error()}
	}
	caps := common.DefaultCapabilities.Copy()
	caps.HelmVersion.Version = "v4.3.0"
	if request.KubeVersion != "" {
		version, err := common.ParseKubeVersion(request.KubeVersion)
		if err != nil {
			return Response{Error: err.Error()}
		}
		caps.KubeVersion = *version
	}
	context, err := commonutil.ToRenderValues(c, values, common.ReleaseOptions{
		Name: request.Release, Namespace: request.Namespace, Revision: 1, IsInstall: true,
	}, caps)
	if err != nil {
		return Response{Error: err.Error()}
	}
	tape := &Tape{request: request, counts: map[string]int{}, functions: template.FuncMap{}}
	tape.functions["randAlphaNum"] = tape.function("dynamic:randAlphaNum")
	for _, name := range request.Unsupported {
		tape.functions[name] = func(...any) (any, error) {
			tape.invalid = "synthetic random replay does not support native effect: " + name
			return nil, fmt.Errorf("%s", tape.invalid)
		}
	}
	if err = tape.instrument(c); err != nil {
		return Response{Error: err.Error()}
	}
	renderer := engine.Engine{CustomTemplateFuncs: tape.functions}
	output, err := renderer.Render(c, context)
	if tape.invalid != "" {
		return Response{Invalid: tape.invalid}
	}
	if tape.next != nil {
		return Response{Request: tape.next}
	}
	if err != nil {
		return Response{Error: err.Error()}
	}
	if tape.position != len(request.Draws) {
		return Response{Invalid: "random replay contains unused draws"}
	}
	for name := range output {
		if strings.HasSuffix(name, "NOTES.txt") {
			delete(output, name)
		}
	}
	hooks, manifests, err := releaseutil.SortManifests(output, caps.APIVersions, releaseutil.InstallOrder)
	if err != nil {
		return Response{Error: err.Error()}
	}
	var result strings.Builder
	for _, manifest := range manifests {
		fmt.Fprintf(&result, "---\n# Source: %s\n%s\n", manifest.Name, strings.TrimSpace(manifest.Content))
	}
	for _, hook := range hooks {
		fmt.Fprintf(&result, "---\n# Source: %s\n%s\n", hook.Path, strings.TrimSpace(hook.Manifest))
	}
	return Response{Output: result.String()}
}

// main reads one bounded render request and emits a single machine-readable response.
//
// Returns:
//
//	No value. Malformed protocol input or output failures exit with status one.
func main() {
	var request Request
	if err := json.NewDecoder(os.Stdin).Decode(&request); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	if err := json.NewEncoder(os.Stdout).Encode(render(request)); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
