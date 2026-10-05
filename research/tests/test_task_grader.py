import json
from pathlib import Path
from research.task_grader import grade, load_tasks

def test_tasks_are_separated_and_keys_not_in_prompts():
    prompts, keys = load_tasks(Path("research/tasks"))
    assert len(prompts) == len(keys) == 12
    assert {x["family"] for x in prompts.values()} == {"alignment", "confounding", "diagnostics", "functional"}
    for key in keys.values():
        assert grade(key, key["answer_key"])["pass"]
    for prompt in prompts.values():
        assert "solution" not in json.dumps(prompt).lower()

def test_wrong_contrast_is_detected():
    task={"id":"x","rubric":{"required":{"contrast":"treated/control"},"forbidden":{}}}
    assert not grade(task,{"contrast":"control/treated"})["pass"]
