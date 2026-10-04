# Bioinformática: planejamento para execução pelo Codex

Data: 04/10/2026. Status: RASCUNHO — somente planejamento; nenhuma implementação realizada.

## 1. Objetivo e conclusão da pesquisa

Construir uma reanálise reproduzível de RNA-seq e transformá-la em uma tarefa científica com avaliação objetiva para agentes de IA.

**Recomendação:** esta é a rota prática mais adequada ao perfil de software do usuário e ao prazo curto. A recomendação é uma inferência de alinhamento técnico, não uma garantia de seleção nem prova de que seja a melhor alternativa em todas as situações.

O anúncio oficial da Turing exige programação científica, análises em várias etapas, soluções de referência, critérios de avaliação e execução em ambientes sem rede. Bioinformática aparece entre as especialidades aceitas [1]. Portanto, somente um notebook de análise cobre parte do objetivo: a tarefa avaliável é o diferencial relevante para essa vaga.

## 2. Especificação do projeto

**Nome sugerido:** airway-rnaseq-agent-task.

**Pergunta:** quais genes apresentam mudança de expressão após dexametasona em células de músculo liso das vias aéreas humanas, considerando o pareamento por doador?

**Dataset:** airway, derivado de GSE52778. Recorte com oito amostras: quatro doadores, cada um com controle e tratamento, sem albuterol. A documentação Bioconductor descreve esse recorte e sua proveniência [2]. O estudo GEO completo contém outros tratamentos; não usar suas 16 amostras como se fossem esse recorte.

**Hipótese de trabalho:** há mudanças de expressão associadas ao tratamento. Relatar os resultados encontrados, inclusive discordâncias; não ajustar métodos para obter uma lista desejada de genes.

**Escopo:** aquisição de contagens e metadados → validação → QC da matriz → análise diferencial → figuras → interpretação → referência independente → tarefa avaliável → reprodução offline.

**Arquitetura:** CLI Python com etapas sequenciais e arquivos locais. Docker para reprodução. Uma referência R/DESeq2 será gerada separadamente para validação; o pipeline principal permanece Python. Não construir serviços, banco de dados ou orquestrador.

**Stack proposta:** Python 3.11, PyDESeq2 0.5.4, pandas, NumPy, SciPy, matplotlib, scikit-learn e pytest. Confirmar compatibilidade e fixar dependências transitivas na primeira etapa. A versão PyDESeq2 é a documentada na fonte consultada [3], não uma instrução para atualizar sempre para a mais recente.

**Ambiente:** Windows com comandos de uso em PowerShell; contêiner Linux via Docker Desktop. Preflight deve verificar Docker disponível e recursos antes de downloads ou instalações demoradas.

## 3. Contratos científicos

- Aquisição preferida: exportar contagens e metadados do objeto `airway` oficial, aproveitando o ambiente R da referência. Exportação única, documentada; não exigir R para executar a CLI Python.
- Atalho permitido: CSVs do workshop [4], fixados em commit imutável, somente após conferir identidade das amostras e igualdade das contagens com o objeto oficial. Não confiar apenas no nome do arquivo.
- Registrar URLs, versões, recorte, data de obtenção, tamanho e SHA-256 dos arquivos em `data/manifest.json`. Conferir termos de reutilização antes de distribuir dados.
- Entrada canônica: `data/counts.csv`, genes nas linhas e oito amostras nas colunas; `data/metadata.csv`, colunas `sample_id`, `donor`, `condition`.
- Condições canônicas: `control` e `treated`. Converter `cell` para `donor` e `dex` para `condition` com mapeamento explícito e auditável.
- Preservar IDs Ensembl; não agregar genes automaticamente por símbolo.
- Rejeitar IDs duplicados, valores ausentes, negativos ou fracionários, amostras sem correspondência e pares incompletos. Reordenar por ID, nunca pela posição original.
- Confirmar proveniência de contagens não normalizadas. TPM/FPKM são proibidos como entrada do modelo; integralidade sozinha não prova que sejam contagens válidas [3,5].
- Pré-filtro fixo: manter genes com pelo menos 10 contagens em pelo menos quatro das oito amostras; registrar quantos foram removidos. A regra segue a orientação de menor grupo na documentação DESeq2 [5].
- Modelo: `~ donor + condition`; contraste explícito tratamento versus controle. Log2FC positivo significa maior expressão no tratamento. Verificar posto completo da matriz de desenho.
- Normalização e estimação pela biblioteca; teste Wald bilateral de mudança diferente de zero, ajuste Benjamini–Hochberg, alpha 0,05. Registrar opções de filtros independentes e tratamento de outliers.
- Critério estatístico: `padj < 0,05`. Destaque exploratório adicional: `abs(log2FC) >= 1`. Esse destaque não equivale a testar formalmente um efeito maior que 1.
- Exportar log2FC sem shrinkage no MVP, claramente rotulado. Valores de p ou padj ausentes devem ter motivo documentado; não convertê-los em zero.
- QC limitado à matriz: totais por amostra, distribuição, PCA e correlações. Não afirmar controle de qualidade de reads, alinhamento ou cobertura, pois FASTQ/BAM não serão processados.
- PCA: log2 de contagens normalizadas + 1, nos até 500 genes de maior variância, com condição e doador identificados. Descrever essa transformação como exploratória, sem chamá-la de VST.
- Figuras: totais por amostra, PCA, volcano e heatmap dos até 20 genes com menor padj válido. Desempate por ID; heatmap com z-score por gene, omitindo variância zero.
- Não excluir amostras por aparência da PCA. Qualquer exclusão exige justificativa documentada e revisão do desenho.
- Interpretação: discutir até três genes com apoio no artigo original e fontes primárias; distinguir resultado, hipótese biológica e limitação. Não fazer inferência clínica.

