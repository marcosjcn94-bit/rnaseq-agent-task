"""Metrics for known-truth differential expression simulations."""
from __future__ import annotations

import numpy as np
import pandas as pd


def empirical_donor_effect_sd(diagnostics):
    columns = [c for c in diagnostics.columns if c.startswith("donor_")]
    if len(columns) != 3:
        raise ValueError(f"expected three fitted donor contrasts, found {len(columns)}")
    effects = diagnostics[columns].to_numpy(dtype=float) / np.log(2)
    if not np.isfinite(effects).all():
        raise ValueError("donor contrast estimates contain nonfinite values")
    effects = np.column_stack([np.zeros(len(effects)), effects])
    centered = effects - effects.mean(axis=1, keepdims=True)
    return float(np.sqrt(np.sum(centered**2) / (len(effects) * (effects.shape[1] - 1))))


def sample_negative_binomial(rng, mu, dispersion):
    """Draw NB counts parameterized by Var(Y)=mu+dispersion*mu**2."""
    mu, dispersion = np.asarray(mu, float), np.asarray(dispersion, float)
    if np.any(mu < 0) or np.any(dispersion <= 0) or not np.isfinite(mu).all() or not np.isfinite(dispersion).all():
        raise ValueError("mu must be finite/nonnegative and dispersion finite/positive")
    size = 1 / dispersion
    return rng.negative_binomial(size, size / (size + mu))


def metrics(truth, rejected, estimate, se, alpha=0.05):
    truth = np.asarray(truth, dtype=bool)
    rejected = np.asarray(rejected, dtype=bool)
    estimate, se = np.asarray(estimate, float), np.asarray(se, float)
    if not (truth.shape == rejected.shape == estimate.shape == se.shape):
        raise ValueError("truth and result vectors must have matching shapes")
    if np.any(se < 0) or not 0 < alpha < 1:
        raise ValueError("invalid standard errors or alpha")
    n_rej, n_true = rejected.sum(), truth.sum()
    fdp = ((rejected & ~truth).sum() / max(n_rej, 1))
    power = (rejected & truth).sum() / max(n_true, 1) if n_true else float("nan")
    null = ~truth
    type1 = (rejected & null).sum() / max(null.sum(), 1) if null.any() else float("nan")
    z = 1.959963984540054
    covered = (estimate - z * se <= 0) & (estimate + z * se >= 0)
    coverage = float(np.mean(covered[truth])) if truth.any() else float("nan")
    return {"fdp": float(fdp), "power": float(power), "type1": float(type1),
            "coverage": coverage, "rejections": int(n_rej)}


def summarize_replicates(per_rep):
    coverage_col = "coverage" if "coverage" in per_rep.columns else "coverage_zero"
    grouped = per_rep.groupby(["engine", "pairs", "de_fraction", "interaction_sd"], dropna=False)
    return grouped.agg(
        replicates=("replicate", "count"),
        failures=("failure", lambda x: int((x.notna() & x.astype(str).str.len().gt(0)).sum())),
        fdp_mean=("fdp", "mean"),
        fdp_mcse=("fdp", lambda x: x.std(ddof=1)/np.sqrt(x.notna().sum())),
        power_mean=("power", "mean"),
        power_mcse=("power", lambda x: x.std(ddof=1)/np.sqrt(x.notna().sum())),
        type1_mean=("type1", "mean"),
        type1_mcse=("type1", lambda x: x.std(ddof=1)/np.sqrt(x.notna().sum())),
        coverage_mean=(coverage_col, "mean"),
        coverage_mcse=(coverage_col, lambda x: x.std(ddof=1)/np.sqrt(x.notna().sum())),
        testable_mean=("testable", "mean"),
    ).reset_index()
