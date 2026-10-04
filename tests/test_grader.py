import json
import numpy as np
import pandas as pd
from pathlib import Path
from benchmark.grader import grade

def submission(path):
    path.mkdir()
    values = pd.DataFrame({"gene_id":["a","b","c"],"baseMean":[10,20,30],"log2FoldChange":[2,-2,0],"lfcSE":[.2]*3,"stat":[10,-10,0],"pvalue":[.001,.001,1],"padj":[.002,.002,1],"significant":[True,True,False],"highlight":[True,True,False],"na_reason":["none"]*3})
    values.to_csv(path/"differential_expression.csv",index=False)
    summary = {"design":"~ donor + condition","contrast":["condition","treated","control"],"prefilter":{"min_count":10,"min_samples":4},"genes_input":3,"genes_tested":3,"significant":2,"highlight":2,"versions":{"pydeseq2":"0.5.4"}}
    (path/"analysis_summary.json").write_text(json.dumps(summary))
    (path/"interpretation.md").write_text("This is an exploratory paired bulk RNA-seq reanalysis. Biological replicates, FDR and matrix-only quality control limit interpretation. No clinical claim.")
    # Real PNG fixtures; corrupt files must not receive artifact credit.
    from PIL import Image
    (path/"figures").mkdir()
    for name in ["library_sizes","pca","volcano","heatmap"]:
        Image.new("RGB",(400,300),"white").save(path/"figures"/f"{name}.png")
    return values

def test_valid_artifacts_score_85_but_need_human_and_execution(tmp_path):
    sub,gold = tmp_path/"sub",tmp_path/"gold"
    submission(sub); submission(gold)
    result = grade(sub,gold)
    assert result["automatic_score"] == 85
    assert result["status"] == "pending_execution_and_human_review"
    assert not result["approved"]

def test_header_only_is_critical(tmp_path):
    sub,gold = tmp_path/"sub",tmp_path/"gold"
    values = submission(sub); submission(gold)
    values.iloc[:0].to_csv(sub/"differential_expression.csv",index=False)
    result = grade(sub,gold)
    assert result["critical_failures"]
    assert not result["approved"]

def test_reverse_contrast_is_critical(tmp_path):
    sub,gold = tmp_path/"sub",tmp_path/"gold"
    values = submission(sub); submission(gold)
    values["log2FoldChange"] *= -1
    values.to_csv(sub/"differential_expression.csv",index=False)
    result = grade(sub,gold)
    assert "numeric_mismatch" in result["critical_failures"]

def test_unpaired_manifest_is_critical(tmp_path):
    sub,gold = tmp_path/"sub",tmp_path/"gold"
    submission(sub); submission(gold)
    summary = json.loads((sub/"analysis_summary.json").read_text())
    summary["design"] = "~ condition"
    (sub/"analysis_summary.json").write_text(json.dumps(summary))
    assert "design_or_contrast" in grade(sub,gold)["critical_failures"]

def test_missing_gene_is_critical(tmp_path):
    sub,gold = tmp_path/"sub",tmp_path/"gold"
    values = submission(sub); submission(gold)
    values.iloc[:2].to_csv(sub/"differential_expression.csv",index=False)
    assert "gene_coverage" in grade(sub,gold)["critical_failures"]

def test_forged_claims_do_not_approve(tmp_path):
    sub,gold = tmp_path/"sub",tmp_path/"gold"
    submission(sub); submission(gold)
    (sub/"execution_receipt.json").write_text(json.dumps({"status":"success","network":"none"}))
    assert not grade(sub,gold)["approved"]
