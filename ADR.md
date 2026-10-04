# Decisões arquiteturais

## ADR-01 — Contagens prontas (aceita, 2026-10-04)
Contexto: foco em análise e avaliação reproduzível.
Escolha: objeto airway oficial; nenhum processamento FASTQ/BAM.
Alternativa: refazer alinhamento, com recursos e escopo maiores.
Consequência: QC restrito à matriz; preservar proveniência e anotação histórica.

## ADR-02 — Python e referência R (aceita, 2026-10-04)
Escolha: PyDESeq2 0.5.4 na CLI; DESeq2 em imagem separada.
Alternativa: um único backend, sem confronto entre implementações.
Consequência: versões e opções explícitas; concordância não prova independência conceitual dos métodos.

## ADR-03 — Modelo pareado (aceita, 2026-10-04)
Escolha: ~ donor + condition; treated/control, quatro pares.
Alternativa: ignorar doador, confundindo a variabilidade biológica.
Consequência: exigir posto completo, oito amostras e pares íntegros.

## ADR-04 — CLI e arquivos (aceita, 2026-10-04)
Escolha: Python, arquivos locais e Docker, sem API, banco ou frontend.
Alternativa: aplicação web, desnecessária para a pergunta científica.
Consequência: interface reproduzível; diretórios de saída exclusivos.

## ADR-05 — Avaliação demonstrativa (aceita, 2026-10-04)
Escolha: runner offline, grader determinístico de 85 pontos e revisão humana de 15.
Alternativa: LLM juiz ou avaliação apenas por declarações do participante.
Consequência: separar gold; artefatos não provam por si só autoria nem método; revisão do código permanece necessária.

## ADR-06 — Preparação online e execução offline (aceita, 2026-10-04)
Escolha: adquirir e fixar imagens/dados uma vez, executar sem rede.
Alternativa: downloads durante a análise.
Consequência: registrar hashes, versões e imagem; validar termos antes de redistribuir dados.
