# Execução — rnaseq-agent-task

Escopo aprovado: opção 3, sem prazo; execução local por um agente, sem publicação automática. A especificação original PLANO-BIOINFORMATICA.md foi preservada como documento de planejamento; este arquivo registra o estado atual.

- [x] 1. Ambiente, contratos, dados oficiais e proveniência.
- [x] 2. Validação de entrada e QC bruto.
- [x] 3. Modelo pareado, QC normalizado, figuras e manifestos.
- [x] 4. Referência R/DESeq2 e revisão científica computacional.
- [x] 5. Tarefa, runner offline, grader e ensaio adversarial.
- [x] 6. Reprodução, CI configurada/testada localmente, documentação e preparação para entrevista.
- [ ] Revisão científica humana identificada e pontuação dos 15 pontos humanos.
- [ ] Ensaio do usuário: explicar cinco decisões centrais.
- [ ] Publicação autorizada e execução da CI no GitHub.

## Ajustes executados

PCA após normalização; submissão executável; gold isolado; cobertura completa; parâmetros explícitos; duas execuções finais; saídas em diretórios exclusivos. analysis_summary.json substitui summary.json; figuras ficam em cada execução/figures para evitar sobrescrita. Contratos em src/contracts.py; comparação em src/compare.py; gold/runner separados. Os três documentos de continuidade permanecem versionados.

## Evidências por etapa — 2026-10-04

1. GitHub público e vazio, ADMIN autenticado; Docker Engine Linux 29.8.1. Python/R com versões fixas; imagem R verifica todo packages.lock.csv. Exportação do objeto airway 1.30.0: 63.677 genes, oito amostras, quatro pares, sem albuterol. SHA-256 e fontes em data/manifest.json. Commit de preparação dad52a8.
2. Rejeição de IDs duplicados, amostra ausente, metadados incompatíveis, contagens negativas/fracionárias/ausentes, biblioteca zerada, pares incompletos e proveniência TPM. Permutar metadados preserva alinhamento. Fixtures e integração validam erro antes do ajuste.
3. 16.139 genes retidos; 3.879 significativos (2.104 up / 1.775 down); 957 destaques exploratórios. Desenho posto cinco, três graus de liberdade; warning registrado. Quatro figuras e manifestos em results/run-1. Código/modelo e QC validados por testes.
4. R/DESeq2 1.50.2: 4.081 significativos; repetição na imagem com lock reproduziu o hash da tabela inicial. Spearman LFC .9999944; sinais 100% em 852 genes fortes. Gate passou. 308 divergências de classificação e 313 padj ausentes em R preservados. Inspeção de fonte confirmou caminhos distintos de estimação da variância da dispersão com graus de liberdade <=3; contribuição não quantificada. reference/VALIDATION.md, comparison.json e evidence/scientific-audit.json.
5. Correto: 85/85 automáticos, execução verificada, revisão humana pendente. Modelos reais sem doador/invertido: rejeitados (50/60 pontos). Cabeçalho vazio e outras falhas em fixtures. Probe Docker comprovou ausência de rede, entradas/código/root somente leitura e recibo de falha para erro intencional. Imagem sem solução, grader/gold/socket. benchmark/REHEARSAL.md e evidence/.
6. Duas execuções Python, mesma imagem congelada: 122,29 / 129,84 s; RSS do processo pai 327,03 / 329,90 MiB, exclui workers. Tabelas idênticas, tolerância aceita 1e-6/1e-8. Clone com core.autocrlf=true preservou hashes de counts/metadata/manifest. 46 testes offline passaram (76,39 s); pip check passou. Figuras revisadas visualmente. CI rápida com action fixada por SHA configurada; execução remota ainda não realizada. README inglês, interpretação e roteiro de entrevista entregues. Revisão de software do próprio executor em docs/SELF-REVIEW.md.

## Decisões de execução

Usar pasta dedicada e branch implementation em vez de outro worktree: repositório novo, sem trabalho concorrente. Manter PLANO/MEMORIA como ledger conforme especificação. Não delegar; revisão de software pelo executor, referência estatística em implementação R separada. Ferramentas/skills: executing-plans, TDD, debugging e verificação; Context7 consultado, priorizando documentação versionada e código instalado. MCP não é dependência da execução.

## Pendências humanas e publicação

HUMAN_REVIEW.json está incompleto; nenhum ponto humano foi atribuído. docs/INTERVIEW.md prepara o ensaio, sem alegar domínio demonstrado. Publicação não executada: especificação determina “Commits locais por etapa, sem push/publicação automática.” Sem bloqueio técnico local confirmado.