## 4. Arquivos e responsabilidades previstos

| Arquivo/pasta | Responsabilidade |
| --- | --- |
| `PLANO.md` | Passos, checks, evidências e pendências de execução |
| `MEMORIA.md` | Resumo curto e verificável para retomada pelo agente |
| `ADR.md` | Decisões com contexto, alternativas e consequências |
| `README.md` | Pergunta, execução, resultados, limitações e demonstração |
| `config.json` | Parâmetros científicos fixados acima |
| `requirements.txt` e `requirements.lock.txt` | Dependências diretas e versões resolvidas |
| `src/data.py` | Leitura, alinhamento por ID e validações |
| `src/analysis.py` | Pré-filtro, ajuste do modelo e exportação |
| `src/report.py` | QC, figuras e resumo derivado dos resultados |
| `src/cli.py` | Interface das etapas e mensagens de erro |
| `data/` | Contagens, metadados e manifesto; entradas preservadas |
| `results/` | QC, tabela diferencial, resumo e manifesto de execução |
| `figures/` | Quatro figuras em PNG |
| `reference/` | Exportação e solução R/DESeq2, versões e comparação |
| `benchmark/TASK.md` | Enunciado autossuficiente entregue ao agente |
| `benchmark/RUBRIC.md` e `benchmark/grader.py` | Critérios e correção de arquivos submetidos |
| `benchmark/gold/` | Referência validada, separada dos inputs do participante |
| `tests/` e `tests/fixtures/` | Casos inválidos e fixtures pequenas offline |
| `Dockerfile`, `.dockerignore`, `.gitignore` | Ambiente reproduzível e exclusões |
| `.github/workflows/ci.yml` | Testes rápidos; análise completa somente no fechamento |

Não criar notebook no MVP. Caso necessário depois, ele apenas apresenta saídas; a lógica científica permanece na CLI.

## 5. Execução passo a passo — futuro PLANO.md

Executar uma etapa por vez, na mesma sessão/agente, sem delegação automática. Usar `superpowers:executing-plans` quando disponível. Este documento é o desenho e o rascunho de plano; execução depende de solicitação posterior do usuário.

### Etapa 1 — Preparação e contrato dos dados

- [ ] Ler este plano; verificar diretório, Git e regras locais. Preservar trabalho existente.
- [ ] Verificar Python, Docker e disponibilidade das dependências; fixar versões compatíveis, sem atualização desnecessária.
- [ ] Criar `PLANO.md`, `MEMORIA.md` e `ADR.md` com as regras da seção 6.
- [ ] Obter o recorte airway oficial e exportar contagens/metadados uma única vez; registrar versões e hashes.
- [ ] Confirmar oito IDs SRR, quatro pares e ausência de albuterol pela documentação [2].
- [ ] Check: contagens inteiras não negativas, pares identificados e manifesto completo. Dados não confirmados bloqueiam a análise.

### Etapa 2 — Entrada validada e QC

- [ ] Criar testes de IDs duplicados, amostra ausente, metadados fora de ordem, valor negativo/fracionário e par incompleto.
- [ ] Implementar leitura e validação mínimas para esses contratos; rodar os testes relevantes.
- [ ] Produzir `results/qc.json` e figuras de totais e PCA, com rótulos de doador/condição.
- [ ] Check: permutar a ordem dos metadados preserva os dados alinhados; dados inválidos geram erro claro e saída diferente de zero antes do ajuste.

### Etapa 3 — Modelo diferencial e figuras

