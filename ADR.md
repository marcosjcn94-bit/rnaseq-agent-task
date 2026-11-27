# Architecture decisions

## ADR-01 — Prepared counts (accepted, 2026-10-04)

- **Context** — The project focuses on reproducible analysis and evaluation.
- **Decision** — Use the official airway object and start from the count matrix.
- **Alternative** — Repeat read alignment, which would require more resources and a larger scope.
- **Consequence** — Limit QC to the count matrix and preserve provenance and historical annotation.

## ADR-02 — Python pipeline and R reference (accepted, 2026-10-04)

- **Decision** — Use PyDESeq2 0.5.4 in the CLI and DESeq2 in a separate image.
- **Alternative** — Use a single backend without comparing implementations.
- **Consequence** — Record versions and options explicitly. Agreement between implementations leaves the methods' conceptual independence unestablished.

## ADR-03 — Paired model (accepted, 2026-10-04)

- **Decision** — Use `~ donor + condition` for the treated versus control contrast across four pairs.
- **Alternative** — Omit the donor effect and confound biological variability.
- **Consequence** — Require full rank, eight samples, and complete pairs.

## ADR-04 — CLI and files (accepted, 2026-10-04)

- **Decision** — Use a Python CLI, local files, and Docker.
- **Alternative** — Add a web application with an API, database, and frontend. The scientific question requires only the file-based workflow.
- **Consequence** — Provide a reproducible interface and exclusive output directories.

## ADR-05 — Demonstrative evaluation (accepted, 2026-10-04)

- **Decision** — Use an offline runner, a deterministic grader worth 85 points, and human review worth 15.
- **Alternative** — Use an LLM judge or rely on participants' own claims.
- **Consequence** — Keep evaluator reference outputs separate. Code review remains necessary to establish authorship and method beyond the submitted artifacts.

## ADR-06 — Online preparation and offline execution (accepted, 2026-10-04)

- **Decision** — Obtain and pin images and data once, then run without network access.
- **Alternative** — Download dependencies or data during analysis.
- **Consequence** — Record hashes, versions, and the image, and verify the terms before redistributing data.
