import json
import pytest
from benchmark.prepare import prepare
from tests.test_grader import submission

def test_gold_requires_independent_gate_bound_to_actual_table(tmp_path):
    source=tmp_path/"source"; submission(source)
    check=tmp_path/"validation.json"
    check.write_text(json.dumps({"status":"pass","candidate_sha256":"wrong"}))
    with pytest.raises(ValueError,match="independent"):
        prepare(source,check,tmp_path/"gold")
