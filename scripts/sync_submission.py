"""Export public registries from the compiled 88-reference submission sources.

Usage: python scripts/sync_submission.py --manuscript-dir PATH
Requires PyMuPDF for PDF verification. No network access or publication occurs.
"""
import argparse
import csv
import hashlib
import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RELEASE = "v1.2-paper-submission"


def read(path):
    return path.read_text(encoding="utf-8-sig")


def save_csv(path, headers, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(headers)
        writer.writerows(rows)


def export(manuscript):
    import fitz

    aux = read(manuscript / "Manuscript-submission-synced.aux")
    main_labels = dict(re.findall(r"\\bibcite\{(ref\d+)\}\{\{([^}]+)\}", aux))
    assert len(main_labels) == 88 and set(main_labels.values()) == {str(n) for n in range(1, 89)}
    labels = dict(re.findall(r"RegistryLabel@(ref\d+)\\endcsname\{([^}]+)\}",
                             read(manuscript / "registry-reference-labels-condensed.tex")))
    assert labels.items() >= main_labels.items()
    assert set(labels.values()) == set(main_labels.values()) | {f"S{n}" for n in range(1, 6)}
    source = read(manuscript / "appendix-condensed-body.tex")
    used_keys = set()

    def cite(match):
        keys = match[1].split(",")
        used_keys.update(keys)
        return "[" + ", ".join(labels[key] for key in keys) + "]"

    def plain(value):
        value = re.sub(r"\\registrycite\{([^}]+)\}", cite, value)
        value = re.sub(r"\\url\{([^}]+)\}", r"\1", value)
        value = re.sub(r"\\\\\[3pt\]\s*$|&\s*$", "", value)
        value = value.replace(r"\allowbreak{}", "").replace(r"\ensuremath{\rightarrow}", "→")
        value = value.replace(r"\ensuremath{\leftrightarrow}", "↔")
        value = value.replace(r"\textasciitilde{}", "~").replace(r"\texttimes{}", "×")
        value = value.replace("---", "—").replace("--", "–")
        value = value.replace(r"\&", "&").replace(r"\_", "_").replace(r"\%", "%")
        assert not re.search(r"\\[A-Za-z]+|appendix\.t", value), ("Unconverted cell", value)
        return " ".join(value.split())

    outputs = {}
    specs = [(1, "appendix-a-datasets.csv", 30, 8), (2, "appendix-b-method-evidence.csv", 17, 9),
             (3, "appendix-c-availability-ethics.csv", 30, 11), (4, "appendix-d-mp-reid-directions.csv", 12, 5),
             (5, "appendix-e-protocol-registry.csv", 14, 10)]
    for number, name, count, width in specs:
        target = REPO / "tables" / name
        with target.open(encoding="utf-8-sig", newline="") as stream:
            headers = next(csv.reader(stream))
        assert len(headers) == width
        cells = {}
        pattern = rf"% appendix\.t{number:02d}\.r(\d+)\.c(\d+)\s*\n(.*?)(?=% appendix\.|\\end\{{longtable\}})"
        for row, col, value in re.findall(pattern, source, re.S):
            key = (int(row), int(col))
            value = plain(value)
            if key in cells:
                assert cells[key] == value, ("Repeated panel identifier differs", key)
            cells[key] = value
        assert len(cells) == count * width, (name, len(cells))
        rows = [[cells[row, col] for col in range(width)] for row in range(1, count + 1)]
        save_csv(target, headers, rows)
        outputs[name] = rows
    c_rows = outputs["appendix-c-availability-ethics.csv"]
    save_csv(REPO / "evidence/source-manifest.csv",
             ["Dataset", "Evidence source", "Official URL or archived URL", "Source version/date", "Availability checked"],
             [[row[0], row[8], row[9], row[10], row[7]] for row in c_rows])

    records = {}
    for key, entry in re.findall(r"@\w+\{(ref\d+),\s*(.*?)(?=\n@|\Z)", read(manuscript / "references.bib"), re.S):
        fields = dict(re.findall(r"^\s*(\w+)\s*=\s*\{(.*)\},?\s*$", entry, re.M))
        records[key] = {field: value.replace("{", "").replace("}", "") for field, value in fields.items()}
    assert used_keys <= labels.keys() <= records.keys()
    bibliographic_headers = ["citation", "stable_key", "title", "authors", "year", "venue", "doi"]

    def bibliographic_row(key):
        item = records[key]
        return [labels[key], key, item["title"], item.get("author", ""), item.get("year", ""),
                item.get("journal", item.get("booktitle", "")), item.get("doi", "")]

    save_csv(REPO / "evidence/main-references.csv", bibliographic_headers,
             [bibliographic_row(key) for key in sorted(main_labels, key=lambda key: int(main_labels[key]))])
    supp_keys = sorted(labels.keys() - main_labels.keys(), key=lambda key: int(labels[key][1:]))
    save_csv(REPO / "evidence/supplementary-references.csv", bibliographic_headers,
             [bibliographic_row(key) for key in supp_keys])
    old_aux = read(manuscript / "Manuscript-format-corrected.aux")
    old_labels = dict(re.findall(r"\\bibcite\{(ref\d+)\}\{\{([^}]+)\}", old_aux))
    assert len(old_labels) == 118
    save_csv(REPO / "evidence/citation-map.csv", ["stable_key", "original_118_reference_number", "current_citation", "status", "title"],
             [[key, old_labels[key], labels.get(key, ""),
               "main" if key in main_labels else "supplementary-only" if key in labels else "omitted",
               records[key]["title"]] for key in sorted(old_labels, key=lambda key: int(old_labels[key]))])
    save_csv(REPO / "evidence/citation-audit-summary.csv", ["item", "value"], [
        ["snapshot release", RELEASE], ["citation format", "numeric by first appearance in the 88-reference manuscript"],
        ["main references", 88], ["supplementary-only references", 5],
        ["source of registry numbering", "compiled LaTeX citation keys and registry-reference-labels-condensed.tex"],
        ["appendices in supplementary PDF", "A-G"], ["audit date", "2026-10-08"],
        ["registry evidence verification date", "2026-09-04"],
        ["scope", "version and citation synchronisation; no new dataset-availability verification"]])

    pdf_path = manuscript / "Appendix-condensed.pdf"
    pdf = fitz.open(pdf_path)
    pdf_text = "\n".join(page.get_text() for page in pdf)
    assert RELEASE in pdf_text and all(f"Appendix {letter}" in pdf_text for letter in "ABCDEFG")
    assert all(f"[S{n}]" in pdf[-1].get_text() for n in range(1, 6))
    for rows in outputs.values():
        for row in rows:
            for cell in row:
                for group in re.findall(r"\[([S\d, ]+)\]", cell):
                    assert set(group.split(", ")) <= set(labels.values()), group
    # The public PDF is copied only after all source/citation checks pass.
    shutil.copyfile(pdf_path, REPO / "supplementary/appendix.pdf")
    metadata = {"release": RELEASE, "main_references": 88, "supplementary_only_references": 5,
                "main_pdf_filename": "Manuscript-submission-synced.pdf", "supplementary_pages": len(pdf),
                "registry_export_date": "2026-10-08", "registry_evidence_checked": "2026-09-04",
                "exported_table_rows": {name: len(rows) for name, rows in outputs.items()},
                "registry_citation_keys_verified": sorted(used_keys),
                "sha256": {str(path.relative_to(REPO)).replace('\\', '/'): hashlib.sha256(path.read_bytes()).hexdigest()
                           for path in sorted(list((REPO / "tables").glob("*.csv")) + list((REPO / "evidence").glob("*.csv"))
                                              + [REPO / "supplementary/appendix.pdf"])}}
    (REPO / "evidence/submission-snapshot.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: metadata[k] for k in ["release", "main_references", "supplementary_pages", "exported_table_rows"]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manuscript-dir", type=Path, required=True)
    export(parser.parse_args().manuscript_dir.resolve())
