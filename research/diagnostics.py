"""Export PyDESeq2 0.5.4 baseline components for E2."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import time

import pandas as pd

from research.fit import fit_research
from research.inputs import read_paired_inputs
from research.io import write_run
from src.data import prefilter


def run(data: Path, config_path: Path, output: Path):
    started = time.perf_counter()
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    counts, metadata, input_info = read_paired_inputs(data)
    counts, keep = prefilter(counts, config["min_count"], config["min_samples"])
    results, normalized, diagnostics, fit_info = fit_research(counts, metadata, config)
    def sha256(path):
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    code_digest = hashlib.sha256()
    for path in sorted(Path(__file__).parent.rglob("*.py")):
        code_digest.update(path.relative_to(Path(__file__).parent).as_posix().encode())
        code_digest.update(path.read_bytes())
    info = {
        "run_id": output.name, "stage": "E2", "inputs": input_info,
        "input_sha256": {name: sha256(data / name) for name in ["counts.csv", "metadata.csv"]},
        "config_sha256": sha256(config_path), "code_sha256": code_digest.hexdigest(),
        "image_id": os.environ.get("AIRWAY_IMAGE_ID", "not_provided"),
        "config": config, "versions": {"pydeseq2": fit_info["pydeseq2_version"]},
        "design": config["design"], "contrast": config["contrast"],
        "universe": {"input_genes": len(keep), "tested_genes": len(counts),
                     "prefilter": f">={config['min_count']} in >={config['min_samples']} samples"},
        "options": {k: config[k] for k in ["fit_type", "size_factors_fit_type", "refit_cooks", "min_replicates", "cooks_filter", "independent_filter"]},
        "seeds": {}, "warnings": fit_info["warnings"],
        "design_rank": fit_info["design_rank"],
        "residual_degrees_of_freedom": fit_info["residual_degrees_of_freedom"],
        "size_factors": fit_info["size_factors"],
        "prior_disp_var": fit_info["prior_disp_var"],
        "independent_filter_threshold": fit_info["independent_filter_threshold"],
        "independent_filter_threshold_status": fit_info["independent_filter_threshold_status"],
        "status": "complete",
        "elapsed_seconds": time.perf_counter() - started,
        "peak_memory_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
    }
    write_run(output, {
        "results": results, "normalized_counts": normalized,
        "gene_diagnostics": diagnostics,
        "size_factors": pd.DataFrame.from_dict(fit_info["size_factors"], orient="index", columns=["size_factor"]),
    }, info)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.data, args.config, args.output)
