import pytest
from research.task_runner import record_attempt

def test_requires_real_attempt_fields(tmp_path):
    with pytest.raises(ValueError): record_attempt("t", "", "hash", "answer", tmp_path/"attempt.json")

def test_does_not_overwrite(tmp_path):
    p=tmp_path/"attempt.json"
    record_attempt("t","agent","sha256","real response",p)
    with pytest.raises(ValueError): record_attempt("t","agent","sha256","second response",p)
