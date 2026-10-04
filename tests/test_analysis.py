import json
import subprocess
import sys
import numpy as np
import pandas as pd
import pytest
from src.analysis import fit
from src.data import validate
from src.contracts import load_config

def fixture():
    rng = np.random.default_rng(713)
    genes = 400
    means = rng.uniform(100,1000,(genes,1))*np.array([0.8,0.8,1.2,1.2,1,1,0.9,0.9])
    means[:30,1::2] *= 8
    values = rng.negative_binomial(30,30/(30+means))
    counts = pd.DataFrame(values,index=[f"g{i:04}" for i in range(genes)],columns=[f"s{i}" for i in range(8)])
    counts.index.name = "gene_id"
    metadata = pd.DataFrame({"sample_id":counts.columns,"donor":np.repeat(["d1","d2","d3","d4"],2),"condition":["control","treated"]*4})
    return validate(counts,metadata)

def test_paired_model_orientation_and_outputs():
    counts, metadata = fixture()
    config = load_config("config.json")
    result, normalized, model_info = fit(counts,metadata,config)
    assert result.index.is_unique
    assert result.loc[[f"g{i:04}" for i in range(30)],"log2FoldChange"].median() > 2
    assert model_info["design_rank"] == 5
    assert model_info["residual_degrees_of_freedom"] == 3
    assert "residual degrees of freedom" in " ".join(model_info["warnings"])
    assert normalized.shape == counts.shape
    for col in ["pvalue","padj"]:
        valid = result[col].dropna()
        assert valid.between(0,1).all()
    assert set(result["na_reason"]) <= {"none","cooks_outlier","independent_filter","nonfinite_estimate"}

@pytest.mark.parametrize("key,value",[("design","~ condition"),("alpha",0.1),("contrast",["condition","control","treated"]),("min_count",0)])
def test_config_rejects_changed_scientific_contract(tmp_path,key,value):
    config = json.load(open("config.json"))
    config[key] = value
    path = tmp_path/"bad.json"
    path.write_text(json.dumps(config))
    with pytest.raises(ValueError):
        load_config(path)
