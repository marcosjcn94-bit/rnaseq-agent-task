import json
from pathlib import Path
import pytest
from benchmark.runner import output_hashes
from src.data import read_inputs
from tests.test_cli import make_data
from tests.test_grader import submission
from benchmark.grader import grade

def test_output_symlink_is_rejected(tmp_path):
    outside = tmp_path/"outside.txt"; outside.write_text("outside")
    output = tmp_path/"output"; output.mkdir()
    (output/"linked.txt").symlink_to(outside)
    with pytest.raises(ValueError,match="symlink"):
        output_hashes(output)

@pytest.mark.parametrize("kind",["probability","infinity","duplicate","invalid_flags","missing_probability_reason"])
def test_grader_rejects_invalid_statistical_table(tmp_path,kind):
    sub,gold=tmp_path/"sub",tmp_path/"gold"
    table=submission(sub); submission(gold)
    if kind=="probability": table.loc[0,"padj"]=-1
    elif kind=="infinity":
        table["log2FoldChange"]=table["log2FoldChange"].astype(float)
        table.loc[0,"log2FoldChange"]=float("inf")
    elif kind=="duplicate": table.loc[1,"gene_id"]="a"
    elif kind=="invalid_flags": table.loc[0,"significant"]=False
    elif kind=="missing_probability_reason":
        table.loc[0,"padj"]=float("nan")
        table.loc[0,"significant"]=False; table.loc[0,"highlight"]=False
        table.loc[0,"na_reason"]="none"
    table.to_csv(sub/"differential_expression.csv",index=False)
    assert grade(sub,gold)["critical_failures"]

def test_changed_count_provenance_is_rejected(tmp_path):
    data=tmp_path/"data"; make_data(data)
    manifest=json.loads((data/"manifest.json").read_text())
    manifest["count_type"]="TPM"
    (data/"manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError,match="provenance"):
        read_inputs(data)

def test_duplicate_header_is_rejected_before_pandas_mangling(tmp_path):
    from src.contracts import sha256
    data=tmp_path/"data"; make_data(data)
    path=data/"counts.csv"
    lines=path.read_text().splitlines()
    columns=lines[0].split(","); columns[2]=columns[1]; lines[0]=",".join(columns)
    path.write_text("\n".join(lines)+"\n")
    manifest=json.loads((data/"manifest.json").read_text())
    manifest["files"]["counts.csv"]["sha256"]=sha256(path)
    (data/"manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError,match="header"):
        read_inputs(data)