- [ ] Testar regra de pré-filtro, orientação do contraste e desenho com doador. Usar fixture com oito amostras e genes suficientes para ajuste; não testar significância em matriz minúscula.
- [ ] Implementar o modelo especificado sem reimplementar DESeq2 ou seus testes estatísticos.
- [ ] Exportar `results/differential_expression.csv`: gene_id, baseMean, log2FoldChange, lfcSE, stat, pvalue, padj e flags dos critérios.
- [ ] Registrar parâmetros, versões, hashes, tempo e memória em `results/run_manifest.json`; gerar `results/summary.json` e as outras duas figuras.
- [ ] Check: saída completa, IDs únicos, probabilidades válidas quando presentes, motivo dos ausentes e direção tratamento/controle explícita.

### Etapa 4 — Validação científica independente

- [ ] Gerar uma referência R/DESeq2 com os mesmos arquivos, genes filtrados, desenho e contraste; sem shrinkage.
- [ ] Fixar e documentar versões/opções das duas implementações. Alinhar normalização, filtros e outliers antes de comparar; não esperar igualdade numérica perfeita.
- [ ] Comparar genes em comum com log2FC finito. Meta de aceitação proposta: Spearman >= 0,95 para log2FC e concordância de sinal >= 95% no conjunto de referência com padj < 0,01 e abs(log2FC) >= 1.
- [ ] Registrar tamanho do conjunto comparável e casos divergentes. Conjunto vazio torna o check inconclusivo; não aprovar automaticamente.
- [ ] Conferir interpretação de até três genes com a publicação original, mantendo IDs/anotação e referências rastreáveis.
- [ ] Check: salvar `reference/comparison.json` e `reference/VALIDATION.md`. Se houver falha, investigar método/dados; não relaxar os limites apenas para passar.
- [ ] Se a referência R não puder ser produzida, entregar status de validação pendente. Não chamar a solução de referência validada nem concluir a etapa 5.

### Etapa 5 — Tarefa científica avaliável

- [ ] Escrever enunciado em inglês: inspecionar dados, reconhecer desenho, escolher método adequado, analisar, diagnosticar problemas e produzir saídas com interpretação e limitações.
- [ ] Entregar apenas dados, descrições e ambiente ao participante; manter solução e gold fora do pacote de entrada. Não usar dados sintéticos como se fossem pesquisa real.
- [ ] Fixar o contrato de submissão: tabela diferencial, `analysis_summary.json`, quatro figuras e `interpretation.md`. No resumo: desenho, contraste, filtro, versões e contagens de genes.
- [ ] Criar rubric de 100 pontos: integridade/proveniência 20; desenho/contraste 25; concordância numérica 25; reprodução/artefatos 15; interpretação/limitações 15.
- [ ] Automatizar os primeiros 85 pontos usando os mesmos checks já definidos; reservar os últimos 15 para revisão humana, com critérios explícitos e sem LLM juiz pago.
- [ ] Considerar submissão aprovada com pelo menos 85 pontos, revisão humana concluída e nenhum erro crítico de dados, pareamento, contraste ou execução offline.
- [ ] Testar solução correta, tabela vazia, submissão só com cabeçalhos, contraste invertido e ausência do ajuste por doador. O grader deve rejeitar falhas críticas, não só conferir arquivos.
- [ ] Check: solução validada aceita; exemplos errados rejeitados pelo motivo esperado. Snapshot próprio testa estabilidade, mas não substitui a referência independente da etapa 4.
- [ ] Rotular como tarefa demonstrativa. Um único dataset conhecido não mede capacidade geral de agentes nem impede memorização se o gold estiver público.

### Etapa 6 — Reprodução, documentação e entrega

- [ ] Preparar imagem e dados com rede; separar aquisição/build da execução científica.
- [ ] Rodar pipeline completo em contêiner novo, rede desativada, diretório de saída vazio e dados de entrada somente leitura.
- [ ] Executar tests offline e grader; comparar tabelas de duas execuções no mesmo ambiente: mesmos IDs/flags e tolerância numérica rtol 1e-6, atol 1e-8, preservando ausentes. Não exigir hashes iguais de figuras ou timestamps.
- [ ] Configurar CI rápida com fixtures locais; realizar análise completa final uma vez após os checks passarem.
- [ ] Revisar figuras visualmente: texto legível, eixos corretos, IDs/rótulos consistentes e ausência de clipping.
- [ ] Escrever README em inglês com execução por PowerShell, preparação online e execução offline, proveniência, métodos, resultados reais, limitações e tempo/memória medidos.
- [ ] Incluir resumo de estudo: contagens versus TPM, replicação biológica, pareamento, log2FC, múltiplos testes, FDR e limites do QC realizado.
- [ ] Registrar uso de IA e o que foi revisado pelo usuário. Não alegar publicação, descoberta nova ou revisão externa inexistente.
- [ ] Consolidar MEMORIA e ADR; salvar evidências dos checks no PLANO. Commits locais por etapa, sem push/publicação automática.
- [ ] Check final: execução offline comprovada, referência independente documentada, testes passando, grader funcionando e usuário capaz de explicar cinco decisões centrais.

