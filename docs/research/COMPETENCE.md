# Concepts and practice exercises

This study material is intended for practice. Personal proficiency requires a separate assessment.

## Concepts to explain in your own words

- In a paired design, the donor is the experimental unit. The two conditions for the same donor are dependent. Pairing reduces between-donor variation, and the number of independent units stays the same.
- When batch and condition are perfectly confounded, the design lacks the information needed to separate their effects. Report the effect as unidentifiable. A causal coefficient cannot be recovered from this design.
- For the negative binomial distribution, `Var(Y)=mu + alpha*mu²`. Dispersion `alpha` describes extra-Poisson variation. The standard error measures the uncertainty of an estimator under the model.
- A Wald test uses the estimate divided by its standard error under an asymptotic approximation. Benjamini–Hochberg (BH) controls the procedure’s false discovery rate under appropriate conditions. Interpret `padj` as an adjusted p-value. It does not give the posterior probability that a gene is a false discovery.
- `padj=NA` can result from independent filtering or an unavailable estimate or test, depending on the method. Preserve the reason.
- Unshrunken maximum likelihood estimates (MLEs) support the specified inference. Shrinkage stabilizes effect estimates. Interpret MLE standard errors and confidence intervals separately from shrinkage estimates.
- Correlation and functional enrichment provide associative evidence. Causal mechanisms and clinical benefit require additional evidence.

## Exercise A — Shuffled pairs

Use `research/tasks/practice/paired-shuffled.json`. Identify the pairs and describe a check that aligns counts by `sample_id` across differing sample orders. Explain the error that could result from relying on column position alone.

## Exercise B — Perfect confounding

Use `research/tasks/practice/confounded-batch.json`. Write out the conceptual design matrix and explain why it cannot separate condition and batch. The expected conclusion is an unidentifiable effect. A coefficient or p-value for that effect would be unsupported.

## Decisions for future external review

1. Suitability of the experimental unit and paired design.
2. Interpretation of `padj=NA` and filtering.
3. Comparability of Python and R effect estimates on the log2 scale.
4. Suitability of the pathway universe and methods.
5. Limits of external contextual validation and causal language.

Record reviewer identity, qualifications, review date, and responses once the review takes place.
