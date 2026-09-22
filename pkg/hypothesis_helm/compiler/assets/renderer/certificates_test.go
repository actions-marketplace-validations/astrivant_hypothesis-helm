package main

import (
	"crypto"
	"crypto/x509"
	"encoding/json"
	"encoding/pem"
	"reflect"
	"testing"
	"time"
)

// invokeCertificate calls an intercepted function with its original native argument types.
//
// Args:
//
//	t (*testing.T): Assertion owner.
//	tape (*Tape): Recording or replaying renderer.
//	name (string): Native generator name, also the synthetic test call site.
//	arguments (...any): Concrete Go arguments; nil becomes the required typed zero.
//
// Returns:
//
//	any: Native result, preserving the private Sprig certificate struct.
func invokeCertificate(t *testing.T, tape *Tape, name string, arguments ...any) any {
	t.Helper()
	function := reflect.ValueOf(tape.certificateFunction(name, name))
	inputs := make([]reflect.Value, len(arguments))
	for index, value := range arguments {
		inputs[index] = reflect.Zero(function.Type().In(index))
		if value != nil {
			inputs[index] = reflect.ValueOf(value)
		}
	}
	output := function.Call(inputs)
	if tape.invalid != "" || tape.unavailable != "" {
		t.Fatalf("invalid=%s unavailable=%s", tape.invalid, tape.unavailable)
	}
	if len(output) == 2 && !output[1].IsNil() {
		t.Fatal(output[1].Interface())
	}
	return output[0].Interface()
}

// parseCertificate checks that a returned PEM certificate actually matches its private key.
//
// Args:
//
//	t (*testing.T): Assertion owner.
//	value (any): Sprig's native certificate result.
//
// Returns:
//
//	*x509.Certificate: Parsed certificate with a matching RSA or ECDSA private key.
func parseCertificate(t *testing.T, value any) *x509.Certificate {
	t.Helper()
	native := reflect.ValueOf(value)
	block, _ := pem.Decode([]byte(native.FieldByName("Cert").String()))
	if block == nil {
		t.Fatal("missing certificate PEM")
	}
	certificate, err := x509.ParseCertificate(block.Bytes)
	if err != nil {
		t.Fatal(err)
	}
	keyBlock, _ := pem.Decode([]byte(native.FieldByName("Key").String()))
	if keyBlock == nil {
		t.Fatal("missing private key PEM")
	}
	var signer crypto.Signer
	switch keyBlock.Type {
	case "RSA PRIVATE KEY":
		signer, err = x509.ParsePKCS1PrivateKey(keyBlock.Bytes)
	case "EC PRIVATE KEY":
		signer, err = x509.ParseECPrivateKey(keyBlock.Bytes)
	default:
		t.Fatalf("unexpected key type %s", keyBlock.Type)
	}
	if err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(signer.Public(), certificate.PublicKey) {
		t.Fatal("certificate public key does not match its private key")
	}
	return certificate
}

// TestCertificateChain verifies real crypto properties before and after native-type replay.
//
// Args:
//
//	t (*testing.T): Assertion owner.
//
// Returns:
//
//	No value. Failures identify a broken signing chain, changed native type or argument loss.
func TestCertificateChain(t *testing.T) {
	var records []Draw
	tape := &Tape{request: Request{MaxCalls: 20, MaxBytes: 1 << 20}, counts: map[string]int{}}
	tape.exchange = func(draw Draw) (Draw, error) {
		if draw.Result == nil {
			draw.Generate = true
		} else {
			records = append(records, draw)
		}
		return draw, nil
	}
	ca := invokeCertificate(t, tape, "genCA", "test-ca", 2)
	caParsed := parseCertificate(t, ca)
	validity := caParsed.NotAfter.Sub(caParsed.NotBefore)
	// Sprig reads the clock twice; a second boundary can fall between those reads.
	if !caParsed.IsCA || caParsed.Subject.CommonName != "test-ca" || validity < 48*time.Hour || validity > 48*time.Hour+time.Second {
		t.Fatal("CA properties or requested validity were lost")
	}
	leaf := invokeCertificate(t, tape, "genSignedCert", "leaf", []any{"127.0.0.1"}, []any{"service.local"}, 1, ca)
	leafParsed := parseCertificate(t, leaf)
	roots := x509.NewCertPool()
	roots.AddCert(caParsed)
	if _, err := leafParsed.Verify(x509.VerifyOptions{Roots: roots, DNSName: "service.local", CurrentTime: caParsed.NotBefore.Add(time.Minute)}); err != nil {
		t.Fatal(err)
	}
	if len(leafParsed.IPAddresses) != 1 || leafParsed.IPAddresses[0].String() != "127.0.0.1" || leafParsed.IsCA {
		t.Fatal("leaf IP constraints or role were lost")
	}
	key := invokeCertificate(t, tape, "genPrivateKey", "ecdsa").(string)
	withKey := invokeCertificate(t, tape, "genCAWithKey", "key-ca", 2, key)
	parseCertificate(t, withKey)
	if reflect.ValueOf(withKey).FieldByName("Key").String() != key {
		t.Fatal("supplied private key was replaced")
	}
	for _, result := range []any{
		invokeCertificate(t, tape, "genSelfSignedCert", "self", nil, nil, 1),
		invokeCertificate(t, tape, "genSelfSignedCertWithKey", "self", nil, nil, 1, key),
		invokeCertificate(t, tape, "genSignedCertWithKey", "leaf", nil, nil, 1, withKey, key),
	} {
		parseCertificate(t, result)
	}
	// Passing through JSON reproduces the actual process boundary, including the unexported type.
	encoded, err := json.Marshal(records)
	if err != nil {
		t.Fatal(err)
	}
	var decoded []Draw
	if err := json.Unmarshal(encoded, &decoded); err != nil {
		t.Fatal(err)
	}
	replay := &Tape{request: tape.request, counts: map[string]int{}}
	replay.exchange = func(draw Draw) (Draw, error) {
		result := decoded[0]
		decoded = decoded[1:]
		return result, nil
	}
	replayedCA := invokeCertificate(t, replay, "genCA", "test-ca", 2)
	replayedLeaf := invokeCertificate(t, replay, "genSignedCert", "leaf", []any{"127.0.0.1"}, []any{"service.local"}, 1, replayedCA)
	if !reflect.DeepEqual(ca, replayedCA) || !reflect.DeepEqual(leaf, replayedLeaf) {
		t.Fatal("certificate replay changed bytes or native types")
	}
}
