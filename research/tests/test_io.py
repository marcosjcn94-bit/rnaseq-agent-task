import json

import pandas as pd
import pytest

from research.io import write_run


def test_write_run_creates_hash_manifest_and_preserves_na(tmp_path):
    output = tmp_path / "run"
    write_run(output, {"results": pd.DataFrame({"pvalue": [0.1, None]})}, {"run_id": "test"})
    manifest = json.loads((output / "manifest.json").read_text())
    assert manifest["status"] == "complete"
    assert len(manifest["output_sha256"]["results.csv"]) == 64
    assert "NaN" not in (output / "manifest.json").read_text()


def test_nonempty_output_is_never_overwritten(tmp_path):
    output = tmp_path / "run"
    output.mkdir()
    sentinel = output / "keep.txt"
    sentinel.write_text("existing")
    with pytest.raises(FileExistsError):
        write_run(output, {"results": pd.DataFrame({"x": [1]})}, {})
    assert sentinel.read_text() == "existing"
