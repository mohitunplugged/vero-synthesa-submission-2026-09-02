# System card: Synthesa Compiled Proof Guidance

## Trust doctrine

```text
MODEL = UNTRUSTED PROPOSER
LEAN KERNEL + VERO GRADER = AUTHORITY
```

A model may propose a helper lemma, invariant, proof skeleton, implementation,
or proof-friendly refactor. It cannot mark a theorem proven, admit residual
obligations, alter the benchmark boundary, or override Lean/Vero.

## Compilation flow

```text
frozen Vero repository and mode
  -> Lean-environment obligation elaboration
  -> parent-contract/GIGO adequacy check
  -> fixed deterministic tactic and constructor floor
  -> normalized residuals
  -> semantic obligation graph and clustering
  -> verified-library/public-oracle/finite-certificate lookup
  -> bounded proposal only for an exact missing abstraction
  -> content pin
  -> Lean build and axiom check
  -> verified lemma/certificate library
  -> exact slot projections
  -> signed software.plan
  -> terminal-once software.build
  -> untouched Vero clean render and grader
  -> COMPLETE or HOLD plus lineage
```

## Deterministic components

- Vero manifest and slot-schedule parsing.
- Lean declaration resolution and elaborated obligation extraction.
- Stable binders, target, dependency, import, source, implementation-head, and
  environment digests.
- Bounded tactic/proof-constructor execution.
- Lean diagnostic normalization, including unresolved goal, missing rewrite,
  induction/case split, missing declaration/instance, type mismatch,
  termination, and arithmetic residuals.
- Obligation graph construction and deterministic clustering.
- Parent-contract adequacy and GIGO decisions.
- Precompiled oracle and public-document provenance checks.
- Content-addressed helper/certificate storage and dependency DAG scheduling.
- Exact projection into Vero-approved slots.
- Signed plan verification, terminal replay refusal, environment drift checks,
  and receipt generation.
- Independent `vero-extract`, clean render, compilation, axiom checks, and
  grading.

## Model boundary

During R&D, remote Qwen 4B, DeepSeek V4 Flash, GPT-5.5, and Claude Sonnet were
used in 33 pinned calls. Prompts were generated from exact residuals and asked
for the smallest missing artifact under a narrow output grammar, with examples,
counterexamples, and choices where applicable. Rejected responses remained
evidence only. Accepted mathematical content was validated by Lean and then
compiled into deterministic artifacts, so replay does not call the model.

## Formal and deterministic solvers

The broader Synthesa stack includes finite decision/oracle compilation,
counterexample-guided synthesis, SMT/SyGuS integration, cvc5, SAT/LRAT-style
evidence paths, and policy/seam completeness checking. The Vero campaign used
the same architectural principle: atomize a repository wall into bounded
contracts, prove the generic core once, and instantiate checked adapters.
These tools assist candidate construction; Lean remains the authority for Vero
proof validity.

## Governance

- Canonical Synthesa-SDLC actuator line: commit
  `89347c3594319c1c7c9a7ad1d07f7932b7096f66`.
- Active Vero research worktree base:
  `e5f700e74c12611ff5e47bf576cb45552251796f` plus a preserved dirty research
  diff.
- Qualified campaign compiler:
  `0653c7421f2aa681fb8d7795b400fc43cec2e3cfd24be85ecc928e921f2666aa`.
- Campaign root:
  `cfd0bc418a41ca32eb5b8ede967d2e55c4be38ca514fc0b6e503369711ea3d8c`.
- Campaign file SHA-256:
  `0647594c46286406b223699a3246d41332ad7d40768dfefc2a55792ea1c97b74`.
- Vero commit:
  `0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09`.
- Lean binary SHA-256:
  `3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`.
- Lake binary SHA-256:
  `a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359`.

The research worktree is not claimed as a clean release commit. Reproduction of
the benchmark result is intentionally decoupled through extracted artifacts;
source-release qualification is a separate product gate.

## Prohibited behavior

- No `sorry`, `admit`, unauthorized axiom, or unsafe escape in accepted slots.
- No repository-name branches or hard-coded expected outputs in the generic
  compiler.
- No modification of frozen Vero files surviving the clean re-render.
- No conversion of proof-search failure into a benchmark-defect claim.
- No Synthesa status substituted for an official Vero verdict.

## Known limitations

- The current result is an iterative, benchmark-seen research campaign.
- The strongest portfolio mixes proof and codeproof modes.
- The Vero-specific research code is not yet represented by a clean source
  commit.
- Full compute, orchestration, and labor costs are not metered.
- Some successful proof artifacts contain scheduled support lemmas specialized
  to their repository; cross-repository portability varies.
- Three repositories remain incomplete, with different parent-contract and
  translation issues documented separately.
