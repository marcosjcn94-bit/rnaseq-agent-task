# Trilha de pesquisa AIRWAY

A baseline permanece em `src/`, `tests/`, `data/`, `config.json` e `reference/`. A trilha experimental está em `research/`; entradas e saídas pesadas ficam sob `.artifacts/research/` e não devem ser copiadas para referências baseline.

## Ambientes

```powershell
docker build -f research/python.Dockerfile -t airway-research-python .
docker build -f research/r.Dockerfile -t airway-research-r .
# Somente para auditoria/processamento GPL96, sem instalar no host:
docker build -f research/r-e5.Dockerfile -t airway-research-r:e5 .
```

As imagens herdam digests fixados; análise roda com `--network none`, `--read-only`, limites explícitos e volume de saída separado. `r-e5.Dockerfile` acrescenta somente `hgu133acdf` ao ambiente R E0. E5 não executa RMA enquanto a escolha de amostras não estiver documentada.

## Verificações

```powershell
docker run --rm --network none airway-research-python python -m pytest research/tests -q -p no:cacheprovider
docker run --rm --network none -v "${PWD}:/workspace:ro" -w /workspace airway-research-r Rscript research/r/test_pathway_utils.R
```

O job baseline em `.github/workflows/ci.yml` fica separado do job `research`; nenhum deles baixa a coorte nem roda simulação extensa.

## Análises

- E2/E3: `research/diagnostics.py` e `research/robustness.py`, usando configs versionadas em `research/configs/`.
- E4: `research/r/annotation.R` e `research/r/pathways.R`; tabelas integrais, manifesta e relatórios gerados em saída nova. Ver `docs/research/PATHWAYS.md`.
- E5: siga a decisão e os hashes em `docs/research/EXTERNAL-PROTOCOL.md`. Só retome inferência se metadados resolverem estímulo e pareamento.
- E6: `python -m research.simulate --config research/configs/simulation.json --output /output/E6 [--replicates 10]`. Réplicas são retomáveis por cenário; `10` é piloto e `200` produção. R n=4: `Rscript research/r/simulate_four_pairs.R <diagnostics.csv> <output-dir> [replicates]`.
- A execução de produção divide pares em `research/configs/simulation-production-n*.json`; cada config fixa 200 réplicas e pode ser retomada a partir dos CSVs por cenário.
- Agregue uma execução já concluída sem reajustar genes via `python -m research.summarize_simulation --replicates <summary-replicates.csv> --execution-manifest <provenance.json> --output <novo-diretório>`.
- E7: prompts visíveis em `research/tasks/participant/`; gabaritos são exclusivos do avaliador em `research/tasks/evaluator/`. Não monte esse diretório em ambiente participante. `task_runner.record_attempt` registra somente uma tentativa real fornecida explicitamente.

Registre alterações de protocolo e evidências em `docs/research/STATUS.md`; não substitua resultados anteriores. A execução e os limites científicos estão descritos em `docs/research/`.
