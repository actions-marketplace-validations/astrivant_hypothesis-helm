package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"reflect"

	"github.com/Masterminds/sprig/v3"
)

// Only native generators belong here. Deterministic buildCustomCert stays native.
var certificateFunctions = func() map[string]any {
	functions := sprig.GenericFuncMap()
	selected := map[string]any{}
	for _, name := range []string{
		"genCA", "genCAWithKey", "genPrivateKey", "genSelfSignedCert",
		"genSelfSignedCertWithKey", "genSignedCert", "genSignedCertWithKey",
	} {
		selected[name] = functions[name]
	}
	return selected
}()

// certificateArgument retains native element types in otherwise ambiguous JSON lists.
//
// Args:
//
//	value (reflect.Value): One already type-checked native function argument.
//
// Returns:
//
//	any: JSON-compatible argument identity, distinguishing nil, lists and scalar types.
func certificateArgument(value reflect.Value) any {
	if !value.IsValid() || (value.Kind() == reflect.Interface && value.IsNil()) {
		return nil
	}
	if value.Kind() == reflect.Interface {
		return certificateArgument(value.Elem())
	}
	var content any = value.Interface()
	if value.Kind() == reflect.Slice && !value.IsNil() {
		items := make([]any, value.Len())
		for index := range items {
			items[index] = certificateArgument(value.Index(index))
		}
		content = items
	}
	return map[string]any{"type": value.Type().String(), "value": content}
}

// certificateFunction intercepts results without reimplementing Sprig's crypto semantics.
//
// Args:
//
//	name (string): Selected Sprig generator.
//	site (string): Source location or explicit dynamic tpl identity.
//
// Returns:
//
//	any: Function with the original signature, including Sprig's private certificate type.
func (t *Tape) certificateFunction(name, site string) any {
	native := reflect.ValueOf(certificateFunctions[name])
	signature := native.Type()
	return reflect.MakeFunc(signature, func(arguments []reflect.Value) []reflect.Value {
		// Keeping the signature lets text/template enforce arity and Go argument types.
		output := make([]reflect.Value, signature.NumOut())
		for index := range output {
			output[index] = reflect.Zero(signature.Out(index))
		}
		if t.position >= t.request.MaxCalls {
			t.unavailable = "certificate input exceeds configured invocation budget"
			return output
		}
		encoded := make([]any, len(arguments))
		for index, argument := range arguments {
			encoded[index] = certificateArgument(argument)
		}
		identity, err := json.Marshal(encoded)
		if err != nil {
			t.unavailable = "certificate arguments cannot be recorded: " + err.Error()
			return output
		}
		if len(identity) > t.request.MaxBytes {
			t.unavailable = "certificate arguments exceed configured byte budget"
			return output
		}
		occurrence := t.counts[site]
		t.counts[site]++
		t.position++
		call := Draw{Path: fmt.Sprintf("$render.crypto[%q][%d]", site, occurrence), Function: name, Arguments: identity}
		reply, err := t.exchange(call)
		if err != nil || reply.Path != call.Path || reply.Function != name || !sameJSON(reply.Arguments, identity) {
			t.invalid = "certificate input stream failed or returned a mismatched call"
			return output
		}
		if reply.Generate {
			// First execution uses upstream code, its clock, and cryptographic randomness.
			output = native.Call(arguments)
			call.Result, err = json.Marshal(output[0].Interface())
			if err != nil {
				t.invalid = "certificate result cannot be recorded: " + err.Error()
				return output
			}
			if len(output) == 2 && !output[1].IsNil() {
				call.Error = output[1].Interface().(error).Error()
			}
			if len(call.Result)+len(call.Error)+len(identity) > t.request.MaxBytes {
				t.unavailable = "certificate result exceeds configured byte budget"
				return output
			}
			reply, err = t.exchange(call)
		}
		if err != nil || reply.Generate || reply.Path != call.Path || reply.Function != name || !sameJSON(reply.Arguments, identity) {
			t.invalid = "certificate replay does not match this call"
			return output
		}
		// Allocate the original unexported Sprig type; a map with Cert/Key is not interchangeable.
		value := reflect.New(signature.Out(0))
		decoder := json.NewDecoder(bytes.NewReader(reply.Result))
		decoder.DisallowUnknownFields()
		if bytes.Equal(reply.Result, []byte("null")) || decoder.Decode(value.Interface()) != nil {
			t.invalid = "certificate replay has an invalid native result"
			return output
		}
		output[0] = value.Elem()
		if len(output) == 2 {
			output[1] = reflect.Zero(signature.Out(1))
		}
		if reply.Error != "" {
			if len(output) != 2 {
				t.invalid = "certificate replay supplies an error for a string-only function"
			} else {
				output[1] = reflect.ValueOf(fmt.Errorf("%s", reply.Error))
			}
		}
		return output
	}).Interface()
}

// sameJSON compares call identities after decoding so object-key order is irrelevant.
//
// Args:
//
//	left (json.RawMessage): Response identity.
//	right (json.RawMessage): Original native identity.
//
// Returns:
//
//	bool: Both identities are valid and equal, preserving integer precision.
func sameJSON(left, right json.RawMessage) bool {
	decode := func(raw json.RawMessage) (any, error) {
		decoder := json.NewDecoder(bytes.NewReader(raw))
		decoder.UseNumber()
		var value any
		err := decoder.Decode(&value)
		return value, err
	}
	a, aerr := decode(left)
	b, berr := decode(right)
	return aerr == nil && berr == nil && reflect.DeepEqual(a, b)
}
