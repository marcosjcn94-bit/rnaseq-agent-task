"""Deterministic artifact checks; execution and human review remain separate gates."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
from src.contracts import write_json,sha256

NUMERIC = ["baseMean","log2FoldChange","lfcSE","stat","pvalue","padj"]
FLAGS = ["significant","highlight","na_reason"]

def _table(directory):
    path = directory/"differential_expression.csv"
    if path.stat().st_size > 100*1024**2:
        raise ValueError("table too large")
    with path.open(newline="",encoding="utf-8") as stream:
        header = next(csv.reader(stream),[])
    if len(header)!=len(set(header)):
        raise ValueError("duplicate columns")
    frame = pd.read_csv(path,index_col="gene_id")
    if frame.empty or not frame.index.is_unique or frame.index.isna().any():
        raise ValueError("empty table or duplicate/missing gene IDs")
    if not set(NUMERIC+FLAGS)<=set(frame.columns):
        raise ValueError("missing required result columns")
    for name in NUMERIC:
        frame[name] = pd.to_numeric(frame[name],errors="raise")
        if np.isinf(frame[name]).any():
            raise ValueError("infinite statistical value")
    for name in ["pvalue","padj"]:
        if not frame[name].dropna().between(0,1).all():
            raise ValueError("probability outside [0,1]")
    if (frame.baseMean<0).any() or frame.baseMean.isna().any() or (frame.lfcSE.dropna()<0).any():
        raise ValueError("invalid mean or standard error")
    for name in ["significant","highlight"]:
        if frame[name].dtype != bool:
            raise ValueError("flags must be booleans")
    significant = frame.padj.notna() & (frame.padj<.05)
    highlight = significant & (frame.log2FoldChange.abs()>=1)
    if not frame.significant.equals(significant) or not frame.highlight.equals(highlight):
        raise ValueError("flags contradict statistical values")
    if not set(frame.na_reason)<= {"none","cooks_outlier","independent_filter","nonfinite_estimate"}:
        raise ValueError("unknown missing-value reason")
    return frame

def grade(submission, gold, receipt=None, human_review=None):
    submission,gold = Path(submission).resolve(),Path(gold).resolve()
    reference = _table(gold)
    expected = json.loads((gold/"analysis_summary.json").read_text(encoding="utf-8"))
    points = {"integrity_provenance":0,"design_contrast":0,"numeric_agreement":0,"artifacts":0}
    critical = []
    details = {}
    try:
        candidate = _table(submission)
    except (OSError,ValueError,KeyError,pd.errors.ParserError) as error:
        return {"automatic_score":0,"points":points,"critical_failures":["invalid_table"],
                "details":{"invalid_table":str(error)},"approved":False,"status":"rejected"}
    if set(candidate.index)!=set(reference.index):
        critical.append("gene_coverage")
    else:
        points["integrity_provenance"] += 10
        candidate = candidate.reindex(reference.index)
    try:
        summary = json.loads((submission/"analysis_summary.json").read_text(encoding="utf-8"))
        if not isinstance(summary,dict):
            raise ValueError("summary must be a JSON object")
    except (OSError,ValueError) as error:
        summary = {}
        details["summary"] = str(error)
        critical.append("invalid_summary")
    design_ok = all(summary.get(key)==expected.get(key) for key in ["design","contrast","prefilter"])
    if design_ok and summary.get("design")=="~ donor + condition" and summary.get("contrast")==["condition","treated","control"]:
        points["design_contrast"] = 25
    else:
        critical.append("design_or_contrast")
    counts_ok = all(summary.get(key)==expected.get(key) for key in ["genes_input","genes_tested","significant","highlight"])
    counts_ok = counts_ok and summary.get("genes_tested")==len(candidate) and summary.get("significant")==int(candidate.significant.sum()) and summary.get("highlight")==int(candidate.highlight.sum())
    provenance_ok = summary.get("input_hashes")==expected.get("input_hashes")
    version_ok = summary.get("versions",{}).get("pydeseq2")=="0.5.4"
    if counts_ok and provenance_ok and version_ok:
        points["integrity_provenance"] += 10
    else:
        critical.append("summary_or_provenance")
    if "gene_coverage" not in critical:
        mismatched = []
        for column in NUMERIC:
            if not np.allclose(candidate[column],reference[column],rtol=1e-6,atol=1e-8,equal_nan=True):
                mismatched.append(column)
        for column in FLAGS:
            if not candidate[column].equals(reference[column]):
                mismatched.append(column)
        if not mismatched:
            points["numeric_agreement"] = 25
        else:
            critical.append("numeric_mismatch")
            details["numeric_mismatch"] = mismatched
    valid_figures = []
    for name in ["library_sizes","pca","volcano","heatmap"]:
        try:
            path = submission/"figures"/f"{name}.png"
            if path.stat().st_size > 20*1024**2:
                raise ValueError("figure too large")
            with Image.open(path) as image:
                if image.format!="PNG" or min(image.size)<200:
                    raise ValueError("invalid PNG dimensions")
                image.verify()
            valid_figures.append(name)
            points["artifacts"] += 2
        except (OSError,ValueError,SyntaxError):
            pass
    if summary: points["artifacts"] += 3
    interpretation = submission/"interpretation.md"
    if interpretation.is_file() and 80 <= interpretation.stat().st_size <= 100*1024:
        points["artifacts"] += 4
    if len(valid_figures)!=4 or not interpretation.is_file():
        critical.append("missing_artifacts")
    # Participant-provided execution claims are never read here.
    execution_ok = False
    if receipt:
        execution_ok = (
            receipt.get("status")=="success" and receipt.get("exit_code")==0
            and receipt.get("network_mode")=="none"
            and receipt.get("read_only_root") is True
            and receipt.get("source_unchanged") is True
            and bool(receipt.get("image_id"))
            and receipt.get("output_hashes")=={
                str(p.relative_to(submission)).replace("\\","/"):sha256(p)
                for p in sorted(submission.rglob("*")) if p.is_file()
            }
        )
    review_ok = bool(human_review and human_review.get("completed") is True
                    and human_review.get("reviewer")
                    and human_review.get("method_verified") is True
                    and human_review.get("figures_reviewed") is True
                    and human_review.get("sources_reviewed") is True
                    and type(human_review.get("score")) is int
                    and 0 <= human_review["score"] <= 15)
    automatic = sum(points.values())
    human = human_review["score"] if review_ok else None
    approved = not critical and execution_ok and review_ok and automatic+human>=85
    status = "rejected" if critical else "approved" if approved else "pending_execution_and_human_review" if not execution_ok else "pending_human_review"
    return {"automatic_score":automatic,"human_score":human,"points":points,
            "critical_failures":critical,"details":details,"execution_verified":execution_ok,
            "human_review_completed":review_ok,"approved":approved,"status":status,
            "numeric_tolerance":{"rtol":1e-6,"atol":1e-8}}

def validate_gold(directory):
    directory = Path(directory)
    validation = json.loads((directory/"validation.json").read_text(encoding="utf-8"))
    if validation.get("status")!="pass" or validation.get("candidate_sha256")!=sha256(directory/"differential_expression.csv"):
        raise ValueError("gold table hash is not bound to passing independent validation")
    manifest = json.loads((directory/"gold_manifest.json").read_text(encoding="utf-8"))
    actual = {p.relative_to(directory).as_posix():sha256(p)
              for p in sorted(directory.rglob("*")) if p.is_file() and p.name!="gold_manifest.json"}
    if not manifest.get("files") or manifest["files"]!=actual:
        raise ValueError("gold artifact hash mismatch")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--submission",required=True); parser.add_argument("--gold",required=True)
    parser.add_argument("--receipt"); parser.add_argument("--human-review")
    parser.add_argument("--output",required=True)
    args = parser.parse_args()
    # Gold is only authoritative after the independent validation gate.
    validate_gold(args.gold)
    def external_record(path):
        if not path: return None
        resolved = Path(path).resolve()
        if resolved.is_relative_to(Path(args.submission).resolve()):
            raise ValueError("evaluator record must be outside participant output")
        return json.loads(resolved.read_text(encoding="utf-8"))
    result = grade(args.submission,args.gold,external_record(args.receipt),external_record(args.human_review))
    write_json(args.output,result)
    print(json.dumps(result,indent=2))
    raise SystemExit(1 if result["critical_failures"] else 0)

if __name__=="__main__":
    main()
