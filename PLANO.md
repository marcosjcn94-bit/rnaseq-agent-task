# Execução e estado do projeto AIRWAY

Escopo: opção 3, MVP completo com testes de falhas, revisão científica computacional, tarefa demonstrativa e preparação para entrevista. A especificação original `PLANO-BIOINFORMATICA.md` foi preservada; este arquivo registra execução e pendências.

## Entregas de engenharia concluídas

- Dados oficiais airway 1.30.0: 63.677 genes, oito amostras, quatro pares controle/tratado sem albuterol; proveniência, licença e hashes documentados.
- Validação de contagens brutas, IDs, metadados, pares e configuração; rejeição de entradas inválidas.
- PyDESeq2 0.5.4, modelo `~ donor + condition`, saídas tabulares, resumo, QC e quatro figuras.
- Reanálise de referência em R/DESeq2 1.50.2, comparação pré-especificada e auditoria das diferenças.
- Tarefa científica, runner Docker offline, grader determinístico, ensaios adversariais e evidências verificáveis.
- Duas execuções científicas Python produziram tabelas idênticas; 46 testes locais passaram; `pip check` passou.
- Branch `implementation` publicado no GitHub: [rnaseq-agent-task](https://github.com/marcosjcn94-bit/rnaseq-agent-task). Acompanhar o workflow remoto na aba Actions; a CI verifica fixtures e não refaz a análise científica completa.
- Guias em português para revisão humana, preparação para entrevista e avaliação científica.

## Resultados e limites

Foram retidos 16.139 genes. Python encontrou 3.879 genes com `padj < 0,05` (2.104 aumentados, 1.775 reduzidos); 957 também tiveram `abs(log2FC) >= 1`, critério de destaque exploratório. R encontrou 4.081 significativos. Correlação Spearman do log2FC: 0,999994; concordância de direção: 100% em 852 genes fortes. As 308 divergências de classificação e 313 `padj` ausentes em R permanecem documentadas. A causa de cada discrepância não foi estabelecida.

Há quatro doadores e três graus de liberdade residuais; não há QC de FASTQ/alinhamento nem coorte independente. É uma reanálise computacional, não uma descoberta nova ou uma conclusão clínica.

## Revisão humana e candidatura

O ensaio de referência marcou 85/85 pontos automáticos, sem falhas críticas, com execução verificada; estado correto: `pending_human_review`. Nenhum ponto humano foi atribuído. O roteiro para uma revisão genuína está em `docs/HUMAN-REVIEW.md`; não alterar o modelo de revisão para declarar uma etapa que não ocorreu.

Resta o usuário demonstrar que consegue executar e explicar a análise. `docs/INTERVIEW.md` traz respostas de estudo; sua leitura não prova domínio. `docs/SCIENTIFIC-ASSESSMENT.md` discute extensões futuras, que não são necessárias para concluir o MVP de portfólio.

## Evidências

- [Comparação Python/R](reference/comparison.json) e [interpretação científica](docs/INTERPRETATION.md).
- [Ensaio do avaliador](benchmark/REHEARSAL.md), [rubrica](benchmark/RUBRIC.md) e [pacote de evidências](evidence/).
- [Revisão de implementação](docs/SELF-REVIEW.md): feita pelo executor, não por um revisor externo.
