# Rubric: 100 points, execution and human gates

| Category | Points | Check |
|---|---:|---|
| Integrity / provenance | 20 | Complete gene coverage (10); consistent counts, input hashes and PyDESeq2 version (10) |
| Design / contrast | 25 | Declared paired formula, treated/control contrast, fixed prefilter |
| Numeric agreement | 25 | Six statistical columns, IDs, missingness, significance/highlight flags and NA reasons match validated Python gold; rtol=1e-6, atol=1e-8 |
| Artifacts | 15 | Four valid PNGs (8), summary (3), interpretation file (4) |
| Human scientific review | 15 | Method and source (5), figures/QC (5), biological interpretation and limitations (5) |

Automatic points verify artifacts and declarations. Numeric agreement catches rehearsed wrong algorithms but cannot prove that submitted source actually implements the method; human source review remains required.

Critical failures include invalid/empty tables, missing/duplicate genes, invalid probabilities, wrong flags, incompatible design/contrast, incorrect provenance, numeric mismatch or missing required artifacts. The execution gate additionally requires an evaluator-generated successful Docker receipt, network none, read-only root, unchanged source and unchanged output hashes.

Approval requires >=85 total, no critical failures, execution verified and completed human review. The HUMAN_REVIEW.json template remains incomplete until an identified reviewer inspects the evidence. Never assign human points from an LLM judge or file presence.

Reviewer's method questions: raw counts? four complete donor pairs? actual formula and contrast in source? fixed filters/outliers? unshrunk effects? missing values retained? Figures: correct sample labels, legible axes, normalization/PCA disclosed, volcano cap and heatmap scaling? Interpretation: primary attribution, up to three ID-preserved genes, observed association separated from hypothesis, small-sample and R/Python discrepancies acknowledged, no clinical claim?

This demonstrative known dataset does not measure general agent capability. Correct-reference rehearsal is evaluator verification, not a new agent performance score.
