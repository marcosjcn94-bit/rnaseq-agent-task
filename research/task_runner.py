"""Record explicitly supplied attempts; never fabricate agent runs."""
import json
from datetime import datetime, timezone
from pathlib import Path

def record_attempt(task_id: str, agent: str, prompt_sha256: str, response: str, output: Path):
    if not agent.strip() or not prompt_sha256 or not response.strip():
        raise ValueError("agent, prompt hash and response are required")
    output = Path(output)
    if output.exists():
        raise ValueError("attempt output already exists")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"task_id":task_id,"agent":agent,"prompt_sha256":prompt_sha256,
        "response":response,"recorded_at_utc":datetime.now(timezone.utc).isoformat()},indent=2)+"\n",encoding="utf-8")
