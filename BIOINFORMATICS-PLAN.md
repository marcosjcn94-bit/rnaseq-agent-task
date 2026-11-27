# Bioinformatics implementation plan for Codex

Date: 2026-10-04. Status at drafting: planning only, before implementation.

## 1. Goal and research conclusion

Build a reproducible RNA-seq reanalysis and package it as a scientific task with objective evaluation for AI agents.

**Recommendation.** This is the most practical route given the user's software background and short timeline. The recommendation reflects technical fit. Selection and superiority over other approaches would require separate evidence.

The official Turing posting calls for scientific programming, multistep analysis, reference solutions, evaluation criteria, and execution without network access. Bioinformatics is among the accepted specialties [1]. An analysis notebook covers only part of that scope. Packaging the analysis as an evaluable task addresses the remaining requirements.

## 2. Project specification

- **Suggested name** — airway-rnaseq-agent-task.
- **Question** — Which genes change expression after dexamethasone treatment in human airway smooth muscle cells when the analysis accounts for donor pairing?
- **Dataset** — airway, derived from GSE52778. Use eight samples from four donors, one control and one treated sample per donor, with no albuterol. Bioconductor documents the subset and its provenance [2]. The full GEO study has 16 samples and includes other treatments, so preserve the predefined subset.
- **Working hypothesis** — Treatment is associated with changes in expression. Report observed results and disagreements. Keep the methods fixed independently of the gene list obtained.
- **Scope** — Acquire counts and metadata, validate the inputs, run count-matrix QC, perform differential expression analysis, create figures, interpret the results, generate a separate reference, package an evaluable task, and reproduce it offline.
- **Architecture** — Use a sequential Python CLI with local files and Docker for reproduction. Generate a separate R/DESeq2 reference for validation. The main pipeline stays in Python. The workflow uses local files and requires no services, database, or orchestrator.
- **Proposed software** — Python 3.11, PyDESeq2 0.5.4, pandas, NumPy, SciPy, matplotlib, scikit-learn, and pytest. Confirm compatibility and lock transitive dependencies during preparation. PyDESeq2 0.5.4 is the documented version consulted when drafting the plan [3].
- **Environment** — Windows with PowerShell commands and Linux containers through Docker Desktop. Check Docker availability and resources before downloading or installing large dependencies.

## 3. Scientific contracts

- Prefer a one-time export of counts and metadata from the official `airway` object, using the R environment for the reference. Document the export and make the Python CLI runnable independently of R.
- The workshop CSVs [4] are an acceptable shortcut only when pinned to an immutable commit and verified against the official object for exact sample identities and count equality. Filenames alone are insufficient.
- Record URLs, versions, subset, acquisition date, size, and SHA-256 of each file in `data/manifest.json`. Verify reuse terms before distributing data.
- The canonical inputs are `data/counts.csv`, with genes in rows and eight samples in columns, and `data/metadata.csv`, with columns `sample_id`, `donor`, and `condition`.
- Use the canonical conditions `control` and `treated`. Map `cell` to `donor` and `dex` to `condition` explicitly and auditably.
- Preserve Ensembl IDs and keep genes separate when their symbols match.
- Reject duplicate IDs, missing values, negative or fractional values, unmatched samples, and incomplete pairs. Align by ID independently of file order.
- Verify that the data source supplies unnormalized counts. Reject TPM and FPKM as model inputs. Provenance is required even for integer values [3,5].
- Retain only genes with at least 10 counts in at least four of the eight samples. Record how many genes were removed. The rule follows DESeq2 guidance on using the smallest group [5].
- Fit `~ donor + condition` with treatment versus control as the explicit contrast. Positive log2FC denotes higher expression under treatment. Verify full rank.
- Use the library's normalization and estimation. Apply a two-sided Wald test of nonzero change and Benjamini–Hochberg adjustment at alpha 0.05. Record independent filtering and outlier-handling options.
- Use `padj < 0.05` for significance and `abs(log2FC) >= 1` for exploratory highlights. A formal test against an effect threshold requires a different hypothesis.
- Export and label unshrunk log2FC in the MVP. Document the reason for missing p-values or adjusted p-values and preserve them as missing.
- Limit QC to the count matrix, with per-sample totals, distributions, PCA, and correlations. Read, alignment, and coverage QC require FASTQ or BAM processing beyond this study.
- Run exploratory PCA on log2(normalized counts + 1), using up to the 500 most variable genes. Label condition and donor. Name the transformation explicitly to distinguish it from VST.
- Plot totals by sample, PCA, a volcano plot, and a heatmap for up to the 20 genes with the smallest valid adjusted p-values. Break ties by ID. Use per-gene z-scores in the heatmap and omit zero-variance genes.
- Keep samples regardless of the visual appearance of the PCA. Any exclusion requires documented justification and design review.
- Discuss up to three genes using the original paper and primary sources. Distinguish results, biological hypotheses, and limitations. Confine claims to the computational study.

