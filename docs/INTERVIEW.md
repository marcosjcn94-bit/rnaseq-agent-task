# Preparação para entrevista

O projeto reanalisa um experimento público e constrói uma tarefa executável com correção objetiva. Não houve descoberta nova, estudo clínico ou avaliação de um agente desconhecido.

## Conceitos para explicar

- Contagens versus TPM: o modelo usa contagens inteiras não normalizadas e estima fatores de tamanho. TPM/FPKM já transformam os dados e não são entradas equivalentes.
- Replicação biológica: são quatro doadores, cada um com duas condições; oito amostras não significam oito doadores independentes.
- Pareamento: ~ donor + condition controla diferenças basais entre doadores e estima o efeito do tratamento dentro desse desenho. A matriz tem posto cinco e três graus de liberdade residuais.
- Log2FC: positivo significa maior expressão no tratamento. +1 corresponde a aproximadamente duas vezes; os efeitos exportados não têm shrinkage.
- Múltiplos testes: BH controla FDR sob suas condições; padj<.05 não significa 95% de probabilidade de um gene ser verdadeiro, nem garante que cada gene tenha 5% de chance de erro.
- QC: analisamos a matriz de contagens, não reads, alinhamentos ou cobertura. A PCA usa log2 de contagens normalizadas+1 e é exploratória.
- Validação: duas execuções Python verificam reprodução; R fornece uma implementação independente. A concordância de efeitos não elimina diferenças nos testes.
- Avaliação: 85 pontos automáticos verificam saídas. Revisão humana inspeciona código, figuras e afirmações. O exemplo conhecido pode ser memorizado.
- Docker: a preparação usa rede; a execução tem rede desativada, limites de recursos e entradas somente leitura. Gold e avaliador nunca entram no contêiner do participante.

## Ensaio de cinco perguntas

1. Por que usar o desenho pareado e o que mudaria ao retirar donor?
2. Por que TPM não serve como substituto para essas contagens?
3. Como interpretar log2FC, padj e o destaque abs(log2FC)>=1?
4. Como você distingue reprodução Python, concordância com R e revisão científica humana?
5. Como o runner impede que uma submissão altere os inputs ou receba o gold?

Responda em voz alta, em até dois minutos por pergunta. Abra config.json, data/manifest.json, reference/comparison.json e benchmark/runner.py como evidências. Explique também por que não adicionou API, banco ou cloud: a tarefa é uma análise em arquivos, sem necessidade de serviço.

## Demonstração prática

Execute os comandos do README, mostre os quatro gráficos e explique uma limitação de cada um. Mostre a reprovação de contraste invertido e de modelo sem doador no ensaio. Apresente as 308 divergências de classificação entre R/Python sem ocultá-las.

Texto defensável para currículo: “Desenvolvi, com assistência de IA, uma reanálise pareada de RNA-seq com PyDESeq2, validação independente em R/DESeq2 e uma tarefa científica offline com runner Docker, testes de falhas e grader determinístico.”

A revisão humana e sua capacidade de explicar essas decisões ainda precisam ser demonstradas. Não afirmar que já foram concluídas.
