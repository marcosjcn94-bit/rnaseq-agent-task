# How to conduct human review

The reviewer inspects a submission and evaluates its method, figures, and claims. This completes the benchmark rubric. The review applies to the task submission, and peer review and discovery claims remain separate.

The template `benchmark/HUMAN_REVIEW.json` starts incomplete. **Perform the checks first and record the actual result.** You may act as a reviewer if you identify the review as self-review. A bioinformatician or experienced researcher can provide a stronger external assessment for the portfolio.

## Procedure

1. Open `benchmark/TASK.md`, `benchmark/RUBRIC.md`, `benchmark/SOURCES.md`, `reference/VALIDATION.md`, and `docs/SCIENTIFIC-ASSESSMENT.md`.
2. Read the input, model, and reporting code in `src/data.py`, `src/analysis.py`, `src/report.py`, and `reference/run_deseq2.R`.
3. Check the method and code criteria below. Compare configuration, implementation, and evidence with the claims in the submission summary.
4. Open all four figures from a complete run under `results/run-1/figures/`. Check titles, samples, axes, transformations, and the stated caveats.
5. Read `docs/INTERPRETATION.md` and verify its claims against the original paper and sources. Distinguish observations, hypotheses, and causal claims.
6. Assign a justified score from 0 to 15, complete the JSON template, and record evidence and limitations in the notes.
7. For a benchmark submission, run the grader with the completed review and the corresponding receipt. The local rehearsal remains pending human review.

## Human scoring criteria (15 points)

| Category | Points | What to verify |
|---|---:|---|
| Method and code | 0–5 | Raw counts, eight samples forming four pairs, prefilter, actual formula and contrast, filter and outlier settings, unshrunk effect sizes, and preserved missing values. |
| Figures and QC | 0–5 | Four readable, consistent PNGs, condition and donor labels, PCA identified as exploratory log2(normalized counts + 1), adjusted p-values and plotting cap on the volcano plot, and per-gene z-scores on the heatmap. |
| Interpretation and sources | 0–5 | IDs and annotation, context supported by sources, observations distinguished from hypotheses, sample limitations, 308 differences and 313 missing R adjusted p-values reported with appropriate causal caution, and claims bounded to the computational study. |

Award credit only for verified items. A failure can warrant a partial deduction. Explain the reason. When you cannot assess an item, record the limitation and mark that category as incompletely checked.

## Template fields

- `reviewer` — An identifiable reviewer name. Use your own name for self-review.
- `score` — Justified total as an integer from 0 to 15.
- `method_verified`, `figures_reviewed`, and `sources_reviewed` — Set to `true` only after verifying the corresponding category.
- `completed` — Set to `true` once the inspection is complete. Record any failed checks separately.
- `notes` — Date, review type (self-review or external), paths and sources checked, findings, per-category scores, and pending items.

The rubric requires completed human review for approval. The total threshold is 85, which is also the maximum automatic score, so there is no separate minimum human score. **The review must be complete even when its score is low.** The flags and identity are reviewer declarations. Cryptographic identity verification is outside this procedure.

Keep `completed: false` in the template until the review is complete.
