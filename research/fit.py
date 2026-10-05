"""Instrumented PyDESeq2 fit used only by the research track."""
import warnings

import numpy as np
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats


def fit_research(counts: pd.DataFrame, metadata: pd.DataFrame, config: dict):
    required = {"design", "contrast", "fit_type", "size_factors_fit_type", "refit_cooks",
                "min_replicates", "n_cpus", "alpha", "cooks_filter", "independent_filter",
                "lfc_highlight"}
    if not required.issubset(config):
        raise ValueError(f"config missing keys: {sorted(required - set(config))}")
    if not counts.index.is_unique or not counts.columns.is_unique:
        raise ValueError("count IDs must be unique")
    if list(metadata.index) != list(counts.columns):
        raise ValueError("metadata must be aligned to count columns")
    dds = DeseqDataSet(
        counts=counts.T, metadata=metadata, design=config["design"],
        fit_type=config["fit_type"], size_factors_fit_type=config["size_factors_fit_type"],
        refit_cooks=config["refit_cooks"], min_replicates=config["min_replicates"],
        n_cpus=config["n_cpus"], quiet=True,
    )
    design = np.asarray(dds.obsm["design_matrix"], dtype=float)
    rank = int(np.linalg.matrix_rank(design))
    if rank != design.shape[1] or design.shape[0] <= rank:
        raise ValueError("design matrix must be full rank with residual degrees of freedom")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        dds.deseq2()
        stats = DeseqStats(
            dds, contrast=config["contrast"], alpha=config["alpha"],
            cooks_filter=config["cooks_filter"],
            independent_filter=config["independent_filter"],
            n_cpus=config["n_cpus"], quiet=True,
        )
        stats.summary()
    results = stats.results_df.copy().reindex(counts.index)
    results["significant"] = results.padj.notna() & (results.padj < config["alpha"])
    results["highlight"] = results.significant & (results.log2FoldChange.abs() >= config["lfc_highlight"])
    results["na_reason"] = "none"
    results.loc[results.pvalue.notna() & results.padj.isna(), "na_reason"] = "independent_filter"
    results.loc[results.pvalue.isna(), "na_reason"] = "nonfinite_estimate"
    cooks_outlier = dds.var.get("_pvalue_cooks_outlier")
    if cooks_outlier is not None:
        cooks_outlier = pd.Series(np.asarray(cooks_outlier, dtype=bool), index=dds.var_names)
        results.loc[results.pvalue.isna() & cooks_outlier.reindex(results.index, fill_value=False), "na_reason"] = "cooks_outlier"
    normalized = pd.DataFrame(dds.layers["normed_counts"].T, index=counts.index, columns=counts.columns)
    diagnostics = dds.var.copy().reindex(counts.index)
    diagnostics["converged"] = np.asarray(dds.var.get("LFC_converged", pd.Series(True, index=dds.var_names)), dtype=bool)
    diagnostics["pvalue_cooks_outlier"] = (
        np.asarray(cooks_outlier.reindex(counts.index, fill_value=False), dtype=bool)
        if cooks_outlier is not None else False
    )
    if "cooks" in dds.layers:
        cooks = np.asarray(dds.layers["cooks"])
        diagnostics["max_cooks"] = np.nanmax(cooks, axis=0)
        for sample, values in zip(counts.columns, cooks):
            diagnostics[f"cooks::{sample}"] = values
    info = {
        "warnings": list(dict.fromkeys(str(item.message) for item in caught)),
        "design_rank": rank, "design_columns": list(dds.obsm["design_matrix"].columns),
        "residual_degrees_of_freedom": int(design.shape[0] - rank),
        "size_factors": {str(k): float(v) for k, v in zip(counts.columns, dds.obs["size_factors"])},
        "effective_dispersion_fit": str(dds.uns.get("disp_function_type", config["fit_type"])),
        "lfc_scale": "log2; unshrunk; treated/control",
        "pydeseq2_version": __import__("importlib.metadata", fromlist=["version"]).version("pydeseq2"),
        "prior_disp_var": _json_array(dds.uns.get("prior_disp_var")),
        "independent_filter_threshold": None,
        "independent_filter_threshold_status": "unavailable_in_pydeseq2_0.5.4_adapter",
    }
    return results, normalized, diagnostics, info


def _json_array(value):
    if value is None:
        return None
    array = np.asarray(value)
    return array.item() if array.ndim == 0 else array.tolist()
