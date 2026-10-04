import json
from pathlib import Path
import numpy as np
import pandas as pd
root=Path(__file__).resolve().parents[1]
p=pd.read_csv(root/"results/run-1/differential_expression.csv",index_col="gene_id")
r=pd.read_csv(root/"reference/final-output/differential_expression.csv",index_col="gene_id").reindex(p.index)
a=pd.read_csv(root/"data/annotation.csv")
merged=p.reset_index().merge(a,on="gene_id")
left=set(p.loc[p.padj<.05].index); right=set(r.loc[r.padj<.05].index)
pn=pd.read_csv(root/"results/run-1/normalized_counts.csv",index_col="gene_id")
rn=pd.read_csv(root/"reference/final-output/normalized_counts.csv",index_col="gene_id").reindex(pn.index).reindex(pn.columns,axis=1)
delta=np.abs(p.log2FoldChange-r.log2FoldChange)
audit={"python_significant":len(left),"r_significant":len(right),"intersection":len(left&right),
       "python_only":len(left-right),"r_only":len(right-left),"jaccard":len(left&right)/len(left|right),
       "lfc_absolute_difference_median":float(delta.median()),"lfc_absolute_difference_max":float(delta.max()),
       "normalized_counts_max_relative_difference":float(np.max(np.abs(pn.to_numpy()-rn.to_numpy())/np.maximum(np.abs(rn.to_numpy()),1))),
       "genes":merged[merged.symbol.isin(["CRISPLD2","KLF15","DUSP1"])][["gene_id","symbol","baseMean","log2FoldChange","padj"]].to_dict(orient="records"),
       "python_only_gene_ids":sorted(left-right),"r_only_gene_ids":sorted(right-left),
       "independent_filter_missing_r":int(r.padj.isna().sum()),
       "independent_filter_missing_python":int(p.padj.isna().sum())}
(root/".artifacts/scientific-audit.json").write_text(json.dumps(audit,indent=2,allow_nan=False)+"\n")
print(json.dumps({k:v for k,v in audit.items() if not k.endswith("gene_ids")},indent=2))
