# Extensão AIRWAY — relatório de execução

Data: 2026-10-05. Este relatório reúne evidência computacional local das etapas E0–E8. Baseline, entradas originais, gold e alterações anteriores permanecem preservadas.

## Resultados

- E0 reproduziu a implementação de referência dentro da tolerância congelada; ver [BASELINE.md](BASELINE.md) e [PROTOCOL.md](PROTOCOL.md).
- E2 descreve 308 discordâncias entre PyDESeq2 e DESeq2; a causa integral não foi resolvida. E3 avalia estabilidade por retirada de doador, sem tratar folds como coortes independentes. Ver [PYTHON-R.md](PYTHON-R.md) e [ROBUSTNESS.md](ROBUSTNESS.md).
- E4 completou anotação e testes de CAMERA/ORA/GOseq; interpretação permanece condicionada às escolhas e aos graus de liberdade baixos. Ver [PATHWAYS.md](PATHWAYS.md).
- E5 foi classificada `insufficient_metadata`; nenhum contraste externo foi ajustado. Ver [EXTERNAL-PROTOCOL.md](EXTERNAL-PROTOCOL.md).
- E6 completou produção: 3.200 réplicas PyDESeq2 (16 cenários) e 800 DESeq2 (quatro cenários n=4), 200 por cenário, sem falhas e com manifests/hashes. Os motores geraram datasets independentes; comparação entre engines é descritiva. Ver [SIMULATION.md](SIMULATION.md).
- E7 entrega 12 tarefas sintéticas com fixtures/rubricas separadas; nenhuma tentativa de agente foi executada ou pontuada.

## Limites e pendências

Quatro doadores limitam precisão e generalização. Associações não demonstram causalidade. E5 não permite inferência externa sem metadados por amostra que resolvam os estímulos. Demonstração individual, revisão científica externa, interpretação humana das vias e validação das rubricas não ocorreram; nenhuma tentativa real de agente foi simulada ou pontuada. CI foi validado apenas localmente; não houve execução remota. Não houve publicação, mensagem, chamada paga ou push.
