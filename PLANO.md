# Execução — rnaseq-agent-task

Spec: PLANO-BIOINFORMATICA.md. Escopo aprovado: opção 3, sem prazo; execução local, um agente, sem publicação automática.

- [ ] 1. Ambiente, contratos, dados oficiais e proveniência.
- [ ] 2. Validação de entrada e QC bruto.
- [ ] 3. Modelo pareado, QC normalizado, figuras e manifestos.
- [ ] 4. Referência independente R/DESeq2 e revisão científica.
- [ ] 5. Tarefa, runner offline, grader e ensaio adversarial.
- [ ] 6. Reprodução, CI, documentação, revisão e entrevista.

## Ajustes aprovados na revisão
PCA após normalização; submissão executável; gold isolado; cobertura completa dos genes; opções estatísticas explícitas; duas execuções finais Python; erros e escrita de saídas definidos.

## Evidências
2026-10-04: GitHub ADMIN, remoto vazio e público; Docker Engine 29.8.1; Git local inicializado. Escrita autorizada pela revisão automática para preparação.

## Decisões de execução
Ruling: usar a pasta dedicada atual e uma branch de implementação em vez de outro worktree: repositório novo, sem trabalho concorrente; evita duplicar dados. Custo se errado: isolamento adicional necessário.
Ruling: preservar MEMORIA.md e PLANO.md versionados como ledger; instrução específica do projeto prevalece sobre ledger temporário da skill. Custo se errado: nenhum algoritmo afetado, formato de continuidade diferente.
Ruling: não delegar nem anunciar revisão externa; fazer revisão separada pelo próprio executor conforme regra do plano. Custo se errado: menor independência na revisão de software; referência estatística continua separada em R.
