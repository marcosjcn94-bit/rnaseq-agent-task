"""Create a separate auditable scenario summary from completed replicate rows."""
import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

from research import simulation_metrics
from research.simulation_metrics import summarize_replicates


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicates", type=Path, required=True)
    parser.add_argument("--execution-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        raise ValueError("summary output must be a new empty directory")
    args.output.mkdir(parents=True, exist_ok=True)
    rows = pd.read_csv(args.replicates)
    if rows.duplicated(["engine", "pairs", "de_fraction", "interaction_sd", "replicate"]).any():
        raise ValueError("replicate IDs must be unique within a scenario")
    summary = summarize_replicates(rows)
    summary.to_csv(args.output / "scenario-summary.csv", index=False)
    manifest = {"status": "summary_complete", "replicate_rows": len(rows),
        "replicates_sha256": sha256(args.replicates),
        "execution_manifest_sha256": sha256(args.execution_manifest),
        "summary_code_sha256": sha256(Path(__file__)),
        "metric_code_sha256": sha256(Path(simulation_metrics.__file__)),
        "execution": json.loads(args.execution_manifest.read_text(encoding="utf-8-sig")),
        "summary_file_sha256": sha256(args.output / "scenario-summary.csv")}
    (args.output / "manifest-summary.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "scenarios": len(summary), "rows": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
