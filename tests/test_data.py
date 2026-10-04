import numpy as np
import pandas as pd
import pytest
from src.data import validate, prefilter

def inputs():
    ids = [f"s{i}" for i in range(8)]
    counts = pd.DataFrame([[10]*8, [9]*8, [10]*4+[0]*4], index=["g1","g2","g3"], columns=ids)
    meta = pd.DataFrame({"sample_id":ids,"donor":np.repeat(["d1","d2","d3","d4"],2),"condition":["control","treated"]*4})
    return counts, meta

def test_aligns_metadata_by_id():
    counts, meta = inputs()
    matrix, aligned = validate(counts, meta.sample(frac=1, random_state=1))
    assert list(aligned.index) == list(matrix.columns)
    assert aligned.loc["s1","condition"] == "treated"

@pytest.mark.parametrize("kind", ["negative","fractional","missing","duplicate_gene","duplicate_sample","extra_sample","bad_condition","incomplete_pair","zero_library","empty"])
def test_rejects_invalid_input(kind):
    counts, meta = inputs()
    counts = counts.astype(float)
    if kind == "negative": counts.iloc[0,0] = -1
    elif kind == "fractional": counts.iloc[0,0] = 1.5
    elif kind == "missing": counts.iloc[0,0] = np.nan
    elif kind == "duplicate_gene": counts.index = ["g1","g1","g3"]
    elif kind == "duplicate_sample": meta.loc[1,"sample_id"] = "s0"
    elif kind == "extra_sample": meta.loc[0,"sample_id"] = "other"
    elif kind == "bad_condition": meta.loc[0,"condition"] = "unknown"
    elif kind == "incomplete_pair": meta.loc[0,"condition"] = "treated"
    elif kind == "zero_library": counts.iloc[:,0] = 0
    elif kind == "empty": counts = counts.iloc[:0]
    with pytest.raises(ValueError):
        validate(counts, meta)

def test_prefilter_boundary():
    counts, _ = inputs()
    kept, mask = prefilter(counts, min_count=10, min_samples=4)
    assert list(kept.index) == ["g1","g3"]
    assert mask.to_dict() == {"g1":True,"g2":False,"g3":True}

def test_prefilter_empty_is_error():
    counts, _ = inputs()
    with pytest.raises(ValueError, match="filter"):
        prefilter(counts*0, min_count=10, min_samples=4)
