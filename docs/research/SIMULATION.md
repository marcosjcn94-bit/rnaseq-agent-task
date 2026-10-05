# E6 — simulações NB pareadas

Protocolo em `research/configs/simulation.json`; geradores Python/R em `research/simulate.py` e `research/r/simulate_four_pairs.R`; métricas em `research/simulation_metrics.py`. Seed-base 20261005. Cada réplica gera 1.000 genes com parâmetros empíricos de média/dispersão do export R E2, efeitos basais por doador, fatores de tamanho e NB com tamanho `1/dispersion`, equivalente a variância `mu + dispersion*mu^2`. Efeitos DE têm módulo 1 log2 e sinais balanceados; cenários incluem heterogeneidade por interação.

O SD basal entre doadores vem dos três coeficientes R por gene, convertidos para log2, com referência zero, centragem por gene e desvio-padrão pooled residual: `0.6445065` log2. A primeira versão com SD arbitrário 0.35 permanece separada como exploratória e não sustenta conclusões.

## Produção (200 réplicas por cenário)

Execução offline nos containers fixados: PyDESeq2 0.5.4 / NumPy 2.4.6 / pandas 2.3.3 / SciPy 1.17.1 (imagem `sha256:ece5e898...c82d23`); DESeq2 1.50.2 / R 4.5.2 / Bioconductor 3.22 (imagem `sha256:f63cb28...ce5ec06`). Foram concluídos 3.200 ajustes PyDESeq2 em 16 cenários (4/8/12/20 pares) e 800 ajustes DESeq2 em quatro cenários (4 pares); nenhum ajuste falhou e cada réplica teve 1.000 genes testáveis. Réplicas, manifests e hashes completos estão em `.artifacts/research/E6/production-python-n{4,8,12,20}/`, `.artifacts/research/E6/production-R-n4/`; agregados finais e manifests de sumarização estão em `.artifacts/research/E6/production-summary-python/summary-final/` e `production-summary-R/summary-certified/`.

Estimativas entre réplicas; MCSE entre parênteses. Em 10% DE, FDP é a fração média de falsos entre rejeições; potência é a fração de genes verdadeiros rejeitados. Tipo I e cobertura Wald são médias por gene. Valores nulos de `fdp_mean` equivalem à frequência de ao menos uma rejeição e não são estimativa de FDR em genes alternativos.

| Engine | Pares | SD interação | FDP (MCSE) | Potência (MCSE) | Tipo I | Cobertura 95% |
|---|---:|---:|---:|---:|---:|---:|
| PyDESeq2 | 4 | 0 | 0,0458 (0,0016) | 0,7982 (0,0028) | 0,0043 | 0,9611 |
| PyDESeq2 | 4 | 0,5 | 0,0707 (0,0025) | 0,5676 (0,0047) | 0,0049 | 0,9464 |
| PyDESeq2 | 8 | 0 | 0,0548 (0,0017) | 0,9133 (0,0021) | 0,0060 | 0,9495 |
| PyDESeq2 | 8 | 0,5 | 0,0817 (0,0020) | 0,8606 (0,0025) | 0,0086 | 0,9390 |
| PyDESeq2 | 12 | 0 | 0,0592 (0,0016) | 0,9548 (0,0014) | 0,0067 | 0,9492 |
| PyDESeq2 | 12 | 0,5 | 0,0805 (0,0020) | 0,9304 (0,0018) | 0,0092 | 0,9355 |
| PyDESeq2 | 20 | 0 | 0,0604 (0,0018) | 0,9874 (0,0008) | 0,0071 | 0,9429 |
| PyDESeq2 | 20 | 0,5 | 0,0770 (0,0019) | 0,9782 (0,0011) | 0,0092 | 0,9401 |
| DESeq2 | 4 | 0 | 0,0393 (0,0015) | 0,7863 (0,0030) | 0,0036 | 0,9600 |
| DESeq2 | 4 | 0,5 | 0,0655 (0,0023) | 0,5475 (0,0043) | 0,0043 | 0,9459 |

Nos cenários sem DE, a taxa de réplicas com pelo menos uma rejeição foi PyDESeq2 n=4/8/12/20: 0,460/0,210/0,125/0,200 (interação 0) e 0,185/0,275/0,235/0,295 (interação 0,5); DESeq2 n=4: 0,295/0,190. Com limites de amostra pequenos e heterogeneidade por doador, esses resultados não demonstram controle da taxa familiar em 0,05. Cada engine sorteou dados independentemente da mesma distribuição; a comparação entre engines é descritiva por cenário, sem pareamento de réplica.

O resumo dos 200 por cenário é a análise de produção principal. A seção de piloto abaixo permanece apenas para comparação histórica.

As primeiras 10 réplicas de cada cenário foram retomadas dos checkpoints do piloto calibrado v2; portanto, as estatísticas do piloto e da produção se sobrepõem e não são replicações independentes. A produção permanece com 200 IDs de réplica únicos por cenário.

## Resultados do piloto calibrado v2 (10 réplicas por cenário)

10 réplicas por cenário, 1.000 genes testáveis por réplica e zero falhas de ajuste. Cada linha resume métricas entre réplicas; MCSE em parênteses. FDP é a fração média de falsos entre rejeições. Cobertura Wald refere-se apenas aos genes com efeito verdadeiro.

| Pares | SD interação | FDP (MCSE) | Potência (MCSE) | Tipo I | Cobertura 95% |
|---:|---:|---:|---:|---:|---:|
| 4 | 0 | 0,042 (0,0049) | 0,802 (0,0128) | 0,0039 | 0,962 |
| 4 | 0,5 | 0,058 (0,0076) | 0,530 (0,0293) | 0,0038 | 0,936 |
| 8 | 0 | 0,052 (0,0098) | 0,908 (0,0073) | 0,0057 | 0,949 |
| 8 | 0,5 | 0,091 (0,0104) | 0,851 (0,0124) | 0,0094 | 0,940 |
| 12 | 0 | 0,047 (0,0078) | 0,953 (0,0078) | 0,0053 | 0,955 |
| 12 | 0,5 | 0,077 (0,0111) | 0,932 (0,0063) | 0,0088 | 0,937 |
| 20 | 0 | 0,073 (0,0062) | 0,990 (0,0033) | 0,0087 | 0,937 |
| 20 | 0,5 | 0,081 (0,0100) | 0,983 (0,0060) | 0,0098 | 0,939 |

Em cenários nulos, como FDR = probabilidade de ao menos uma rejeição, as estimativas PyDESeq2 nos níveis de interação 0/0,5 foram: 4 pares 0,4/0,3; 8 pares 0,2/0,3; 12 pares 0/0,1; 20 pares 0,1/0,4. Com apenas dez réplicas, a incerteza Monte Carlo é grande; os valores não demonstram calibração a 0,05.

DESeq2/R também completou 10 réplicas por cenário de quatro pares: para interação 0/0,5, FDP foi 0,043/0,072, potência 0,762/0,564, tipo I 0,0039/0,0048 e cobertura 0,974/0,950. Cada engine gerou amostras aleatórias independentes da mesma distribuição, portanto a comparação é descritiva em nível de cenário, não um teste pareado réplica a réplica.

## Evidência e limites

Réplicas, resumos e manifests com hashes/imagens do piloto estão em `.artifacts/research/E6/pilot-v2/` e `R-pilot-v2/`; produção está registrada nas pastas acima. Quatro doadores dão incerteza às médias/dispersões e ao SD de efeito basal. Genes simulados independentemente não calibram teste de vias nem fornecem tamanho amostral universal; os resultados não estabelecem tamanho amostral universal nem substituem validação humana.
