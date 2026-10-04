"""Verify the local or freshly cloned evidence bundle using only the standard library."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
index=json.loads((root/"evidence/index.json").read_text(encoding="utf-8"))
for name,expected in index["files"].items():
    assert digest(root/"evidence"/name)==expected, f"evidence hash mismatch: {name}"
manifest=json.loads((root/"data/manifest.json").read_text(encoding="utf-8"))
for name,entry in manifest["files"].items():
    assert digest(root/"data"/name)==entry["sha256"], f"input hash mismatch: {name}"
run=json.loads((root/"evidence/run-1.json").read_text(encoding="utf-8"))
for name,expected in run["code_hashes"].items():
    assert digest(root/"src"/name)==expected, f"scientific source hash mismatch: {name}"
print("All input, scientific source and evidence hashes verified")
