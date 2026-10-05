"""Resumable known-truth paired negative-binomial simulation study."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

from research.fit import fit_research
from research.simulation_metrics import empirical_donor_effect_sd, metrics, sample_negative_binomial, summarize_replicates


def generate(rng, base_mean, dispersion, n_pairs, de_fraction, interaction_sd, donor_sd):
    g = len(base_mean)
    truth = np.zeros(g, dtype=bool)
    truth[: int(round(g * de_fraction))] = True
    rng.shuffle(truth)
    effects = np.zeros(g)
    effects[truth] = rng.choice([-1.0, 1.0], truth.sum())
    donor = rng.normal(0, donor_sd, size=(n_pairs, g))
    interaction = rng.normal(0, interaction_sd, size=(n_pairs, g))
    sf = rng.lognormal(0, 0.16, size=2 * n_pairs)
    arr = np.empty((g, 2 * n_pairs), dtype=np.int64)
    for d in range(n_pairs):
        for c in range(2):
            log2mu = np.log2(np.maximum(base_mean, 0.1)) + donor[d] + c * (effects + interaction[d])
            mu = np.maximum(0.05, 2 ** log2mu) * sf[2 * d + c]
            arr[:, 2*d+c] = sample_negative_binomial(rng, mu, np.maximum(dispersion, 1e-6))
    genes = [f"SIM{i:04d}" for i in range(g)]
    cols = [f"D{d}_{cond}" for d in range(n_pairs) for cond in ("control", "treated")]
    counts = pd.DataFrame(arr, index=genes, columns=cols)
    metadata = pd.DataFrame([{"sample_id": col, "donor": f"D{i//2}", "condition": "control" if i%2 == 0 else "treated"}
                             for i, col in enumerate(cols)]).set_index("sample_id")
    return counts, metadata, truth, effects


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def run(config_path, output, replicates=None):
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8-sig"))
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    diagnostics_path = Path(cfg["empirical_diagnostics"])
    diag = pd.read_csv(diagnostics_path)
    donor_sd = empirical_donor_effect_sd(diag)
    means = diag.baseMean.to_numpy(float)
    disp = diag.dispersion.to_numpy(float)
    good = np.isfinite(means) & np.isfinite(disp) & (means > 0) & (disp > 0)
    rng0 = np.random.default_rng(cfg["seed"])
    chosen = rng0.choice(np.flatnonzero(good), size=cfg["genes"], replace=len(np.flatnonzero(good)) < cfg["genes"])
    base_mean, dispersion = means[chosen], disp[chosen]
    nrep = cfg["replicates"] if replicates is None else replicates
    rows = []
    fit_cfg = {"design":"~ donor + condition", "contrast":["condition","treated","control"],
        "fit_type":"parametric", "size_factors_fit_type":"ratio", "refit_cooks":False,
        "min_replicates":7, "n_cpus":1, "alpha":cfg["alpha"], "cooks_filter":False,
        "independent_filter":False, "lfc_highlight":1.0}
    for pairs in cfg["pairs"]:
      for frac in cfg["de_fractions"]:
       for isd in cfg["interaction_sd"]:
        key = f"py-n{pairs}-de{frac}-int{isd}"
        done_path = output / f"{key}.csv"
        done = pd.read_csv(done_path).to_dict("records") if done_path.exists() else []
        for rep in range(len(done), nrep):
            seed = cfg["seed"] + pairs*1_000_000 + int(frac*100)*10_000 + int(isd*10)*1_000 + rep
            rng = np.random.default_rng(seed)
            counts, meta, truth, effects = generate(rng, base_mean, dispersion, pairs, frac, isd, donor_sd)
            try:
                res, _, _, info = fit_research(counts, meta, fit_cfg)
                rej = res.padj.fillna(1).to_numpy() < cfg["alpha"]
                valid = res.log2FoldChange.notna().to_numpy() & res.lfcSE.notna().to_numpy()
                m = metrics(truth[valid], rej[valid], res.log2FoldChange.to_numpy()[valid]-effects[valid], res.lfcSE.to_numpy()[valid])
                row = {"engine":"pydeseq2", "pairs":pairs,"de_fraction":frac,"interaction_sd":isd,
                       "replicate":rep,"seed":seed,"testable":int(valid.sum()),"failure":None,**m}
            except Exception as exc:
                row = {"engine":"pydeseq2", "pairs":pairs,"de_fraction":frac,"interaction_sd":isd,
                       "replicate":rep,"seed":seed,"testable":0,"failure":type(exc).__name__+": "+str(exc),
                       "fdp":np.nan,"power":np.nan,"type1":np.nan,"coverage":np.nan,"rejections":0}
            done.append(row)
            pd.DataFrame(done).to_csv(done_path,index=False)
        rows.extend(done)
    per_rep = pd.DataFrame(rows)
    per_rep.to_csv(output / "summary-replicates.csv", index=False)
    aggregate = summarize_replicates(per_rep)
    aggregate.to_csv(output / "scenario-summary.csv", index=False)
    manifest={"status":"completed_batch","config_sha256":sha(Path(config_path)),"empirical_sha256":sha(diagnostics_path),
              "seed":cfg["seed"],"requested_replicates":nrep,
              "pairs":cfg["pairs"],"de_fractions":cfg["de_fractions"],"interaction_sd":cfg["interaction_sd"],
              "scenarios":len(cfg["pairs"])*len(cfg["de_fractions"])*len(cfg["interaction_sd"]),"engines":["pydeseq2"],
              "donor_effect_sd_log2":donor_sd,"donor_effect_sd_source":"pooled within-gene variance of fitted E2 R donor contrasts, including reference donor zero",
              "note":"Per-replicate files are resumable; pilot is not production calibration."}
    (output/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    return manifest


def main():
    p=argparse.ArgumentParser(); p.add_argument("--config",required=True); p.add_argument("--output",required=True); p.add_argument("--replicates",type=int)
    a=p.parse_args(); print(json.dumps(run(a.config,a.output,a.replicates),indent=2))

if __name__ == "__main__": main()