## 4. Planned files and responsibilities

| Path | Responsibility |
| --- | --- |
| `PLAN.md` | Execution steps, checks, evidence, and pending items |
| `PROJECT-HISTORY.md` | Short, verifiable continuity notes for the agent |
| `ADR.md` | Decisions with context, alternatives, and consequences |
| `README.md` | Question, commands, results, limitations, and demonstration |
| `config.json` | Prespecified scientific parameters |
| `requirements.txt` and `requirements.lock.txt` | Direct dependencies and resolved versions |
| `src/data.py` | Data loading, alignment by ID, and validation |
| `src/analysis.py` | Prefilter, model fitting, and export |
| `src/report.py` | QC, figures, and summary derived from results |
| `src/cli.py` | Pipeline entry points and error messages |
| `data/` | Preserved counts, metadata, and manifest |
| `results/` | QC, differential expression table, summary, and run manifest |
| `figures/` | Four PNG figures |
| `reference/` | Export and R/DESeq2 solution, versions, and comparison |
| `benchmark/TASK.md` | Self-contained instructions for the participant |
| `benchmark/RUBRIC.md` and `benchmark/grader.py` | Scoring criteria and grading of submitted files |
| `benchmark/gold/` | Validated evaluator reference separate from participant inputs |
| `tests/` and `tests/fixtures/` | Invalid-input cases and small offline fixtures |
| `Dockerfile`, `.dockerignore`, `.gitignore` | Reproducible environment and exclusions |
| `.github/workflows/ci.yml` | Fast tests, with the full scientific analysis reserved for closeout |

The MVP is a CLI. A later notebook may present outputs while the scientific logic remains in the CLI.

## 5. Execution sequence for the planned `PLAN.md`

Complete one phase at a time in the same session with one agent and manual control over delegation. Use `superpowers:executing-plans` when available. This original draft records the design. Start implementation only after the user's request.

### Phase 1 — Preparation and data contract

- [ ] Read this plan and check the directory, Git, and local rules. Preserve existing work.
- [ ] Check Python, Docker, and dependency availability. Pin compatible versions and avoid routine upgrades.
- [ ] Create `PLAN.md`, `PROJECT-HISTORY.md`, and `ADR.md` using section 6.
- [ ] Obtain the official airway subset, export counts and metadata once, and record versions and hashes.
- [ ] Verify the eight SRR IDs, four pairs, and absence of albuterol against the documentation [2].
- [ ] Check that counts are nonnegative integers, pairs are identified, and the manifest is complete. Proceed only after input provenance is confirmed.

### Phase 2 — Validated inputs and QC

- [ ] Test duplicate IDs, a missing sample, out-of-order metadata, negative and fractional values, and incomplete pairs.
- [ ] Implement the input reader and contract checks. Run the affected tests.
- [ ] Produce `results/qc.json`, a totals plot, and PCA with donor and condition labels.
- [ ] Verify that permuting the metadata preserves alignment and that invalid inputs give a clear error and nonzero exit before model fitting.

### Phase 3 — Differential expression and figures

