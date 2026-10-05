# Preparação para entrevista

Este projeto é uma reanálise computacional de um conjunto público conhecido e uma tarefa de bioinformática executável em ambiente isolado. Foi desenvolvido com assistência do Codex. Não é uma descoberta nova, estudo clínico nem avaliação de desempenho de um agente independente.

## Cinco respostas curtas

### 1. Por que usar o desenho pareado e o que mudaria sem `donor`?

Cada um dos quatro doadores tem uma amostra controle e uma tratada. O modelo `~ donor + condition` compara as condições controlando diferenças basais entre doadores. Sem `donor`, o modelo ignora esse pareamento e pode estimar de forma diferente a variabilidade e a incerteza do efeito. O desenho tem oito amostras, posto cinco e três graus de liberdade residuais.

### 2. Por que TPM não substitui estas contagens?

O DESeq2/PyDESeq2 modela contagens brutas inteiras e estima fatores de tamanho para comparar as amostras. TPM e FPKM já foram transformados e ajustados por comprimento e composição; não são entradas equivalentes para este modelo. Também verifico no manifesto que os dados fornecidos são contagens brutas.

### 3. Como interpretar log2FC, padj e o destaque?

Log2FC positivo significa maior expressão no tratamento que no controle; +1 equivale a aproximadamente o dobro. `padj < 0,05` é o critério definido após ajuste Benjamini–Hochberg para testes múltiplos. Não significa que cada gene tenha 95% de probabilidade de ser verdadeiro. O destaque adicional `abs(log2FC) >= 1` é exploratório: não é um teste formal de que o efeito ultrapasse esse limiar.

### 4. Qual é a diferença entre reprodução, comparação com R e revisão humana?

Duas execuções Python com resultados idênticos demonstram reprodução nesse ambiente e nesses dados. A comparação com R/DESeq2 confere uma implementação separada: os efeitos tiveram Spearman 0,999994 e as direções coincidiram em 852 genes fortes, mas 308 decisões de significância divergiram. A revisão humana avalia se código, método, figuras e interpretação fazem sentido. Nenhuma dessas evidências, isoladamente, prova uma descoberta biológica.

### 5. Como o runner protege dados e solução de referência?

A submissão executa em Docker sem rede e como usuário não privilegiado, com sistema de arquivos raiz, entradas e código somente leitura, limites de recursos e sem socket Docker. O gold e o avaliador ficam fora do contêiner. O avaliador registra recibos e hashes fora da saída que a submissão pode escrever.

## Roteiro de demonstração

1. Mostre `config.json`, `data/manifest.json` e a fórmula/contraste.
2. Execute os comandos do README e explique o escopo de cada figura. QC é da matriz de contagens; não houve análise de FASTQ, alinhamentos ou cobertura.
3. Mostre a tabela da comparação Python/R e explique as 308 divergências sem atribuí-las todas a uma causa já comprovada.
4. Mostre a reprovação das execuções com contraste invertido e sem pareamento, mais o teste de falha/isolamento.
5. Diga explicitamente que a tarefa usa um conjunto conhecido e que a execução correta é uma verificação do avaliador, não uma medição de capacidade geral de um agente.

## Frase defensável para currículo

> Desenvolvi, com assistência de IA, uma reanálise pareada de RNA-seq com PyDESeq2, comparação computacional com R/DESeq2 e uma tarefa científica offline com execução Docker isolada, critérios determinísticos e testes adversariais.

Acrescente “revisão humana” ou “domínio demonstrado” apenas depois de realizar e documentar essas etapas.