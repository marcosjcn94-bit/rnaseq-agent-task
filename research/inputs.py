"""Input validation for variable-size paired research analyses."""
from pathlib import Path

import numpy as np
import pandas as pd


def read_paired_inputs(directory: Path, min_pairs: int = 3):
    directory = Path(directory)
    counts = pd.read_csv(directory / "counts.csv", index_col=0)
    metadata = pd.read_csv(directory / "metadata.csv", dtype=str)
    required = {"sample_id", "donor", "condition"}
    if not required.issubset(metadata.columns):
        raise ValueError(f"metadata missing columns: {sorted(required - set(metadata.columns))}")
    if metadata[list(required)].isna().any().any() or (metadata[list(required)] == "").any().any():
        raise ValueError("sample_id, donor, and condition must be non-empty")
    if metadata.sample_id.duplicated().any():
        raise ValueError("sample_id values must be unique")
    if counts.index.has_duplicates or counts.columns.has_duplicates:
        raise ValueError("count gene and sample IDs must be unique")
    if set(metadata.condition) != {"control", "treated"}:
        raise ValueError("condition must contain control and treated")
    if set(counts.columns) != set(metadata.sample_id):
        raise ValueError("count columns and metadata sample IDs must match exactly")
    values = counts.to_numpy()
    if not np.isfinite(values).all() or (values < 0).any() or not np.equal(values, np.floor(values)).all():
        raise ValueError("counts must be finite non-negative integers")

    per_donor = metadata.groupby("donor", sort=False).condition.agg(list)
    if (~per_donor.map(lambda values: sorted(values) == ["control", "treated"])).any():
        raise ValueError("each donor must have exactly one control and one treated sample")
    if len(per_donor) < min_pairs:
        raise ValueError(f"at least {min_pairs} complete donor pairs are required")
    metadata = metadata.set_index("sample_id").loc[counts.columns].copy()
    metadata["donor"] = pd.Categorical(metadata.donor, categories=sorted(metadata.donor.unique()))
    metadata["condition"] = pd.Categorical(metadata.condition, categories=["control", "treated"], ordered=True)
    design = pd.get_dummies(metadata[["donor", "condition"]], drop_first=True, dtype=float)
    matrix = np.column_stack([np.ones(len(metadata)), design.to_numpy()])
    rank = int(np.linalg.matrix_rank(matrix))
    if rank != matrix.shape[1] or len(metadata) <= rank:
        raise ValueError("design must be full rank with residual degrees of freedom")
    manifest = {
        "samples": list(counts.columns), "genes": len(counts),
        "donors": list(dict.fromkeys(metadata.donor)), "n_pairs": len(per_donor),
        "design_rank": rank, "residual_degrees_of_freedom": len(metadata) - rank,
    }
    return counts, metadata, manifest
