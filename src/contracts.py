"""Shared scientific contracts and deterministic artifact helpers."""
import hashlib
import importlib.metadata
import json
from pathlib import Path

FIXED = {
    "schema_version":1, "min_count":10, "min_samples":4,
    "design":"~ donor + condition",
    "contrast":["condition","treated","control"],
    "alpha":0.05, "lfc_highlight":1,
    "fit_type":"parametric", "size_factors_fit_type":"ratio",
    "refit_cooks":True, "min_replicates":7,
    "cooks_filter":True, "independent_filter":True,
    "pca_genes":500, "heatmap_genes":20,
}

def load_config(path):
    with Path(path).open(encoding="utf-8") as stream:
        config = json.load(stream)
    if set(config) != set(FIXED) | {"n_cpus"}:
        raise ValueError("config keys do not match the scientific contract")
    for key, expected in FIXED.items():
        if config[key] != expected or type(config[key]) is not type(expected):
            raise ValueError(f"fixed scientific parameter: {key}={expected!r}")
    if type(config["n_cpus"]) is not int or not 1 <= config["n_cpus"] <= 2:
        raise ValueError("n_cpus must be 1 or 2")
    return config

def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            digest.update(block)
    return digest.hexdigest()

def write_json(path, value):
    path = Path(path)
    # Atomic replacement prevents a partial JSON from claiming completion.
    temporary = path.with_suffix(path.suffix+".tmp")
    temporary.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
    temporary.replace(path)

def versions():
    return {name:importlib.metadata.version(name) for name in
            ["pydeseq2","pandas","numpy","scipy","matplotlib","scikit-learn"]}
