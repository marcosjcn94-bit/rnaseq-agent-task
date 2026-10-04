# Paired airway RNA-seq agent task

An independent computational reanalysis of dexamethasone-treated human airway smooth muscle cells, packaged as an offline, executable scientific task. This is a portfolio demonstration on a known dataset, not a clinical tool or a general agent benchmark.

## Scope and architecture

Eight samples, four donor-matched control/treated pairs, without albuterol, exported from the official Bioconductor airway 1.30.0 object. A Python CLI validates raw counts and provenance, fits PyDESeq2 0.5.4, and writes tables, QC and figures. A separate R/DESeq2 1.50.2 implementation checks effect sizes and directions. An evaluator-owned Docker runner executes submissions without network access; gold and grading code stay outside the participant environment.

No frontend, API, database or cloud deployment is necessary for this file-based scientific workload. Docker is the deployment artifact.

## Run on Windows / PowerShell

Prerequisite: Docker Desktop with Linux containers. Preparation requires network access; analysis and tests run offline. No host Python packages, cloud account or paid model API are required.

```powershell
docker build --target pipeline -t rnaseq-pipeline:validated .
New-Item -ItemType Directory -Force results | Out-Null
$projectPath = (Get-Location).Path
$imageId = docker image inspect rnaseq-pipeline:validated --format '{{.Id}}'
docker run --rm --network none --read-only --cpus 2 --memory 4g --tmpfs /tmp:rw,nosuid,size=512m --env "RNASEQ_IMAGE_ID=$imageId" --mount "type=bind,src=$projectPath\results,dst=/output" rnaseq-pipeline:validated python -m src.cli run --data /data --output /output/run-1 --config /app/config.json
```

Each output directory must be empty or absent. Reusing a nonempty directory fails rather than overwriting results. The image contains the preserved inputs; its root filesystem is read-only.

Outputs: differential_expression.csv, normalized_counts.csv, gene_filter.csv, qc.json, analysis_summary.json, run_manifest.json and four figures under figures/. The manifest records input/code/configuration hashes, package versions, image ID, elapsed time and parent-process peak RSS. Worker memory is excluded. Scientific warnings are preserved in the summary and printed.

```powershell
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=512m rnaseq-pipeline:validated python -m pytest -q -p no:cacheprovider
docker run --rm --network none rnaseq-pipeline:validated pip check
```

## Fixed scientific method

Raw integer counts only; align samples by ID and require four complete donor pairs. Prefilter >=10 counts in >=4 samples. Fit ~ donor + condition, treated/control contrast, ratio size factors, parametric dispersion fit, two-sided Wald test of LFC=0, BH adjustment at alpha .05, explicit Cook's/independent-filter settings, no LFC shrinkage. Positive log2FC means higher expression after treatment.

Significant means padj <.05. The additional abs(log2FC)>=1 highlight is exploratory, not a test of an effect exceeding that threshold. Missing statistics remain missing with a reason.

QC covers count matrices only. PCA uses log2(normalized counts+1) over up to 500 highest-variance genes; this is not VST. The heatmap selects up to 20 lowest-padj genes and applies per-gene z-scores. Volcano displays adjusted p-values, capped at 50 on the -log10 axis. No sample was excluded based on the PCA.

## Results and validation

The final validated analysis retained 16,139 of 63,677 genes; Python found 3,879 significant genes (2,104 up / 1,775 down), with 957 exploratory highlights. The independent R run found 4,081 significant genes. Effect-size Spearman was 0.9999944, and direction agreement was 100% over 852 strong reference genes.

These are concordant effect estimates, **not identical statistical results**: 308 significance classifications differ, and R has 313 adjusted p-values missing through independent filtering. See [reference/VALIDATION.md](reference/VALIDATION.md), [comparison.json](reference/comparison.json) and [docs/INTERPRETATION.md](docs/INTERPRETATION.md). Two final offline runs returned identical tables (also within rtol=1e-6, atol=1e-8) in 122.29 and 129.84 seconds; parent peak RSS was 327.03 and 329.90 MiB. These timings reflect this local machine and concurrent workloads. Final measured reproduction evidence is in [evidence/](evidence/).

