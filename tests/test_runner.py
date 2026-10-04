import pytest
from benchmark.runner import execute

def test_requires_executable_source(tmp_path):
    source = tmp_path/"source"; source.mkdir()
    with pytest.raises(ValueError,match="analyze.py"):
        execute(source,tmp_path/"out",tmp_path/"receipt.json")

def test_rejects_receipt_in_participant_output(tmp_path):
    source = tmp_path/"source"; source.mkdir()
    (source/"analyze.py").write_text("pass")
    with pytest.raises(ValueError,match="evaluator-owned"):
        execute(source,tmp_path/"out",tmp_path/"out"/"receipt.json")

def test_rejects_source_output_overlap(tmp_path):
    source = tmp_path/"source"; source.mkdir()
    (source/"analyze.py").write_text("pass")
    with pytest.raises(ValueError,match="disjoint"):
        execute(source,source/"out",tmp_path/"receipt.json")
