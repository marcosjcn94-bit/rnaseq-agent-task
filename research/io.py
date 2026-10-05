"""Safe, deterministic research-run output writer."""
import hashlib
import json
from pathlib import Path

import pandas as pd


def _json_safe(value):
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if hasattr(value, "item"):
        return _json_safe(value.item())
    if pd.isna(value):
        return None
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"unsupported manifest value: {type(value).__name__}")


def write_run(output: Path, tables: dict[str, pd.DataFrame], info: dict) -> None:
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise FileExistsError(f"output directory is not empty: {output}")
    if not tables or any(not name.replace("_", "").isalnum() for name in tables):
        raise ValueError("tables must have safe, non-empty names")
    hashes = {}
    try:
        for name, frame in tables.items():
            if not isinstance(frame, pd.DataFrame):
                raise TypeError(f"table {name} is not a DataFrame")
            path = output / f"{name}.csv"
            frame.to_csv(path, index=True, na_rep="")
            hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest = {**info, "status": "complete", "output_sha256": hashes}
        (output / "manifest.json").write_text(
            json.dumps(_json_safe(manifest), indent=2, sort_keys=True, allow_nan=False) + "\n",
            encoding="utf-8",
        )
    except Exception:
        (output / "failure.log").write_text("run output incomplete; inspect container logs\n", encoding="utf-8")
        raise
