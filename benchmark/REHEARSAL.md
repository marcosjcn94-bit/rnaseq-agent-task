# Evaluator rehearsal

Local executions on 2026-10-04 using the fixed participant image and evaluator-owned receipts. The submission is a copy of this project's reference implementation; these are validation experiments, not independent AI-agent performance measurements.

| Case | Execution | Automatic points | Decision |
|---|---|---:|---|
| Correct paired solution | Offline success, source unchanged | 85/85 | Pending human review |
| Actual model without donor | Offline success | 50/85 | Rejected: summary/count inconsistency and numeric mismatch |
| Actual reversed contrast | Offline success | 60/85 | Rejected: log2FC and Wald-statistic mismatch |
| Intentional runtime failure | Nonzero exit | Not scored | Failed execution receipt; no success claim |

The two wrong implementations kept the correct design/contrast declarations in their summaries. Grading their actual numerical outputs still rejected them. Source review is required because declarations and output equality alone cannot prove the submitted method.

Fixture tests additionally reject header-only/empty tables, missing/duplicate IDs, invalid probabilities/infinities, inconsistent flags, missing genes, incorrect provenance, forged participant execution claims and changed gold artifacts. See evidence/tests.log (46 passing tests).

The failure probe confirmed:
- raw inputs, source and root paths reject writes;
- an outbound socket cannot connect with network none;
- Docker socket is absent;
- evaluator reports intentional failure with nonzero exit, rather than success.

The participant-image inspection confirmed no solution module, grading code or gold. Actual Docker receipts record network mode, read-only root, source/output hashes, image ID and mounts. New receipts also include runtime user and resource limits. Receipts/logs remain outside participant mounts.

See evidence/grade-*.json, receipt-*.json, participant-isolation.json and isolation-failure.log. Participant source is mounted read-only; no evaluator workspace or host Docker socket is mounted there. Full local submission outputs are under results/ and are ignored by Git.

No human points were awarded; HUMAN_REVIEW.json remains incomplete. Approval and scientific source review require an identified human reviewer.
