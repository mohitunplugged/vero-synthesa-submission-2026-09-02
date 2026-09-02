#!/usr/bin/env python3
"""Convenience wrapper around Vero's own clean-render evaluation function.

The Vero maintainers may ignore this wrapper and use their normal private
submission runner. It intentionally contains no proof, score, or axiom logic.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

VERO_COMMIT = "0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vero-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--only", nargs="*", default=[])
    parser.add_argument("--timeout", type=int, default=900)
    return parser.parse_args()


def git_head(repo: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()


def benchmark_map(vero_root: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for manifest in sorted((vero_root / "benchmarks").glob("*/manifest.json")):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        benchmark_id = data.get("benchmark_id") or data.get("id")
        if benchmark_id:
            result[benchmark_id] = manifest.parent
    return result


def main() -> int:
    args = parse_args()
    submission_root = Path(__file__).resolve().parent.parent
    inventory = json.loads(
        (submission_root / "inventory.json").read_text(encoding="utf-8")
    )

    actual_head = git_head(args.vero_root)
    if actual_head != VERO_COMMIT:
        raise SystemExit(
            f"refusing Vero drift: expected {VERO_COMMIT}, got {actual_head}"
        )
    if args.output.exists() and any(args.output.iterdir()):
        raise SystemExit(f"output must be new or empty: {args.output}")
    args.output.mkdir(parents=True, exist_ok=True)

    sys.path.insert(0, str(args.vero_root / "src"))
    from vero.evaluation.runner import run_evaluation
    from vero.generation.extractor import read_artifact

    benchmarks = benchmark_map(args.vero_root)
    requested = set(args.only)
    if requested:
        known = {row["repository"] for row in inventory}
        unknown = requested - known
        if unknown:
            raise SystemExit(f"unknown --only repositories: {sorted(unknown)}")
        inventory = [row for row in inventory if row["repository"] in requested]

    rows: list[dict] = []
    for row in inventory:
        repository = row["repository"]
        benchmark_id = row["benchmark_id"]
        mode = row["mode"]
        benchmark_dir = benchmarks.get(benchmark_id)
        if benchmark_dir is None:
            raise SystemExit(f"no benchmark manifest for {benchmark_id}")

        artifact_path = submission_root / row["artifact"]
        artifact = read_artifact(artifact_path)
        if artifact.benchmark_id != benchmark_id or artifact.mode != mode:
            raise SystemExit(f"artifact identity mismatch: {artifact_path}")

        run_root = args.output / repository.replace("/", "_")
        run_evaluation(
            benchmark_dir=benchmark_dir,
            artifact=artifact,
            mode=mode,
            eval_sandbox_dir=run_root / "clean-sandbox",
            report_dir=run_root / "report",
            lake_timeout=args.timeout,
        )
        report_path = run_root / "report" / "report.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        summary = report["summary"]
        reproduced = (
            summary["passed_specs"] == row["passed_specs"]
            and summary["total_specs"] == row["total_specs"]
        )
        rows.append(
            {
                "repository": repository,
                "benchmark_id": benchmark_id,
                "mode": mode,
                "expected_passed_specs": row["passed_specs"],
                "actual_passed_specs": summary["passed_specs"],
                "total_specs": summary["total_specs"],
                "reproduced": reproduced,
                "report": str(report_path.relative_to(args.output)),
            }
        )
        print(
            f"{repository}: {summary['passed_specs']}/{summary['total_specs']} "
            f"({'MATCH' if reproduced else 'MISMATCH'})",
            flush=True,
        )

    output = {
        "schema": "synthesa.vero.maintainer-grading-convenience.v1",
        "vero_commit": actual_head,
        "rows": rows,
        "metrics": {
            "repositories": len(rows),
            "reproduced": sum(1 for row in rows if row["reproduced"]),
            "passed_specs": sum(row["actual_passed_specs"] for row in rows),
            "total_specs": sum(row["total_specs"] for row in rows),
        },
        "decision": (
            "REPRODUCED" if all(row["reproduced"] for row in rows) else "MISMATCH"
        ),
    }
    summary_path = args.output / "grading-summary.json"
    summary_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(summary_path)
    return 0 if output["decision"] == "REPRODUCED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
