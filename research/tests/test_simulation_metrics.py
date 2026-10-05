import numpy as np
import pandas as pd
import pytest

from research.simulation_metrics import empirical_donor_effect_sd, metrics, sample_negative_binomial, summarize_replicates
from research.simulate import generate


def test_metrics_known_truth_and_no_rejections():
    m = metrics([1, 1, 0], [1, 0, 1], [0, 0, 0], [1, 1, 1])
    assert m["fdp"] == 0.5 and m["power"] == 0.5 and m["type1"] == 1
    assert metrics([0, 0], [0, 0], [0, 0], [1, 1])["fdp"] == 0


def test_metrics_reject_mismatched_vectors():
    with pytest.raises(ValueError):
        metrics([1], [1, 0], [0], [1])


def test_negative_binomial_mean_and_variance_parameterization():
    rng = np.random.default_rng(7301)
    draws = sample_negative_binomial(rng, np.full(200_000, 20.0), np.full(200_000, 0.1))
    assert abs(draws.mean() - 20) < 0.2
    assert abs(draws.var() - 60) < 1.5


def test_resume_aggregation_handles_legacy_coverage_column():
    rows = pd.DataFrame([{"engine":"py","pairs":4,"de_fraction":0,"interaction_sd":0,
        "replicate":i,"failure":None,"fdp":v,"power":v,"type1":v,
        "coverage_zero":0.95,"testable":100} for i,v in enumerate([0.1,0.3])])
    got = summarize_replicates(rows).iloc[0]
    assert got.replicates == 2 and got.failures == 0
    assert got.fdp_mean == 0.2 and got.fdp_mcse > 0
    assert got.coverage_mean == 0.95 and got.coverage_mcse == 0


def test_empirical_donor_scale_centers_with_reference_donor():
    d = pd.DataFrame({"donor_a": [np.log(2), -np.log(2)],
                      "donor_b": [0.0, 0.0], "donor_c": [-np.log(2), np.log(2)]})
    assert empirical_donor_effect_sd(d) == pytest.approx(np.sqrt(2/3))


def test_generator_is_seed_reproducible_and_pair_aligned():
    args = (np.random.default_rng(99), np.array([100., 300.]), np.array([.1, .2]), 3, .5, .2, .64)
    a = generate(*args)
    b = generate(np.random.default_rng(99), *args[1:])
    pd.testing.assert_frame_equal(a[0], b[0])
    pd.testing.assert_frame_equal(a[1], b[1])
    np.testing.assert_array_equal(a[2], b[2])
    np.testing.assert_array_equal(a[3], b[3])
    assert len(a[0].columns) == 2 * a[1].donor.nunique()
