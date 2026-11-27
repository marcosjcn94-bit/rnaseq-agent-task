# Baseline and extension provenance

Recorded on 2026-10-05 before changes to the research track.

- Branch `implementation`; HEAD `f908afcbe483167bd0de40cef26fff6e92d26dfd`.
- Initial state had a preexisting removal of `benchmark/HUMAN_REVIEW.json` and preexisting untracked `docs/RESEARCH-AUDIT-2026-10-05.md` and `docs/superpowers/`. Preserve these items and their recorded state.
- `scripts/verify_evidence.py`: exit 0, “All input, scientific source and evidence hashes verified”. Ran in this session.
- IDs recorded in `reference/environment.json`: initial Python `sha256:13b69b245a31c45a9ab9c37d319797b1c25b1a9f3145286c8e601db3d500cd97`; reference R `sha256:be72a4cb6b900259697fd30c5253ebeabe2c8ded98b2ae82a54a28f904d22706`; validated R `sha256:ad8eb7fc6c64ca4fc5535e50034db232822c0de4b5ba82ce1e214d6735736c58`; scientific Python `sha256:5d61a9a0192f6a4128a5b135ac833ee94c65b0027142d8b34857760e64560eec`; CI baseline `sha256:4a0c28c913eb937bece661f05d26389a0f3a7222857500804f57f78013f4347d`; participant `sha256:dc7aa8d4f631ca4fc5535e50034db232822c0de4b5ba82ce1e214d6735736c58`.
- E0 images were built with the pinned base images: research Python `sha256:fa5709341bef9077bcc81677191fa94a0c2e815f004d83701aed6f61818378e4`; research R `sha256:f63cb28be3ec39dd5fecdc5102fc566e21877314451889dcd1e94f891ce5ec06`. The R image uses R 4.5.2, Bioconductor 3.22, and DESeq2 1.50.2. The build checked 218 packages against `research/r-packages.lock.csv`.
- Recorded SHA-256 hashes. `data/counts.csv` `69D93E59052F921CEA64B82F9B207AEBDE9D6B9532A9D12CDBA4A06AD5391736`; `data/metadata.csv` `285C9BB58AC5CCEF7345906158D3F2F4F88A0C0489E939D8FD639FA02C7BBC8D`; `data/annotation.csv` `3219D6B73D51CF6DE99BA3C9EF7D99F728C737781746EE47FB1DA368855D07DE`; `reference/comparison.json` `4658A61B32186C25E2B7F10959AE594A2FA15356AE55DC42158B8F078247F5B6`; `evidence/analysis-summary.json` `627766D7975CEAFEEFB0D31F50ABB241B533EF53E490C609F65A53E9F6D606F1`.
- The plan and audit record historical tables and discrepancy counts. A new fit was outside the scope of this stage.
- The sandbox denied the first `docker info` request. A read-only request succeeded after auto-review authorization. The host lacked `Rscript`. The extension ran entirely in separate images and used no host package installations.

## Limitations and resumption

Reference IDs originate from `reference/environment.json`. E0 IDs identify images built locally during this run. The verifier checks evidence hashes. Model refitting requires a separate run. Keep the baseline as the reproduction reference and retain historical summaries as context.
