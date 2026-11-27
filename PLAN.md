# AIRWAY execution and project status

The approved scope was option 3, a complete MVP with failure tests, computational scientific review, a demonstrative task, and interview preparation. The [original bioinformatics plan](BIOINFORMATICS-PLAN.md) records the specification. This file records the work completed and pending at the close of the MVP.

## Completed engineering work

- Acquired official airway 1.30.0 data with 63,677 genes and eight samples from four control and treated pairs without albuterol. Documented provenance, licensing, and hashes.
- Validated raw counts, IDs, metadata, pairs, and configuration. Invalid inputs are rejected.
- Ran PyDESeq2 0.5.4 with `~ donor + condition` and produced tables, a summary, QC results, and four figures.
- Ran an R/DESeq2 1.50.2 reference reanalysis, compared the implementations using prespecified criteria, and audited their differences.
- Packaged the scientific task with an offline Docker runner, a deterministic grader, adversarial rehearsals, and verifiable evidence.
- Reproduced identical tables in two Python analysis runs. All 46 local tests and `pip check` passed.
- Published the `implementation` branch on GitHub. CI runs fixture tests. A complete scientific rerun uses the separate reproduction workflow. [Repository and Actions tab](https://github.com/marcosjcn94-bit/rnaseq-agent-task)
- Wrote guides for human review, interview preparation, and scientific assessment. The original MVP guides were written in Portuguese.

## Results and limitations

The filter retained 16,139 genes. Python found 3,879 genes with `padj < 0.05` (2,104 upregulated and 1,775 downregulated). Of those, 957 also met the exploratory threshold `abs(log2FC) >= 1`. R found 4,081 significant genes. Log2FC Spearman correlation was 0.999994 and direction agreed for all 852 strong genes. The 308 differences in significance classification and 313 missing R adjusted p-values remain documented. The cause of each discrepancy remains unresolved.

The study has four donors and three residual degrees of freedom. The count matrix supports computational reanalysis within this cohort. FASTQ and alignment QC, an independent cohort, new biological discoveries, and clinical conclusions are outside the available evidence.

## Human review and application

The reference rehearsal earned 85 of 85 automatic points, with verified execution and zero critical failures. Its recorded state is `pending_human_review`, with zero human points assigned. The [human review guide](docs/HUMAN-REVIEW.md) describes the procedure. Complete the review template only after carrying out that review.

The user still needs to demonstrate that they can run and explain the analysis. The [interview guide](docs/INTERVIEW.md) provides study answers. Demonstrate understanding through the rehearsal. The [scientific assessment](docs/SCIENTIFIC-ASSESSMENT.md) describes possible extensions beyond the portfolio MVP.

## Evidence

- [Python and R comparison](reference/comparison.json) and [scientific interpretation](docs/INTERPRETATION.md).
- [Evaluator rehearsal](benchmark/REHEARSAL.md), [rubric](benchmark/RUBRIC.md), and [evidence package](evidence/).
- [Implementation review by the executing agent](docs/SELF-REVIEW.md).
