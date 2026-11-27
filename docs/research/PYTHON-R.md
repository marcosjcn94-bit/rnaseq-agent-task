# E2 — Initial analysis of Python and R discrepancies

Date 2026-10-05. The protocol is in `PROTOCOL.md`, with frozen configurations in `research/configs/diagnostics*.json`. All fits ran offline in separate images with 2 CPUs, 4 GiB, a read-only root filesystem, and isolated output under `.artifacts/research/E2/`. Manifests record versions, hashes, parameters, warnings, and resource use.

## Reproduction and universe

The SHA-256 of the Python results table matched its recorded value in `reference/comparison.json` byte for byte (`740a5d…577363`). The R table also matched its recorded value (`c54635…a37ef5`). Both outputs contain 16,139 genes, and the Ensembl join retained all IDs. The reproduced classification was:

| Result | Genes |
|---|---:|
| Significant in both | 3,826 |
| Python only | 53 |
| R only | 255 |
| Non-significant in both | 12,005 |

R had 313 missing `padj` values. Both implementations returned a `pvalue` for every gene. These results reproduce the historical computational outputs. Independent biological validation would require new evidence.

## Components

Exports include full-precision size factors and normalized counts. Per-gene outputs include the fields available in each version: gene-wise, trend, and final MAP dispersion, convergence, coefficient, standard error, Wald statistic, p-value, `padj`, sample-level Cook’s distance, and masks. Python records `prior_disp_var=0.25`. The PyDESeq2 0.5.4 adapter lacks access to the effective independent-filtering threshold, so its manifest marks that field as unavailable. R records a threshold of 10.3192 and parametric trend coefficients `asymptDisp=0.01` and `extraPois=3.1955`. These parameters refer to different internal components.

Across 16,139 genes, absolute differences in gene-wise dispersions had median `4.65e-8` and P95 `0.000592`. For dispersion trends, median and P95 were `0.001592` and `0.03136`. For final dispersions, they were `0.001935` and `0.01509`. Absolute log2FC differences had median `0.000160` and P95 `0.002185`. Standard error differences had median `0.00747`, P95 `0.01926`, and maximum `0.61068`. Absolute Wald statistic differences had median `0.04257` and P95 `0.38766`. Similar log2FC estimates alongside larger differences in standard errors and test statistics suggest a connection between classification discrepancies and uncertainty, testing, and filtering. The analysis establishes associations among those quantities.

## Isolated contrasts

Each comparison changes one option from baseline and keeps the other fixed.

| Run | Changed p-values | Changed `padj` | Significant genes before → after | Disagreements after |
|---|---:|---:|---:|---:|
| Python, independent filtering off | 0 | 0 | 3,879 → 3,879 | 308 |
| R, independent filtering off | 0 | 15,544 | 4,081 → 4,068 | 283 |
| Python, Cook’s distance off | 0 | 0 | 3,879 → 3,879 | 308 |
| R, Cook’s distance off | 0 | 0 | 4,081 → 4,081 | 308 |

Turning off independent filtering in R changed 37 gene classifications. Of those genes, 31 were among the original discrepancies, and the net total dropped from 308 to 283. The count of reclassified genes and the net difference measure different outcomes. The Cook’s distance option left p-values, `padj`, and classifications identical in this cohort. Both exports contained zero missing p-values. Effects of options may overlap, so their counts cannot be summed as exclusive causes. A complete explanation for the 308 cases remains unresolved.

## Cases selected by rule

- Largest absolute standard-error difference: `ENSG00000179593`, with standard errors `1.66246` in Python and `1.05179` in R, and log2FC `9.50198` in both. The gene was significant in both outputs despite the difference in uncertainty.
- R `padj` closest to 0.05: `ENSG00000116161`, significant only in R with `padj=0.0499763`, versus Python `padj=0.0728619`.
- Lowest `baseMean` among R cases with missing `padj` and a finite p-value: `ENSG00000267683`. Its R `baseMean=6.1365` fell below the `10.3192` threshold. R returned `p=0.003069` and `padj=NA`, while Python returned `padj=0.019078`. Filtering accounts for the missing adjusted result in R.
- Concordant significant control selected for the highest `baseMean` in that group: `ENSG00000164692`, with log2FC `-0.438146` and significant classification in both implementations.

## Interpretation and limitations

PyDESeq2 estimates the prior variance using a MAD and trigamma approach. DESeq2 1.50.2 uses a special simulation path with only three residual degrees of freedom. The measured internal values differ. How much each choice contributes to the 308 discrepancies remains unquantified. The analysis kept each implementation’s internal components in place because equivalence across implementations was unverified. Cook’s distance contributed zero classification changes here, and independent filtering in R accounted for a subset of changes.

Full outputs and manifests are in `.artifacts/research/E2/`. The summary and reproducible cases are in `summary-v3/summary.json`. The results retain unresolved discrepancies as observed.
