# E4 — Functional pathway analysis

Date 2026-10-05. This exploratory treated/control analysis describes associations. Biological review and evidence of causal activation remain separate requirements.

## Protocol and universe

The universe starts with the 16,139 genes tested at baseline and uses GO Biological Process with ancestral associations (`GOALL`). Contemporary functional annotation was frozen at `org.Hs.eg.db` 3.22.0 and `GO.db` 3.22.0. Historical Ensembl 75 counts were preserved. Gene lengths are based on the union of exons per gene (`reduce(rowRanges(airway))`, airway 1.30.0). The snapshot contains 16,319 raw Ensembl–Entrez relationships, 13,772 reciprocal one-to-one mappings, 879,448 gene–term relationships, and 13,855 BP terms. The raw table retains IDs excluded due to ambiguity. Missing `padj` excluded 170 mapped genes from the GOseq universe. All one-to-one mappings retained an exon length.

Each analysis froze eligible term sizes at 15–500 genes in its testable universe. The primary method used edgeR/TMM followed by limma-voom with `~ donor + condition` and the treated/control contrast. Directional CAMERA used the limma model ranking, `use.ranks=TRUE`, `allow.neg.cor=FALSE`, and estimated correlation (`inter.gene.cor=NA`). The sensitivity analysis changed only that correlation to 0.01. BH was applied to the eligible terms separately for each analysis and fold. Four folds each dropped one complete donor pair.

## Results

- **CAMERA with estimated correlation.** 4,265 terms were eligible at baseline. Zero had FDR < 0.05. The folds had 4,261–4,263 eligible terms and zero below 0.05.
- **CAMERA with fixed correlation of 0.01.** The baseline had 11 terms with FDR < 0.05, and the folds ranged from 7 to 13. This sensitivity to the correlation assumption is material with four pairs and three residual degrees of freedom. Both analyses use the same cohort.
- **ORA sensitivity analysis.** The DESeq2 list used `padj < 0.05` and excluded missing `padj` from the universe. 1,422 of 4,247 terms had FDR < 0.05. With independent filtering disabled and a shared testable universe, 1,470 of 4,265 crossed that threshold. These comparisons evaluate sensitivity to a large list of selected genes. The primary ranking comes from limma.
- **Separate GOseq sensitivity analyses.** Wallenius tests used explicit categories and the same GO collection and eligible universe. With exon length, 1,187 overrepresented and 57 underrepresented terms had FDR < 0.05. With mean normalized counts, the corresponding counts were 1,035 and 76. Selection probability curves are in `selection_probability_curves.csv`. Differences reflect sensitivity to the bias model. Length and expression were evaluated separately.

Five eligible GOseq p-values exceeded 1 because of numerical error. The maximum excess before clipping was `4.9e-11`. P-values were clipped to the mathematical interval [0, 1], and BH was recalculated after applying the 15–500 gene limit. `goseq_sensitivities.csv` preserves each raw value, the correction flag, and both tails. The `nullp` fit also warned that the starting point was close to the constraints. Consider the curves and warnings when interpreting the results.

The results retain the differences among CAMERA with estimated and fixed correlations, ORA, and GOseq. No single set of terms was selected for further testing based on those differences. Overlapping GO terms describe related annotations. Human review of functional interpretation remains pending. Claims are limited to the reported enrichment and sensitivity outcomes.

## Reproducible evidence

- Configuration and commands are in `research/configs/pathways.json`, `research/r/annotation.R`, `pathways.R`, `finalize_annotation.R`, and `finalize_pathways.R`.
- Synthetic checks and quality assurance tests in `research/r/test_pathway_utils.R`, `test_annotation.R`, and `test_pathway_results.R` passed offline in the `airway-research-r:e0` image.
- Manifests and per-artifact SHA-256 hashes are in `.artifacts/research/E4/annotation-v2/manifest.json` and `.artifacts/research/E4/pathways-final/manifest.json`. Large outputs are stored under `.artifacts/research/`.
- The original annotation attempt, which had ambiguous headings for supplementary `GOALL` columns, was preserved in `.artifacts/research/E4/annotation-attempt1/`. The final snapshot was normalized and tested in a separate directory.
