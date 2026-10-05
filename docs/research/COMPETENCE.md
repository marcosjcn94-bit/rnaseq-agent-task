# Guia de conceitos e exercícios de prática

Material para estudo; não é avaliação da proficiência pessoal do usuário.

## Conceitos para explicar com as próprias palavras

- Em desenho pareado, doador é a unidade experimental; as duas condições do mesmo doador são dependentes. Pareamento reduz variação entre doadores, mas não cria novas unidades independentes.
- Se lote e condição forem perfeitamente confundidos, não há informação no desenho para separar seus efeitos. Não se deve reportar coeficiente causal identificável.
- Para binomial negativa, `Var(Y)=mu + alpha*mu²`; dispersão `alpha` descreve variação extra Poisson, enquanto erro-padrão mede incerteza de um estimador sob o modelo.
- Wald avalia estimativa/erro-padrão sob aproximação assintótica. BH controla FDR do procedimento em condições apropriadas; `padj` não é probabilidade posterior de um gene ser falso.
- `padj=NA` pode resultar de filtro independente ou estimativa/teste indisponível, conforme método. Deve-se guardar o motivo.
- MLE não encolhido serve à inferência especificada; shrinkage estabiliza estimativas de efeito e não deve ser confundido com SE/CI MLE.
- Correlação ou enriquecimento funcional não demonstra mecanismo causal nem benefício clínico.

## Exercício A — pares embaralhados

Use `research/tasks/practice/paired-shuffled.json`. Identifique os pares e descreva uma validação que alinha contagens por `sample_id`, mesmo quando a ordem difere. Explique qual erro ocorreria ao confiar apenas na posição das colunas.

## Exercício B — confundimento perfeito

Use `research/tasks/practice/confounded-batch.json`. Escreva a matriz de desenho conceitual e explique por que condição e lote não são separáveis. Resposta esperada: efeito não identificável; não fabricar coeficiente nem p-valor.

## Decisões para uma revisão externa futura

1. Adequação da unidade experimental e do desenho pareado.
2. Interpretação do `padj=NA` e dos filtros.
3. Comparabilidade dos efeitos Python/R e escala log2.
4. Adequação do universo e dos métodos de vias.
5. Limites da validação contextual externa e da linguagem causal.

Revisor, qualificação, data e respostas só serão registrados quando a revisão acontecer.
