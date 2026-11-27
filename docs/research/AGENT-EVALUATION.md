# E7 — Evaluation of reasoning tasks

The suite contains 12 synthetic cases in four families: alignment and pairing, confounding, diagnosis of discrepancies and missing values, and functional interpretation. Each family has training, validation, and held-out cases. Prompts are in `research/tasks/participant/`. Answer keys and rubrics are in `research/tasks/evaluator/` and are loaded exclusively by the evaluator. The grader checks structured fields. The runner records an attempt only when it receives a real response, the agent identity, and the prompt hash. It rejects overwrites.

No agent attempts were run or scored during this session. The accessible configuration had no ready local agent or API, and the session used no paid services. These cases are initial fixtures. A held-out evaluation with new parameters still requires freezing the agent and prompt first. Human review of the rubrics’ semantic adequacy is pending.
