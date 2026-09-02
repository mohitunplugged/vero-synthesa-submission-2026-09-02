#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INVENTORY="$ROOT/inventory.json"

test -f "$ROOT/MANIFEST.sha256"
(
  cd "$ROOT"
  sha256sum --check MANIFEST.sha256
)

test "$(jq 'length' "$INVENTORY")" -eq 43
test "$(jq '[.[] | select(.full_repository)] | length' "$INVENTORY")" -eq 40
test "$(jq '[.[].passed_specs] | add' "$INVENTORY")" -eq 2606
test "$(jq '[.[].total_specs] | add' "$INVENTORY")" -eq 2705

extra_total=0
while IFS= read -r row; do
  artifact="$ROOT/$(jq -r '.artifact' <<<"$row")"
  expected_sha="$(jq -r '.artifact_sha256' <<<"$row")"
  benchmark_id="$(jq -r '.benchmark_id' <<<"$row")"
  mode="$(jq -r '.mode' <<<"$row")"

  test -f "$artifact"
  test "$(sha256sum "$artifact" | awk '{print $1}')" = "$expected_sha"
  test "$(jq -r '.benchmark_id' "$artifact")" = "$benchmark_id"
  test "$(jq -r '.mode' "$artifact")" = "$mode"
  test "$(jq '.file_errors | length' "$artifact")" -eq 0
  extra_total=$((extra_total + $(jq '.extras | length' "$artifact")))
done < <(jq -c '.[]' "$INVENTORY")

test "$extra_total" -eq 10
test "$(jq '[.[] | select(.mode=="proof")] | length' "$INVENTORY")" -eq 37
test "$(jq '[.[] | select(.mode=="codeproof")] | length' "$INVENTORY")" -eq 6
test "$(jq '.development_calls' "$ROOT/results/cost-summary.json")" -eq 33
test "$(jq '.scoring_replay_model_calls' "$ROOT/results/cost-summary.json")" -eq 0

printf '%s\n' 'VERO_EXTRACTED_SUBMISSION_VERIFIED'
