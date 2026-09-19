// Command builtins extracts template function facts from pinned upstream Go ASTs.
// This is deliberately not a Go interpreter: unresolved calls remain explicit.
package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"flag"
	"fmt"
	"go/ast"
	"go/parser"
	"go/printer"
	"go/token"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
)

type source struct {
	Provider  string `json:"provider"`
	Directory string `json:"directory"`
	Map       string `json:"map"`
}

type unit struct {
	file    string
	imports map[string]string
	node    *ast.File
}

type function struct {
	typ  *ast.FuncType
	body *ast.BlockStmt
	u    *unit
	name string
}

type packageSource struct {
	set       *token.FileSet
	units     []*unit
	functions map[string]*function
	types     map[string]ast.Expr
	provider  string
}

type binding struct {
	expr ast.Expr
	u    *unit
}

type facts struct {
	Provider       string   `json:"provider"`
	Implementation string   `json:"implementation"`
	Signature      string   `json:"signature"`
	Shape          string   `json:"shape"`
	Fields         []string `json:"fields"`
	Effects        []string `json:"effects"`
	Unresolved     []string `json:"unresolved"`
	Calls          []string `json:"calls"`
	Evidence       []string `json:"evidence"`
	Source         string   `json:"source"`
	Line           int      `json:"line"`
	SHA256         string   `json:"sha256"`
}

type summary struct {
	effects    map[string]bool
	unresolved map[string]bool
	calls      map[string]bool
	evidence   map[string]bool
}

func newSummary() *summary {
	return &summary{map[string]bool{}, map[string]bool{}, map[string]bool{}, map[string]bool{}}
}

func keys(values map[string]bool) []string {
	result := make([]string, 0, len(values))
	for key := range values {
		result = append(result, key)
	}
	sort.Strings(result)
	return result
}

func text(node ast.Node) string {
	var output bytes.Buffer
	if node != nil {
		_ = printer.Fprint(&output, token.NewFileSet(), node)
	}
	return output.String()
}

func digest(data []byte) string {
	hash := sha256.Sum256(data)
	return hex.EncodeToString(hash[:])
}

func read(source source) (*packageSource, error) {
	p := &packageSource{set: token.NewFileSet(), functions: map[string]*function{}, types: map[string]ast.Expr{}, provider: source.Provider}
	paths, err := filepath.Glob(filepath.Join(source.Directory, "*.go"))
	if err != nil {
		return nil, err
	}
	for _, path := range paths {
		if strings.HasSuffix(path, "_test.go") {
			continue
		}
		node, err := parser.ParseFile(p.set, path, nil, parser.ParseComments)
		if err != nil {
			return nil, err
		}
		u := &unit{filepath.Base(path), map[string]string{}, node}
		for _, imp := range node.Imports {
			value, err := strconv.Unquote(imp.Path.Value)
			if err != nil {
				return nil, err
			}
			name := filepath.Base(value)
			if imp.Name != nil {
				name = imp.Name.Name
			}
			u.imports[name] = value
		}
		p.units = append(p.units, u)
		for _, raw := range node.Decls {
			switch decl := raw.(type) {
			case *ast.FuncDecl:
				if decl.Recv == nil {
					p.functions[decl.Name.Name] = &function{decl.Type, decl.Body, u, decl.Name.Name}
				}
			case *ast.GenDecl:
				for _, spec := range decl.Specs {
					if typ, ok := spec.(*ast.TypeSpec); ok {
						p.types[typ.Name.Name] = typ.Type
					}
				}
			}
		}
	}
	if len(p.units) == 0 {
		return nil, fmt.Errorf("no Go files for %s", source.Provider)
	}
	return p, nil
}

