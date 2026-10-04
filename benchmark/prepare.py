"""Freeze an evaluator-only gold after the independent comparison gate."""
import argparse
import json
from pathlib import Path
import shutil
from src.contracts import sha256,write_json

def prepare(source, validation, destination):
    source,validation,destination = Path(source),Path(validation),Path(destination)
    check = json.loads(validation.read_text(encoding="utf-8"))
    if check.get("status")!="pass" or check.get("candidate_sha256")!=sha256(source/"differential_expression.csv"):
        raise ValueError("independent validation must pass and bind the candidate table hash")
    manifest = json.loads((source/"run_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("status")!="success":
        raise ValueError("source run did not succeed")
    for name in ["differential_expression.csv","analysis_summary.json"]:
        if manifest.get("files",{}).get(name)!=sha256(source/name):
            raise ValueError(f"source artifact hash mismatch: {name}")
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("gold destination must be empty")
    destination.mkdir(parents=True,exist_ok=True)
    for name in ["differential_expression.csv","analysis_summary.json","interpretation.md"]:
        shutil.copyfile(source/name,destination/name)
    shutil.copytree(source/"figures",destination/"figures")
    shutil.copyfile(validation,destination/"validation.json")
    files={str(p.relative_to(destination)).replace("\\","/"):sha256(p) for p in sorted(destination.rglob("*")) if p.is_file()}
    write_json(destination/"gold_manifest.json",{"schema_version":1,"files":files})
    return files

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",required=True); parser.add_argument("--validation",required=True)
    parser.add_argument("--destination",default="benchmark/gold")
    args=parser.parse_args()
    prepare(args.source,args.validation,args.destination)
    print(f"Gold prepared: {args.destination}; never mount this directory in participant containers")

if __name__=="__main__":
    main()
