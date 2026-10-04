"""Run the fixed airway analysis offline; never silently overwrite outputs."""
import argparse
from datetime import datetime,timezone
import os
from pathlib import Path
import platform
import sys
import time
from .analysis import fit
from .contracts import load_config,sha256,versions,write_json
from .data import read_inputs,prefilter
from .report import report

def run(data,output,config_path):
    output = Path(output)
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError("output directory must be empty; existing results are preserved")
    config = load_config(config_path)
    raw,metadata,input_hashes,source = read_inputs(data)
    filtered,mask = prefilter(raw,config["min_count"],config["min_samples"])
    started = time.perf_counter()
    result,normalized,info = fit(filtered,metadata,config)
    for warning in info["warnings"]:
        print(f"WARNING: {warning}")
    output.mkdir(parents=True,exist_ok=True)
    result.to_csv(output/"differential_expression.csv",index_label="gene_id")
    mask.to_frame("retained").to_csv(output/"gene_filter.csv",index_label="gene_id")
    normalized.to_csv(output/"normalized_counts.csv",index_label="gene_id")
    report(raw,normalized,metadata,result,output,config,info)
    summary = {
        "schema_version":1,"design":config["design"],"contrast":config["contrast"],
        "prefilter":{"min_count":config["min_count"],"min_samples":config["min_samples"]},
        "genes_input":len(raw),"genes_tested":len(result),"genes_removed":int((~mask).sum()),
        "significant":int(result.significant.sum()),"highlight":int(result.highlight.sum()),
        "upregulated":int((result.significant & (result.log2FoldChange>0)).sum()),
        "downregulated":int((result.significant & (result.log2FoldChange<0)).sum()),
        "missing_pvalue":int(result.pvalue.isna().sum()),"missing_padj":int(result.padj.isna().sum()),
        "na_reasons":{str(k):int(v) for k,v in result.na_reason.value_counts().items()},
        "versions":versions(),"lfc_shrinkage":False,
        "input_hashes":input_hashes,"config_hash":sha256(config_path),
        "model":info,
    }
    write_json(output/"analysis_summary.json",summary)
    peak = None
    try:
        import resource
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
    except ImportError:
        pass
    manifest = {
        "schema_version":1,"status":"success","completed_at":datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds":time.perf_counter()-started,
        "peak_parent_rss_mb":peak,"memory_scope":"parent process peak RSS; excludes worker processes",
        "platform":platform.platform(),"python":platform.python_version(),
        "versions":versions(),"parameters":config,"input_hashes":input_hashes,
        "code_hashes":{p.name:sha256(p) for p in Path(__file__).parent.glob("*.py")},
        "docker_image_id":os.environ.get("RNASEQ_IMAGE_ID"),
        "files":{str(p.relative_to(output)).replace("\\","/"):sha256(p) for p in sorted(output.rglob("*")) if p.is_file()},
    }
    write_json(output/"run_manifest.json",manifest)
    print(f"Success: {len(result)} genes tested; {summary['significant']} significant. Output: {output}")
    return summary

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command",required=True)
    task = commands.add_parser("run",help="validate inputs and run paired analysis")
    task.add_argument("--data",required=True)
    task.add_argument("--output",required=True)
    task.add_argument("--config",default="config.json")
    args = parser.parse_args()
    try:
        run(args.data,args.output,args.config)
    except (ValueError,OSError,KeyError,TypeError) as error:
        print(f"ERROR: {error}",file=sys.stderr)
        return 1
    return 0

if __name__=="__main__":
    raise SystemExit(main())
