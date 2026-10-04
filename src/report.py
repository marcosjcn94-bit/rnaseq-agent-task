"""Matrix-only QC and figures derived from validated analysis outputs."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from sklearn.decomposition import PCA
from .contracts import write_json

COLORS = {"control":"#2563eb","treated":"#e11d48"}

def report(raw, normalized, metadata, result, output, config, model_info):
    figures = Path(output)/"figures"
    figures.mkdir()
    transformed = np.log2(normalized.astype(float)+1)
    variability = transformed.var(axis=1,ddof=1)
    selected = pd.DataFrame({"variance":variability,"gene_id":variability.index}).reset_index(drop=True).sort_values(["variance","gene_id"],ascending=[False,True])
    selected = selected.loc[selected.variance > 0].head(config["pca_genes"]).gene_id
    correlations = transformed.corr().astype(object)
    correlations = correlations.where(pd.notna(correlations), None)
    qc = {
        "scope":"count matrix only; no FASTQ/BAM/read/alignment quality control",
        "sample_order":list(raw.columns),
        "raw_library_sizes":{str(k):int(v) for k,v in raw.sum().items()},
        "raw_count_quantiles":{str(k):[float(v) for v in raw[k].quantile([0,.25,.5,.75,1])] for k in raw},
        "log_normalized_pearson_correlations":correlations.to_dict(),
        "pca_transform":"log2(normalized counts + 1); not VST",
        "pca_gene_count":len(selected),
        "model":model_info,
    }
    fig,ax = plt.subplots(figsize=(8,5))
    ids = list(raw.columns)
    ax.bar(ids,[qc["raw_library_sizes"][x]/1e6 for x in ids],color=[COLORS[str(metadata.loc[x,"condition"])] for x in ids])
    ax.legend(handles=[Patch(facecolor=COLORS[x],label=x) for x in ["control","treated"]])
    ax.set_ylabel("Raw fragment count total (millions)")
    ax.set_title("Library sizes — matrix-level QC")
    ax.tick_params(axis="x",rotation=45)
    fig.tight_layout(); fig.savefig(figures/"library_sizes.png",dpi=150); plt.close(fig)

    fig,ax = plt.subplots(figsize=(8,5))
    if len(selected)>=2:
        pca = PCA(n_components=2,svd_solver="full")
        coordinates = pca.fit_transform(transformed.loc[selected].T)
        qc["pca_explained_variance_ratio"] = [float(x) for x in pca.explained_variance_ratio_]
        for i,sample in enumerate(ids):
            condition,donor = str(metadata.loc[sample,"condition"]),str(metadata.loc[sample,"donor"])
            ax.scatter(*coordinates[i],color=COLORS[condition],marker="o" if condition=="control" else "^",s=70)
            ax.annotate(f"{donor} / {condition}",coordinates[i],xytext=(5,5),textcoords="offset points",fontsize=8)
        ax.margins(.25)
        ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
        ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    else:
        ax.text(.5,.5,"Insufficient nonconstant genes for PCA",ha="center",transform=ax.transAxes)
    ax.set_title("Exploratory PCA — log2 normalized counts + 1")
    fig.tight_layout(); fig.savefig(figures/"pca.png",dpi=150); plt.close(fig)

    fig,ax = plt.subplots(figsize=(8,5))
    valid = result.padj.notna() & np.isfinite(result.log2FoldChange)
    plotted = result.loc[valid]
    y = np.minimum(-np.log10(plotted.padj.clip(lower=np.finfo(float).tiny)),50)
    ax.scatter(plotted.log2FoldChange,y,s=7,c=np.where(plotted.highlight,"#e11d48","#64748b"),alpha=.55,rasterized=True)
    ax.axhline(-np.log10(config["alpha"]),color="black",linestyle="--",linewidth=.8)
    for cutoff in [-1,1]: ax.axvline(cutoff,color="black",linestyle=":",linewidth=.8)
    ax.set_xlabel("Unshrunk log2 fold change (treated / control)")
    ax.set_ylabel("-log10 adjusted p-value (display capped at 50)")
    ax.legend(handles=[Patch(facecolor="#e11d48",label="padj < 0.05 and |log2FC| >= 1"),Patch(facecolor="#64748b",label="Other tested genes")],fontsize=8)
    ax.set_title("Differential expression — paired design")
    fig.tight_layout(); fig.savefig(figures/"volcano.png",dpi=150); plt.close(fig)
    qc["volcano_omitted_genes"] = int((~valid).sum())
    qc["volcano_display_cap"] = 50

    ranked = result.loc[result.padj.notna()].copy()
    ranked["gene_id"] = ranked.index
    top = ranked.reset_index(drop=True).sort_values(["padj","gene_id"]).head(config["heatmap_genes"]).gene_id
    heat = transformed.loc[top]
    standard_deviation = heat.std(axis=1,ddof=1)
    nonconstant = standard_deviation > 0
    qc["heatmap_zero_variance_omitted"] = int((~nonconstant).sum())
    heat = heat.loc[nonconstant]
    zscores = heat.sub(heat.mean(axis=1),axis=0).div(heat.std(axis=1,ddof=1),axis=0)
    qc["heatmap_gene_ids"] = list(zscores.index)
    fig,ax = plt.subplots(figsize=(9,8))
    if not zscores.empty:
        bound = max(float(np.abs(zscores).to_numpy().max()),1)
        image = ax.imshow(zscores,aspect="auto",cmap="RdBu_r",vmin=-bound,vmax=bound)
        ax.set_yticks(range(len(zscores)),list(zscores.index),fontsize=8)
        ax.set_xticks(range(len(ids)),[f"{metadata.loc[x,'donor']}\n{metadata.loc[x,'condition']}" for x in ids],rotation=45,ha="right",fontsize=8)
        fig.colorbar(image,ax=ax,label="Per-gene z-score of log2(normalized counts + 1)")
    else:
        ax.text(.5,.5,"No genes available for heatmap",ha="center",transform=ax.transAxes)
    ax.set_title("Up to 20 genes with smallest valid adjusted p-values")
    fig.tight_layout(); fig.savefig(figures/"heatmap.png",dpi=150); plt.close(fig)
    write_json(Path(output)/"qc.json",qc)
    return qc
