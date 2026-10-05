# E7 — avaliação de tarefas de raciocínio

A suíte contém 12 casos sintéticos em quatro famílias: alinhamento/pareamento, confundimento, diagnóstico de discordância/NA e interpretação funcional. Cada família separa treino, validação e reservado. Enunciados estão em `research/tasks/participant/`; gabaritos e rubricas em `research/tasks/evaluator/`, carregados apenas pelo avaliador. O grader verifica campos estruturados; o runner só registra tentativa quando resposta real, agente e hash do prompt são fornecidos, e recusa sobrescrita.

Estado da medição: nenhuma tentativa de agente foi executada nem pontuada nesta sessão. Não há agente/API local pronto na configuração acessível, e não foram usados serviços pagos. Casos são fixtures iniciais, não teste reservado com novos parâmetros após congelamento de agente/prompt. Revisão humana da adequação semântica das rubricas permanece pendente.