func mapEntries(expr ast.Expr, u *unit, result map[string][]binding) error {
	literal, ok := expr.(*ast.CompositeLit)
	if !ok {
		return fmt.Errorf("function map is no longer a literal: %s", text(expr))
	}
	for _, item := range literal.Elts {
		entry, ok := item.(*ast.KeyValueExpr)
		if !ok {
			return fmt.Errorf("unsupported function map entry")
		}
		name, err := strconv.Unquote(text(entry.Key))
		if err != nil {
			return fmt.Errorf("dynamic function map key: %s", text(entry.Key))
		}
		if _, exists := result[name]; exists {
			return fmt.Errorf("duplicate function: %s", name)
		}
		result[name] = []binding{{entry.Value, u}}
	}
	return nil
}

func (p *packageSource) bindings(target string) (map[string][]binding, []string, error) {
	result := map[string][]binding{}
	removed := map[string]bool{}
	var extractionError error
	found := 0
	for _, u := range p.units {
		ast.Inspect(u.node, func(node ast.Node) bool {
			var expr ast.Expr
			switch n := node.(type) {
			case *ast.ValueSpec:
				if len(n.Names) == 1 && n.Names[0].Name == target && len(n.Values) == 1 {
					expr = n.Values[0]
				}
			case *ast.AssignStmt:
				if len(n.Lhs) == 1 && text(n.Lhs[0]) == target && len(n.Rhs) == 1 {
					expr = n.Rhs[0]
				}
			case *ast.FuncDecl:
				if n.Name.Name == target && n.Body != nil {
					for _, statement := range n.Body.List {
						if ret, ok := statement.(*ast.ReturnStmt); ok && len(ret.Results) == 1 {
							expr = ret.Results[0]
						}
					}
				}
			}
			if expr != nil {
				found++
				if err := mapEntries(expr, u, result); err != nil {
					extractionError = err
				}
			}
			return true
		})
	}
	if extractionError != nil {
		return nil, nil, extractionError
	}
	if found != 1 {
		return nil, nil, fmt.Errorf("expected one %s function map, found %d", target, found)
	}
	// Helm removes Sprig names and replaces placeholder functions at renderer initialization.
	// Inspect the actual assignments, retaining every conditional implementation.
	for _, u := range p.units {
		for _, raw := range u.node.Decls {
			decl, ok := raw.(*ast.FuncDecl)
			if !ok || (decl.Name.Name != "funcMap" && decl.Name.Name != "initFunMap") {
				continue
			}
			ast.Inspect(decl.Body, func(node ast.Node) bool {
				if call, ok := node.(*ast.CallExpr); ok && text(call.Fun) == "delete" && len(call.Args) == 2 && text(call.Args[0]) == "f" {
					name, err := strconv.Unquote(text(call.Args[1]))
					if err == nil {
						removed[name] = true
					} else {
						extractionError = err
					}
				}
				if assign, ok := node.(*ast.AssignStmt); ok && len(assign.Lhs) == 1 && len(assign.Rhs) == 1 {
					if index, ok := assign.Lhs[0].(*ast.IndexExpr); ok && text(index.X) == "funcMap" {
						name, err := strconv.Unquote(text(index.Index))
						if err != nil {
							extractionError = err
							return false
						}
						// Retain the offline placeholder as one possible renderer implementation.
						result[name] = append(result[name], binding{assign.Rhs[0], u})
					}
				}
				return true
			})
		}
	}
	return result, keys(removed), extractionError
}

func (p *packageSource) resolve(value binding) *function {
	switch expr := value.expr.(type) {
	case *ast.Ident:
		return p.functions[expr.Name]
	case *ast.FuncLit:
		return &function{expr.Type, expr.Body, value.u, "closure"}
	case *ast.CallExpr:
		if named, ok := expr.Fun.(*ast.Ident); ok {
			if factory := p.functions[named.Name]; factory != nil && factory.typ.Results != nil && len(factory.typ.Results.List) == 1 {
				if typ, ok := factory.typ.Results.List[0].Type.(*ast.FuncType); ok {
					return &function{typ, factory.body, factory.u, factory.name}
				}
			}
		}
	}
	return nil
}

