# E4 — análise funcional de vias

Data: 2026-10-05. Análise exploratória do contraste tratado/controle; não demonstra ativação causal nem substitui revisão biológica.

## Protocolo e universo

O universo começa nos 16.139 genes testados pela baseline e usa GO Biological Process com associação ancestral (`GOALL`). Anotação funcional contemporânea congelada em `org.Hs.eg.db` 3.22.0/`GO.db` 3.22.0; contagem histórica Ensembl 75 não foi modificada. A tabela de comprimentos vem da união dos exons por gene (`reduce(rowRanges(airway))`, airway 1.30.0). O snapshot contém 16.319 relações Ensembl–Entrez brutas, 13.772 mapeamentos unívocos nos dois sentidos, 879.448 relações gene–termo e 13.855 termos BP. Os IDs excluídos por ambiguidade ficam preservados na tabela bruta; 170 genes mapeados não entraram no universo GOseq por `padj` ausente. Nenhum dos mapeamentos unívocos perdeu comprimento de éxon.

Termos foram congelados por tamanho 15–500 no universo efetivamente testável, por análise. O método principal foi edgeR/TMM → limma-voom, desenho `~ donor + condition`, contraste tratado/controle, CAMERA direcional, ranking do modelo limma, `use.ranks=TRUE`, `allow.neg.cor=FALSE` e correlação estimada (`inter.gene.cor=NA`). Sensibilidade alterou somente essa correlação para 0,01. Cada análise/fold recebeu BH sobre seus próprios termos elegíveis. Quatro folds removeram um doador completo.

## Resultados

- **CAMERA com correlação estimada:** 4.265 termos elegíveis na base; nenhum termo com FDR < 0,05. Os folds tiveram 4.261–4.263 termos, também sem termos abaixo de 0,05.
- **CAMERA com correlação fixa 0,01:** 11 termos com FDR < 0,05 na base; os folds variaram de 7 a 13. O resultado depende da hipótese de correlação; com quatro pares e três graus residuais, essa sensibilidade é material e não deve ser tratada como confirmação independente.
- **ORA (sensibilidade):** lista DESeq2 com `padj < 0,05`, removendo `padj` ausente do universo. Foram 1.422/4.247 termos com FDR < 0,05. Sem independent filtering, no universo comum testável, foram 1.470/4.265. Os resultados são uma sensibilidade baseada numa lista grande de selecionados, não o ranking principal.
- **GOseq (sensibilidades separadas):** Wallenius, categorias explícitas, mesma coleção GO e mesmo universo elegível. Com comprimento de éxons, 1.187 termos enriquecidos e 57 sub-representados tiveram FDR < 0,05; usando média de contagens normalizadas, foram 1.035 e 76. As curvas de probabilidade de seleção por gene estão em `selection_probability_curves.csv`. A diferença entre as sensibilidades mostra dependência do modelo de viés; não combinar comprimento e expressão.

Cinco p-values GOseq elegíveis excederam 1 apenas por erro numérico (máximo observado antes do corte: `4,9e-11`). Foram limitados ao intervalo matemático [0,1], e o BH foi recalculado após restringir 15–500 genes. O valor bruto, flag de correção e ambas as caudas são preservados em `goseq_sensitivities.csv`. O ajuste `nullp` também emitiu o aviso de ponto inicial próximo às restrições; as curvas e os avisos devem ser considerados ao interpretar os resultados.

As diferenças entre CAMERA estimado, CAMERA fixo, ORA e GOseq são parte do resultado e não foram usadas para selecionar um único conjunto de termos para teste. Nomes e grupos GO sobrepostos não equivalem a mecanismos independentes. Ainda falta revisão humana da interpretação funcional; nenhuma conclusão de ativação, causalidade ou validação experimental é reivindicada.

## Evidência reproduzível

- Configuração e comandos: `research/configs/pathways.json`, `research/r/annotation.R`, `pathways.R`, `finalize_annotation.R` e `finalize_pathways.R`.
- Testes sintéticos e QA: `research/r/test_pathway_utils.R`, `test_annotation.R` e `test_pathway_results.R` passaram na imagem `airway-research-r:e0`, com rede desabilitada.
- Manifestos e SHA-256 por artefato: `.artifacts/research/E4/annotation-v2/manifest.json` e `.artifacts/research/E4/pathways-final/manifest.json`; resultados volumosos permanecem sob `.artifacts/research/`.
- A tentativa de anotação original, com cabeçalho ambíguo de colunas adicionais do `GOALL`, foi preservada em `.artifacts/research/E4/annotation-attempt1/`. O snapshot final foi normalizado e testado em um diretório separado.
