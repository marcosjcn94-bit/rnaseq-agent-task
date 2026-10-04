# Revisão técnica do executor — 2026-10-04

Revisão separada da implementação, feita pelo mesmo agente conforme o plano de execução única. Não constitui revisão externa ou independente de software.

Conferidos: alinhamento com a especificação, desenho/contraste, propagação de warnings, validação antes do ajuste, integridade dos dados, isolamento dos mounts/gold, recibos fora das saídas, limites, tratamento de falhas, documentação, licenças e testes relevantes.

Correções provenientes da revisão:
- preservar nomes de índices e evitar ambiguidade entre índice e coluna gene_id;
- preservar hashes no checkout Windows com .gitattributes;
- registrar warnings científicos em vez de descartá-los;
- tratar correlação/PCA indefinida em matriz constante;
- rejeitar symlinks e limitar volume de saída do participante;
- vincular gold ao hash da tabela validada e conferir seus artefatos;
- conferir hashes da tabela/resumo antes de preparar gold;
- verificar CLI do runner, saída não zero e falhas reais em Docker.

Evidências: 46 testes offline no equivalente local da CI; pip check sem inconsistências; duas tabelas Python idênticas; referência R repetida na imagem com lock; ensaios correto/invertido/sem doador/falha; quatro figuras inspecionadas; diff --check e busca por placeholders/segredos sem achados.

Limites reconhecidos: R/Python não produzem estatísticas idênticas; ambiente R verifica versões mas não restaura automaticamente tarballs antigos; imagem Docker oferece isolamento básico; dados conhecidos permitem memorização; flags de revisão humana não provam identidade do revisor e devem ser preenchidas pelo avaliador responsável.

Fora do escopo, por regra explícita do plano: frontend/API/banco/cloud, FASTQ/BAM, enrichment, segundo dataset, treinamento e revisão por subagentes. CI remota e publicação dependem do push autorizado. Capacidade do usuário para explicar as decisões depende do ensaio humano.
