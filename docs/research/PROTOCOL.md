# Research protocol v1

Frozen on 2026-10-05 before the extension calculations. New results remain exploratory pending review and reproduction. Any change to endpoints, universe, or method requires a new protocol version with a rationale. Previously observed results retain their original protocol.

## Baseline and estimand

- Use official `airway` count data. The donor is the experimental unit, with four treated/control pairs and eight samples.
- Estimate the treated/control contrast using `~ donor + condition`, raw counts, the baseline filter of `>=10` counts in `>=4` samples, a zero-LFC Wald test, BH adjustment, alpha 0.05, and unshrunken MLEs.
- Interpret differential expression as an association. Preserve the reason for each missing `padj` and record that classification as unavailable.
- Reproduce the baseline within each implementation with identical IDs, flags, and missing values, using `rtol=1e-6, atol=1e-8`. Evaluate Python and R separately.

## Prespecified endpoints

- E2 compares parameters, intermediate outputs, and classifications in the union of the Ensembl IDs. Evaluate independent filtering and Cook’s distance in isolated contrasts. Describe agreement and disagreement without an agreement target.
- E3 uses baseline and four paired folds with the fixed baseline gene universe. Define exploratory stability for genes with `abs(LFC)>=1` as estimable in all folds, constant direction, and maximum deviation `<=0.5`. Assess sensitivity at 0.25 and 1.0.
- E4 uses versioned GO Biological Process annotations and directional CAMERA after limma-voom, with `inter.gene.cor=NA` and `allow.neg.cor=FALSE`. Run one correlation sensitivity analysis at 0.01. ORA and GOseq are secondary analyses with declared eligible universes.
- E5 prespecifies CRISPLD2, DUSP1, and KLF15 with a predicted positive direction. Estimates and 95% confidence intervals, coverage, and effects in the shared universe provide context. Classify compatibility before testing. Account for platform and drug differences and interpret the estimates alongside FDR.
- E6 begins with seed 20261005 and 16 scenarios defined in the plan. Use 10 replicates for the pilot and target 200 per scenario for production after measurement. Report Monte Carlo uncertainty, testability, and failures.
- E7 covers four families. Freeze attempts before evaluating the held-out set. Keep answer keys evaluator-only and use no paid calls. If an agent is unavailable, measurement stays pending.

## Integrity and execution

Mount inputs and code read-only in the container. Write each run to a dedicated empty directory, initially under `.artifacts/research/`. The planned per-fit limits are 2 CPUs, 4 GiB, and 30 minutes. Docker availability prevented applying or measuring those limits when this protocol was frozen. Execution evidence is recorded separately.
