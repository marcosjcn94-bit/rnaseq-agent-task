"""Read gene-by-sample counts and align metadata by sample identifier."""
import csv
import json
from pathlib import Path
import numpy as np
import pandas as pd
from .contracts import sha256

def validate(counts, metadata):
    if counts.empty or counts.shape[1] != 8:
        raise ValueError("counts must contain genes and exactly eight samples")
    if not counts.index.is_unique or not counts.columns.is_unique:
        raise ValueError("duplicate gene or sample IDs")
    for axis in [counts.index,counts.columns]:
        if any(not isinstance(x,str) or not x.strip() or x != x.strip() for x in axis):
            raise ValueError("IDs must be nonempty strings without surrounding whitespace")
    required = {"sample_id","donor","condition"}
    if set(metadata.columns) != required:
        raise ValueError("metadata columns must be sample_id, donor, condition")
    if metadata.isna().any().any():
        raise ValueError("metadata contains missing values")
    if any(not isinstance(x,str) or not x.strip() or x != x.strip()
           for x in metadata.to_numpy().ravel()):
        raise ValueError("metadata values must be nonempty strings")
    if not metadata.sample_id.is_unique:
        raise ValueError("duplicate metadata sample IDs")
    if set(metadata.sample_id) != set(counts.columns):
        raise ValueError("counts/metadata sample IDs differ")
    if set(metadata.condition) != {"control","treated"}:
        raise ValueError("unknown or missing condition")
    pairs = pd.crosstab(metadata.donor,metadata.condition)
    if pairs.shape != (4,2) or not (pairs.to_numpy()==1).all():
        raise ValueError("four complete donor pairs are required")
    try:
        values = counts.to_numpy(dtype=np.float64)
    except (TypeError,ValueError) as error:
        raise ValueError("counts must be numeric") from error
    if not np.isfinite(values).all() or (values < 0).any():
        raise ValueError("counts must be finite and nonnegative")
    if (values != np.floor(values)).any() or (values > 2**53).any():
        raise ValueError("counts must be exactly representable integers")
    if (values.sum(axis=0)==0).any():
        raise ValueError("zero-total sample library")
    # Stable ordering makes metadata/column permutations immaterial.
    matrix = counts.astype("int64").sort_index().reindex(sorted(counts.columns),axis=1)
    aligned = metadata.set_index("sample_id").loc[matrix.columns].copy()
    aligned.index.name = "sample_id"
    aligned["donor"] = pd.Categorical(aligned.donor,categories=sorted(aligned.donor.unique()))
    aligned["condition"] = pd.Categorical(aligned.condition,categories=["control","treated"],ordered=True)
    return matrix, aligned

def prefilter(counts, min_count=10, min_samples=4):
    mask = (counts >= min_count).sum(axis=1) >= min_samples
    if not mask.any():
        raise ValueError("no genes survive the prefilter")
    return counts.loc[mask].copy(), mask

def _csv_header(path):
    with path.open(newline="",encoding="utf-8") as stream:
        header = next(csv.reader(stream),[])
    if not header or len(header) != len(set(header)):
        raise ValueError(f"empty or duplicate CSV header: {path.name}")

def read_inputs(directory):
    directory = Path(directory)
    with (directory/"manifest.json").open(encoding="utf-8") as stream:
        manifest = json.load(stream)
    if manifest.get("count_type") != "raw_fragment_counts":
        raise ValueError("raw count provenance is required; TPM/FPKM are not allowed")
    hashes = {}
    for name in ["counts.csv","metadata.csv"]:
        path = directory/name
        if path.stat().st_size > 100*1024**2:
            raise ValueError("input file exceeds 100 MiB")
        _csv_header(path)
        actual = sha256(path)
        if actual != manifest.get("files",{}).get(name,{}).get("sha256"):
            raise ValueError(f"input hash mismatch: {name}")
        hashes[name] = actual
    counts = pd.read_csv(directory/"counts.csv",index_col=0)
    if counts.index.name != "gene_id":
        raise ValueError("first counts column must be gene_id")
    metadata = pd.read_csv(directory/"metadata.csv",dtype=str)
    matrix, aligned = validate(counts,metadata)
    if manifest.get("genes") != len(matrix) or manifest.get("samples") != 8:
        raise ValueError("manifest dimensions differ from data")
    if set(manifest.get("sample_ids",[])) != set(matrix.columns):
        raise ValueError("manifest sample IDs differ from data")
    hashes["manifest.json"] = sha256(directory/"manifest.json")
    return matrix, aligned, hashes, manifest
