# AIRWAY research track

The baseline is in `src/`, `tests/`, `data/`, `config.json`, and `reference/`. The experimental track is in `research/`. Store large inputs and outputs under `.artifacts/research/` to keep baseline references reproducible.

## Environments

```powershell
docker build --target dependencies -t rnaseq-python:dev .
docker build -f research/python.Dockerfile -t airway-research-python .
docker build -f reference/Dockerfile -t rnaseq-reference:dev reference
docker build -f research/r.Dockerfile -t airway-research-r .
# For GPL96 audit or processing, using the container environment:
docker build -f research/r-e5.Dockerfile -t airway-research-r:e5 .
```

The images inherit pinned digests. Run analysis with `--network none`, `--read-only`, explicit resource limits, and a dedicated output volume. `r-e5.Dockerfile` adds `hgu133acdf` to the E0 R environment. E5 requires documented sample selection before RMA.

## Checks

```powershell
docker run --rm --network none airway-research-python python -m pytest research/tests -q -p no:cacheprovider
docker run --rm --network none -v "${PWD}:/workspace:ro" -w /workspace airway-research-r Rscript research/r/test_pathway_utils.R
```

The baseline job in `.github/workflows/ci.yml` runs separately from the `research` job. Both jobs operate on available inputs and skip cohort downloads and extended simulations.

## Analyses

- E2 and E3 use `research/diagnostics.py` and `research/robustness.py` with versioned configurations in `research/configs/`.
- E4 uses `research/r/annotation.R` and `research/r/pathways.R`. Write the full tables, manifest, and reports to a new output directory. See `docs/research/PATHWAYS.md`.
- E5 follows the decision and hashes in `docs/research/EXTERNAL-PROTOCOL.md`. Resume inference once metadata resolve stimulus assignment and pairing.
- E6 runs with `python -m research.simulate --config research/configs/simulation.json --output /output/E6 [--replicates 10]`. Runs can resume per scenario. Use 10 replicates for the pilot and 200 for production. For four pairs in R, run `Rscript research/r/simulate_four_pairs.R <diagnostics.csv> <output-dir> [replicates]`.
- Production splits pair counts across `research/configs/simulation-production-n*.json`. Each configuration sets 200 replicates and can resume from the scenario CSVs.
- Aggregate a completed run without refitting genes using `python -m research.summarize_simulation --replicates <summary-replicates.csv> --execution-manifest <provenance.json> --output <new-directory>`.
- E7 prompts are in `research/tasks/participant/`. Mount `research/tasks/evaluator/` exclusively in the evaluator environment. `task_runner.record_attempt` requires a real attempt supplied explicitly.

Record protocol changes and evidence in `docs/research/STATUS.md` and preserve previous results. Execution evidence and scientific limitations are documented under `docs/research/`.
