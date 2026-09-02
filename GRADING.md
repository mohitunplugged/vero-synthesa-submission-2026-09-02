# Grading instructions

## Frozen inputs

Clone Vero and check out exactly:

```bash
git clone https://github.com/sunblaze-ucb/vero.git
cd vero
git checkout 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
```

Use the repository's documented environment and Lean
`leanprover/lean4:v4.29.1`.

## Artifact mapping

`inventory.json` is the canonical mapping. Each row includes:

```text
repository
benchmark_id
mode
source_benchmark
artifact
artifact_sha256
passed_specs / total_specs
full_repository
```

Do not infer a mode from the filename alone; verify that the inventory, the
artifact's `mode`, and the grader mode agree.

## Preferred grading path

Use the Vero team's own artifact-ingestion path to:

1. load the artifact;
2. render a new sandbox from the source benchmark;
3. overlay only expected scheduled slot bodies;
4. drop `artifact.extras`;
5. build the repository harness;
6. check declaration hygiene and axioms;
7. evaluate every spec; and
8. emit a new report.

This is the same authority boundary described by Vero's fully decoupled agent
workflow:

<https://github.com/sunblaze-ucb/vero/blob/main/docs/agents.md#option-b-fully-decoupled-no-vero-code>

## Convenience runner

From this repository:

```bash
python tools/grade_submission.py \
  --vero-root /absolute/path/to/vero \
  --output /absolute/path/to/new/grading-output
```

To grade one or more repositories first:

```bash
python tools/grade_submission.py \
  --vero-root /absolute/path/to/vero \
  --output /absolute/path/to/new/grading-output \
  --only sortedcontainers unicode
```

The script imports Vero's own `read_artifact` and `run_evaluation` functions;
it does not implement a second grader. The final authority should still be the
maintainers' normal process.

## Expected aggregate

```text
repositories: 43
full repositories: 40
passed specifications: 2606
total specifications: 2705
```

Mode subsets:

```text
proof:     37 repositories, 35 full, 2286/2382 specs
codeproof:  6 repositories,  5 full,  320/323 specs
```

Expected incomplete repositories:

```text
dedekind_reals  proof      0/82
flocq           proof    189/203
verdict         codeproof 116/119
```

If a result differs, please retain the generated sandbox, report, Vero commit,
Lean toolchain, and failing diagnostic. Do not edit the submitted artifact;
we will reconcile the mismatch against its SHA-256.