func (p *packageSource) shape(expr ast.Expr, seen map[string]bool) (string, []string) {
	switch typ := expr.(type) {
	case *ast.MapType:
		return "map", []string{}
	case *ast.ArrayType:
		return "sequence", []string{}
	case *ast.StarExpr:
		return p.shape(typ.X, seen)
	case *ast.StructType:
		fields := []string{}
		for _, field := range typ.Fields.List {
			for _, name := range field.Names {
				if name.IsExported() {
					fields = append(fields, name.Name)
				}
			}
		}
		sort.Strings(fields)
		return "record", fields
	case *ast.Ident:
		if strings.Contains("|bool|string|int|int8|int16|int32|int64|uint|uint8|uint16|uint32|uint64|uintptr|float32|float64|complex64|complex128|byte|rune|", "|"+typ.Name+"|") {
			return "scalar", []string{}
		}
		if underlying, ok := p.types[typ.Name]; ok && !seen[typ.Name] {
			seen[typ.Name] = true
			return p.shape(underlying, seen)
		}
	}
	return "any", []string{}
}

func (s *summary) effect(name, evidence string) {
	s.effects[name] = true
	s.evidence[name+": "+evidence] = true
}

// Copying or filtering entries under their original keys is independent of map
// iteration order. Reject calls, cross-key reads and loop exits from this proof.
func independentMapWrites(loop *ast.RangeStmt) bool {
	key, ok := loop.Key.(*ast.Ident)
	if !ok || key.Name == "_" {
		return false
	}
	safe, writes := true, false
	ast.Inspect(loop.Body, func(node ast.Node) bool {
		if !safe {
			return false
		}
		switch n := node.(type) {
		case *ast.CallExpr, *ast.ReturnStmt, *ast.BranchStmt, *ast.RangeStmt,
			*ast.ForStmt, *ast.IncDecStmt, *ast.GoStmt, *ast.DeferStmt, *ast.SendStmt, *ast.FuncLit, *ast.GenDecl:
			safe = false
		case *ast.IndexExpr:
			if text(n.Index) != key.Name {
				safe = false
			}
		case *ast.AssignStmt:
			if n.Tok == token.DEFINE {
				for _, name := range n.Lhs {
					if text(name) == key.Name {
						safe = false
					}
				}
				break
			}
			if n.Tok != token.ASSIGN {
				safe = false
				break
			}
			for _, target := range n.Lhs {
				index, ok := target.(*ast.IndexExpr)
				if !ok || text(index.Index) != key.Name {
					safe = false
					break
				}
				writes = true
			}
		}
		return safe
	})
	return safe && writes
}

// Boundaries name primitive APIs, not Helm aliases. Anything else stays unresolved.
func (s *summary) external(path, name string) {
	qualified := path + "." + name
	s.calls[qualified] = true
	switch {
	case path == "crypto/rand" || path == "math/rand" || path == "math/rand/v2":
		s.effect("randomness", qualified)
	case path == "time" && (name == "Now" || name == "Since" || name == "Until" || name == "Local" || name == "LoadLocation"):
		s.effect("clock-or-timezone", qualified)
	case path == "net" || strings.HasPrefix(path, "k8s.io/client-go/"):
		s.effect("external-state", qualified)
	case path == "path/filepath":
		s.effect("platform", qualified)
	case path == "dario.cat/mergo":
		s.effect("mutation", qualified)
	case path == "golang.org/x/crypto/bcrypt" && name == "GenerateFromPassword":
		s.effect("randomness", qualified)
	case path == "github.com/huandu/xstrings" && name == "Shuffle":
		s.effect("randomness", qualified)
	case path == "github.com/Masterminds/goutils" && strings.HasPrefix(name, "CryptoRandom"):
		s.effect("randomness", qualified)
	case path == "github.com/google/uuid" && name == "New":
		s.effect("randomness", qualified)
	}
	// A detected effect is a lower bound. Imported implementations have not been analyzed.
	s.unresolved[qualified] = true
}

