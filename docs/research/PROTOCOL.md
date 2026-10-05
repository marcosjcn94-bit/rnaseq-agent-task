# Protocolo de pesquisa v1

Congelado em 2026-10-05 antes dos cálculos de extensão. Resultados novos serão exploratórios até revisão e reprodução. Mudança de endpoints, universo ou método exige protocolo versionado novo e justificativa; não altera retrospectivamente resultados vistos.

## Base e estimando

- Dados oficiais de contagem do pacote `airway`; unidade experimental = doador, quatro pares controle/tratado, oito amostras.
- Contraste tratado/controle, desenho `~ donor + condition`, contagens brutas, filtro baseline `>=10` em `>=4` amostras, teste Wald de LFC zero, BH, alfa 0,05 e estimativas MLE sem shrinkage.
- Não interpretar expressão diferencial como causalidade clínica ou mecanismo. Ausência de `padj` conserva seu motivo; não a converter em não significativo conhecido.
- Reproduzir baseline dentro da mesma implementação: IDs/flags/ausências idênticos e tolerância numérica `rtol=1e-6, atol=1e-8`. Não impor igualdade Python/R.

## Endpoints fixados

- E2: comparar parâmetros/intermediários e classificações em universo unido por Ensembl; separar filtragem independente e Cook em contrastes isolados. Relatar concordância e discordância, sem meta de reduzi-las.
- E3: baseline e quatro folds de pares; universo principal fixo de genes baseline. Estabilidade exploratória de genes com `abs(LFC)>=1`: todos os folds estimáveis, sinal constante e desvio máximo `<=0,5`; sensibilidade dos limites 0,25 e 1,0.
- E4: GO Biological Process versionado; CAMERA direcional após limma-voom, `inter.gene.cor=NA`, `allow.neg.cor=FALSE`; sensibilidade única com correlação 0,01. ORA e GOseq ficam como análises secundárias com universo elegível declarado.
- E5: endpoints prévios CRISPLD2, DUSP1 e KLF15 (direção positiva); estimativas e IC95%, cobertura e efeitos no universo comum são contextuais. Classificar compatibilidade antes do teste; não igualar plataformas/drogas nem exigir apenas FDR <0,05.
- E6: semente inicial 20261005; 16 cenários definidos no plano. Dez réplicas são piloto; 200 por cenário é alvo de produção após medição. Informar incerteza Monte Carlo, testabilidade e falhas.
- E7: quatro famílias e tentativas congeladas antes de avaliar teste reservado. Sem acesso do participante ao gold; sem chamadas pagas. Medição pendente quando não houver agente disponível.

## Integridade e execução

Entradas/código somente leitura no container; saídas em diretório vazio próprio, inicialmente `.artifacts/research/`; limites planejados por ajuste: 2 CPUs, 4 GiB, 30 min. Esses limites não foram medidos/aplicados nesta sessão por indisponibilidade do Docker. Nada aqui declara análises executadas.
