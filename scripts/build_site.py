"""Build static site from papers/ directory.

Scans papers/ for metadata.json and notes.md, generates site/papers.json
for the frontend to consume.

Usage:
    python scripts/build_site.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "papers"
SITE_DIR = ROOT / "site"


def scan_papers():
    papers = []
    for d in sorted(PAPERS_DIR.iterdir()):
        if not d.is_dir():
            continue

        slug = d.name
        meta_path = d / "metadata.json"
        notes_path = d / "notes.md"
        pdf_path = d / "paper.pdf"

        entry = {
            "slug": slug,
            "has_pdf": pdf_path.exists(),
            "has_notes": notes_path.exists(),
            "metadata": None,
            "notes": None,
        }

        if meta_path.exists():
            try:
                entry["metadata"] = json.loads(meta_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                print(f"WARN: bad JSON in {meta_path}: {e}", file=sys.stderr)

        if notes_path.exists():
            entry["notes"] = notes_path.read_text(encoding="utf-8")

        papers.append(entry)

    # Sort: completed (has notes) first, then by year desc, then by title
    def sort_key(p):
        has_notes = 0 if p["has_notes"] else 1
        raw_year = p["metadata"].get("year") if p["metadata"] else None
        year = -int(raw_year) if isinstance(raw_year, int) else 0
        title = p["metadata"].get("title", p["slug"]) if p["metadata"] else p["slug"]
        return (has_notes, year, title)

    papers.sort(key=sort_key)
    return papers


def main():
    SITE_DIR.mkdir(exist_ok=True)
    papers = scan_papers()

    out_path = SITE_DIR / "papers.json"
    out_path.write_text(json.dumps(papers, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {out_path} ({len(papers)} papers)")

    # Summary
    with_notes = sum(1 for p in papers if p["has_notes"])
    with_pdf = sum(1 for p in papers if p["has_pdf"])
    print(f"  {with_notes} with notes, {with_pdf} with PDF, {len(papers)} total")


if __name__ == "__main__":
    main()