- [ ] Test the prefilter, contrast orientation, and donor design. Use a fixture with eight samples and enough genes for fitting. Reserve significance testing for an adequately sized matrix.
- [ ] Implement the specified model using DESeq2 methodology as provided by the library.
- [ ] Export `results/differential_expression.csv` with `gene_id`, `baseMean`, `log2FoldChange`, `lfcSE`, `stat`, `pvalue`, `padj`, and criterion flags.
- [ ] Record parameters, versions, hashes, time, and memory in `results/run_manifest.json`. Create `results/summary.json` and the other two figures.
- [ ] Verify complete outputs, unique IDs, valid probabilities where present, explained missingness, and explicit treated-versus-control orientation.

### Phase 4 — Independent computational validation

- [ ] Generate an R/DESeq2 reference from the same files, filtered genes, design, and contrast, with unshrunk effects.
- [ ] Pin and document versions and options for both implementations. Align normalization, filtering, and outlier handling before comparison. Evaluate agreement against the specified tolerances.
- [ ] Compare shared genes with finite log2FC. The proposed acceptance thresholds are Spearman correlation of at least 0.95 for log2FC and sign agreement of at least 95% in the reference set with adjusted p-value below 0.01 and absolute log2FC at least 1.
- [ ] Record the comparable set size and discrepancies. An empty set makes the check inconclusive and cannot pass.
- [ ] Verify interpretation of up to three genes against the original publication, preserving traceable identifiers, annotation, and references.
- [ ] Write `reference/comparison.json` and `reference/VALIDATION.md`. Investigate method and data if checks fail. Preserve the prespecified thresholds.
- [ ] If the R reference is unavailable, record validation as pending and defer phase 5 until there is a validated reference.

### Phase 5 — Evaluable scientific task

- [ ] Write the task in English. Ask the participant to inspect the data, identify the design, choose a suitable method, run the analysis, diagnose issues, and report interpretations and limitations.
- [ ] Give the participant only the data, descriptions, and environment. Keep the solution and evaluator reference outside the input package. Label any synthetic data as such.
- [ ] Require a differential expression table, `analysis_summary.json`, four figures, and `interpretation.md`. The summary must capture design, contrast, filter, versions, and gene counts.
- [ ] Define a 100-point rubric. Integrity and provenance earn 20, design and contrast 25, numerical agreement 25, reproduction and artifacts 15, and interpretation and limitations 15.
- [ ] Automate the first 85 points using the defined checks. Reserve 15 points for human review with explicit criteria. The rubric uses deterministic checks and human judgment.
- [ ] Pass submissions scoring at least 85 points with completed human review and no critical data, pairing, contrast, or offline-execution error.
- [ ] Test a correct solution, an empty table, headers only, reversed contrast, and omission of donor adjustment. Verify that the grader detects critical errors inside supplied files.
- [ ] Verify that the validated solution passes and incorrect examples fail for the expected reasons. A local snapshot tests stability. The separate reference from phase 4 provides cross-implementation validation.
- [ ] Label the task as demonstrative. Measuring general agent capability requires broader evidence. A public reference on a well-known dataset permits memorization.

### Phase 6 — Reproduction, documentation, and delivery

- [ ] Prepare the image and data online. Separate acquisition and build from scientific execution.
- [ ] Run the full pipeline in a fresh container with networking disabled, an empty output directory, and read-only inputs.
- [ ] Run offline tests and the grader. Compare two tables generated in the same environment for identical IDs and flags, numeric agreement at rtol 1e-6 and atol 1e-8, and preserved missing values. Compare scientific content separately from figure hashes and timestamps.
- [ ] Set up fast CI with local fixtures. Run the complete final analysis once the checks pass.
- [ ] Inspect figures for legibility, correct axes, consistent IDs and labels, and unclipped elements.
- [ ] Write an English README with PowerShell commands, online preparation and offline execution, provenance, methods, actual results, limitations, and measured time and memory.
- [ ] Include study notes on counts and TPM, biological replication, pairing, log2FC, multiple testing, FDR, and the scope of QC.
- [ ] Record the use of AI and what the user reviewed. Make publication, discovery, and external-review claims only when supported.
- [ ] Consolidate `PROJECT-HISTORY.md` and `ADR.md` and save check evidence in `PLAN.md`. Make local commits per phase and keep pushes and publication under user control.
- [ ] Verify offline execution, documented independent validation, passing tests, and grader operation. The user should be able to explain five central decisions.

