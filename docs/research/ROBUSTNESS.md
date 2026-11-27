# E3 — Donor robustness, quality control, and effect estimates

Date 2026-10-05. The primary universe was fixed at the 16,139 genes retained by the baseline filter. Each fold dropped both samples from one donor. Fits ran offline in separate images limited to 2 CPUs and 4 GiB. All four folds had six samples, three pairs, design rank 4, and two residual degrees of freedom. Both engines returned estimates for every gene in every fold.

## Effect sensitivity

A gene with baseline `abs(log2FC)>=1` was considered stable only when its effect was estimable in all four folds, retained its sign, and had a maximum deviation below the fixed threshold relative to the complete-data fit. The 0.25, 0.5, and 1.0 thresholds were specified in advance.

| Measure | Python | R |
|---|---:|---:|
| Baseline genes with `abs(log2FC)>=1` | 1,090 | 1,091 |
| Retained direction in all folds | 1,090 | 1,091 |
| Stable at threshold 0.25 | 688 | 685 |
| Stable at threshold 0.5 | 1,003 | 1,004 |
| Stable at threshold 1.0 | 1,087 | 1,088 |
| Median maximum LFC deviation among high-effect genes | 0.206 | 0.207 |
| P95 maximum deviation | 0.569 | 0.567 |

Every effect with `abs(log2FC)>=1` retained its direction across folds. Some exceeded the magnitude thresholds. Directional stability applies to the observed cohort. Generalization requires new donors.

## Significance lists

| Donor removed | Python DE / lost / gained | R DE / lost / gained |
|---|---:|---:|
| N052611 | 2,717 / 1,223 / 61 | 2,653 / 1,482 / 54 |
| N061011 | 2,476 / 1,437 / 34 | 2,375 / 1,734 / 28 |
| N080611 | 3,456 / 712 / 289 | 3,227 / 1,078 / 224 |
| N61311 | 2,838 / 1,105 / 64 | 2,736 / 1,403 / 58 |

With three pairs, precision is lower and the list of `padj<0.05` genes shifts substantially. Interpret a loss of significance alongside effect estimates and standard errors, which accompany the lists. The overlapping folds represent sensitivity analyses within one study. A valid jackknife interval would require a separate justification. The optional sensitivity analysis that reapplies a `>=10` filter in `>=3` samples remains pending.

## Quality control and shrinkage

VST used `blind=FALSE` to explore treatment response. Model fitting continued to use raw counts. Baseline PCA on log2 normalized counts explained 33.4% and 30.1% on PC1 and PC2. VST PCA explained 48.1% and 23.5%. Exports include sample distances and the mean–variance relationship. Visual inspection confirmed legible scales and identifiable samples, conditions, and donors. All samples were retained after PCA.

`lfcShrink(type="apeglm")` was exported separately for `condition_treated_vs_control`. The rank correlation of MLE and apeglm effect magnitudes was 0.9366. The original MLE table and inference were preserved. Posterior standard deviation and MLE standard error describe different quantities.

Each cross-engine comparison in the four folds retained 16,139 IDs. Depending on the donor removed, absolute log2FC differences had medians of `4.4e-5` to `1.2e-4`, P95 values of 0.0030 to 0.0042, and maxima of 0.072 to 0.155.

## Limitations and artifacts

Three donors leave two residual degrees of freedom per fold. The Python manifest retains dispersion warnings. Results remain exploratory and apply to sensitivity within the available cohort. Tables, manifests, PNG and PDF figures, and summaries are in `.artifacts/research/E3/`. The latest visual review used the figures in `r-v3/`.
