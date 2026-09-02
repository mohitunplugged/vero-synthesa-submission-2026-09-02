# Proposed GitHub issue: DedekindReals frozen specs do not elaborate

Suggested title:

> `[DedekindReals] Multiplication specs fail to elaborate because RinvSig closes over global Rneq/R_of_Q`

Suggested labels: `dedekind-reals`, `benchmark-defect`, `elaboration`, `proof-mode`

## Summary

At Vero commit `0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09`,
`DedekindReals.Spec.Multiplication` does not elaborate. The bundle's `Rinv`
field accepts a proof about the global reference declarations
`DedekindReals.Rneq` and `DedekindReals.R_of_Q`, while six frozen
specifications pass proofs formed with the corresponding fields of an
arbitrary `impl`.

This is a frozen type mismatch before candidate proof search. It prevents the
spec layer from building, so neither `prove_*`, `disprove_*`, nor the ordinary
audit slots can repair it.

## Reproduction

```bash
git checkout 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
cd benchmarks/DedekindReals
lake build DedekindReals.Spec.Multiplication
```

Using the pinned Lean `v4.29.1` toolchain, this exits nonzero with seven type
errors at lines 146, 153, 154, 161, 169, 176, and 183. Representative output:

```text
Application type mismatch: The argument
  xNZ
has type
  impl.dedekindReals.Rneq x (impl.dedekindReals.R_of_Q 0)
but is expected to have type
  Rneq x (R_of_Q 0)
in the application
  impl.dedekindReals.Rinv x xNZ
```

## Affected frozen specifications

```text
spec_Rinv_0_lt_compat
spec_Ropp_inv_permute       -- two failing applications
spec_Rinv_l_pos
spec_Rinv_l_neg
spec_Rinv_l
spec_Rinv_r
```

Because the frozen spec module does not elaborate, the local official run
times out/fails its repository build and reports 0/82. That score should not be
interpreted as 82 failed theorem searches.

## Root cause

`DedekindReals/Impl/Multiplication.lean` defines a closed signature:

```lean
abbrev RinvSig := (x : R) -> Rneq x (R_of_Q 0) -> R
```

The bundle later declares:

```lean
structure DedekindRealsBundle where
  -- ...
  Rneq : RneqSig
  R_of_Q : ROfQSig
  -- ...
  Rinv : RinvSig
```

The type of `Rinv` is therefore independent of the preceding bundle fields.
By contrast, `Spec/Multiplication.lean` constructs `xNZ` with
`impl.dedekindReals.Rneq` and `impl.dedekindReals.R_of_Q`. Those types agree
only for the canonical reference bundle, not for the arbitrary `impl :
RepoImpl` required by the specification layer.

## Why candidate proofs cannot fix it

The error occurs while Lean elaborates the frozen definition of the
specification, before it reaches an editable proof body. A candidate cannot
cast between these proof types without first having a well-typed proposition,
and Vero's clean render correctly discards edits outside scheduled slots.

This is also not yet a Vero formal-audit theorem: no well-formed frozen
proposition exists for the affected declarations. The appropriate state is a
curator/GIGO hold, not `unsat` or `disprove` credit.

## Suggested repair

Make the inverse signature depend on the operations carried by the same
bundle:

```lean
abbrev RinvSig (rneq : RneqSig) (rOfQ : ROfQSig) :=
  (x : R) -> rneq x (rOfQ 0) -> R

structure DedekindRealsBundle where
  -- ...
  Rneq : RneqSig
  R_of_Q : ROfQSig
  -- ...
  Rinv : RinvSig Rneq R_of_Q
```

Declaring the dependent function type directly on the field would be
equivalent. The canonical implementation can retain its concrete behavior
after instantiation.

## Acceptance criteria

- `lake build DedekindReals.Spec.Multiplication` succeeds from a clean checkout.
- All six affected declarations elaborate for arbitrary `impl : RepoImpl`.
- `Rinv`'s nonzero witness uses the same bundle's `Rneq` and `R_of_Q`.
- No proposition is weakened and arbitrary bundles are not silently identified
  with `canonical`.
- Both proof and codeproof renders pass the frozen-spec build before scoring.

## Evidence identity

```text
Lean toolchain: leanprover/lean4:v4.29.1
Lean binary SHA-256:
  3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf
Normalized diagnostic SHA-256:
  7361eb09be199e55b768aca3a4676221e20b3747d566a037699674804d0b6f49
Failure receipt root:
  444a17c59c815beac1055103fcfb2158ea2beb6aa9320c2b0f803e581c099a80
```

We can provide the complete normalized and raw diagnostic receipt privately.
