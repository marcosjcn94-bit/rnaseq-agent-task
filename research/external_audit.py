"""Audit GEO SOFT and MINiML metadata for the preregistered six-sample contrast."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import tarfile
import xml.etree.ElementTree as ET
from pathlib import Path

SAMPLES = {
    "2": ("GSM332914", "GSM332925"),
    "3": ("GSM332915", "GSM332926"),
    "4": ("GSM332916", "GSM332927"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_soft(path: Path, selected: set[str]) -> dict[str, dict[str, list[str]]]:
    records: dict[str, dict[str, list[str]]] = {}
    current: str | None = None
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as stream:
        for line in stream:
            line = line.rstrip("\r\n")
            if line.startswith("^SAMPLE = "):
                accession = line.split("=", 1)[1].strip()
                current = accession if accession in selected else None
                if current:
                    records[current] = {}
            elif current and line.startswith("!Sample_"):
                key, _, value = line.partition("=")
                key = key.removeprefix("!Sample_").strip()
                value = value.strip().strip('"')
                records[current].setdefault(key, []).append(value)
    return records


def parse_miniml(path: Path, selected: set[str]) -> dict[str, dict[str, object]]:
    if tarfile.is_tarfile(path):
        with tarfile.open(path, "r:*") as archive:
            members = [m for m in archive.getmembers() if m.name == "GSE13168_family.xml"]
            if len(members) != 1:
                raise ValueError("MINiML archive must contain exactly one family XML")
            stream = archive.extractfile(members[0])
            if stream is None:
                raise ValueError("MINiML archive XML entry is unreadable")
            root = ET.parse(stream).getroot()
    else:
        root = ET.parse(path).getroot()
    records: dict[str, dict[str, object]] = {}
    for sample in (node for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "Sample"):
        accession = sample.attrib.get("iid")
        if accession not in selected:
            continue
        record: dict[str, object] = {"accession": accession}
        for node in sample.iter():
            name = node.tag.rsplit("}", 1)[-1]
            value = (node.text or "").strip()
            if name in {"Title", "Source", "Treatment-Protocol", "Data-Processing"} and value:
                record.setdefault(name, []).append(value)
            elif name == "Platform-Ref":
                record.setdefault("platform", []).append(node.attrib.get("ref", ""))
            elif name == "Supplementary-Data":
                record.setdefault("supplementary_data", []).append(
                    {"type": node.attrib.get("type", ""), "value": value}
                )
            elif name == "External-Data":
                record.setdefault("external_data", []).append(value)
            elif name == "Name" and value == "VALUE":
                record["value_description"] = next(
                    ((child.text or "").strip() for child in node.iter()
                     if child.tag.rsplit("}", 1)[-1] == "Description"), ""
                )
        records[accession] = record
    return records


def audit(soft: Path, miniml: Path) -> dict[str, object]:
    selected = {sample for pair in SAMPLES.values() for sample in pair}
    soft_records = parse_soft(soft, selected)
    xml_records = parse_miniml(miniml, selected)
    missing = {"soft": sorted(selected - soft_records.keys()),
               "miniml": sorted(selected - xml_records.keys())}
    if any(missing.values()):
        raise ValueError(f"GEO records missing: {missing}")
    pairs = []
    for donor, (control, treated) in SAMPLES.items():
        c_xml, t_xml = xml_records[control], xml_records[treated]
        c_title = " ".join(c_xml.get("Title", []))
        t_title = " ".join(t_xml.get("Title", []))
        if f"donor{donor}" not in c_title or f"donor{donor}" not in t_title:
            raise ValueError(f"donor pairing mismatch for donor {donor}: {c_title!r}, {t_title!r}")
        if c_xml.get("platform") != ["GPL96"] or t_xml.get("platform") != ["GPL96"]:
            raise ValueError(f"unexpected platform for donor {donor}")
        pairs.append({"donor": donor, "control": control, "treated": treated,
                      "control_title": c_title, "treated_title": t_title})
    return {"status": "metadata_audited", "series": "GSE13168", "pairs": pairs,
            "soft_sha256": sha256(soft), "miniml_sha256": sha256(miniml),
            "records": {sample: {"soft": soft_records[sample], "miniml": xml_records[sample]}
                        for sample in sorted(selected)}}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--soft", type=Path, required=True)
    parser.add_argument("--miniml", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("output already exists")
    result = audit(args.soft, args.miniml)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "pairs": result["pairs"]}, indent=2))


if __name__ == "__main__":
    main()
