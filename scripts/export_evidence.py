"""Collect measured local evidence without publishing full result matrices or gold."""
import json
from pathlib import Path
import shutil
from src.contracts import sha256, write_json

root=Path(__file__).resolve().parents[1]
out=root/"evidence"
out.mkdir(exist_ok=True)
items={
    "results/run-1/run_manifest.json":"run-1.json",
    "results/run-2/run_manifest.json":"run-2.json",
    "results/run-1/analysis_summary.json":"analysis-summary.json",
    "results/run-1/qc.json":"qc.json",
    ".artifacts/reproduction.json":"reproduction.json",
    ".artifacts/scientific-audit.json":"scientific-audit.json",
    ".artifacts/participant-isolation.json":"participant-isolation.json",
    ".artifacts/tests-ci-equivalent.log":"tests.log",
    ".artifacts/pip-check.log":"pip-check.log",
    "reference/final-output/manifest.json":"reference-run.json",
    "results/receipts/failure.json":"receipt-failure.json",
    "results/receipts/failure.log":"isolation-failure.log",
}
for original,target in items.items():
    raw=(root/original).read_bytes()
    if raw.startswith((b"\xff\xfe",b"\xfe\xff")):
        (out/target).write_text(raw.decode("utf-16"),encoding="utf-8")
    else:
        shutil.copyfile(root/original,out/target)
for case in ["correct","unpaired","reversed"]:
    shutil.copyfile(root/f"results/grade-{case}.json",out/f"grade-{case}.json")
    shutil.copyfile(root/f"results/receipts/{case}.json",out/f"receipt-{case}.json")
runs=[json.loads((out/f"run-{i}.json").read_text()) for i in [1,2]]
assert runs[0]["docker_image_id"]==runs[1]["docker_image_id"]
for name,digest in runs[0]["code_hashes"].items():
    assert sha256(root/"src"/name)==digest, f"scientific source drift: {name}"
assert json.loads((out/"reproduction.json").read_text())["status"]=="pass"
write_json(out/"index.json",{"schema_version":1,"scope":"local computational evidence; no external scientist or user interview verification",
    "scientific_image_id":runs[0]["docker_image_id"],
    "final_runs":[{"elapsed_seconds":r["elapsed_seconds"],"peak_parent_rss_mb":r["peak_parent_rss_mb"]} for r in runs],
    "files":{p.name:sha256(p) for p in sorted(out.iterdir()) if p.is_file() and p.name!="index.json"}})
print("Evidence exported and scientific source hashes verified")
