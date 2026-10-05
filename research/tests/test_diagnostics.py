import numpy as np
import pandas as pd
import pytest

from research.diagnostics_common import benjamini_hochberg, compare_result_tables, natural_log_to_log2
from research.fit import fit_research


def test_log_conversion_is_analytic_and_preserves_na():
    actual = natural_log_to_log2(np.array([np.log(2), np.log(4), np.nan]))
    np.testing.assert_allclose(actual[:2], [1, 2], rtol=0, atol=1e-14)
    assert np.isnan(actual[2])


def test_bh_matches_known_vector_and_preserves_na():
    actual = benjamini_hochberg([0.01, 0.04, 0.03, np.nan])
    np.testing.assert_allclose(actual[:3], [0.03, 0.04, 0.04])
    assert np.isnan(actual[3])


def test_join_keeps_all_gene_ids_and_reports_missingness():
    python = pd.DataFrame({"padj": [0.01, np.nan]}, index=["g1", "g2"])
    r = pd.DataFrame({"padj": [0.2, 0.02]}, index=["g1", "g3"])
    joined = compare_result_tables(python, r)
    assert set(joined.index) == {"g1", "g2", "g3"}
    assert joined.loc["g1", "classification"] == "python_only"
    assert joined.loc["g2", "padj_missing_r"]


def test_reversing_contrast_reverses_effect_without_changing_two_sided_pvalues():
    rng = np.random.default_rng(20261005)
    samples = ["C1", "T1", "C2", "T2", "C3", "T3", "C4", "T4"]
    metadata = pd.DataFrame({
        "donor": pd.Categorical(["D1", "D1", "D2", "D2", "D3", "D3", "D4", "D4"], categories=["D1", "D2", "D3", "D4"]),
        "condition": pd.Categorical(["control", "treated"]*4, categories=["control", "treated"], ordered=True),
    }, index=samples)
    base = rng.uniform(25, 400, 120)
    counts = pd.DataFrame({sample: rng.negative_binomial(12, 12/(12+base*(1.5 if sample.startswith("T") else 1))) for sample in samples},
                          index=[f"g{i}" for i in range(len(base))])
    common = {"design": "~ donor + condition", "fit_type": "parametric", "size_factors_fit_type": "ratio",
              "refit_cooks": False, "min_replicates": 7, "n_cpus": 1, "alpha": 0.05,
              "cooks_filter": False, "independent_filter": False, "lfc_highlight": 1}
    forward = fit_research(counts, metadata, {**common, "contrast": ["condition", "treated", "control"]})[0]
    reverse = fit_research(counts, metadata, {**common, "contrast": ["condition", "control", "treated"]})[0]
    np.testing.assert_allclose(forward.log2FoldChange, -reverse.log2FoldChange, rtol=1e-6, atol=1e-8, equal_nan=True)
    np.testing.assert_allclose(forward.stat, -reverse.stat, rtol=1e-6, atol=1e-8, equal_nan=True)
    np.testing.assert_allclose(forward.pvalue, reverse.pvalue, rtol=1e-6, atol=1e-8, equal_nan=True)
