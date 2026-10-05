"""Extract only preregistered GPL96/CEL files from the audited GEO bundle."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import shutil
import tarfile
from pathlib import Path

from research.external_audit import SAMPLES, sha256


def prepare(downloads: Path, output: Path) -> dict[str, object]:
    archive_path = downloads / "GSE13168_family.xml.tgz"
    soft_path = downloads / "GSE13168_family.soft.gz"
    allowed = {"GPL96-tbl-1.txt"}
    cels = sorted(sample for pair in SAMPLES.values() for sample in pair)
    allowed.update(f"{sample}-tbl-1.txt" for sample in cels)
    if output.exists() and any(output.iterdir()):
        raise ValueError("extraction output must be empty")
    output.mkdir(parents=True, exist_ok=True)
    platform_dir = output / "platform"
    platform_dir.mkdir()
    extracted: dict[str, str] = {}
    with tarfile.open(archive_path, "r:gz") as archive:
        for member_name in sorted(allowed):
            members = [member for member in archive.getmembers() if member.name == member_name]
            if len(members) != 1 or not members[0].isfile():
                raise ValueError(f"expected exactly one regular GEO entry: {member_name}")
            source = archive.extractfile(members[0])
            if source is None:
                raise ValueError(f"unreadable GEO entry: {member_name}")
            target = platform_dir / member_name
            with target.open("xb") as stream:
                shutil.copyfileobj(source, stream)
            extracted[member_name] = sha256(target)
    cel_dir = output / "CEL"
    cel_dir.mkdir()
    cel_hashes: dict[str, str] = {}
    for sample in cels:
        source = downloads / "CEL" / f"{sample}.CEL.gz"
        target = cel_dir / f"{sample}.CEL"
        with gzip.open(source, "rb") as compressed, target.open("xb") as raw:
            shutil.copyfileobj(compressed, raw)
        cel_hashes[target.name] = sha256(target)
    inputs = [soft_path, archive_path, *(downloads / "CEL" / f"{sample}.CEL.gz" for sample in cels)]
    return {
        "status": "extracted",
        "inputs_sha256": {path.name if path.parent == downloads else path.relative_to(downloads).as_posix(): sha256(path) for path in inputs},
        "gpl96_tables_sha256": extracted,
        "cel_sha256": cel_hashes,
        "cel_uncompressed_bytes": {f"{sample}.CEL": (cel_dir / f"{sample}.CEL").stat().st_size for sample in cels},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--downloads", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = prepare(args.downloads, args.output)
    target = args.output / "manifest.json"
    target.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "samples": len(manifest["cel_sha256"]),
                      "probe_rows": "raw platform table extracted"}, indent=2))


if __name__ == "__main__":
    main()
