# Proposed GitHub issue: Verdict conversion parent is opaque and source-misaligned

Suggested title:

> `[Verdict] Three certFromParsed specs have no editable or kernel-visible conversion contract`

Suggested labels: `verdict`, `codeproof`, `proof-parent`, `translation`

## Summary

At Vero commit `0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09`,
the last three Verdict specifications constrain `Verdict.certFromParsed`.
That declaration is opaque, has no defining equations visible to Lean, and is
not an editable benchmark API. The specifications ignore `RepoImpl` and the
rendered project imports no preservation theorem for the outer signature OID,
inner signature OID, or validity bounds.

The untouched codeproof result is **116/119**. We have proved that the exposed
function type admits both satisfying and violating interpretations, but we
have not proved either polarity for the fixed opaque constant. The three slots
therefore remain unfilled and receive no benchmark credit.

## Reproduction boundary

```text
Vero commit: 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
Lean: leanprover/lean4:v4.29.1
Mode: codeproof
Result: 116/119
Current official report SHA-256:
  e4b306fbf3dae1b617c1f3efce8b1220f8d56f92faeedf748eedfb59771585bf
Pinned upstream Verdict commit:
  9bc18bc5a287c1608dcb74a6eee7b9ca94a62b67
```

## Affected specifications

```text
spec_cert_from_parsed_sig_alg_outer
spec_cert_from_parsed_sig_alg_inner
spec_cert_from_parsed_validity
```

## Frozen Lean surface

`Verdict/Impl/Convert.lean` exposes only:

```lean
opaque certFromParsed :
  Verdict.Certificate → Option Verdict.Policy.AbstractCertificate
```

The Vero manifest exposes zero implementation slots for this conversion. Each
of the three specifications refers directly to the opaque declaration and
does not depend on the candidate `RepoImpl`. Consequently a codeproof agent
cannot implement the function, unfold it, or select an alternative
proof-friendly implementation.

## Kernel-checked independence diagnostic

We parameterized the exact three preservation shapes over an arbitrary
function with the same exposed type. Lean verifies axiom-clean that:

- an all-`none` function satisfies all three implications vacuously;
- one function of the same type violates outer-OID preservation;
- another violates inner-OID preservation; and
- another violates validity preservation.

This establishes that the type alone entails neither polarity. It does **not**
establish a proposition about the fixed `Verdict.certFromParsed`; opacity is
not falsity. The diagnostic therefore remains outside the score.

## Public source mismatch

The pinned upstream Rust implementation (`verdict/src/convert.rs`, Apache-2.0)
constructs the complete abstract certificate and converts OID arc sequences to
dotted-decimal text through `spec_oid_to_string`.

The frozen Vero relation instead interprets a raw `List UInt8` by converting
each byte directly to a character. No verified adapter equates those
representations. Public source is useful evidence of intended semantics, but
cannot add a theorem about an opaque Lean constant with a different exposed
relation.

## Why more proof search cannot close the gap

All three goals require exactly the missing semantic bridge: if
`certFromParsed cert = some abstract`, then selected fields of `abstract`
match selected fields of `cert`. Tactics, induction, finite enumeration, and a
model can only rearrange known hypotheses; none can synthesize a true theorem
about an unconstrained opaque parent while keeping Lean as proof authority.

## Suggested repairs

Any one of these would create a checkable task:

1. make `certFromParsed` a scored implementation slot in codeproof mode;
2. provide a kernel-reducible canonical definition in proof mode;
3. provide axiom-clean preservation theorems for the three projections;
4. specify an inductive conversion relation whose constructors expose those
   equalities; and
5. align the OID representation with the pinned source's dotted-decimal
   semantics, or document and verify the intended alternative.

If the conversion becomes editable, please also prevent an all-`none`
implementation from satisfying all three conditional specifications
vacuously—for example by adding a success/completeness condition where the
source parser is valid.

## Acceptance criteria

- The implementation is editable or its behavior is kernel-visible through an
  exact definition/theorems.
- The source and Lean OID representations have a verified relation.
- The three specs can be meaningfully proved or disproved without an
  unauthorized axiom.
- A clean `vero-extract` artifact re-renders and grades under the corrected
  benchmark commit.

## Integrity statement

This issue is a proof-parent completeness and translation report. It is not a
claim that the official grader is buggy, that the three specifications are
false, or that 119/119 should be awarded on the current commit.
