# E6 — Paired negative binomial simulations

The protocol is in `research/configs/simulation.json`. Python and R generators are in `research/simulate.py` and `research/r/simulate_four_pairs.R`, and metrics are in `research/simulation_metrics.py`. Base seed 20261005. Each replicate generates 1,000 genes using empirical mean and dispersion parameters from the E2 R export, baseline donor effects, size factors, and a negative binomial distribution with size `1/dispersion` and variance `mu + dispersion*mu^2`. Differential expression (DE) effects have absolute value 1 on the log2 scale and balanced signs. Scenarios include interaction-driven heterogeneity.

The baseline between-donor SD uses three R coefficients per gene, converted to log2, with zero for the reference donor. Centering effects by gene gives a pooled residual SD of `0.6445065` log2 units. The initial exploratory version used an arbitrary SD of 0.35 and is archived separately. All conclusions use the calibrated version.

## Production (200 replicates per scenario)

Runs were offline in pinned containers. The Python environment used PyDESeq2 0.5.4, NumPy 2.4.6, pandas 2.3.3, and SciPy 1.17.1 (image `sha256:ece5e898...c82d23`). The R environment used DESeq2 1.50.2, R 4.5.2, and Bioconductor 3.22 (image `sha256:f63cb28...ce5ec06`). PyDESeq2 completed 3,200 fits across 16 scenarios (4, 8, 12, or 20 pairs), and DESeq2 completed 800 fits across four scenarios (4 pairs). Every fit completed and each replicate contained 1,000 testable genes. Replicates, manifests, and full hashes are in `.artifacts/research/E6/production-python-n{4,8,12,20}/` and `.artifacts/research/E6/production-R-n4/`. Final aggregates and summary manifests are in `.artifacts/research/E6/production-summary-python/summary-final/` and `production-summary-R/summary-certified/`.

The table summarizes estimates across replicates and gives Monte Carlo standard errors (MCSE) in parentheses. With 10% DE, FDP is the mean fraction of false discoveries among rejections, and power is the fraction of true alternatives rejected. Type I error and Wald interval coverage are gene-level averages. Under the global null, `fdp_mean` equals the fraction of replicates with at least one rejection. This quantity concerns a scenario with zero alternative genes.

| Engine | Pairs | Interaction SD | FDP (MCSE) | Power (MCSE) | Type I error | 95% coverage |
|---|---:|---:|---:|---:|---:|---:|
| PyDESeq2 | 4 | 0 | 0.0458 (0.0016) | 0.7982 (0.0028) | 0.0043 | 0.9611 |
| PyDESeq2 | 4 | 0.5 | 0.0707 (0.0025) | 0.5676 (0.0047) | 0.0049 | 0.9464 |
| PyDESeq2 | 8 | 0 | 0.0548 (0.0017) | 0.9133 (0.0021) | 0.0060 | 0.9495 |
| PyDESeq2 | 8 | 0.5 | 0.0817 (0.0020) | 0.8606 (0.0025) | 0.0086 | 0.9390 |
| PyDESeq2 | 12 | 0 | 0.0592 (0.0016) | 0.9548 (0.0014) | 0.0067 | 0.9492 |
| PyDESeq2 | 12 | 0.5 | 0.0805 (0.0020) | 0.9304 (0.0018) | 0.0092 | 0.9355 |
| PyDESeq2 | 20 | 0 | 0.0604 (0.0018) | 0.9874 (0.0008) | 0.0071 | 0.9429 |
| PyDESeq2 | 20 | 0.5 | 0.0770 (0.0019) | 0.9782 (0.0011) | 0.0092 | 0.9401 |
| DESeq2 | 4 | 0 | 0.0393 (0.0015) | 0.7863 (0.0030) | 0.0036 | 0.9600 |
| DESeq2 | 4 | 0.5 | 0.0655 (0.0023) | 0.5475 (0.0043) | 0.0043 | 0.9459 |

In DE-free scenarios, the fraction of PyDESeq2 replicates with at least one rejection at 4, 8, 12, and 20 pairs was 0.460, 0.210, 0.125, and 0.200 at interaction SD 0, and 0.185, 0.275, 0.235, and 0.295 at SD 0.5. The corresponding DESeq2 fractions at four pairs were 0.295 and 0.190. With small sample sizes and donor heterogeneity, these estimates fail to establish control of the family-wise error rate at 0.05. Each engine independently sampled data from the same distribution, so comparisons are descriptive at the scenario level and use unpaired replicates.

The primary analysis uses all 200 replicates per scenario. The pilot section is retained for historical comparison. The first 10 replicates of each scenario were resumed from calibrated v2 pilot checkpoints, so the two summaries overlap. Production contains 200 unique replicate IDs per scenario.

## Calibrated v2 pilot results (10 replicates per scenario)

Each scenario had 10 replicates, 1,000 testable genes per replicate, and zero fit failures. Each row summarizes across replicates, with MCSE in parentheses. FDP averages the fraction of false discoveries among rejections. Wald coverage is calculated only for genes with a true effect.

| Pairs | Interaction SD | FDP (MCSE) | Power (MCSE) | Type I error | 95% coverage |
|---:|---:|---:|---:|---:|---:|
| 4 | 0 | 0.042 (0.0049) | 0.802 (0.0128) | 0.0039 | 0.962 |
| 4 | 0.5 | 0.058 (0.0076) | 0.530 (0.0293) | 0.0038 | 0.936 |
| 8 | 0 | 0.052 (0.0098) | 0.908 (0.0073) | 0.0057 | 0.949 |
| 8 | 0.5 | 0.091 (0.0104) | 0.851 (0.0124) | 0.0094 | 0.940 |
| 12 | 0 | 0.047 (0.0078) | 0.953 (0.0078) | 0.0053 | 0.955 |
| 12 | 0.5 | 0.077 (0.0111) | 0.932 (0.0063) | 0.0088 | 0.937 |
| 20 | 0 | 0.073 (0.0062) | 0.990 (0.0033) | 0.0087 | 0.937 |
| 20 | 0.5 | 0.081 (0.0100) | 0.983 (0.0060) | 0.0098 | 0.939 |

Under the global null, FDR equals the probability of at least one rejection. PyDESeq2 estimates at interaction SD 0 and 0.5 were 0.4 and 0.3 for four pairs, 0.2 and 0.3 for eight pairs, 0 and 0.1 for 12 pairs, and 0.1 and 0.4 for 20 pairs. With only 10 replicates, substantial Monte Carlo uncertainty precludes establishing calibration at 0.05.

DESeq2 in R also completed 10 replicates per scenario for four pairs. At interaction SD 0 and 0.5, respectively, FDP was 0.043 and 0.072, power was 0.762 and 0.564, Type I error was 0.0039 and 0.0048, and coverage was 0.974 and 0.950. Each engine generated independent samples from the same distribution, so comparisons are descriptive at the scenario level.

## Evidence and limitations

Pilot replicates, summaries, and manifests with hashes and image IDs are in `.artifacts/research/E6/pilot-v2/` and `R-pilot-v2/`. The production folders are listed above. Estimating means, dispersions, and baseline effect SD from four donors introduces uncertainty. Independently simulated genes support calibration of gene-level tests within these scenarios. Pathway tests and sample-size recommendations for other settings require separate evidence. Human validation remains pending.
