# E1 — External scientific review package

**Status:** Ready for the user to share. Reviewer selection, contact, responses, and approval are pending.

## Question and scope

The study reanalyzes four paired AIRWAY donors for their transcriptional response to a glucocorticoid. It compares Python and R implementations, assesses stability after removing individual donors, and examines functional annotations and gene sets. The scope covers computational associations within this dataset. The study does not test causal mechanisms or claim a new discovery. Results, configurations, and provenance are recorded in `PROTOCOL.md`, `BASELINE.md`, `PYTHON-R.md`, `ROBUSTNESS.md`, and `PATHWAYS.md`.

## Five decisions for review

1. Do the experimental unit and the `~ donor + condition` design adequately represent pairing and the available degrees of freedom?
2. Is the interpretation of outcomes with independent filtering and Cook’s distance enabled or disabled correct, including missing `padj` values?
3. Does the diagnosis of the 308 PyDESeq2 and DESeq2 discrepancies distinguish demonstrated causes from unresolved statistical differences?
4. Do the donor-removal results, VST and PCA, and interpretation of effect estimates characterize stability while accounting for overlap among the folds?
5. Are the Ensembl–Entrez mapping, GO size thresholds, CAMERA settings, and GOseq sensitivity analyses defensible? Which pathway conclusions require more qualified wording?

## Review record

Complete this record after the user makes contact and receives the review. Capture the reviewer’s declared name and qualifications, the date, the artifacts and versions reviewed, responses to each question, limitations raised, and the authors’ response. Include reviewer personal or contact information in publishable artifacts only where necessary and with consent.

| Field | Status |
|---|---|
| Reviewer and declared qualifications | `pending` |
| Date and scope reviewed | `pending` |
| Comments and responses | `pending` |
| Individual demonstration by the user | `pending` |

Computational review and local tests provide evidence for an independent scientific assessment, which remains pending.
