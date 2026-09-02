# Full result disclosure

## Aggregate

| View | Repositories represented | Full repositories | Specifications | Meaning |
|---|---:|---:|---:|---|
| Qualified portfolio | 43 | 40 | 2606/2705 | One strongest authority-bound artifact per repository; mixed mode |
| Proof subset | 37 | 35 | 2286/2382 | Only repositories whose selected artifact is proof mode |
| Codeproof subset | 6 | 5 | 320/323 | Only repositories whose selected artifact is codeproof mode |
| Initial baseline | 43 | 2 | 1030/2705 | Campaign starting point |
| Improvement | 43 | +38 | +1576 | Portfolio change, not a uniform-mode ablation |

The three incomplete repositories are:

| Repository | Mode | Accepted | Residual | Status |
|---|---|---:|---:|---|
| DedekindReals | proof | 0/82 | 82 | Frozen spec module fails elaboration before proof search |
| FLoCq | proof | 189/203 | 14 | Wrapper/decoder/native-Float parent gaps; two other specs pass by formal audit |
| Verdict | codeproof | 116/119 | 3 | Opaque, non-editable conversion lacks preservation contract |

Per-repository rows, report hashes, plan roots, receipt roots, and artifact
hashes are in `full-results.csv` and `full-results.json`.

## Result authority

Each row in the qualified portfolio points to an official report produced by
the frozen Vero evaluation implementation. Forty rows additionally carry a
signed v2 plan and terminal build receipt; DedekindReals, Piggybank, and
Pythonconstraint are retained as pinned untouched-Vero baseline reports without
Synthesa Act receipts. The campaign verifier re-hashes every live report and
all authority artifacts that a row declares. The private bundle then runs the
upstream `vero-extract` over each exact graded clean sandbox. The benchmark
maintainers can ignore Synthesa's campaign object and independently grade those
extracted artifacts.

## Formal-audit accounting

Specifications accepted through Vero's audit polarity count only when an
axiom-clean `disprove_*`, `unsat_*`, or accepted joint audit is present in the
artifact and the Vero grader marks it passed. Source observations and GIGO
decisions do not count. The FLoCq issue deliberately illustrates this
distinction.

## Comparison boundary

The Vero paper reports 27/43 for its strongest codeproof configuration and
25/43 for its strongest proof configuration. Because this campaign selects
mode per repository and was developed iteratively against the benchmark, its
40/43 portfolio is not an apples-to-apples single-run replacement for either
baseline. Independent grading still establishes the artifact validity; it does
not erase the experimental-design difference.
