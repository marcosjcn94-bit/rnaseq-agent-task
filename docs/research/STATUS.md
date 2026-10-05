# Status da extensão de pesquisa

Data: 2026-10-05. Plano: `docs/superpowers/plans/2026-10-05-airway-research-extension.md`.

| Etapa | Estado | Evidência / próxima ação |
|---|---|---|
| E0 | Concluída | Núcleo, imagens separadas e lock R; 8 testes; reprodução baseline dentro de `rtol=1e-6, atol=1e-8`. `BASELINE.md`. |
| E1 | Parcial | Guia, prática e pacote de revisão prontos; demonstração individual e parecer externo pendentes. `EXTERNAL-REVIEW.md`. |
| E2 | Concluída | Hashes baseline reproduzidos; 16.139 genes, 308 discordâncias; causa integral não resolvida. `PYTHON-R.md`. |
| E3 | Concluída | Quatro folds pareados, efeitos/PCA/distâncias e figuras inspecionadas. `ROBUSTNESS.md`. |
| E4 | Computacional concluída | Anotação congelada e CAMERA/ORA/GOseq executados/testados. Interpretação humana pendente; `PATHWAYS.md`. |
| E5 | Auditoria concluída; sem inferência | SOFT/MINiML e seis CEL auditados/hash; `insufficient_metadata` para estímulo por amostra. RMA não executado; `EXTERNAL-PROTOCOL.md`. |
| E6 | Computacional concluída | Produção offline: 3.200 PyDESeq2 (16 cenários) + 800 DESeq2 (4 cenários n=4), 200/cenário, zero falhas; agregados e manifests/hash por lote disponíveis. Comparação entre engines não pareada. `SIMULATION.md`. |
| E7 | Suíte inicial validada | 12 casos sintéticos com fixtures explícitos, chaves separadas; 4 testes grader/runner passaram. Sem tentativas reais de agente; rubricas aguardam revisão. |
| E8 | Validação local concluída | Baseline hash check passou; 25 testes Python, fixture R e lock R passaram; `git diff --check` limpo. Job CI separado adicionado, sem execução remota. |

**Pendências humanas:** demonstração individual, revisão externa, interpretação das vias, validação de rubricas e julgamento de compatibilidade externa. Nenhuma inventada; execução independente continua.

**Integridade:** baseline e alterações preexistentes preservadas (`BASELINE.md`); nenhuma instalação no host, serviço pago, mensagem, publicação ou push. Evidência E6 da rodada inicial com SD=0,35 está retida apenas para rastreabilidade e explicitamente excluída da interpretação principal.
