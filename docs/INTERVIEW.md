# Interview preparation

This Codex-assisted project uses a known public dataset for computational reanalysis and packages an executable bioinformatics task in an isolated environment. Its scope is reproduction and task evaluation. Claims about biological discovery, clinical findings, or independent agent performance require additional evidence.

## Five short answers

### 1. Why use the paired design, and what changes without `donor`?

Each of the four donors has a control sample and a treated sample. The model `~ donor + condition` compares conditions while controlling for baseline differences between donors. Omitting `donor` removes that pairing from the model and can change estimates of variability and effect uncertainty. The design has eight samples, rank five, and three residual degrees of freedom.

### 2. Why does TPM fail to substitute for these counts?

DESeq2 and PyDESeq2 model raw integer counts and estimate size factors to compare samples. TPM and FPKM already incorporate transformations and adjustments for length and composition. I also verify in the manifest that the supplied data are raw counts.

### 3. How do you interpret log2FC, adjusted p-values, and the highlights?

Positive log2FC indicates higher expression under treatment than under control. A value of +1 corresponds to roughly twice the expression. The threshold `padj < 0.05` applies after Benjamini–Hochberg multiple-testing adjustment. It controls the false discovery rate across tests under the method's assumptions and yields no single-gene probability of truth. The additional `abs(log2FC) >= 1` highlight is an exploratory flag applied to point estimates. A formal effect-threshold test would require a different hypothesis.

### 4. What does each check establish?

Identical outputs from two Python runs demonstrate reproduction with those data and that environment. The R/DESeq2 comparison checks a separate implementation. Log2FC Spearman correlation was 0.999994 and directions matched for 852 strong genes. The significance decisions differed for 308 genes. Human review checks whether the code, method, figures, and interpretation are sound. Establishing a biological discovery would require evidence beyond any one of those checks.

### 5. How does the runner protect inputs and the reference solution?

The submission runs in Docker without network access, as an unprivileged user, with the root filesystem, inputs, and source mounted read-only. The runner applies resource limits and gives the submission no Docker socket. The evaluator and the reference outputs stay outside the container. The evaluator records receipts and hashes outside the paths writable by the submission.

## Demonstration outline

1. Show `config.json`, `data/manifest.json`, the formula, and the contrast.
2. Run the README commands and explain what each figure shows. The QC covers the count matrix. FASTQ, alignment, and coverage analysis fall outside its scope.
3. Show the comparison table for Python and R. Explain the 308 discrepancies and identify which causes remain unresolved.
4. Show the rejection of the reversed-contrast and unpaired runs, along with the failure and isolation test.
5. Explain that the task uses a known dataset. The successful reference run verifies the evaluator. General agent capability would require separate measurement.

## Defensible résumé entry

> Built an AI-assisted paired RNA-seq reanalysis with PyDESeq2 and a computational comparison against R/DESeq2. Packaged it as an offline scientific task with isolated Docker execution, deterministic criteria, and adversarial tests.

Add human review or demonstrated proficiency only after completing and documenting those steps.
