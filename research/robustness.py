"""Leave-one-donor-pair-out sensitivity analysis for the fixed gene universe."""
import argparse
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import resource
import time

import numpy as np
import pandas as pd

from research.fit import fit_research
from research.inputs import read_paired_inputs
from research.io import write_run
from research.robustness_metrics import summarize_folds, wald_interval


def run(data: Path, config_path: Path, baseline_path: Path, output: Path):
    started = time.perf_counter()
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    counts, metadata, input_info = read_paired_inputs(data, min_pairs=4)
    baseline = pd.read_csv(Path(baseline_path) / "results.csv", index_col=0)
    counts = counts.reindex(baseline.index)
    if counts.isna().any().any() or len(counts) != 16139:
        raise ValueError("baseline result IDs differ from the fixed 16,139-gene universe")
    all_rows, fold_info = [], []
    for donor in metadata.donor.cat.categories:
        samples = metadata.index[metadata.donor != donor].tolist()
        fold_counts = counts.loc[:, samples]
        fold_metadata = metadata.loc[samples].copy()
        fold_metadata["donor"] = fold_metadata.donor.cat.remove_unused_categories()
        fold_metadata["condition"] = fold_metadata.condition.cat.remove_unused_categories()
        not_estimable = fold_counts.sum(axis=1) == 0
        usable = fold_counts.loc[~not_estimable]
        results, _, diagnostics, info = fit_research(usable, fold_metadata, config)
        per_fold = pd.DataFrame(index=counts.index)
        per_fold["excluded_donor"] = str(donor)
        per_fold["status"] = "not_estimable"
        for column in ["log2FoldChange", "lfcSE", "pvalue", "padj"]:
            per_fold[column] = np.nan
        valid = results.log2FoldChange.notna() & results.lfcSE.notna()
        per_fold.loc[results.index[valid], "status"] = "estimable"
        per_fold.loc[results.index, ["log2FoldChange", "lfcSE", "pvalue", "padj"]] = results[["log2FoldChange", "lfcSE", "pvalue", "padj"]]
        intervals = [wald_interval(lfc, se) for lfc, se in zip(per_fold.log2FoldChange, per_fold.lfcSE)]
        per_fold["ci95_low"] = [item[0] for item in intervals]
        per_fold["ci95_high"] = [item[1] for item in intervals]
        per_fold.index.name = "gene_id"
        all_rows.append(per_fold.reset_index())
        fold_info.append({
            "excluded_donor": str(donor), "samples": samples,
            "pairs": int(fold_metadata.donor.nunique()), "design_rank": info["design_rank"],
            "residual_degrees_of_freedom": info["residual_degrees_of_freedom"],
            "not_estimable_all_zero": int(not_estimable.sum()), "warnings": info["warnings"],
        })
    fold_table = pd.concat(all_rows, ignore_index=True)
    stability = summarize_folds(baseline, fold_table, tuple(config["stability_thresholds"]))
    full_sig = set(baseline.index[baseline.padj.notna() & (baseline.padj < config["alpha"])])
    list_changes = []
    for donor in metadata.donor.cat.categories:
        part = fold_table.loc[fold_table.excluded_donor == str(donor)].set_index("gene_id")
        significant = set(part.index[part.padj.notna() & (part.padj < config["alpha"])])
        list_changes.append({
            "excluded_donor": str(donor), "significant_genes": len(significant),
            "lost_vs_full": len(full_sig-significant), "gained_vs_full": len(significant-full_sig),
        })
    code_digest = hashlib.sha256()
    for path in sorted(Path(__file__).parent.rglob("*.py")):
        code_digest.update(path.relative_to(Path(__file__).parent).as_posix().encode())
        code_digest.update(path.read_bytes())
    def sha256(path):
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    info = {
        "run_id": output.name, "stage": "E3", "status": "complete",
        "input_sha256": {name: sha256(data/name) for name in ["counts.csv", "metadata.csv"]},
        "baseline_manifest_sha256": sha256(Path(baseline_path)/"manifest.json"),
        "config_sha256": sha256(config_path), "code_sha256": code_digest.hexdigest(),
        "image_id": os.environ.get("AIRWAY_IMAGE_ID", "not_provided"),
        "versions": {"pydeseq2": version("pydeseq2")},
        "design": config["design"], "contrast": config["contrast"],
        "universe": {"fixed_baseline_genes": len(baseline), "folds": len(fold_info)},
        "options": config, "seeds": {}, "input_manifest": input_info,
        "folds": fold_info, "significant_list_changes": list_changes,
        "stability_threshold_counts": {
            str(t): int(stability[f"stable_{str(t).replace('.', '_')}"].sum())
            for t in config["stability_thresholds"]
        },
        "warnings": [warning for fold in fold_info for warning in fold["warnings"]],
        "elapsed_seconds": time.perf_counter()-started,
        "peak_memory_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
    }
    write_run(output, {"fold_results": fold_table.set_index(["gene_id", "excluded_donor"]),
                       "stability": stability, "significant_list_changes": pd.DataFrame(list_changes)}, info)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--baseline-results", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.data, args.config, args.baseline_results, args.output)
