# Interpretation of the fixed paired reanalysis

The retained matrix contains 16,139 genes and four donor-matched dexamethasone/control pairs. At BH-adjusted p<.05, the fixed Python analysis reports 3,879 significant genes: 2,104 higher and 1,775 lower after treatment. Positive unshrunk log2FC denotes treated/control. The 957 genes additionally meeting abs(log2FC)>=1 are an exploratory subset, not the result of a threshold-based effect test.

Three illustrative observations, using the supplied historical Ensembl annotation:

| Ensembl ID | Symbol | log2FC | Adjusted p |
|---|---|---:|---:|
| ENSG00000103196 | CRISPLD2 | 2.6271 | 1.456e-60 |
| ENSG00000120129 | DUSP1 | 2.9437 | 9.250e-138 |
| ENSG00000163884 | KLF15 | 4.4603 | 3.977e-100 |

[Himes et al. (2014)](https://doi.org/10.1371/journal.pone.0099625) investigated glucocorticoid responses in these cells, including experimental support for increased CRISPLD2 and discussion of DUSP1/KLF15 as responsive genes. Our positive estimates are consistent with that context. This association does not establish a causal mechanism in our reanalysis, treatment efficacy or a clinical recommendation.

The paper used a different original analysis; its reported gene count is not an acceptance target. We did not tune filters to reproduce a desired gene list. Gene symbols are labels from Ensembl 75 / GRCh37.p13, not current annotation or a replacement for IDs.

Limits: four biological replicates, three residual degrees of freedom, no FASTQ/alignment QC, no independent cohort, no clinical outcomes and no effect-size shrinkage. Exploratory log-normalized PCA is not VST. The R effect/direction gate passes, but 308 adjusted-p significance classifications differ; R's independent filter leaves 313 padj missing. Python and R statistical results are therefore not interchangeable. See reference/VALIDATION.md.

This is a known-dataset reanalysis assisted by AI, not a new biological discovery or external scientist-reviewed report.
