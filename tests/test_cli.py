import json
import subprocess
import sys
from pathlib import Path
import pandas as pd
from tests.test_analysis import fixture

def command(data,output):
    return [sys.executable,"-m","src.cli","run","--data",str(data),"--output",str(output),"--config","config.json"]

def make_data(path):
    from src.contracts import sha256
    path.mkdir()
    counts, metadata = fixture()
    counts.to_csv(path/"counts.csv",index_label="gene_id")
    metadata.reset_index().to_csv(path/"metadata.csv",index=False)
    manifest = {"count_type":"raw_fragment_counts","samples":8,"genes":len(counts),"sample_ids":list(counts.columns),"files":{}}
    for name in ["counts.csv","metadata.csv"]:
        manifest["files"][name]={"sha256":sha256(path/name)}
    (path/"manifest.json").write_text(json.dumps(manifest))

def test_cli_produces_artifacts_and_refuses_overwrite(tmp_path):
    data,out = tmp_path/"data",tmp_path/"out"
    make_data(data)
    result = subprocess.run(command(data,out),capture_output=True,text=True)
    assert result.returncode == 0, result.stderr
    manifest = json.loads((out/"run_manifest.json").read_text())
    assert manifest["status"] == "success"
    for file in ["differential_expression.csv","analysis_summary.json","qc.json","gene_filter.csv"]:
        assert (out/file).is_file()
    assert len(list((out/"figures").glob("*.png"))) == 4
    retry = subprocess.run(command(data,out),capture_output=True,text=True)
    assert retry.returncode != 0
    assert "empty" in retry.stderr.lower()

def test_cli_hash_failure_writes_no_success(tmp_path):
    data,out = tmp_path/"data",tmp_path/"out"
    make_data(data)
    with (data/"counts.csv").open("a") as stream: stream.write("\n")
    result = subprocess.run(command(data,out),capture_output=True,text=True)
    assert result.returncode != 0
    assert not (out/"run_manifest.json").exists()
