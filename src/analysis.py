"""Paired bulk RNA-seq analysis delegated to PyDESeq2."""
import warnings
import numpy as np
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

def fit(counts, metadata, config):
    dds = DeseqDataSet(
        counts=counts.T, metadata=metadata,
        design=config["design"], fit_type=config["fit_type"],
        size_factors_fit_type=config["size_factors_fit_type"],
        refit_cooks=config["refit_cooks"],min_replicates=config["min_replicates"],
        n_cpus=config["n_cpus"],quiet=True,
    )
    design = np.asarray(dds.obsm["design_matrix"],dtype=float)
    rank = int(np.linalg.matrix_rank(design))
    if rank != design.shape[1] or design.shape[0] <= rank:
        raise ValueError("design matrix must be full rank with residual degrees of freedom")
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        dds.deseq2()
        stats = DeseqStats(
            dds,contrast=config["contrast"],alpha=config["alpha"],
            cooks_filter=config["cooks_filter"],
            independent_filter=config["independent_filter"],
            n_cpus=config["n_cpus"],quiet=True,
        )
        stats.summary()
    result = stats.results_df.copy().reindex(counts.index)
    result["significant"] = result.padj.notna() & (result.padj < config["alpha"])
    result["highlight"] = result.significant & (result.log2FoldChange.abs() >= config["lfc_highlight"])
    result["na_reason"] = "none"
    independent = result.pvalue.notna() & result.padj.isna()
    result.loc[independent,"na_reason"] = "independent_filter"
    missing = result.pvalue.isna()
    result.loc[missing,"na_reason"] = "nonfinite_estimate"
    if "_pvalue_cooks_outlier" in dds.var:
        cooks = pd.Series(np.asarray(dds.var["_pvalue_cooks_outlier"],dtype=bool),index=dds.var_names)
        result.loc[missing & cooks.reindex(result.index,fill_value=False),"na_reason"] = "cooks_outlier"
    normalized = pd.DataFrame(dds.layers["normed_counts"].T,index=counts.index,columns=counts.columns)
    info = {
        "warnings":list(dict.fromkeys(str(item.message) for item in captured)),
        "design_rank":rank,"design_columns":list(dds.obsm["design_matrix"].columns),
        "residual_degrees_of_freedom":int(design.shape[0]-rank),
        "size_factors":{str(k):float(v) for k,v in zip(counts.columns,dds.obs["size_factors"])},
        "effective_dispersion_fit":str(dds.uns.get("disp_function_type",config["fit_type"])),
        "lfc_scale":"log2; unshrunk; treated/control",
    }
    return result, normalized, info