## 6. Os três documentos de continuidade

### MEMORIA.md — até 40 linhas

Manter apenas: objetivo atual; dataset/recorte confirmados; conceitos científicos aprendidos; problemas resolvidos; fatos de ambiente úteis; etapa atual; próxima ação e bloqueios reais. Incluir data e caminhos para evidências. Não guardar logs, segredos, histórico de conversa ou resultados ainda não obtidos. Atualizar ao encerrar cada etapa, substituindo informações obsoletas.

### ADR.md — até 6 decisões, cerca de 10 linhas por decisão

Cada decisão contém ID, data, status, contexto, escolha, alternativa descartada e consequência. Decisões propostas: contagens prontas em vez de FASTQ; Python/PyDESeq2 no pipeline e R/DESeq2 na validação; desenho pareado; CLI/arquivos/Docker; tarefa com grader determinístico e revisão humana; política de proveniência/cache/offline. Marcar como propostas até confirmadas na execução; mudanças citam a decisão substituída.

### PLANO.md — checklist e evidências

Usar as seis etapas acima. Marcar checkbox somente com evidência; ao fim de cada etapa, registrar checks executados, resultado, arquivos produzidos e bloqueio/próxima ação. Separar claramente planejamento, implementação concluída e validação pendente. Referenciar MEMORIA e ADR sem duplicar seu conteúdo.

## 7. Economia de tokens e tempo

- Na retomada, ler MEMORIA, a etapa pendente do PLANO e somente ADRs/arquivos relevantes. Não reler todo o repositório.
- Uma análise, um recorte, um contraste e uma tarefa. Sem dashboard, RAG, cloud, treinamento de modelo, enrichment ou segundo dataset no MVP.
- Downloads e exportação uma vez; preservar entradas. Reutilizar ajuste só se hashes dos dados, configuração e versões coincidirem. Ao mudar método/input, invalidar as saídas dependentes.
- Durante desenvolvimento, rodar testes afetados e fixture pequena; análise real após etapa científica e fechamento. Repetir checks aprovados somente por alteração relevante ou falha.
- Referência R tem custo inicial adicional, justificado por validação independente; não repetir sua instalação a cada execução.
- Logs ficam em arquivos. Mensagens ao usuário: avanço, bloqueio e próxima ação; evitar despejar matrizes e stack traces completos.
- Se uma dependência ou origem falhar, fazer uma tentativa orientada pelo erro, registrar bloqueio e ajustar a rota com evidência. Não iniciar ciclos de reinstalação ou pesquisas amplas.
- Não inventar limites de tokens do provedor. A economia vem de escopo, leitura seletiva e reaproveitamento de resultados confirmados.

## 8. Valor para candidatura

Quando concluído, apresentar como **projeto independente de reanálise computacional e avaliação de agentes**, com links e resultados verificáveis. 

## 9. Fontes consultadas

1. [Turing — Agentic Life Science Expert](https://work.turing.com/r/qzScy-BjHO): requisitos e natureza das tarefas avaliáveis.
2. [Bioconductor — airway, documentação do experimento](https://bioconductor.org/packages/release/data/experiment/vignettes/airway/inst/doc/airway.html): amostras, tratamentos, contagens e artigo original.
3. [PyDESeq2 — workflow oficial](https://pydeseq2.readthedocs.io/en/stable/auto_examples/plot_minimal_pydeseq2_pipeline.html): entradas, ajuste e contraste multifatorial.
4. [bioconnector — workshop airway](https://github.com/bioconnector/workshops/blob/master/r-rnaseq-airway.Rmd): possível atalho de distribuição dos CSVs; validar antes de usar.
5. [DESeq2 — documentação oficial](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html): contagens não normalizadas, alinhamento de amostras, desenho e pré-filtro.
6. [EMBL-EBI — Introductory bioinformatics](https://www.ebi.ac.uk/training/online/courses/introductory-bioinformatics-pathway/): material gratuito; estimativa de três horas para o conteúdo principal.
7. [EMBL-EBI — Introduction to RNA-seq and functional interpretation](https://www.ebi.ac.uk/training/materials/introduction-to-rna-seq-materials/): apoio conceitual à análise.

Nenhum dado foi baixado, dependência instalada, código científico escrito ou resultado calculado nesta fase.
