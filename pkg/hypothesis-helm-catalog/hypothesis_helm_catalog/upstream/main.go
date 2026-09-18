// Catalog rebuilding uses Kubernetes' Go AST and its actual reusable validators.
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
	"io"
	"os"
	"path/filepath"
	"reflect"
	"runtime"
	"strconv"
	"strings"

	validation "k8s.io/apimachinery/pkg/util/validation"
)

type Record map[string]any

func must(err error) {
	if err != nil {
		panic(err)
	}
}
func hash(data []byte) string { h := sha256.Sum256(data); return hex.EncodeToString(h[:]) }
func encode(value any)        { must(json.NewEncoder(os.Stdout).Encode(value)) }
func expression(e ast.Expr, constants map[string]ast.Expr) any {
	switch e := e.(type) {
	case *ast.BasicLit:
		if e.Kind == token.STRING {
			v, err := strconv.Unquote(e.Value)
			must(err)
			return v
		}
		v, err := strconv.Atoi(e.Value)
		must(err)
		return v
	case *ast.Ident:
		return expression(constants[e.Name], constants)
	case *ast.BinaryExpr:
		if e.Op == token.ADD {
			return expression(e.X, constants).(string) + expression(e.Y, constants).(string)
		}
	}
	panic("unsupported constant expression")
}
func canonical(node ast.Node) string {
	var b bytes.Buffer
	must(printer.Fprint(&b, token.NewFileSet(), node))
	return hash(b.Bytes())
}
func declarations(file string) (map[string]ast.Expr, map[string]*ast.FuncDecl) {
	set := token.NewFileSet()
	node, err := parser.ParseFile(set, file, nil, parser.ParseComments)
	must(err)
	constants := map[string]ast.Expr{}
	functions := map[string]*ast.FuncDecl{}
	for _, raw := range node.Decls {
		switch decl := raw.(type) {
		case *ast.GenDecl:
			for _, raw := range decl.Specs {
				if spec, ok := raw.(*ast.ValueSpec); ok && len(spec.Names) == 1 && len(spec.Values) == 1 {
					constants[spec.Names[0].Name] = spec.Values[0]
				}
			}
		case *ast.FuncDecl:
			functions[decl.Name.Name] = decl
		}
	}
	return constants, functions
}
func profiles(root string) Record {
	source := filepath.Join(root, "staging/src/k8s.io/apimachinery/pkg/util/validation/validation.go")
	constants, funcs := declarations(source)
	file, _ := runtime.FuncForPC(reflect.ValueOf(validation.IsDNS1123Subdomain).Pointer()).FileLine(0)
	_, compiled := declarations(file)
	result := Record{}
	for _, row := range []struct{ name, fn, regex, length string }{
		{"dns1123-subdomain", "IsDNS1123Subdomain", "dns1123SubdomainRegexp", "DNS1123SubdomainMaxLength"},
		{"dns1123-label", "IsDNS1123Label", "dns1123LabelRegexp", "DNS1123LabelMaxLength"},
		{"dns1035-label", "IsDNS1035Label", "dns1035LabelRegexp", "DNS1035LabelMaxLength"},
	} {
		if funcs[row.fn] == nil || compiled[row.fn] == nil || canonical(funcs[row.fn]) != canonical(compiled[row.fn]) {
			panic("source and oracle validator differ: " + row.fn)
		}
		call, ok := constants[row.regex].(*ast.CallExpr)
		if !ok || len(call.Args) != 1 {
			panic("unsupported regexp declaration")
		}
		pattern := expression(call.Args[0], constants).(string)
		if !strings.HasPrefix(pattern, "^") || !strings.HasSuffix(pattern, "$") {
			panic("validator regexp is not anchored")
		}
		schema := Record{"type": "string", "pattern": strings.TrimSuffix(pattern, "$") + `(?![\s\S])`, "maxLength": expression(constants[row.length], constants)}
		result[row.name] = Record{"schema": schema, "function": row.fn, "function_sha256": canonical(funcs[row.fn])}
	}
	port := funcs["IsValidPortNum"]
	if port == nil || canonical(port) != canonical(compiled["IsValidPortNum"]) || len(port.Body.List) != 2 {
		panic("unsupported port validator")
	}
	condition, ok := port.Body.List[0].(*ast.IfStmt)
	if !ok || condition.Else != nil {
		panic("unsupported port guard")
	}
	conjunction, ok := condition.Cond.(*ast.BinaryExpr)
	if !ok || conjunction.Op != token.LAND {
		panic("unsupported port range")
	}
	lower, ok := conjunction.X.(*ast.BinaryExpr)
	if !ok || lower.Op != token.LEQ {
		panic("unsupported lower bound")
	}
	upper, ok := conjunction.Y.(*ast.BinaryExpr)
	if !ok || upper.Op != token.LEQ {
		panic("unsupported upper bound")
	}
	if lower.Y.(*ast.Ident).Name != "port" || upper.X.(*ast.Ident).Name != "port" {
		panic("unsupported port operand")
	}
	result["port-number"] = Record{"schema": Record{"type": "integer", "minimum": expression(lower.X, constants), "maximum": expression(upper.Y, constants)}, "function": "IsValidPortNum", "function_sha256": canonical(port)}
	return result
}
func fields(root string) (Record, []Record, Record) {
	rules := Record{}
	unresolved := []Record{}
	hashes := Record{}
	base := filepath.Join(root, "staging/src/k8s.io/api")
	must(filepath.WalkDir(base, func(path string, entry os.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if entry.IsDir() || entry.Name() != "types.go" {
			return nil
		}
		data, err := os.ReadFile(path)
		if err != nil {
			return err
		}
		relative, _ := filepath.Rel(root, path)
		hashes[filepath.ToSlash(relative)] = hash(data)
		set := token.NewFileSet()
		file, err := parser.ParseFile(set, path, data, parser.ParseComments)
		if err != nil {
			return err
		}
		pkg, _ := filepath.Rel(base, filepath.Dir(path))
		prefix := "io.k8s.api." + strings.ReplaceAll(filepath.ToSlash(pkg), "/", ".")
		for _, raw := range file.Decls {
			decl, ok := raw.(*ast.GenDecl)
			if !ok {
				continue
			}
			for _, raw := range decl.Specs {
				spec, ok := raw.(*ast.TypeSpec)
				if !ok {
					continue
				}
				body, ok := spec.Type.(*ast.StructType)
				if !ok {
					continue
				}
				for _, field := range body.Fields.List {
					if field.Doc == nil {
						continue
					}
					name := ""
					if field.Tag != nil {
						tag, err := strconv.Unquote(field.Tag.Value)
						if err != nil {
							return err
						}
						name = strings.Split(reflect.StructTag(tag).Get("json"), ",")[0]
					}
					id := prefix + "." + spec.Name.Name + "/" + name
					for _, comment := range field.Doc.List {
						tag := strings.TrimSpace(strings.TrimPrefix(comment.Text, "//"))
						if !strings.HasPrefix(tag, "+k8s:") {
							continue
						}
						evidence := Record{"type_field": id, "file": filepath.ToSlash(relative), "line": set.Position(comment.Pos()).Line, "tag": tag}
						key, value, has := strings.Cut(strings.TrimPrefix(tag, "+k8s:"), "=")
						keyword := ""
						switch key {
						case "minimum", "maximum", "minLength", "maxLength":
							keyword = key
						}
						if keyword == "" || !has || name == "" || name == "-" {
							evidence["reason"] = "unsupported or conditional annotation"
							unresolved = append(unresolved, evidence)
							continue
						}
						number, err := strconv.Atoi(value)
						if err != nil {
							evidence["reason"] = "non-integer annotation"
							unresolved = append(unresolved, evidence)
							continue
						}
						// Only scalar fields can receive these independent bounds. Named types remain unresolved.
						typ := field.Type
						if pointer, ok := typ.(*ast.StarExpr); ok {
							typ = pointer.X
						}
						basic, ok := typ.(*ast.Ident)
						integer := ok && (basic.Name == "int32" || basic.Name == "int64" || basic.Name == "int")
						text := ok && basic.Name == "string"
						if !(integer && (key == "minimum" || key == "maximum") || text && (key == "minLength" || key == "maxLength")) {
							evidence["reason"] = "annotation target is not a supported scalar"
							unresolved = append(unresolved, evidence)
							continue
						}
						evidence["schema"] = Record{keyword: number}
						rows, _ := rules[id].([]Record)
						rules[id] = append(rows, evidence)
					}
				}
			}
		}
		return nil
	}))
	return rules, unresolved, hashes
}
func oracle() {
	decoder := json.NewDecoder(os.Stdin)
	for {
		var test struct {
			Profile string          `json:"profile"`
			Value   json.RawMessage `json:"value"`
		}
		err := decoder.Decode(&test)
		if err == io.EOF {
			return
		}
		must(err)
		valid := false
		if test.Profile == "port-number" {
			var value int
			must(json.Unmarshal(test.Value, &value))
			valid = len(validation.IsValidPortNum(value)) == 0
		} else {
			var value string
			must(json.Unmarshal(test.Value, &value))
			switch test.Profile {
			case "dns1123-subdomain":
				valid = len(validation.IsDNS1123Subdomain(value)) == 0
			case "dns1123-label":
				valid = len(validation.IsDNS1123Label(value)) == 0
			case "dns1035-label":
				valid = len(validation.IsDNS1035Label(value)) == 0
			default:
				panic("unknown profile")
			}
		}
		encode(valid)
	}
}
func main() {
	root := flag.String("source", "", "pinned Kubernetes checkout")
	verify := flag.Bool("oracle", false, "evaluate actual upstream validators on JSON Lines")
	flag.Parse()
	if *verify {
		oracle()
		return
	}
	if *root == "" {
		fmt.Fprintln(os.Stderr, "--source is required")
		os.Exit(2)
	}
	rules, unresolved, hashes := fields(*root)
	for _, path := range []string{"staging/src/k8s.io/apimachinery/pkg/util/validation/validation.go", "pkg/apis/core/validation/validation.go", "api/openapi-spec/swagger.json"} {
		data, err := os.ReadFile(filepath.Join(*root, path))
		must(err)
		hashes[path] = hash(data)
	}
	encode(Record{"profiles": profiles(*root), "fields": rules, "unresolved": unresolved, "source_hashes": hashes})
}
