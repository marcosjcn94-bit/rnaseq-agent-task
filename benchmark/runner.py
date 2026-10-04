"""Evaluator-owned Docker runner. Participant code receives no gold or Docker socket."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import subprocess
import time
from src.contracts import sha256,write_json

def source_hashes(directory):
    files = list(directory.rglob("*"))
    if any(p.is_symlink() for p in files):
        raise ValueError("submission symlinks are not allowed")
    regular = [p for p in files if p.is_file()]
    if sum(p.stat().st_size for p in regular)>20*1024**2:
        raise ValueError("submission source exceeds 20 MiB")
    return {str(p.relative_to(directory)).replace("\\","/"):sha256(p) for p in sorted(regular)}

def output_hashes(directory):
    files = list(directory.rglob("*"))
    if any(p.is_symlink() for p in files):
        raise ValueError("output symlinks are not allowed")
    regular = [p for p in files if p.is_file()]
    if len(regular)>100 or sum(p.stat().st_size for p in regular)>100*1024**2:
        raise ValueError("output exceeds file count or size limits")
    return {str(p.relative_to(directory)).replace("\\","/"):sha256(p) for p in sorted(regular)}

def execute(source, output, receipt, image="rnaseq-participant:validated", timeout=1800):
    source,output,receipt = Path(source).resolve(),Path(output).resolve(),Path(receipt).resolve()
    if not (source/"analyze.py").is_file():
        raise ValueError("submission must contain analyze.py")
    if output==source or output.is_relative_to(source) or source.is_relative_to(output):
        raise ValueError("source and output directories must be disjoint")
    if receipt.is_relative_to(output) or receipt.is_relative_to(source):
        raise ValueError("receipt must be evaluator-owned, outside participant mounts")
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError("output directory must be empty")
    before = source_hashes(source)
    image_info = json.loads(subprocess.check_output(["docker","image","inspect",image],text=True))[0]
    output.mkdir(parents=True,exist_ok=True)
    receipt.parent.mkdir(parents=True,exist_ok=True)
    options = [
        "docker","create","--network","none","--read-only","--cap-drop","ALL",
        "--security-opt","no-new-privileges","--memory","4g","--cpus","2",
        "--pids-limit","128","--tmpfs","/tmp:rw,nosuid,size=512m",
        "--mount",f"type=bind,src={source},dst=/submission,readonly",
        "--mount",f"type=bind,src={output},dst=/output",
        image_info["Id"],"--data","/data","--output","/output","--config","/task/config.json",
    ]
    started = time.perf_counter()
    container = subprocess.check_output(options,text=True).strip()
    record = {"schema_version":1,"status":"failed","image_id":image_info["Id"],
              "source_hashes":before,"started_at":datetime.now(timezone.utc).isoformat()}
    try:
        process = subprocess.run(["docker","start","--attach",container],capture_output=True,text=True,timeout=timeout)
        log = receipt.with_suffix(".log")
        log.write_text(process.stdout+"\n"+process.stderr,encoding="utf-8")
        inspection = json.loads(subprocess.check_output(["docker","inspect",container],text=True))[0]
        record.update(
            exit_code=int(inspection["State"]["ExitCode"]),
            network_mode=inspection["HostConfig"]["NetworkMode"],
            read_only_root=inspection["HostConfig"]["ReadonlyRootfs"],
            source_unchanged=source_hashes(source)==before,
            mounts=[{"destination":m["Destination"],"read_write":m["RW"]} for m in inspection["Mounts"]],
            output_hashes=output_hashes(output),
            log_sha256=sha256(log),
        )
        record["status"] = "success" if record["exit_code"]==0 and record["source_unchanged"] else "failed"
    except subprocess.TimeoutExpired:
        subprocess.run(["docker","kill",container],capture_output=True)
        record.update(status="timeout",exit_code=None)
    except (OSError,ValueError,subprocess.CalledProcessError) as error:
        record.update(status="failed",error=str(error))
    finally:
        record["elapsed_seconds"] = time.perf_counter()-started
        write_json(receipt,record)
        subprocess.run(["docker","rm","--force",container],capture_output=True,check=True)
    return record

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",required=True); parser.add_argument("--output",required=True)
    parser.add_argument("--receipt",required=True); parser.add_argument("--image",default="rnaseq-participant:validated")
    args = parser.parse_args()
    result = execute(args.source,args.output,args.receipt,args.image)
    print(json.dumps(result,indent=2))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",required=True)
    parser.add_argument("--output",required=True)
    parser.add_argument("--receipt",required=True)
    parser.add_argument("--image",default="rnaseq-participant:validated")
    args = parser.parse_args()
    result = execute(args.source,args.output,args.receipt,args.image)
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result["status"]=="success" else 1)

if __name__=="__main__":
    main()
