import json
from pathlib import Path

import numpy as np

from research.fit import fit_research
from src.analysis import fit as fit_baseline
from src.data import prefilter, read_inputs


def test_instrumented_full_fit_reproduces_baseline():
    root = Path("/data")
    counts, metadata, _, _ = read_inputs(root)
    with (Path("/app/config.json")).open(encoding="utf-8") as stream:
        config = json.load(stream)
    counts, _ = prefilter(counts, config["min_count"], config["min_samples"])
    baseline, baseline_norm, _ = fit_baseline(counts, metadata, config)
    research, normalized, diagnostics, info = fit_research(counts, metadata, config)
    assert research.index.equals(baseline.index)
    assert research.columns.equals(baseline.columns)
    assert research.na_reason.equals(baseline.na_reason)
    np.testing.assert_allclose(research.select_dtypes("number"), baseline.select_dtypes("number"), rtol=1e-6, atol=1e-8, equal_nan=True)
    np.testing.assert_allclose(normalized, baseline_norm, rtol=1e-6, atol=1e-8)
    assert len(diagnostics) == len(counts)
    assert info["design_rank"] == 5
    assert info["residual_degrees_of_freedom"] == 3
