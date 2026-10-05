import pandas as pd
import pytest

from research.robustness_metrics import summarize_folds, wald_interval


def test_donor_concentrated_effect_is_marked_sensitive():
    baseline = pd.DataFrame({"log2FoldChange": [1.5]}, index=["g1"])
    folds = pd.DataFrame({
        "gene_id": ["g1"]*4, "excluded_donor": ["D1", "D2", "D3", "D4"],
        "log2FoldChange": [1.4, 1.6, 1.5, 0.1], "status": ["estimable"]*4,
    })
    summary = summarize_folds(baseline, folds).loc["g1"]
    assert not summary["stable_0_25"]
    assert not summary["stable_0_5"]
    assert not summary["stable_1_0"]
    assert summary["sign_concordance"] == 1.0
    assert summary["max_abs_lfc_change"] == 1.4


def test_nonestimable_fold_is_preserved_not_counted_as_zero_or_flip():
    baseline = pd.DataFrame({"log2FoldChange": [1.2]}, index=["zero"])
    folds = pd.DataFrame({
        "gene_id": ["zero"]*4, "excluded_donor": ["D1", "D2", "D3", "D4"],
        "log2FoldChange": [1.1, 1.3, float("nan"), 1.2],
        "status": ["estimable", "estimable", "not_estimable", "estimable"],
    })
    summary = summarize_folds(baseline, folds).loc["zero"]
    assert summary["estimable_folds"] == 3
    assert summary["not_estimable_folds"] == 1
    assert summary["sign_concordance"] == 1.0
    assert not summary["stable_0_5"]


def test_wald_interval_uses_unshrunk_se():
    lower, upper = wald_interval(1.0, 0.5)
    assert lower == pytest.approx(0.02)
    assert upper == pytest.approx(1.98)
