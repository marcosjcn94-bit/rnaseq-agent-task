# Paired airway RNA-seq reanalysis

You receive raw fragment counts from eight human airway smooth muscle cell samples, four donor-matched control/dexamethasone pairs without albuterol. Examine the metadata and explain why pairing matters.

Implement an offline executable submission named analyze.py. The evaluator runs:
python /submission/analyze.py --data /data --output /output --config /task/config.json

Use the installed PyDESeq2 0.5.4 and the fixed contract in config.json:
- Verify input hashes and raw-count provenance; align by identifiers.
- Reject invalid counts, duplicate identifiers and incomplete donor pairs.
- Keep genes with >=10 counts in >=4 samples.
- Fit ~ donor + condition; contrast treated against control.
- Use ratio normalization, parametric dispersion fitting, Wald two-sided test of LFC=0, alpha=.05, Cook's filtering/refit and independent filtering as configured; no LFC shrinkage.
- Retain Ensembl IDs; do not use TPM/FPKM or collapse gene symbols.
- Statistical significance: padj <.05. Additional exploratory highlight: significant and abs(log2FC)>=1, not a threshold-based hypothesis test.
- No downloads, credentials or paid APIs at execution time.

Produce:
1. differential_expression.csv with gene_id, baseMean, log2FoldChange, lfcSE, stat, pvalue, padj, significant, highlight, na_reason. Include every retained gene; preserve missing values. na_reason is none, independent_filter, cooks_outlier, or nonfinite_estimate, justified by the library's result masks.
2. analysis_summary.json: design, contrast, prefilter {min_count,min_samples}, genes_input, genes_tested, significant, highlight, versions {pydeseq2,...}, input_hashes {counts.csv,metadata.csv,manifest.json}.
3. figures/library_sizes.png, pca.png, volcano.png, heatmap.png.
4. interpretation.md: discuss up to three genes using SOURCES.md and the supplied historical annotation, separate observed results from hypotheses, identify limitations, and avoid clinical conclusions.

Matrix-only QC: raw library sizes and distributions; PCA/correlations on log2(normalized counts+1), not VST. PCA uses up to 500 nonconstant genes ranked by descending variance and ascending ID. Heatmap uses up to 20 smallest valid padj, ties by ID, with per-gene z-scores; omit zero-variance genes. Do not remove samples merely because of PCA appearance. Volcano y-axis uses adjusted p-values; disclose any display cap.

Create all outputs in the supplied empty directory; nonzero exit on invalid data or failed analysis. Inputs and submission source are read-only. Limits: 2 CPUs, 4 GiB RAM, 128 processes, 30-minute timeout. Environment has no network, no root privileges and no gold or evaluator code.

Automatic checks total 85 points. Passing artifacts do not prove the scientific method or justify biological claims: evaluator execution and human review of source, figures and interpretation are mandatory. This is a demonstrative task on a known public dataset, not a general measure of agent capability. No particular gene list is an expected discovery.
