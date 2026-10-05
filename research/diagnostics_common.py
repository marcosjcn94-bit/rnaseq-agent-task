"""Small, testable transformations shared by Python-side diagnostics."""
import numpy as np
import pandas as pd


def natural_log_to_log2(values):
    return np.asarray(values, dtype=float) / np.log(2.0)


def benjamini_hochberg(pvalues):
    values = np.asarray(pvalues, dtype=float)
    result = np.full(values.shape, np.nan)
    valid = np.isfinite(values)
    p = values[valid]
    if np.any((p < 0) | (p > 1)):
        raise ValueError("p-values must lie in [0, 1]")
    order = np.argsort(p, kind="stable")
    adjusted = p[order] * len(p) / np.arange(1, len(p) + 1)
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
    restored = np.empty_like(adjusted)
    restored[order] = np.minimum(adjusted, 1.0)
    result[valid] = restored
    return result


def compare_result_tables(python: pd.DataFrame, r: pd.DataFrame, alpha=0.05):
    joined = python.join(r, how="outer", lsuffix="_python", rsuffix="_r", validate="one_to_one")
    for engine in ("python", "r"):
        padj = joined[f"padj_{engine}"]
        joined[f"significant_{engine}"] = padj.notna() & (padj < alpha)
    joined["classification"] = np.select(
        [joined.significant_python & joined.significant_r,
         joined.significant_python & ~joined.significant_r,
         ~joined.significant_python & joined.significant_r],
        ["concordant_significant", "python_only", "r_only"], default="concordant_not_significant",
    )
    joined["padj_missing_python"] = joined.padj_python.isna()
    joined["padj_missing_r"] = joined.padj_r.isna()
    joined["python_distance_to_alpha"] = (joined.padj_python - alpha).abs()
    joined["r_distance_to_alpha"] = (joined.padj_r - alpha).abs()
    return joined
