"""Summarize Python/R leave-one-donor-pair-out E3 outputs."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from research.robustness_metrics import summarize_folds


def stability_summary(label, baseline, folds):
    metrics = summarize_folds(baseline, folds, (0.25, 0.5, 1.0))
    high = metrics.loc[metrics.baseline_log2FoldChange.abs() >= 1]
    finite = high.max_abs_lfc_change.dropna()
    lists = []
    full_sig = set(baseline.index[baseline.padj.notna() & (baseline.padj < 0.05)])
    for donor in sorted(folds.excluded_donor.unique()):
        part = folds.loc[folds.excluded_donor == donor].set_index("gene_id")
        sig = set(part.index[part.padj.notna() & (part.padj < 0.05)])
        lists.append({"excluded_donor": str(donor), "significant_genes": len(sig),
                      "lost_vs_full": len(full_sig-sig), "gained_vs_full": len(sig-full_sig)})
    return metrics, {
        "engine": label, "genes": len(baseline), "high_effect_baseline_genes": int(len(high)),
        "estimable_folds_distribution": {str(int(k)): int(v) for k,v in metrics.estimable_folds.value_counts().sort_index().items()},
        "sign_concordant_all_estimable_high_effect": int((high.sign_concordance == 1).sum()),
        "median_max_abs_lfc_change_high_effect": float(finite.median()) if len(finite) else None,
        "p95_max_abs_lfc_change_high_effect": float(finite.quantile(0.95)) if len(finite) else None,
        "stable_high_effect_counts": {
            str(t): int(high[f"stable_{str(t).replace('.', '_')}"].sum()) for t in (0.25, 0.5, 1.0)
        },
        "list_changes": lists,
    }


def main(root: Path, output: Path):
    py_base = pd.read_csv(root.parent / "E2/python-baseline/results.csv", index_col=0)
    r_base = pd.read_csv(root / "r-v3/baseline_results_mle.csv").set_index("gene_id")
    py_folds = pd.read_csv(root / "python/fold_results.csv")
    r_folds = pd.read_csv(root / "r-v3/fold_results.csv")
    py_metrics, py_summary = stability_summary("PyDESeq2 0.5.4", py_base, py_folds)
    r_metrics, r_summary = stability_summary("DESeq2 1.50.2", r_base, r_folds)
    cross = []
    for donor in sorted(set(py_folds.excluded_donor) & set(r_folds.excluded_donor)):
        p = py_folds.loc[py_folds.excluded_donor == donor].set_index("gene_id")
        r = r_folds.loc[r_folds.excluded_donor == donor].set_index("gene_id")
        delta = (p.log2FoldChange-r.log2FoldChange).abs().replace([np.inf,-np.inf],np.nan).dropna()
        cross.append({"excluded_donor": str(donor), "genes_compared": int(len(delta)),
                      "absolute_lfc_difference_median": float(delta.median()),
                      "absolute_lfc_difference_p95": float(delta.quantile(0.95)),
                      "absolute_lfc_difference_max": float(delta.max())})
    rmanifest = json.loads((root / "r-v3/manifest.json").read_text(encoding="utf-8"))
    summary = {
        "status": "complete", "fixed_universe_genes": int(len(py_base)),
        "four_paired_folds": sorted(py_folds.excluded_donor.unique().tolist()),
        "python": py_summary, "r": r_summary, "cross_engine_fold_effects": cross,
        "apeglm_rank_correlation_absolute_effect": rmanifest["shrinkage"]["spearman_abs_effect_rank"],
        "interpretation_limit": "The four leave-one-pair-out folds overlap; they are sensitivity checks, not independent studies or a jackknife confidence interval.",
    }
    output.mkdir(parents=True, exist_ok=False)
    (output/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
    py_metrics.to_csv(output/"python_gene_stability.csv",index=True,na_rep="")
    r_metrics.to_csv(output/"r_gene_stability.csv",index=True,na_rep="")
    print(json.dumps(summary,indent=2,sort_keys=True))


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    main(args.root,args.output)
