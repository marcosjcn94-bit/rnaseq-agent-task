import json

import pandas as pd
import pytest

from research.inputs import read_paired_inputs


def make_inputs(tmp_path, *, order=("C1", "T1", "C2", "T2"), batch=None):
    metadata = pd.DataFrame([
        {"sample_id": "C1", "donor": "D1", "condition": "control"},
        {"sample_id": "T1", "donor": "D1", "condition": "treated"},
        {"sample_id": "C2", "donor": "D2", "condition": "control"},
        {"sample_id": "T2", "donor": "D2", "condition": "treated"},
    ])
    if batch is not None:
        metadata["batch"] = batch
    metadata.to_csv(tmp_path / "metadata.csv", index=False)
    pd.DataFrame({sample: [10 + i, 20 + i] for i, sample in enumerate(order)},
                 index=pd.Index(["g1", "g2"], name="gene_id")).to_csv(tmp_path / "counts.csv")


def test_aligns_metadata_by_sample_id_not_row_order(tmp_path):
    make_inputs(tmp_path, order=("T2", "C1", "T1", "C2"))
    counts, metadata, manifest = read_paired_inputs(tmp_path, min_pairs=2)
    assert list(metadata.index) == list(counts.columns)
    assert metadata.loc["T2", "condition"] == "treated"
    assert manifest["n_pairs"] == 2


def test_missing_pair_fails(tmp_path):
    make_inputs(tmp_path)
    pd.read_csv(tmp_path / "metadata.csv").iloc[:-1].to_csv(tmp_path / "metadata.csv", index=False)
    with pytest.raises(ValueError, match="match exactly|complete donor pair"):
        read_paired_inputs(tmp_path, min_pairs=2)


def test_duplicate_sample_id_fails(tmp_path):
    make_inputs(tmp_path)
    metadata = pd.read_csv(tmp_path / "metadata.csv")
    metadata.loc[1, "sample_id"] = metadata.loc[0, "sample_id"]
    metadata.to_csv(tmp_path / "metadata.csv", index=False)
    with pytest.raises(ValueError, match="unique"):
        read_paired_inputs(tmp_path, min_pairs=2)


def test_invalid_counts_fail(tmp_path):
    make_inputs(tmp_path)
    counts = pd.read_csv(tmp_path / "counts.csv", index_col=0)
    counts.iloc[0, 0] = -1
    counts.to_csv(tmp_path / "counts.csv")
    with pytest.raises(ValueError, match="non-negative integers"):
        read_paired_inputs(tmp_path, min_pairs=2)


def test_confounded_design_fails(tmp_path):
    make_inputs(tmp_path)
    metadata = pd.read_csv(tmp_path / "metadata.csv")
    metadata["donor"] = ["D1", "D2", "D1", "D2"]
    metadata.to_csv(tmp_path / "metadata.csv", index=False)
    with pytest.raises(ValueError, match="exactly one control and one treated|full rank"):
        read_paired_inputs(tmp_path, min_pairs=1)
