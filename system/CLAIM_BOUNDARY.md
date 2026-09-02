# Claim boundary

## Claims supported now

1. The campaign artifact binds 43 official Vero reports at Vero commit
   `0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09`.
2. Those reports total 2606 accepted specifications out of 2705 and contain 40
   full repositories.
3. The portfolio contains 37 proof-mode evaluations and six codeproof-mode
   evaluations.
4. The campaign records zero false acceptance: no Synthesa-only success was
   counted as an official Vero pass.
5. Frozen result replay requires no generative-model call. Exact proof and
   implementation slot bodies are already present in the extracted artifacts.
6. The research tree contains 33 uniquely priced NanoGPT proposer calls,
   totaling 662,399 tokens and USD 0.710391762755.

## Claims not supported

- **Not a uniform 40/43 proof-mode or codeproof-mode run.** Six repositories
  use codeproof and the rest use proof.
- **Not a blind one-pass agent evaluation.** This was an iterative,
  benchmark-seen systems research campaign.
- **Not a zero-model-development campaign.** Zero calls applies only to frozen
  scoring replay. Models were used 33 times as untrusted proposers during R&D.
- **Not a total cost of USD 0.71.** That is the auditable external proposer API
  spend. Codex orchestration, researcher time, local CPU, storage, and energy
  are not metered in the evidence tree.
- **Not 43/43.** DedekindReals, FLoCq, and Verdict remain incomplete.
- **Not an assertion that all 99 residual specifications are benchmark bugs.**
  The issue drafts distinguish accepted formal audits, translation concerns,
  missing proof-parent laws, and ordinary unfilled obligations.
- **Not independent confirmation.** Independent confirmation occurs only when
  the Vero maintainers grade the `vero-extract` artifacts.

## Public wording

Preferred:

> In an iterative, mixed-mode Vero research portfolio, Synthesa produced
> artifacts whose local untouched-Vero evaluations complete 40 of 43
> repositories and 2606 of 2705 specifications. The portfolio contains 37
> proof-mode and six codeproof-mode artifacts. We have supplied the extracted
> artifacts for independent maintainer grading and do not treat the result as
> a standard single-mode leaderboard row until the benchmark owners confirm
> eligibility.

Avoid:

> Synthesa scored 40/43 on the Vero leaderboard for $0.71 with zero model
> calls.

That sentence collapses mode, development, replay, cost, and independent
authority into one misleading claim.
