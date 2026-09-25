// Command random-renderer renders charts with replayable random and native crypto inputs.
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

// Draw exchanges one random input or native certificate observation, separately from chart values.
type Draw struct {
	Path      string          `json:"path"`
	Length    int             `json:"length"`
	Value     string          `json:"value"`
	Function  string          `json:"function,omitempty"`
	Arguments json.RawMessage `json:"arguments,omitempty"`
	Result    json.RawMessage `json:"result,omitempty"`
	Error     string          `json:"error,omitempty"`
	Generate  bool            `json:"generate,omitempty"`
}

// Request supplies a chart, renderer context, and a stream of random draws.
type Request struct {
	Chart       string          `json:"chart"`
	Values      json.RawMessage `json:"values"`
	Release     string          `json:"release"`
	Namespace   string          `json:"namespace"`
	KubeVersion string          `json:"kube_version"`
	MaxChars    int             `json:"max_chars"`
	MaxCalls    int             `json:"max_calls"`
	MaxBytes    int             `json:"max_bytes"`
	Unsupported []string        `json:"unsupported"`
}

// Response distinguishes another requested input from a rendered result or chart error.
type Response struct {
	ChartDigest string `json:"chart_digest,omitempty"`
	Output      string `json:"output,omitempty"`
	Error       string `json:"error,omitempty"`
	Invalid     string `json:"invalid,omitempty"`
	Request     *Draw  `json:"request,omitempty"`
	Unavailable string `json:"unavailable,omitempty"`
	Ready       bool   `json:"ready,omitempty"`
}

// Tape consumes values in execution order while retaining independent call-site identities.
type Tape struct {
	request     Request
	position    int
	counts      map[string]int
	exchange    func(Draw) (Draw, error)
	unavailable string
	invalid     string
	functions   template.FuncMap
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
			t.unavailable = "random input exceeds configured character or invocation budget"
			return "", fmt.Errorf("%s", t.unavailable)
		}
		occurrence := t.counts[site]
		t.counts[site]++
		path := fmt.Sprintf("$render.random[%q][%d]", site, occurrence)
		draw, err := t.exchange(Draw{Path: path, Length: count})
		if err != nil {
			t.invalid = "random input stream failed: " + err.Error()
			return "", err
		}
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
		selected := bytes.Contains(file.Data, []byte("randAlphaNum"))
		for name := range certificateFunctions {
			selected = selected || bytes.Contains(file.Data, []byte(name))
		}
		if !selected {
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
		type replacement struct{ name, original string }
		replacements := map[int]replacement{}
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
				if n.Ident == "randAlphaNum" || certificateFunctions[n.Ident] != nil {
					location, _ := tree.ErrorContext(n)
					site := name + "@" + location
					digest := sha256.Sum256([]byte(site))
					identifier := "hhRandom_" + hex.EncodeToString(digest[:])
					if n.Ident == "randAlphaNum" {
						t.functions[identifier] = t.function(site)
					} else {
						t.functions[identifier] = t.certificateFunction(n.Ident, site)
					}
					replacements[int(n.Position())] = replacement{identifier, n.Ident}
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
			change := replacements[offset]
			end := offset + len(change.original)
			if offset < 0 || end > len(source) || source[offset:end] != change.original {
				return fmt.Errorf("native parser returned an invalid random call position in %s", name)
			}
			source = source[:offset] + change.name + source[end:]
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

// render evaluates one chart with interactive random draws with Helm's native loader, coalescer, schema checks and engine.
//
// Args:
//
//	request (Request): Chart inputs and configured analysis budgets.
//	decoder (*json.Decoder): Replies from the draw owner.
//	encoder (*json.Encoder): Requests and provenance sent to the draw owner.
//
// Returns:
//
//	Response: Complete manifests, the next synthetic draw, or an explicitly classified failure.
func render(request Request, decoder *json.Decoder, encoder *json.Encoder) (response Response) {
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
	// Publish source identity before asking for a draw, so a stale replay cannot execute.
	if err := encoder.Encode(Response{ChartDigest: chartDigest, Ready: true}); err != nil {
		return Response{Invalid: err.Error()}
	}
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
	tape.exchange = func(call Draw) (Draw, error) {
		if err := encoder.Encode(Response{Request: &call}); err != nil {
			return Draw{}, err
		}
		var reply Draw
		err := decoder.Decode(&reply)
		return reply, err
	}
	tape.functions["randAlphaNum"] = tape.function("dynamic:randAlphaNum")
	for name := range certificateFunctions {
		tape.functions[name] = tape.certificateFunction(name, "dynamic:"+name)
	}
	for _, name := range request.Unsupported {
		tape.functions[name] = func(...any) (any, error) {
			tape.unavailable = "controlled renderer does not support native effect: " + name
			return nil, fmt.Errorf("%s", tape.unavailable)
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
	if tape.unavailable != "" {
		return Response{Unavailable: tape.unavailable}
	}
	if err != nil {
		return Response{Error: err.Error()}
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

// main keeps one native render alive while exchanging draws, then emits its terminal result.
//
// Returns:
//
//	No value. Malformed protocol input or output failures exit with status one.
func main() {
	decoder := json.NewDecoder(os.Stdin)
	encoder := json.NewEncoder(os.Stdout)
	var request Request
	if err := decoder.Decode(&request); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	if err := encoder.Encode(render(request, decoder, encoder)); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
