# Final local authority check

Date: 2026-09-02 UTC

The qualified campaign compiler was invoked against the live v165 aggregate:

```bash
/home/mohitm/decision-platform/research/vero-v3/results/ntheory-jacobi-closure-v1/bin/synthesa-vero-v87 \
  campaign-verify \
  --input /home/mohitm/decision-platform/research/vero-v3/results/campaign-current-v165/FULL_43_CAMPAIGN_CURRENT.json \
  --live=true
```

Output:

```text
VERIFIED FULL_43_CAMPAIGN_COMPLETE cfd0bc418a41ca32eb5b8ede967d2e55c4be38ca514fc0b6e503369711ea3d8c 40/43 2606/2705
```

This verifies the local content/lineage aggregate. It is not a substitute for
the Vero maintainers' independent grading of the extracted artifacts.

The upstream Vero evaluator was also run directly over the two extracted
artifacts with non-empty `extras` arrays. Vero dropped those records before the
clean render and reproduced:

- Sortedcontainers codeproof: 49/49;
- Unicode proof: 46/46.

The machine-readable preflight is
`private-replication/preflight/summary.json` with decision
`EXTRAS_DROPPED_RESULTS_REPRODUCED`.
