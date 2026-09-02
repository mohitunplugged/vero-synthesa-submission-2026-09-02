# Synthesa submission for independent Vero grading

This private repository contains the exact extracted artifacts we are asking
the Vero maintainers to grade independently. It is a reviewer bundle, not a
claim that local results have already been accepted onto the leaderboard.

## Submitted result

```text
Vero commit: 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
Lean toolchain: leanprover/lean4:v4.29.1
Artifacts: 43
Locally qualified portfolio: 40/43 repositories, 2606/2705 specs
False acceptance admitted by Synthesa: 0
```

Important: this is a **mode-selected portfolio**. It contains 37 proof-mode
artifacts and six codeproof-mode artifacts. The proof subset is 35/37 complete
with 2286/2382 specifications; the codeproof subset is 5/6 complete with
320/323. We are asking the Vero team to determine whether this belongs on the
leaderboard as a labeled portfolio, as separate subset results, or requires a
new uniform-mode run. We do not present 40/43 as a standard single-mode score
without that ruling.

## What to grade

- `artifacts/`: 43 JSON files emitted by upstream `vero-extract` from the exact
  locally graded clean sandboxes.
- `inventory.json`: benchmark ID, mode, expected count, and SHA-256 for every
  artifact.
- `results/full-results.{csv,json}`: complete expected results.

Nothing under `system/`, `paper/`, or `issues/` is needed to determine the
score. Synthesa receipts are intentionally excluded: the Vero grader, not
Synthesa, is the submission authority.

## Quick integrity check

```bash
tools/verify_submission.sh
```

Expected final line:

```text
VERO_EXTRACTED_SUBMISSION_VERIFIED
```

## Independent grading

Please use the Vero team's normal private submission runner. `GRADING.md`
documents the mapping from each artifact to its benchmark and mode. For
convenience, `tools/grade_submission.py` invokes Vero's own
`run_evaluation()` over clean renders, but it is not authoritative and may be
ignored in favor of the maintainers' runner.

The requested process is:

```text
provided vero-extract artifact
  -> pristine Vero checkout at the pinned commit
  -> clean Vero render for the declared mode
  -> Vero Lake build and axiom checks
  -> maintainer-generated report
```

Ten extractor `extras` records are disclosed: four in Sortedcontainers and six
in Unicode. Upstream Vero explicitly drops `artifact.extras` before clean
rendering. We independently exercised that exact path and reproduced 49/49 and
46/46 respectively. The extras remain in the submitted JSON because these are
unaltered `vero-extract` outputs.

## Cost disclosure

- Frozen grading replay: zero model calls and zero model API cost.
- Metered external proposer R&D: 33 calls, 662,399 tokens, USD
  0.710391762755.
- The latter is not total campaign cost: Codex orchestration, human effort,
  and local compute were not completely metered.

See `system/COST_REPORT.md` and `results/model-call-ledger.json`.

## Paper and benchmark findings

The accompanying paper is
`paper/synthesa-compiled-proof-guidance-vero-draft.pdf`. It describes an
elaboration-first, deterministic-authority architecture in which models can
only propose pinned artifacts and Lean/Vero retain authority.

The three issue drafts under `issues/` are included for curator review. They
do not request unsupported score credit:

- DedekindReals: frozen specification elaboration failure;
- FLoCq: two accepted formal audits plus separate translation/parent gaps;
- Verdict: opaque non-editable conversion parent without preservation laws.

## Privacy

This repository is private. The extracted artifacts and candidate proof bodies
should remain private unless ByteVerity explicitly requests publication, in
accordance with the submission guidance received from Zhe.
