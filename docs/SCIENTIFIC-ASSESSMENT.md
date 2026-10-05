# Avaliação científica e caminhos para fortalecer o estudo

## O que este projeto sustenta

O projeto demonstra uma reanálise computacional auditável de oito amostras de músculo liso das vias aéreas, em quatro pares controle/tratamento, usando contagens oficiais do objeto airway. Valida proveniência e entradas, ajusta o modelo pareado `~ donor + condition`, gera QC da matriz, compara PyDESeq2 com DESeq2 em R, testa reprodução e falhas e avalia saídas de uma tarefa em Docker.

Duas execuções Python tiveram tabelas idênticas. Em 16.139 genes, a comparação Python/R encontrou correlação de Spearman de 0,999994 nos log2FC e coincidência de direção em 852 genes fortes. Contudo, 308 classificações por `padj < 0,05` diferiram; a referência R deixou 313 valores padj ausentes por filtragem independente. Uma inspeção do código das bibliotecas identificou diferenças nos caminhos de estimação da dispersão em baixa quantidade de graus de liberdade, mas não quantificou seu impacto. Logo, a correlação dos efeitos não implica equivalência dos testes.

O artigo original analisou quatro doadores e relatou variabilidade entre eles, contexto compatível com a cautela desta reanálise. Também descreve os doadores como homens brancos sem doença crônica; não extrapolar estes resultados para todas as pessoas ou para pacientes com asma. O trabalho original inclui experimentos funcionais para CRISPLD2 que não podem ser inferidos da matriz fornecida. [Himes et al. (2014), PLOS ONE](https://doi.org/10.1371/journal.pone.0099625).

## Avaliação para portfólio

**É um projeto de portfólio forte para demonstrar engenharia científica aplicada.** A proveniência, o pareamento, o cross-check com R, as divergências preservadas, a reprodutibilidade e o runner isolado mostram mais do que um notebook isolado.

**Não prova por si só experiência ampla em pesquisa de ciências da vida.** O conjunto tem apenas quatro doadores e não é uma coorte independente. Reproduzir uma análise tampouco demonstra que o autor consegue formular, interpretar e defender decisões científicas sem ajuda. Uma conversa ou teste técnico continua sendo importante.

A cautela sobre amostra pequena é coerente com um estudo de replicabilidade que analisou 18 mil reamostragens de 18 datasets e encontrou que coortes pequenas podem ter baixa replicabilidade de genes diferencialmente expressos e vias. Esse resultado geral não fornece uma taxa de replicação específica para estes dados. [Degen e Medo (2025), PLOS Computational Biology](https://doi.org/10.1371/journal.pcbi.1011630).

## Próximas extensões, por prioridade

1. **Sensibilidade aos doadores:** retirar um par por vez e reajustar; comparar efeitos, direções, intervalos e classificações. Rotular como análise de sensibilidade, pois cada rodada reduz ainda mais a amostra.
2. **Caracterizar a diferença Python/R:** medir máscaras de filtragem e dispersões gene a gene e testar mudanças de uma opção por vez. Não atribuir os 308 casos a uma causa sem decomposição verificável nem calibrar uma implementação para imitar a outra.
3. **Replicação em dados independentes:** localizar uma coorte pública de desenho e tecido compatíveis, declarar a hipótese antes de olhar os resultados e documentar as diferenças de plataforma, protocolo, dose e população. Um dataset inadequado não deve ser tratado como validação só por medir expressão.
4. **Interpretação funcional:** acrescentar análise de vias com universo de fundo, identificadores e versão de anotação explícitos, correção para testes múltiplos e análise de viés de seleção/comprimento. Métodos simples de enriquecimento podem favorecer genes longos ou muito expressos; GOseq foi desenvolvido para corrigir vieses de comprimento em RNA-seq. [Young et al. (2010), Genome Biology](https://doi.org/10.1186/gb-2010-11-2-r14).

As extensões aumentam o valor científico se responderem perguntas explícitas e tratarem vieses. Adicionar complexidade sem novos dados ou uma hipótese melhor não cria evidência nova.