func (p *packageSource) analyze(fn *function, s *summary, visited map[*ast.BlockStmt]bool) {
	if fn == nil || fn.body == nil {
		s.unresolved["missing function body"] = true
		return
	}
	if visited[fn.body] {
		return
	}
	visited[fn.body] = true
	params := map[string]ast.Expr{}
	if fn.typ.Params != nil {
		for _, param := range fn.typ.Params.List {
			for _, name := range param.Names {
				params[name.Name] = param.Type
			}
		}
	}
	ast.Inspect(fn.body, func(node ast.Node) bool {
		if node == nil {
			return false
		}
		location := fn.u.file + ":" + strconv.Itoa(p.set.Position(node.Pos()).Line)
		switch n := node.(type) {
		case *ast.CallExpr:
			s.calls[text(n.Fun)] = true
			switch call := n.Fun.(type) {
			case *ast.Ident:
				if local := p.functions[call.Name]; local != nil {
					p.analyze(local, s, visited)
				} else {
					switch call.Name {
					case "delete", "clear", "copy":
						if len(n.Args) > 0 {
							if _, parameter := params[text(n.Args[0])]; parameter {
								s.effect("mutation", location+" "+text(n.Fun))
							}
						}
					case "make", "new", "len", "cap", "append", "panic", "recover", "string", "bool", "int", "int64", "int32", "uint", "uint64", "uint32", "float64", "float32", "byte", "rune":
					default:
						if _, conversion := p.types[call.Name]; !conversion {
							s.unresolved[text(n.Fun)] = true
						}
					}
				}
			case *ast.SelectorExpr:
				if path := fn.u.imports[text(call.X)]; path != "" {
					s.external(path, call.Sel.Name)
				} else {
					s.unresolved[text(n.Fun)] = true
					if call.Sel.Name == "Execute" || call.Sel.Name == "ExecuteTemplate" {
						s.effect("dynamic-code", location+" "+text(n.Fun))
					}
				}
			default:
				s.unresolved[text(n.Fun)] = true
			}
		case *ast.AssignStmt:
			for _, left := range n.Lhs {
				if index, ok := left.(*ast.IndexExpr); ok {
					if _, parameter := params[text(index.X)]; parameter {
						s.effect("mutation", location+" "+text(left))
					} else {
						s.unresolved["write: "+text(left)] = true
					}
				}
				if _, ok := left.(*ast.StarExpr); ok {
					s.unresolved["indirect write: "+text(left)] = true
				}
				if _, ok := left.(*ast.SelectorExpr); ok {
					s.unresolved["field write: "+text(left)] = true
				}
			}
		case *ast.RangeStmt:
			if param, ok := params[text(n.X)]; ok {
				if variadic, ok := param.(*ast.Ellipsis); ok && n.Value != nil {
					params[text(n.Value)] = variadic.Elt
				}
				if _, ok := param.(*ast.MapType); ok {
					if independentMapWrites(n) {
						s.evidence["order-independent map projection: "+location] = true
					} else {
						s.effect("unordered", location+" range "+text(n.X))
					}
				}
			}
		case *ast.SelectorExpr:
			if path := fn.u.imports[text(n.X)]; path == "crypto/rand" || path == "math/rand" || path == "math/rand/v2" {
				s.effect("randomness", location+" "+path+"."+n.Sel.Name)
			}
			if path := fn.u.imports[text(n.X)]; path == "time" && n.Sel.Name == "Local" {
				s.effect("clock-or-timezone", location+" time.Local")
			}
		case *ast.GoStmt, *ast.SendStmt:
			s.unresolved["concurrency: "+location] = true
		}
		return true
	})
}

