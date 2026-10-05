# E2 — decomposição inicial das divergências Python/R

Data: 2026-10-05. Protocolo: `PROTOCOL.md`; configurações congeladas em `research/configs/diagnostics*.json`. Todos os ajustes foram executados offline em imagens separadas, com 2 CPUs, 4 GiB, raiz somente leitura e saída isolada em `.artifacts/research/E2/`. Os manifests registram versões, hashes, parâmetros, avisos e recursos.

## Reprodução e universo

O ajuste Python produziu uma tabela de resultados cujo SHA-256 coincide byte a byte com `reference/comparison.json` (`740a5d…577363`); a tabela R também coincide com a referência (`c54635…a37ef5`). Cada saída tem 16.139 genes e a junção por Ensembl não perdeu IDs. A classificação recuperada foi:

| Resultado | Genes |
|---|---:|
| Significativos em ambos | 3.826 |
| Somente Python | 53 |
| Somente R | 255 |
| Não significativos em ambos | 12.005 |

Há 313 `padj` ausentes em R e nenhum `pvalue` ausente em qualquer implementação. Os resultados históricos são, portanto, reproduzidos; isso não converte as saídas em validação biológica independente.

## Componentes

Os exports incluem fatores de tamanho com precisão completa, contagens normalizadas, campos por gene disponíveis nas versões, dispersões (estimativa gênica, tendência e final/MAP), convergência, coeficientes/SE/Wald/p/`padj`, Cook por amostra e máscaras. Python registra `prior_disp_var=0.25`; o adaptador PyDESeq2 0.5.4 não expõe um limiar efetivo de independent filtering, então o manifest marca esse campo como indisponível. R registra limiar 10,3192 e os coeficientes da tendência paramétrica (`asymptDisp=0,01`, `extraPois=3,1955`). Esses parâmetros internos não são equivalentes diretos.

Em 16.139 genes, diferenças absolutas entre estimativas gênicas de dispersão têm mediana `4,65e-8` e P95 `0,000592`; entre tendências, mediana `0,001592` e P95 `0,03136`; entre dispersões finais, mediana `0,001935` e P95 `0,01509`. Diferenças absolutas de log2FC têm mediana `0,000160` e P95 `0,002185`, enquanto as de SE têm mediana `0,00747`, P95 `0,01926` e máximo `0,61068`. A diferença absoluta da estatística Wald tem mediana `0,04257` e P95 `0,38766`. Isso aponta associação das divergências de classificação a incerteza/teste e filtragem, não a uma diferença material geral dos log2FC; não prova mecanismo causal.

## Contrastes isolados

Cada contraste abaixo muda uma opção em relação à base, mantendo a outra:

| Execução | p-values alterados | `padj` alterados | Genes significativos antes → depois | Discordâncias depois |
|---|---:|---:|---:|---:|
| Python, IF desligado | 0 | 0 | 3.879 → 3.879 | 308 |
| R, IF desligado | 0 | 15.544 | 4.081 → 4.068 | 283 |
| Python, Cook desligado | 0 | 0 | 3.879 → 3.879 | 308 |
| R, Cook desligado | 0 | 0 | 4.081 → 4.081 | 308 |

Desligar IF em R mudou a classificação de 37 genes; 31 pertenciam às discordâncias iniciais, e o total líquido caiu de 308 para 283. A contagem de genes reclassificados e a diferença líquida são medidas distintas. Cook não alterou p-values, `padj` ou classes nesta coorte; ambos os exports têm zero p-values ausentes. Os efeitos de opções podem se sobrepor e não devem ser somados como causas exclusivas. Não foi encontrado um experimento que explique integralmente os 308 casos.

## Casos definidos por regra

- Maior diferença absoluta de SE: `ENSG00000179593`, SE Python `1,66246` / R `1,05179`; log2FC `9,50198` em ambos. O gene é significativo em ambas as saídas. Exemplo de efeito grande e incerteza muito diferente, não de discordância de classificação.
- R `padj` mais próximo de 0,05: `ENSG00000116161`, R `padj=0,0499763` (R-only) versus Python `padj=0,0728619`.
- Caso filtrado em R com menor `baseMean` entre `padj=NA` e p-value finito: `ENSG00000267683`, R `baseMean=6,1365`, abaixo do limiar `10,3192`; R `p=0,003069`, `padj=NA`, enquanto Python tem `padj=0,019078`. Esse é um caso de filtragem, não de ausência de evidência bruta.
- Controle concordante significativo definido por maior `baseMean` do grupo: `ENSG00000164692`, log2FC Python `-0,438146` / R `-0,438146`, significativo em ambos.

## Interpretação e limite

Os algoritmos registram componentes diferentes: PyDESeq2 estima a variância do prior por uma rota MAD/trigamma; o DESeq2 1.50.2 tem caminho especial de simulação para apenas três graus residuais. Os dados confirmam valores internos distintos, mas isso não quantifica quanto cada escolha explica nos 308 genes. Não substituí componentes internos: não foi demonstrada uma adaptação segura e equivalente entre implementações. Esse mecanismo permanece associado/pendente de quantificação, não confirmado. Cook não contribuiu neste conjunto e a alteração de IF em R explica mudança marginal de classes, não todas as divergências.

Os arquivos completos e manifests ficam em `.artifacts/research/E2/`; o resumo e os casos reproduzíveis estão em `summary-v3/summary.json`. Resultados negativos são válidos. Não houve tentativa de zerar a discordância.
