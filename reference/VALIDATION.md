# Independent scientific validation

The reference uses R 4.5.2, Bioconductor 3.22, DESeq2 1.50.2; Python uses PyDESeq2 0.5.4. Both consume the identical hashed raw counts and metadata, retain 16,139 genes, fit the paired model and the same treated/control contrast, ratio normalization, parametric dispersion fit, alpha .05, explicit independent/Cook's filtering and no shrinkage.

## Predefined acceptance gate

All retained gene IDs must match, all compared log2FC values must be finite, Spearman log2FC >=.95, and direction agreement >=95% among R genes with padj<.01 and abs(log2FC)>=1. An empty strong set is inconclusive. No thresholds were relaxed.

Observed: Spearman 0.9999944126; direction agreement 1.0 over 852 strong genes. Gate: pass. The machine record binds both table hashes in comparison.json.

## Differences preserved

Python: 3,879 significant; R: 4,081. Intersection: 3,826; Python-only: 53; R-only: 255; Jaccard: .925496. There are 308 padj<.05 classification disagreements. R has 313 missing padj values, versus zero in Python, due to independent filtering. Neither has missing raw p-values.

Spearman pvalue .998661 and padj .998630. Median absolute log2FC difference .000159824; maximum .161720. Maximum relative normalized-count discrepancy was approximately 5.55e-15. This supports aligned normalization, but does not establish identical dispersion estimates or hypothesis-test results.

## Installed-source inspection

With eight samples and rank-five design, residual degrees of freedom are three. PyDESeq2 warns that the MAD estimate of log-dispersion variability can be unreliable at this size; the pipeline preserves this warning.

Inspection of PyDESeq2 0.5.4 fit_dispersion_prior and DESeq2 1.50.2 estimateDispersionsPriorVar confirmed different low-degree-of-freedom paths. Python subtracts the trigamma sampling variance from a MAD-based variance estimate, floored at .25. R's <=3 branch estimates prior variance through simulation, grid search, KL histogram discrepancy and smoothing, also floored at .25.

This confirmed implementation difference is a plausible contributor to statistical discrepancies; the inspection does not quantify its contribution or attribute all 308 disagreements to it. Independent-filter masks also differ. We retain the fixed methods and report the discrepancy rather than forcing equality.

The frozen Python gold is accepted only under the specified effect/direction gate. It is not a substitute for the R reference, nor proof of full statistical equivalence. This is executor-led source/scientific review, not external expert peer review.

## Primary references

- [PyDESeq2 0.5.4 API](https://pydeseq2.readthedocs.io/en/v0.5.4/api/docstrings/pydeseq2.dds.DeseqDataSet.html)
- [DESeq2 source](https://bioconductor.org/packages/DESeq2)
- [DESeq2 method paper](https://doi.org/10.1186/s13059-014-0550-8)
- [Himes et al. airway experiment](https://doi.org/10.1371/journal.pone.0099625)

Full local audit output is stored under .artifacts/; reference/audit_algorithms.py and reference/audit_algorithms.R reproduce installed-source inspection.
