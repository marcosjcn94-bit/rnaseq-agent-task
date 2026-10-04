# Continuidade — 2026-10-04
Objetivo: reanálise airway reproduzível e tarefa científica avaliável.
Escopo aprovado: opção 3, sem prazo; um agente; sem push automático.
Estado: MVP local implementado e validado; publicação/revisão humana/ensaio do usuário pendentes.
GitHub: marcosjcn94-bit/rnaseq-agent-task, público, acesso ADMIN verificado.
Git: branch implementation; preparação dad52a8, implementação 18c2da5.
Dataset: airway 1.30.0 oficial, 63.677 genes, oito amostras, quatro pares, sem albuterol.
Método: PyDESeq2 0.5.4, ~ donor + condition, tratado/controle, parâmetros em config.json.
Retidos: 16.139; significativos Python 3.879 (up 2.104 / down 1.775); destaque 957.
Referência: R 4.5.2 / DESeq2 1.50.2; 4.081 significativos.
Gate: Spearman LFC .9999944; sinal 100% em 852 genes fortes; passou.
Limite: 308 classificações divergentes; 313 padj ausentes em R; resultados não idênticos.
Diferença de algoritmo de dispersão em graus de liberdade <=3 confirmada; contribuição não quantificada.
Reprodução: duas tabelas Python idênticas; 122,29/129,84 s; pai 327,03/329,90 MiB.
46 testes offline passaram; pip check passou; hashes preservados em checkout Windows.
Runner: offline, não-root, root/input/source RO, 2 CPU/4 GiB/128 pids/30 min, gold separado.
Ensaio: correto 85 automáticos pendente humano; sem doador/invertido rejeitados; falha intencional detectada.
Problemas resolvidos: índices pandas, JSON com NaN, warnings, newline/hash Windows e integridade do gold.
Imagens locais: rnaseq-pipeline:validated (ciência congelada), rnaseq-ci:verified (testes finais), rnaseq-participant:validated, rnaseq-reference:validated.
Saídas completas locais: results/run-1, run-2, submission-*; gold em benchmark/gold, todos ignorados por Git.
Evidências publicáveis: evidence/, reference/comparison.json, reference/VALIDATION.md, benchmark/REHEARSAL.md.
Skills de execução/testes/verificação usadas; MCP não é necessário para runtime.
Próxima ação: autorização para publicação; depois CI remota, revisão humana e ensaio de cinco perguntas.
Consultar PLANO.md, ADR.md, README.md e docs/INTERVIEW.md; não repetir aquisição/instalação sem necessidade.
