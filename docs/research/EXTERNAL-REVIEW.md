# E1 — pacote para revisão científica externa

**Estado:** pronto para encaminhar por iniciativa do usuário; nenhum revisor foi escolhido ou contatado. Sem respostas ou aprovação registradas.

## Pergunta e escopo

A trilha reanalisa a coorte AIRWAY pareada (quatro doadores) para resposta transcricional a glicocorticoide; compara implementações Python/R, estabilidade por retirada de doador e anotações/conjuntos funcionais. O estudo não testa mecanismo causal e não reivindica descoberta nova. Resultados, configurações e provenance estão em `PROTOCOL.md`, `BASELINE.md`, `PYTHON-R.md`, `ROBUSTNESS.md` e `PATHWAYS.md`.

## Cinco decisões a revisar

1. A unidade experimental e o desenho `~ donor + condition` representam adequadamente o pareamento e os graus de liberdade disponíveis?
2. A comparação de resultados com independent filtering e Cook’s distance ativados/desativados está interpretada corretamente, incluindo `padj` ausente?
3. O diagnóstico das 308 discordâncias PyDESeq2/DESeq2 separa causas demonstradas de diferenças estatísticas ainda não identificadas?
4. A retirada de cada doador, VST/PCA e interpretação dos efeitos descrevem estabilidade sem tratar os folds como replicatas independentes?
5. Mapeamento Ensembl/Entrez, limiares de tamanho GO, CAMERA e sensibilidades GOseq são escolhas defensáveis? Quais conclusões de vias devem ser moderadas?

## Registro da revisão

Preencher somente após contato feito pelo usuário e revisão recebida: nome e qualificação declarados pelo revisor, data, artefatos/versões examinados, respostas a cada questão, limitações apontadas e resposta dos autores. Não inserir dados pessoais ou contato do revisor em artefatos publicáveis sem necessidade/consentimento.

| Campo | Estado |
|---|---|
| Revisor / qualificação declarada | `pending` |
| Data / escopo efetivamente revisado | `pending` |
| Comentários / respostas | `pending` |
| Demonstração individual do usuário | `pending` |

A revisão computacional e os testes locais não substituem esta avaliação científica independente.
