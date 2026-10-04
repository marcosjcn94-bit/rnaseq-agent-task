import numpy as np
import pandas as pd
import pytest
from src.compare import compare_tables

def table():
    return pd.DataFrame({"log2FoldChange":[-3,-2,2,3],"pvalue":[.001]*4,"padj":[.005]*4},index=["a","b","c","d"])

def test_independent_comparison_accepts_concordant():
    result = compare_tables(table(),table())
    assert result["status"] == "pass"
    assert result["spearman_log2fc"] == pytest.approx(1)
    assert result["sign_agreement"] == 1

def test_independent_comparison_rejects_reversed_contrast():
    altered = table()
    altered["log2FoldChange"] *= -1
    assert compare_tables(altered,table())["status"] == "fail"

def test_independent_comparison_rejects_missing_genes():
    with pytest.raises(ValueError,match="gene"):
        compare_tables(table().iloc[:2],table())

def test_empty_strong_set_is_inconclusive():
    ref = table()
    ref["padj"] = .5
    assert compare_tables(ref,ref)["status"] == "inconclusive"
