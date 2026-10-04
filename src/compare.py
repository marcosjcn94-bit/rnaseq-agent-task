"""Independent validation and repeated-run comparison, aligned by gene ID."""
import argparse
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from .contracts import write_json,sha256

NUMERIC = ["baseMean","log2FoldChange","lfcSE","stat","pvalue","padj"]

def compare_tables(candidate, reference):
    if not candidate.index.is_unique or not reference.index.is_unique or set(candidate.index) != set(reference.index):
        raise ValueError("gene coverage must be identical")
    candidate = candidate.reindex(reference.index)
    finite = np.isfinite(candidate.log2FoldChange) & np.isfinite(reference.log2FoldChange)
    correlation = float(spearmanr(candidate.loc[finite,"log2FoldChange"],reference.loc[finite,"log2FoldChange"]).statistic) if finite.sum() >= 2 else float("nan")
    strong = reference.padj.notna() & (reference.padj<.01) & (reference.log2FoldChange.abs()>=1)
    strong_count = int(strong.sum())
    sign_agreement = float((np.sign(candidate.loc[strong,"log2FoldChange"])==np.sign(reference.loc[strong,"log2FoldChange"])).mean()) if strong_count else None
    finite_count = int(finite.sum())
    comparable = strong_count > 0 and np.isfinite(correlation) and finite_count == len(reference)
    status = "pass" if comparable and correlation>=.95 and sign_agreement>=.95 else "fail" if comparable else "inconclusive"
    result = {"status":status,"genes":len(reference),"finite_log2fc_pairs":finite_count,
              "strong_reference_genes":strong_count,
              "spearman_log2fc":correlation if np.isfinite(correlation) else None,
              "sign_agreement":sign_agreement,
              "thresholds":{"spearman_log2fc":.95,"sign_agreement":.95},
              "missingness_disagreements":{}}
    for column in ["pvalue","padj"]:
        result["missingness_disagreements"][column] = int((candidate[column].isna()!=reference[column].isna()).sum())
        valid = np.isfinite(candidate[column]) & np.isfinite(reference[column])
        if valid.sum() >= 2 and candidate.loc[valid,column].nunique()>1 and reference.loc[valid,column].nunique()>1:
            score = float(spearmanr(candidate.loc[valid,column],reference.loc[valid,column]).statistic)
            result[f"spearman_{column}"] = score if np.isfinite(score) else None
        else:
            result[f"spearman_{column}"] = None
        left,right = candidate[column]<.05,reference[column]<.05
        result[f"{column}_threshold_disagreements"] = int((left!=right).sum())
    return result

def repeated_equal(left,right):
    if not left.index.is_unique or not right.index.is_unique or set(left.index)!=set(right.index):
        return False
    right = right.reindex(left.index)
    for name in NUMERIC:
        if not np.allclose(left[name],right[name],rtol=1e-6,atol=1e-8,equal_nan=True):
            return False
    return all(left[name].equals(right[name]) for name in ["significant","highlight","na_reason"])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate"); parser.add_argument("reference")
    parser.add_argument("--output",required=True)
    parser.add_argument("--repeat",action="store_true")
    args = parser.parse_args()
    left = pd.read_csv(args.candidate,index_col="gene_id")
    right = pd.read_csv(args.reference,index_col="gene_id")
    result = {"status":"pass" if repeated_equal(left,right) else "fail",
              "rtol":1e-6,"atol":1e-8} if args.repeat else compare_tables(left,right)
    result["candidate_sha256"] = sha256(args.candidate)
    result["reference_sha256"] = sha256(args.reference)
    write_json(args.output,result)
    print(result)
    raise SystemExit(0 if result["status"]=="pass" else 1)

if __name__=="__main__":
    main()
