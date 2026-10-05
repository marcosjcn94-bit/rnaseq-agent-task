"""Summarize the prespecified E2 one-option-at-a-time runs."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from research.diagnostics_common import compare_result_tables


def load_results(root, path, engine):
    frame = pd.read_csv(root / path / "results.csv", index_col=0 if engine == "python" else "gene_id")
    return frame


def effect(summary, baseline, experiment, engine, other_baseline, other_engine):
    base = load_results(summary, baseline, engine)
    changed = load_results(summary, experiment, engine)
    other = load_results(summary, other_baseline, other_engine)
    same = np.isclose(base.pvalue.to_numpy(float), changed.pvalue.to_numpy(float), rtol=0, atol=1e-12, equal_nan=True)
    padj_same = np.isclose(base.padj.to_numpy(float), changed.padj.to_numpy(float), rtol=0, atol=1e-12, equal_nan=True)
    significant_base = base.padj.notna() & (base.padj < 0.05)
    significant_changed = changed.padj.notna() & (changed.padj < 0.05)
    baseline_join = compare_result_tables(base[["padj"]], other[["padj"]])
    changed_join = compare_result_tables(changed[["padj"]], other[["padj"]])
    original_discordant = baseline_join.classification.isin(["python_only", "r_only"])
    return {
        "pvalue_changed_genes": int((~same).sum()),
        "padj_changed_genes": int((~padj_same).sum()),
        "significance_membership_changed": int((significant_base != significant_changed).sum()),
        "significant_before": int(significant_base.sum()),
        "significant_after": int(significant_changed.sum()),
        "discordant_genes_after": int(changed_join.classification.isin(["python_only", "r_only"]).sum()),
        "baseline_discordant_genes_reclassified": int((baseline_join.classification != changed_join.classification)[original_discordant].sum()),
    }


def difference_metrics(left, right):
    values = (left.astype(float) - right.astype(float)).abs().replace([np.inf, -np.inf], np.nan).dropna()
    return {
        "n": int(len(values)), "median": float(values.median()),
        "p95": float(values.quantile(0.95)), "max": float(values.max()),
    }


def main(root: Path, output: Path):
    py = load_results(root, "python-baseline", "python")
    r = load_results(root, "r-baseline-v3", "r")
    py_diag = pd.read_csv(root / "python-baseline" / "gene_diagnostics.csv", index_col=0)
    r_diag = pd.read_csv(root / "r-baseline-v3" / "gene_diagnostics.csv").set_index("gene_id")
    joined = compare_result_tables(py[["padj"]], r[["padj"]])
    cases = {}
    se_diff = (py.lfcSE - r.lfcSE).abs().dropna()
    cases["largest_se_difference"] = str(se_diff.idxmax())
    near = (r.padj - 0.05).abs().dropna()
    cases["nearest_r_padj_0_05"] = str(near.idxmin())
    filtered = r[r.pvalue.notna() & r.padj.isna()]
    if not filtered.empty:
        cases["r_independent_filter_case"] = str(filtered.baseMean.idxmin())
    concordant = joined[joined.classification == "concordant_significant"].index
    if len(concordant):
        cases["concordant_significant_control"] = str(r.loc[concordant, "baseMean"].idxmax())
    dispersion_differences = {
        "genewise_estimate": difference_metrics(py_diag.genewise_dispersions, r_diag.dispGeneEst),
        "fitted_trend": difference_metrics(py_diag.fitted_dispersions, r_diag.dispFit),
        "final_dispersion": difference_metrics(py_diag.dispersions, r_diag.dispersion),
        "map_dispersion": difference_metrics(py_diag.dispersions, r_diag.dispMAP),
    }
    case_details = {}
    for label, gene_id in cases.items():
        p = py.loc[gene_id]
        rr = r.loc[gene_id]
        pdg = py_diag.loc[gene_id]
        rdg = r_diag.loc[gene_id]
        case_details[label] = {
            "gene_id": gene_id,
            "python": {name: (None if pd.isna(p.get(name)) else float(p.get(name))) for name in ["log2FoldChange", "lfcSE", "stat", "pvalue", "padj"]},
            "r": {name: (None if pd.isna(rr.get(name)) else float(rr.get(name))) for name in ["log2FoldChange", "lfcSE", "stat", "pvalue", "padj", "baseMean"]},
            "python_dispersion": {name: (None if pd.isna(pdg.get(name)) else float(pdg.get(name))) for name in ["genewise_dispersions", "fitted_dispersions", "dispersions"]},
            "r_dispersion": {name: (None if pd.isna(rdg.get(name)) else float(rdg.get(name))) for name in ["dispGeneEst", "dispFit", "dispMAP"]},
            "classification": str(joined.loc[gene_id, "classification"]) if gene_id in joined.index else "not_in_joint_index",
        }
    summary = {
        "status": "complete",
        "genes_joined": int(len(joined)),
        "classification": {str(k): int(v) for k, v in joined.classification.value_counts().items()},
        "padj_missing": {"python": int(joined.padj_missing_python.sum()), "r": int(joined.padj_missing_r.sum())},
        "pvalue_missing": {"python": int(py.pvalue.isna().sum()), "r": int(r.pvalue.isna().sum())},
        "near_alpha_within_0_01": {
            "python": int((joined.python_distance_to_alpha <= 0.01).sum()),
            "r": int((joined.r_distance_to_alpha <= 0.01).sum()),
        },
        "effect_differences": {
            "lfcSE_abs_median": float(se_diff.median()),
            "lfcSE_abs_p95": float(se_diff.quantile(0.95)),
            "lfcSE_abs_max": float(se_diff.max()),
            "lfcSE_max_gene": str(se_diff.idxmax()),
            "abs_log2fc_median": float((py.log2FoldChange-r.log2FoldChange).abs().median()),
            "abs_log2fc_p95": float((py.log2FoldChange-r.log2FoldChange).abs().quantile(0.95)),
            "abs_wald_stat_median": float((py.stat-r.stat).abs().median()),
            "abs_wald_stat_p95": float((py.stat-r.stat).abs().quantile(0.95)),
        },
        "dispersion_differences": dispersion_differences,
        "prespecified_cases": cases,
        "case_details": case_details,
        "one_option_at_a_time": {
            "python_if_off": effect(root, "python-baseline", "python-if-off", "python", "r-baseline-v3", "r"),
            "r_if_off": effect(root, "r-baseline-v3", "r-if-off", "r", "python-baseline", "python"),
            "python_cooks_off": effect(root, "python-baseline", "python-cooks-off", "python", "r-baseline-v3", "r"),
            "r_cooks_off": effect(root, "r-baseline-v3", "r-cooks-off", "r", "python-baseline", "python"),
        },
        "interpretation": "Option effects are marginal contrasts and may overlap; do not sum changed-gene counts as exclusive causes.",
    }
    output.mkdir(parents=True, exist_ok=False)
    (output / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False)+"\n", encoding="utf-8")
    joined.to_csv(output / "joined-classification.csv", index=True, na_rep="")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    main(args.root, args.output)