## 6. Three continuity documents

### `PROJECT-HISTORY.md` — up to 40 lines

Keep the current goal, confirmed dataset and subset, learned scientific concepts, resolved problems, useful environment facts, current phase, next action, and actual blockers. Include dates and evidence paths. Keep logs, secrets, chat history, and unmeasured results outside this file. Replace obsolete information at each phase close.

### `ADR.md` — up to six decisions, approximately ten lines each

Each decision contains its ID, date, status, context, selected option, rejected alternative, and consequence. Proposed decisions cover prepared counts versus FASTQ, Python/PyDESeq2 and R/DESeq2, paired design, CLI/files/Docker, deterministic grading and human review, and provenance/caching/offline policies. Mark decisions as proposed until confirmed during implementation. When changing a decision, cite the superseded decision.

### `PLAN.md` — checklist and evidence

Use the six phases above. Mark a checkbox only when evidence supports it. At the end of each phase, record the checks, results, produced files, blockers, and next action. Clearly identify plan, completed implementation, and pending validation. Link to `PROJECT-HISTORY.md` and `ADR.md` to avoid duplication.

## 7. Token and time efficiency

- On resumption, read `PROJECT-HISTORY.md`, the pending phase in `PLAN.md`, and only relevant decisions and files.
- Keep one analysis, one subset, one contrast, and one task. A dashboard, RAG, cloud, model training, enrichment, and a second dataset are outside the MVP.
- Download and export once, then preserve the inputs. Reuse a fit only when data hashes, settings, and versions match. Invalidate dependent outputs when inputs or methods change.
- During development, run affected tests and a small fixture. Run the real analysis after the scientific phase and at closeout. Repeat passed checks only after relevant changes or a failure.
- The R reference adds initial setup cost in exchange for independent computational validation. Reuse that environment between runs.
- Keep logs in files. Give the user progress, blockers, and the next action without sending complete matrices or stack traces.
- If a dependency or source fails, try a recovery informed by the error, record the blocker, and adjust the route based on evidence. Avoid repeated installations and broad searches.
- Save tokens through scoped work, selective reading, and verified result reuse. Use only documented provider limits.

## 8. Application value

Once complete, present the repository as an **independent computational reanalysis and agent evaluation project**, with verifiable results and links.

## 9. Sources consulted

1. The requirements and nature of evaluable tasks. [Turing — Agentic Life Science Expert](https://work.turing.com/r/qzScy-BjHO)
2. Sample counts, treatments, provenance, and the original paper. [Bioconductor — airway experiment documentation](https://bioconductor.org/packages/release/data/experiment/vignettes/airway/inst/doc/airway.html)
3. Inputs, model fitting, and multifactor contrasts. [PyDESeq2 — official workflow](https://pydeseq2.readthedocs.io/en/stable/auto_examples/plot_minimal_pydeseq2_pipeline.html)
4. A possible source of CSVs that requires validation. [bioconnector — airway workshop](https://github.com/bioconnector/workshops/blob/master/r-rnaseq-airway.Rmd)
5. Raw counts, sample alignment, design, and prefiltering. [DESeq2 — official documentation](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html)
6. Free material with an estimated three hours for the core content. [EMBL-EBI — Introductory bioinformatics](https://www.ebi.ac.uk/training/online/courses/introductory-bioinformatics-pathway/)
7. Conceptual support for analysis and interpretation. [EMBL-EBI — Introduction to RNA-seq and functional interpretation](https://www.ebi.ac.uk/training/materials/introduction-to-rna-seq-materials/)

Data acquisition, dependency installation, scientific coding, and analysis were pending at this planning stage.
