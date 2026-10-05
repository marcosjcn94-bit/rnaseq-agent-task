# E3 — robustez aos doadores, QC e efeitos

Data: 2026-10-05. O universo principal foi fixado nos 16.139 genes filtrados pela baseline. Cada fold retirou as duas amostras de um doador; nenhuma amostra individual foi removida. Os ajustes foram executados sem rede, em imagens separadas, com limite de 2 CPUs/4 GiB. Os quatro folds tiveram seis amostras, três pares, posto 4 e dois graus residuais. Todos os genes foram estimáveis em todos os folds nos dois engines.

## Sensibilidade de efeitos

Genes de efeito basal `abs(log2FC)>=1` foram classificados como estáveis somente quando os quatro folds eram estimáveis, o sinal permanecia igual e o desvio máximo em relação ao ajuste completo ficava abaixo do corte fixo. Limiares 0,25/0,5/1,0 são explorações predefinidas; não foram ajustados aos resultados.

| Medida | Python | R |
|---|---:|---:|
| Genes baseline com `abs(log2FC)>=1` | 1.090 | 1.091 |
| Mantiveram direção em todos os folds | 1.090 | 1.091 |
| Estáveis, corte 0,25 | 688 | 685 |
| Estáveis, corte 0,5 | 1.003 | 1.004 |
| Estáveis, corte 1,0 | 1.087 | 1.088 |
| Mediana do máximo desvio de LFC nos genes de efeito alto | 0,206 | 0,207 |
| P95 do máximo desvio | 0,569 | 0,567 |

Não houve inversão entre os efeitos de `abs(log2FC)>=1` e seus folds; poucos falharam o critério mais estrito por magnitude. Os resultados indicam robustez de direção para esses efeitos na coorte observada, não generalização para novos doadores.

## Listas de significância

| Doador removido | Python DE / perdidos / ganhos | R DE / perdidos / ganhos |
|---|---:|---:|
| N052611 | 2.717 / 1.223 / 61 | 2.653 / 1.482 / 54 |
| N061011 | 2.476 / 1.437 / 34 | 2.375 / 1.734 / 28 |
| N080611 | 3.456 / 712 / 289 | 3.227 / 1.078 / 224 |
| N61311 | 2.838 / 1.105 / 64 | 2.736 / 1.403 / 58 |

Com três pares, há menor precisão e a lista de `padj<0,05` muda substancialmente. Perder significância isoladamente não refuta um efeito; os efeitos e SEs acompanham as listas. Os quatro folds se sobrepõem e não são quatro estudos independentes, nem fornecem automaticamente um intervalo jackknife válido. A sensibilidade opcional de refiltrar `>=10` em `>=3` amostras não foi executada.

## QC e shrinkage

O VST foi calculado com `blind=FALSE` para explorar a resposta ao tratamento; modelos continuaram usando contagens brutas. PCA da baseline (log2 de contagens normalizadas) mostrou PC1/PC2 de 33,4%/30,1%; VST mostrou 48,1%/23,5%. Distâncias entre amostras e relação média-variância foram exportadas. As figuras foram inspecionadas: amostras, condições e doadores estão identificados, escalas legíveis, e não há regra de exclusão por aparência. Nenhuma amostra foi retirada por PCA.

`lfcShrink(type="apeglm")` foi exportado separadamente para `condition_treated_vs_control`; a correlação de ranking de magnitude MLE/apeglm foi 0,9366. A tabela MLE e inferência original permanecem intactas; SD posterior não é tratado como SE MLE.

Entre engines, nos quatro folds, cada comparação manteve 16.139 IDs. A diferença absoluta de log2FC teve mediana entre `4,4e-5` e `1,2e-4`, P95 entre 0,0030 e 0,0042, e máximo entre 0,072 e 0,155, conforme doador removido.

## Limites e artefatos

Três doadores em cada fold dão só dois graus residuais; alertas de dispersão foram mantidos no manifest Python. Resultados continuam exploratórios e não estimam variabilidade entre novas coortes. Tabelas, manifests, PNG/PDF e resumos ficam em `.artifacts/research/E3/`; imagens da última revisão visual em `r-v3/`.
