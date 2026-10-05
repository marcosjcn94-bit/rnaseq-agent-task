# Como realizar a revisão humana

A revisão humana verifica se uma pessoa consegue inspecionar a solução e avaliar método, figuras e afirmações. Ela completa a rubrica do benchmark; não transforma a reanálise em revisão por pares nem comprova uma descoberta nova.

O arquivo `benchmark/HUMAN_REVIEW.json` começa deliberadamente incompleto. **Não preencha os campos para obter aprovação automática. Faça as verificações primeiro e registre o resultado verdadeiro.** Você pode atuar como revisor se identificar a revisão como autorrevisão. Um bioinformata ou pesquisador experiente oferece uma avaliação externa mais forte para o currículo.

## Passo a passo

1. Abra `benchmark/TASK.md`, `benchmark/RUBRIC.md`, `benchmark/SOURCES.md`, `reference/VALIDATION.md` e `docs/SCIENTIFIC-ASSESSMENT.md`.
2. Leia o código de entrada, modelo e relatórios: `src/data.py`, `src/analysis.py`, `src/report.py` e `reference/run_deseq2.R`.
3. Confira a seção “Método e código” abaixo. Compare configurações, implementação e evidências; não confie apenas no resumo que a submissão declara.
4. Abra as quatro imagens de uma execução completa: `results/run-1/figures/`. Confira títulos, amostras, eixos, transformação e ressalvas indicadas.
5. Leia `docs/INTERPRETATION.md` e confira as afirmações no artigo original e nas fontes. Separe observação, hipótese e causalidade.
6. Atribua uma nota justificada de 0 a 15, complete o modelo JSON e mantenha as evidências e limitações nas notas.
7. Se a revisão for sobre uma submissão do benchmark, o avaliador deve usar o arquivo preenchido e o recibo correto ao rodar o grader. A saída local de ensaio ainda está pendente de revisão e não deve ser apresentada como aprovada.

## Critérios da nota humana (15 pontos)

| Bloco | Pontos | O que conferir |
|---|---:|---|
| Método e código | 0–5 | Contagens brutas; oito amostras correspondem a quatro pares; filtro; fórmula e contraste reais; configurações de filtros/outliers; efeito sem shrinkage; valores ausentes preservados. |
| Figuras e QC | 0–5 | Quatro PNGs legíveis e coerentes; condições/doadores; PCA rotulada como exploratória em log2 de contagens normalizadas + 1, não VST; volcano com padj e limite de exibição; heatmap com z-score por gene. |
| Interpretação e fontes | 0–5 | IDs e anotações; contexto apoiado em fontes; observação separada de hipótese; limitações da amostra; 308 divergências e 313 padj ausentes em R relatadas sem atribuição causal exagerada; nenhuma conclusão clínica. |

Dê crédito somente ao que verificou. Uma falha não precisa zerar o bloco todo: desconte pontos e explique o motivo. Se não conseguir avaliar um item, anote a limitação e não marque o bloco como plenamente verificado.

## Campos do modelo

- `reviewer`: nome identificável do revisor; use seu próprio nome se fizer autorrevisão.
- `score`: nota total justificada, inteiro de 0 a 15.
- `method_verified`, `figures_reviewed`, `sources_reviewed`: marque `true` apenas após conferir o bloco correspondente.
- `completed`: `true` quando a inspeção terminar; não significa que todos os itens passaram.
- `notes`: data, tipo de revisão (autorrevisão ou externa), caminhos/fontes examinados, achados, nota por bloco e pendências.

A rubrica exige revisão humana concluída para aprovação. Como o limiar total é 85 e os pontos automáticos já podem somar 85, a nota humana não funciona como nota mínima adicional: **a revisão concluída é uma etapa obrigatória, mesmo se a nota for baixa**. Os flags e a identidade são declarações do revisor, não verificação criptográfica de identidade.

O modelo permanece com `completed: false) até a revisão acontecer.