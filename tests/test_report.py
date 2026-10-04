import numpy as np
import pandas as pd
from src.report import report
from src.contracts import load_config

def test_constant_qc_records_undefined_correlations_as_missing(tmp_path):
    raw = pd.DataFrame(10,index=["g1","g2"],columns=[f"s{i}" for i in range(8)])
    metadata = pd.DataFrame({"donor":["d1","d1","d2","d2","d3","d3","d4","d4"],"condition":["control","treated"]*4},index=raw.columns)
    results = pd.DataFrame({"padj":[.5,np.nan],"log2FoldChange":[0,np.nan],"highlight":[False,False]},index=raw.index)
    qc = report(raw,raw,metadata,results,tmp_path,load_config("config.json"),{})
    assert qc["log_normalized_pearson_correlations"]["s0"]["s1"] is None
    assert qc["pca_gene_count"] == 0
    assert len(list((tmp_path/"figures").glob("*.png"))) == 4
