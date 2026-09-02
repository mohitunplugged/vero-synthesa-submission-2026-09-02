# Proposed GitHub issue: FLoCq proof-mode translation and parent-contract findings

Suggested title:

> `[FLoCq] Two accepted formal audits and 14 residual translation/proof-parent gaps at 0a7325d`

Suggested labels: `flocq`, `formal-audit`, `translation`, `proof-mode`

## Summary

At Vero commit `0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09`
with Lean `v4.29.1`, we evaluated FLoCq in proof mode against the supplied
canonical implementation. The untouched grader accepts **189/203**
specifications, reports zero failed specifications, and leaves 14 unfilled.

This issue reports three different kinds of evidence and keeps their authority
separate:

1. two axiom-clean `disprove_*` proofs already accepted by Vero's formal-audit
   path;
2. one source-equivalence concern where the Lean translation drops a public
   FLoCq range premise; and
3. thirteen proof-parent gaps: twelve disconnected arithmetic wrappers and one
   opaque native-Float roundtrip.

Only category 1 receives benchmark credit. Categories 2 and 3 remain unfilled
and are presented for curator review, not as claims that Vero's grader is
incorrect.

## Reproduction boundary

```text
Vero commit: 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
Lean: leanprover/lean4:v4.29.1
Mode: proof
Result: 189/203; 14 unfilled; 0 failed
Current official report SHA-256:
  a1a79d97b77ba2607ac79c833162be771e7756e514bdeed03188f09a82520a84
Public FLoCq source commit:
  7aab8f55bceec0cfafc3b3bc0e77e0dbb5a70c5f
Model calls used to establish these findings: 0
```

The complete extracted artifact can be shared privately.

## Finding A: unrestricted finite values make the encoder non-injective

Affected specification:

```text
spec_binary_float_of_bits_of_binary_float
```

The translated Lean `BinaryFloat` finite constructor has no validity proof.
The following distinct values collide under the frozen encoder:

```lean
let x1 : BinaryFloat 24 128 :=
  BinaryFloat.finite false (2 ^ 23) 0
let x2 : BinaryFloat 24 128 :=
  BinaryFloat.finite false (2 * (2 ^ 23)) (-1)
```

An axiom-clean proof derives equality of `x1` and `x2` from the proposed left
inverse and closes the contradiction by constructor injectivity and `omega`.
It does not evaluate or constrain the opaque decoder. The untouched grader
accepts `disprove_binary_float_of_bits_of_binary_float`.

This appears to be Vero's formal-audit mechanism working as intended. The
translated domain is broader than public FLoCq's valid representation.

Suggested repair: quantify over a validity-refined value, add the source
validity premise, or refine the translated constructor so invalid
mantissa/exponent pairs are unrepresentable.

## Finding B: unrestricted NaN payloads make `b2Prim` non-injective

Affected specification:

```text
spec_Prim2B_B2Prim
```

The translated `BinaryFloat.nan` admits any payload, while the frozen `b2Prim`
normalizes payload zero to one. Therefore:

```lean
let x0 : BinaryFloat 53 1024 := BinaryFloat.nan false 0
let x1 : BinaryFloat 53 1024 := BinaryFloat.nan false 1
```

are distinct constructors with the same `b2Prim` image. A right inverse would
equate them. The resulting `disprove_Prim2B_B2Prim` proof is axiom-clean and is
accepted by the untouched grader; it needs no equation for `Float.toBits` or
`Float.ofBits`.

Suggested repair: restrict the domain to canonical valid binary64 values,
refine the type, or state equality modulo NaN normalization.

## Finding C: `spec_bits_of_binary_float_of_bits` drops a source premise

Pinned public FLoCq states, in `src/IEEE754/Bits.v`:

```coq
Theorem bits_of_binary_float_of_bits :
  forall x,
  (0 <= x < 2^(mw+ew+1))%Z ->
  bits_of_binary_float (binary_float_of_bits x) = x.
```

The Vero Lean specification quantifies over every `n : Int` without the range
premise:

```lean
def spec_bits_of_binary_float_of_bits (impl : RepoImpl) : Prop :=
  ∀ (mw ew : Int) (n : Int),
    impl.flocq.bitsOfBinaryFloat mw ew
      (impl.flocq.binaryFloatOfBits mw ew n) = n
```

We have not proved the exact canonical Lean proposition false. The frozen
decoder ends in an unconstrained trusted declaration, and the broader Lean
encoder is itself surjective at a zero-width diagnostic instance. Therefore
both polarities remain unfilled. This is a translation-equivalence question,
not a formal-audit result.

Suggested repair: restore the range premise, or document why the stronger
statement is intended and provide its required decoder law.

## Finding D: twelve wrapper equalities compare disconnected operations

Affected specifications:

```text
spec_b32Plus_def   spec_b32Minus_def  spec_b32Mult_def
spec_b32Div_def    spec_b32Sqrt_def   spec_b32Fma_def
spec_b64Plus_def   spec_b64Minus_def  spec_b64Mult_def
spec_b64Div_def    spec_b64Sqrt_def   spec_b64Fma_def
```

For example, the supplied wrapper elaborates to a call to the trusted root
declaration `_root_.bplus`, while the specification compares it with the
separately defined `Flocq.bplus`:

```lean
noncomputable def Flocq.b32Plus : Flocq.B32PlusSig :=
  fun mode x y => _root_.bplus 24 128 Flocq.binopNanPl32 mode x y

-- required by the spec
Flocq.b32Plus mode x y =
  Flocq.bplus 24 128 mode Flocq.binopNanPl32 x y
```

The same split occurs for `bminus`, `bmult`, `bdiv`, `bsqrt`, and `bfma` at
both widths. The root operations are permitted trusted axioms, but the rendered
environment supplies no equality law relating them to their namespace
implementations. Trusting a declaration does not create an extensional
equation.

As a result, neither the positive equality nor a concrete negative witness is
derivable from the exposed parent. All twelve remain unfilled.

Suggested repair: define wrappers with the namespace implementations, bind
both names to the same declaration, or supply exact alignment theorems. A
single generic alignment schema should address all twelve.

## Finding E: native Float roundtrip has no kernel-visible inverse law

Affected specification:

```text
spec_B2Prim_Prim2B
```

Lean 4.29.1 declares:

```lean
@[extern "lean_float_of_bits"] opaque Float.ofBits : UInt64 → Float
@[extern "lean_float_to_bits"] opaque Float.toBits : Float → UInt64
```

The rendered project imports no theorem of shape
`Float.ofBits (Float.toBits x) = x`. Native execution can test the C
implementation but cannot establish the required axiom-clean kernel theorem.
We therefore leave both proof polarities unfilled.

Suggested repair: include a trusted inverse theorem under an explicit trust
policy, use a kernel-reducible bit-pattern model, or revise the proposition.

## Requested curator actions

1. Confirm the two accepted `disprove_*` findings and decide whether the
   translated domains should be restricted.
2. Review the missing source range premise and equivalence metadata.
3. Link or replace the six root arithmetic declarations used by b32/b64
   wrappers.
4. Decide how native Float bit-roundtrip semantics should be exposed to the
   kernel.
5. After any change, rerender from a clean checkout and do not carry the
   current 189/203 result across benchmark commits.

## Integrity statement

No source mismatch, runtime experiment, Synthesa HOLD, or public Coq theorem is
reported as a Vero pass. Only the two machine-checked negative proofs accepted
by the untouched grader receive formal-audit credit.