Only four biological replicates and three residual degrees of freedom are available. The installed Python implementation warns about unstable dispersion-prior estimation; the warning is retained. The gold is fixed to the Python environment after the predefined R effect/direction gate passes.

## Independent reference

```powershell
docker build -f reference/Dockerfile -t rnaseq-reference:validated reference
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,size=512m --mount "type=bind,src=$projectPath,dst=/work" rnaseq-reference:validated Rscript /work/reference/run_deseq2.R /work/data /work/reference/output /work/config.json
docker run --rm --network none --mount "type=bind,src=$projectPath,dst=/work" -w /work rnaseq-pipeline:validated python -m src.compare results/run-1/differential_expression.csv reference/output/differential_expression.csv --output reference/comparison.json
```

R preparation checks every package against reference/packages.lock.csv. It rejects repository drift; it does not restore old package tarballs automatically. Preserve the validated image for offline reruns. Base images are pinned by digest and Python transitives by exact version; binary availability from upstream repositories is still an online rebuild dependency.

data/manifest.json records official source URLs, export versions, sample mapping and SHA-256 hashes. reference/export_airway.R documents the one-time acquisition. .gitattributes preserves LF bytes across Windows Git checkouts so hashes remain valid. Annotation is historical Ensembl 75 / GRCh37.p13; gene IDs are not collapsed to symbols.

## Demonstrative task and evaluator

Read [benchmark/TASK.md](benchmark/TASK.md), [SOURCES.md](benchmark/SOURCES.md) and [RUBRIC.md](benchmark/RUBRIC.md). Participants write analyze.py and receive only data, instructions, configuration and installed libraries.

```powershell
docker build --target participant -t rnaseq-participant:validated .
# Freeze evaluator-only gold after the passing R comparison:
docker run --rm --network none --mount "type=bind,src=$projectPath,dst=/work" -w /work rnaseq-pipeline:validated python -m benchmark.prepare --source results/run-1 --validation reference/comparison.json
# Host Python uses only the standard library for the evaluator-owned runner:
py -3.13 -m benchmark.runner --source YOUR_SUBMISSION --output results/submission-1 --receipt results/receipts/submission-1.json
# Mount the evaluator workspace only in this separate grading container:
docker run --rm --network none --mount "type=bind,src=$projectPath,dst=/work" -w /work rnaseq-pipeline:validated python -m benchmark.grader --submission results/submission-1 --gold benchmark/gold --receipt results/receipts/submission-1.json --human-review benchmark/HUMAN_REVIEW.json --output results/grade-1.json
```

Before gold preparation, copy the reviewed interpretation into results/run-1/interpretation.md. The pipeline calculates results; the interpretation is separately authored and reviewed.

[benchmark/REHEARSAL.md](benchmark/REHEARSAL.md) records the correct solution (85 automatic points, human review pending), rejection of real unpaired and reversed-contrast executions, and read-only/network/failure probes.

The runner enforces 2 CPUs, 4 GiB, 128 processes, 30-minute timeout, no network, non-root execution, read-only root/input/source and no Docker socket or evaluator mounts. Receipts and logs remain outside participant mounts. This is basic container isolation, not a claim of protection against every hostile-kernel exploit.

Automatic grading totals 85 points; human review adds up to 15. A score of 85 alone is pending review, not approved. Human review checks source, method, figures and biological claims. A copied reference solution rehearses the mechanics; it is not a measured AI-agent attempt. Known public data can be memorized; future generalization requires unseen tasks.

## Review, interview and provenance

[docs/INTERVIEW.md](docs/INTERVIEW.md) contains a Portuguese study guide and five technical questions. [PLANO.md](PLANO.md) records evidence and remaining human/publication checks. CI runs small offline fixtures, not the complete airway analysis.

Code and documentation were developed with Codex assistance. Separate Python/R implementations and source inspection provide computational cross-checks; no external scientist review or user mastery is claimed. Human review and interview rehearsal must be recorded honestly.

Own code is MIT licensed. Dataset/source licensing and attribution are separate: see [data/LICENSE-NOTES.md](data/LICENSE-NOTES.md). This reanalysis makes no novel-discovery or clinical claims.
