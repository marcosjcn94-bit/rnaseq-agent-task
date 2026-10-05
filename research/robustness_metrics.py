"""Metrics for overlapping leave-one-donor-pair-out folds."""
import numpy as np
import pandas as pd


def wald_interval(log2_fold_change, standard_error, z=1.96):
    if not np.isfinite(log2_fold_change) or not np.isfinite(standard_error):
        return np.nan, np.nan
    return log2_fold_change - z * standard_error, log2_fold_change + z * standard_error


def summarize_folds(baseline, folds, thresholds=(0.25, 0.5, 1.0)):
    rows = []
    fold_count = int(folds.excluded_donor.nunique())
    by_gene = {gene_id: part for gene_id, part in folds.groupby("gene_id", sort=False)}
    for gene_id, base in baseline.iterrows():
        part = by_gene.get(gene_id, folds.iloc[0:0])
        estimable = part.loc[(part.status == "estimable") & np.isfinite(part.log2FoldChange)]
        baseline_lfc = float(base.log2FoldChange)
        values = estimable.log2FoldChange.to_numpy(dtype=float)
        same_sign = (np.sign(values) == np.sign(baseline_lfc)) if len(values) else np.array([], dtype=bool)
        max_change = float(np.max(np.abs(values - baseline_lfc))) if len(values) else np.nan
        amplitude = float(np.max(values) - np.min(values)) if len(values) else np.nan
        row = {
            "gene_id": gene_id, "baseline_log2FoldChange": baseline_lfc,
            "folds_expected": fold_count, "estimable_folds": int(len(values)),
            "not_estimable_folds": int(fold_count - len(values)),
            "sign_concordance": float(np.mean(same_sign)) if len(values) else np.nan,
            "max_abs_lfc_change": max_change, "fold_lfc_amplitude": amplitude,
        }
        for threshold in thresholds:
            label = str(threshold).replace(".", "_")
            row[f"stable_{label}"] = bool(
                abs(baseline_lfc) >= 1.0 and len(values) == fold_count
                and same_sign.all() and max_change <= threshold
            )
        rows.append(row)
    return pd.DataFrame(rows).set_index("gene_id")
