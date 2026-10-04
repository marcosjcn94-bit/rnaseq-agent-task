import json
import pytest
from benchmark.grader import validate_gold
from src.contracts import sha256
from tests.test_grader import submission

def test_gold_table_change_invalidates_independent_gate(tmp_path):
    gold=tmp_path/"gold"; submission(gold)
    (gold/"validation.json").write_text(json.dumps({"status":"pass","candidate_sha256":sha256(gold/"differential_expression.csv")}))
    files={p.relative_to(gold).as_posix():sha256(p) for p in gold.rglob("*") if p.is_file()}
    (gold/"gold_manifest.json").write_text(json.dumps({"files":files}))
    validate_gold(gold)
    with (gold/"differential_expression.csv").open("a") as stream:
        stream.write("\n")
    with pytest.raises(ValueError,match="hash"):
        validate_gold(gold)