func (p *packageSource) describe(name string, variants []binding) facts {
	s := newSummary()
	f := facts{Provider: p.provider, Shape: "any", Fields: []string{}}
	shapes := map[string]bool{}
	for _, value := range variants {
		fn := p.resolve(value)
		f.Implementation = text(value.expr)
		f.Source = value.u.file
		f.Line = p.set.Position(value.expr.Pos()).Line
		f.SHA256 = digest([]byte(text(value.expr)))
		if fn != nil {
			f.Implementation = fn.name
			f.Source = fn.u.file
			f.Line = p.set.Position(fn.typ.Pos()).Line
			f.Signature = text(fn.typ)
			f.SHA256 = digest([]byte(text(fn.typ) + text(fn.body)))
			shape, fields := "any", []string{}
			if fn.typ.Results != nil && len(fn.typ.Results.List) > 0 {
				shape, fields = p.shape(fn.typ.Results.List[0].Type, map[string]bool{})
			}
			shapes[shape] = true
			f.Fields = fields
			p.analyze(fn, s, map[*ast.BlockStmt]bool{})
		} else {
			shapes["any"] = true
			if selector, ok := value.expr.(*ast.SelectorExpr); ok && value.u.imports[text(selector.X)] != "" {
				s.external(value.u.imports[text(selector.X)], selector.Sel.Name)
			} else {
				s.unresolved[text(value.expr)] = true
			}
		}
	}
	if len(shapes) == 1 {
		for shape := range shapes {
			f.Shape = shape
		}
	}
	// Renderer and language intrinsics have behavior beyond their placeholder Go bodies.
	// These four contracts are semantic boundaries, not a second function inventory.
	switch name {
	case "include", "tpl":
		delete(s.effects, "mutation") // Writes to the renderer's includedNames bookkeeping are internal.
		s.effect("dynamic-code", "Helm renderer executes template code")
	case "call":
		s.effect("dynamic-code", "Go template interpreter dispatch")
	case "lookup":
		s.effect("external-state", "Helm renderer installs a cluster client when enabled")
	case "fail", "required":
		s.effect("rejection", "Helm renderer rejection contract")
	}
	f.Effects, f.Unresolved, f.Calls, f.Evidence = keys(s.effects), keys(s.unresolved), keys(s.calls), keys(s.evidence)
	return f
}

func union(left, right []string) []string {
	result := map[string]bool{}
	for _, value := range append(left, right...) {
		result[value] = true
	}
	return keys(result)
}

func extract(sources []source) (map[string]facts, []string, error) {
	result := map[string]facts{}
	removed := map[string]bool{}
	for _, source := range sources {
		p, err := read(source)
		if err != nil {
			return nil, nil, err
		}
		bindings, deletions, err := p.bindings(source.Map)
		if err != nil {
			return nil, nil, err
		}
		for _, name := range deletions {
			delete(result, name)
			removed[name] = true
		}
		for name, variants := range bindings {
			next := p.describe(name, variants)
			if prior, exists := result[name]; exists {
				// Conditional renderer overrides must also retain their prior implementation.
				next.Effects = union(prior.Effects, next.Effects)
				next.Unresolved = union(prior.Unresolved, next.Unresolved)
				next.Calls = union(prior.Calls, next.Calls)
				next.Evidence = union(prior.Evidence, next.Evidence)
				if prior.Shape != next.Shape {
					next.Shape = "any"
					next.Fields = []string{}
				}
			}
			result[name] = next
		}
	}
	return result, keys(removed), nil
}

func run() error {
	config := flag.String("config", "", "JSON list of pinned provider directories and function maps")
	flag.Parse()
	data, err := os.ReadFile(*config)
	if err != nil {
		return err
	}
	var sources []source
	if err := json.Unmarshal(data, &sources); err != nil {
		return err
	}
	functions, removed, err := extract(sources)
	if err != nil {
		return err
	}
	return json.NewEncoder(os.Stdout).Encode(map[string]any{"functions": functions, "removed": removed})
}

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
