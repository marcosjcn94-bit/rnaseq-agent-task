# Scientific assessment and ways to strengthen the study

## What the project supports

The project demonstrates an auditable computational reanalysis of eight airway smooth muscle samples in four paired control and treatment groups, using official counts from the airway object. It validates provenance and inputs, fits the paired `~ donor + condition` model, generates count-matrix QC, compares PyDESeq2 with R/DESeq2, tests reproduction and failure handling, and evaluates task outputs in Docker.

Two Python runs produced identical tables. Across 16,139 genes, Python and R log2FC estimates had Spearman correlation of 0.999994, and direction matched for 852 strong genes. At `padj < 0.05`, 308 classifications differed. Independent filtering left 313 R adjusted p-values missing. Inspection of the libraries found different dispersion-estimation paths at low degrees of freedom. Their contribution remains unquantified, so statistical equivalence remains unestablished.

The original paper analyzed four donors and reported variability among them, consistent with the caution in this reanalysis. It describes the donors as white men without chronic disease, which limits generalization to other populations and patients with asthma. The original study also includes functional CRISPLD2 experiments that require evidence beyond the supplied count matrix. [Himes et al. (2014), PLOS ONE](https://doi.org/10.1371/journal.pone.0099625)

## Portfolio assessment

The provenance, matched design, cross-check against R, documented discrepancies, reproducibility, and isolated runner show how to build and evaluate a scientific computing workflow.

The evidence covers one cohort of four donors. Scientific breadth and the author's ability to formulate, interpret, and defend methodological decisions independently are best assessed in a technical discussion or task.

A replicability study using 18,000 resamples across 18 datasets found that small cohorts can yield low replicability of differentially expressed genes and pathways. It supports caution about sample size. The replication rate for this dataset remains unknown. [Degen and Medo (2025), PLOS Computational Biology](https://doi.org/10.1371/journal.pcbi.1011630)

## Possible extensions, in priority order

1. **Donor sensitivity.** Leave out one pair at a time, refit, and compare effects, directions, intervals, and classifications. Label this as sensitivity analysis because each fit further reduces the sample size.
2. **Characterize Python and R differences.** Compare filtering masks and dispersions gene by gene and vary one option at a time. Attribute the 308 cases only where the decomposition can be verified. Preserve the independently specified settings instead of calibrating the results to match.
3. **Independent replication.** Identify a public cohort with a compatible design and tissue, specify the hypothesis before examining results, and document platform, protocol, dose, and population differences. Require design compatibility before treating a dataset as validation.
4. **Functional interpretation.** Add pathway analysis with an explicit background universe, identifiers, annotation version, multiple-testing adjustment, and assessment of selection and length bias. Simple enrichment methods can favor long or highly expressed genes. GOseq was developed to address length bias in RNA-seq. [Young et al. (2010), Genome Biology](https://doi.org/10.1186/gb-2010-11-2-r14)

Extensions add scientific value when they answer explicit questions, address bias, and provide evidence beyond the existing analysis.
