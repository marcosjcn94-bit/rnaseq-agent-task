# Research extension status

Date 2026-10-05. Plan in `docs/superpowers/plans/2026-10-05-airway-research-extension.md`.

| Stage | Status | Evidence and next action |
|---|---|---|
| E0 | Complete | Core workflow, separate images, and R lockfile. Eight tests. Baseline reproduced within `rtol=1e-6, atol=1e-8`. `BASELINE.md`. |
| E1 | Partial | Guide, practice material, and review package ready. Individual demonstration and external opinion pending. `EXTERNAL-REVIEW.md`. |
| E2 | Complete | Baseline hashes reproduced across 16,139 genes. A complete explanation for the 308 discrepancies remains unresolved. `PYTHON-R.md`. |
| E3 | Complete | Four paired folds, effect estimates, PCA, and distances. Figures inspected. `ROBUSTNESS.md`. |
| E4 | Computation complete | Frozen annotations and completed CAMERA, ORA, and GOseq runs and tests. Human interpretation pending. `PATHWAYS.md`. |
| E5 | Audit complete | SOFT, MINiML, and six CEL files audited and hashed. Sample-level stimulus metadata received `insufficient_metadata`. Inference and RMA did not run. `EXTERNAL-PROTOCOL.md`. |
| E6 | Computation complete | Offline production with 3,200 PyDESeq2 fits across 16 scenarios and 800 DESeq2 fits across four scenarios with four pairs, 200 per scenario, zero failures. Aggregates, manifests, and hashes are available by batch. The engine comparisons use independent simulations. `SIMULATION.md`. |
| E7 | Initial suite validated | Twelve synthetic cases with explicit fixtures and separate keys. Four grader and runner tests passed. Agent attempts and rubric review pending. |
| E8 | Local validation complete | Baseline hash check, 25 Python tests, an R fixture, and the R lockfile check passed. `git diff --check` was clean. As of the October 5 run, a separate CI job had been added and remote execution was pending. |

**Pending human work.** Individual demonstration, external review, pathway interpretation, rubric validation, and judgment of external compatibility. The independent work continues.

**Integrity.** Baseline and preexisting changes were preserved, as documented in `BASELINE.md`. The October 5 run took place without host package installations, paid services, messages, publication, or pushes. E6 evidence from the initial SD=0.35 run is retained for traceability and excluded from the primary interpretation.
