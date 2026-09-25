// Command catalog extracts Helm function facts and Kubernetes validation constraints
// from pinned upstream sources for the Python catalog rebuild commands.
package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"io"
	"os"
)

// Record holds the JSON fields shared by catalog extraction operations.
type Record map[string]any

// must propagates failures when a pinned source no longer matches the supported syntax.
//
// Args:
//
//	err (error): Failure to propagate, or nil to continue.
//
// Panics:
//
//	The supplied error when it is not nil.
func must(err error) {
	if err != nil {
		panic(err)
	}
}

// hash computes a stable SHA-256 identity for source bytes or canonical syntax.
//
// Args:
//
//	data ([]byte): Content to identify.
//
// Returns:
//
//	string: Lowercase hexadecimal digest.
func hash(data []byte) string {
	digest := sha256.Sum256(data)
	return hex.EncodeToString(digest[:])
}

// run selects exactly one catalog operation and writes its JSON result.
//
// Args:
//
//	args ([]string): Flags for Helm extraction, Kubernetes extraction or validation.
//	input (io.Reader): JSON Lines boundary cases for oracle mode.
//	output (io.Writer): Destination for extracted facts or validation results.
//	diagnostics (io.Writer): Destination for flag usage and parsing errors.
//
// Returns:
//
//	error: Invalid arguments, failed extraction or output failure; nil on success.
func run(args []string, input io.Reader, output, diagnostics io.Writer) error {
	flags := flag.NewFlagSet("catalog", flag.ContinueOnError)
	flags.SetOutput(diagnostics)
	config := flags.String("config", "", "JSON list of pinned Helm, Sprig and Go function-map sources")
	root := flags.String("source", "", "pinned Kubernetes checkout")
	verify := flags.Bool("oracle", false, "evaluate Kubernetes validators on JSON Lines")
	if err := flags.Parse(args); err != nil {
		return err
	}
	selected := 0
	for _, enabled := range []bool{*config != "", *root != "", *verify} {
		if enabled {
			selected++
		}
	}
	if selected != 1 || flags.NArg() != 0 {
		return fmt.Errorf("select exactly one of --config, --source or --oracle; positional arguments are not accepted")
	}
	if *verify {
		return oracle(input, output)
	}
	var result Record
	if *config != "" {
		var err error
		result, err = helm(*config)
		if err != nil {
			return err
		}
	} else {
		result = kubernetes(*root)
	}
	return json.NewEncoder(output).Encode(result)
}

// main dispatches the catalog operation and reports command failures to stderr.
//
// Returns:
//
//	No value. The process exits with status one on failure and zero on success or help.
func main() {
	if err := run(os.Args[1:], os.Stdin, os.Stdout, os.Stderr); err != nil && !errors.Is(err, flag.ErrHelp) {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
