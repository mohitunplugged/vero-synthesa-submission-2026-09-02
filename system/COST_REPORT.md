# Cost and model-use report

## Two cost surfaces

### Frozen scoring replay

- Generative-model calls: **0**
- Generative-model tokens: **0**
- Generative-model API cost: **USD 0**

This means all proposal outputs needed by the final artifacts have already been
compiled and pinned. A maintainer can grade the extracted artifacts without
calling Qwen, DeepSeek, GPT, Claude, Codex, or any hosted model. It does **not**
mean the artifacts were created without model-assisted research.

### Metered external proposer R&D

| Model | Calls | Prompt tokens | Completion tokens | Total tokens | Cost (USD) |
|---|---:|---:|---:|---:|---:|
| Qwen 3.5 4B | 11 | 167,582 | 13,331 | 180,913 | 0.01845318 |
| DeepSeek V4 Flash | 16 | 401,988 | 6,329 | 408,317 | 0.052827032755 |
| GPT-5.5 | 4 | 40,414 | 13,054 | 53,468 | 0.56400550 |
| Claude Sonnet 4.6 | 2 | 18,038 | 1,663 | 19,701 | 0.07510605 |
| **Total** | **33** | **628,022** | **34,377** | **662,399** | **0.710391762755** |

This is a conservative scan of every uniquely priced NanoGPT response under
the Vero v3 research results tree, whether accepted, rejected, or diagnostic.
The per-call ledger includes response digests so entries cannot be silently
removed or duplicated.

## Unmetered costs

The following were not reliably captured and must not be represented by the
USD 0.71 figure:

- Codex orchestration used to conduct and implement the research campaign;
- human principal-engineering and review time;
- local Lean/Lake compilation and Vero grading CPU time;
- storage, network, and electricity;
- earlier exploratory work outside the scanned v3 results tree, if any.

Accordingly, the entry should report USD 0.710391762755 as **auditable external
proposer API spend**, zero as **frozen replay inference spend**, and total
development cost as **not fully metered**. If Vero requires one comparable
cost number, we should agree on a rerun protocol with Zhe and meter the complete
uniform-mode run end to end.

Machine-readable sources: `cost-summary.json` and `model-call-ledger.json`.
