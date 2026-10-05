"""Deterministic rubric grader; protected answer keys stay outside participant tasks."""
from __future__ import annotations
import json
from pathlib import Path

def grade(task: dict, answer: dict) -> dict:
    required = task["rubric"]["required"]
    forbidden = task["rubric"]["forbidden"]
    missing = sorted(k for k, v in required.items() if answer.get(k) != v)
    violations = sorted(k for k, v in forbidden.items() if answer.get(k) == v)
    return {"task_id": task["id"], "score": len(required)-len(missing)-len(violations),
            "max_score": len(required), "missing": missing, "violations": violations,
            "pass": not missing and not violations}

def load_tasks(root: Path):
    participant, keys = root / "participant", root / "evaluator"
    prompts = {p.stem: json.loads(p.read_text(encoding="utf-8-sig")) for p in participant.glob("*.json")}
    solutions = {p.stem: json.loads(p.read_text(encoding="utf-8-sig")) for p in keys.glob("*.json")}
    if not prompts or prompts.keys() != solutions.keys():
        raise ValueError("participant prompts and evaluator keys must match")
    if any("rubric" in task or "solution" in task for task in prompts.values()):
        raise ValueError("protected evaluator material leaked into participant tasks")
    return prompts, solutions
