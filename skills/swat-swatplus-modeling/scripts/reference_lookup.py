#!/usr/bin/env python3
"""Portable inventory / on-demand page search for user-supplied SWAT reference PDFs.

Uses poppler's `pdftotext` if present, otherwise optional `pypdf`.
Never downloads, redistributes, uploads, or stores PDF contents.
Page indices are 1-based PDF page indices (not necessarily printed page numbers).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = SKILL_DIR / "lookup" / "knowledge-index.json"


def catalog():
    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    documents = data.get("documents", [])
    for entry in documents:
        name = entry.get("file", "")
        p = Path(name)
        if p.is_absolute() or ".." in p.parts or not str(p).startswith("references/"):
            raise ValueError(f"Unsafe path in document catalog: {name!r}")
        if entry.get("model") not in ("swat", "swatplus"):
            raise ValueError(f"Unknown model domain in catalog: {entry!r}")
    return documents


def absolute_file(entry, override=None):
    rel = Path(entry["file"])
    if override is not None:
        return Path(override).resolve() / rel.relative_to("references")
    return SKILL_DIR / rel


def status(args):
    documents = catalog()
    count = {"swat": 0, "swatplus": 0}
    for entry in documents:
        p = absolute_file(entry, args.references_dir)
        ready = p.is_file() and p.stat().st_size > 4
        if ready:
            with p.open("rb") as handle:
                ready = handle.read(4) == b"%PDF"
        if ready:
            count[entry["model"]] += 1
        tag = "READY" if ready else "MISSING"
        print(f"[{tag:7}] {entry['model']:8} {entry['id']:22} {p.name}")
        if not ready:
            print(f"          source: {entry.get('source_url','(none)')}")
    print(f"\nLocal PDFs available: classic SWAT {count['swat']}; SWAT+ {count['swatplus']}.")
    print("Catalog entries are references, not an embedded search database.")
    return 0


def pdf_pages(path):
    exe = shutil.which("pdftotext")
    if exe:
        # Text with form-feed page separators; explicit UTF-8 where supported.
        out = subprocess.run([exe, "-enc", "UTF-8", "-layout", str(path), "-"],
                             capture_output=True, check=True).stdout.decode("utf-8", errors="replace")
        pages = out.split("\f")
        if pages and not pages[-1].strip():
            pages.pop()
        return pages
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("No pdftotext executable or pypdf package found. "
                           "Install pypdf with: python -m pip install -r scripts/requirements.txt") from exc
    r = PdfReader(str(path))
    return [(p.extract_text() or "") for p in r.pages]


def collapse(s):
    return re.sub(r"\s+", " ", s).strip()


def page_match(content, phrase, mode):
    low = content.casefold()
    terms = [w.casefold() for w in phrase.split() if w]
    if not terms:
        return None
    if mode == "phrase":
        needle = " ".join(terms)
        pos = low.find(needle)
        score = low.count(needle)
    else:
        present = [t for t in terms if t in low]
        if mode == "all" and len(present) != len(terms):
            return None
        if mode == "any" and not present:
            return None
        pos = min(low.find(t) for t in present)
        score = sum(low.count(t) for t in present)
    return (pos, score) if pos >= 0 else None


def search(args):
    try:
        entries = [d for d in catalog() if args.model == "both" or d['model'] == args.model]
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"Catalog error: {exc}", file=sys.stderr)
        return 2
    results = []
    used = 0
    for entry in entries:
        path = absolute_file(entry, args.references_dir)
        if not path.is_file():
            continue
        used += 1
        try:
            pages = pdf_pages(path)
        except Exception as exc:
            # Errors are not evidence that a PDF or page can be cited.
            print(f"WARNING: Could not read {path.name}: {exc}", file=sys.stderr)
            continue
        for number, page in enumerate(pages, start=1):
            txt = collapse(page)
            hit = page_match(txt, args.query, args.match)
            if hit is None:
                continue
            at, score = hit
            left = max(0, at - args.context // 2)
            right = min(len(txt), at + args.context)
            snippet = ("…" if left else "") + txt[left:right] + ("…" if right < len(txt) else "")
            results.append({
                'document_id': entry['id'], 'model': entry['model'],
                'document': entry['title'], 'version': entry['version'],
                'file': path.name, 'pdf_page': number,
                'section': None,  # A section label must be independently verified.
                'score': score, 'snippet': snippet
            })
    if used == 0:
        print("No local PDF files for the selected model. See references/README.md.", file=sys.stderr)
        return 1
    results.sort(key=lambda r:(-r['score'], r['document_id'], r['pdf_page']))
    results = results[:args.limit]
    if args.json:
        print(json.dumps({'query': args.query, 'match':args.match, 'results':results},indent=2,ensure_ascii=False))
    else:
        for r in results:
            print(f"[{r['model']}] {r['document']} ({r['version']}), PDF page {r['pdf_page']}")
            print(f"  {r['snippet']}\n")
        if not results:
            print("No matching page in accessible local PDFs. Try fewer keywords or consult official online documentation.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--references-dir', type=Path, default=None,
                        help='Optional folder of user-supplied reference PDFs (defaults to skill/references).')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('status', help='List locally available manuals and missing expected filenames.')
    s = sub.add_parser('search', help='Find candidate PDF pages. Verify full context before citing.')
    s.add_argument('--model', choices=('swat','swatplus','both'), required=True)
    s.add_argument('--query', required=True, help='Keywords or exact phrase to search.')
    s.add_argument('--match', choices=('all','any','phrase'), default='all',
                   help='all=every term somewhere on page; any=any term; phrase=adjacent terms.')
    s.add_argument('--limit', type=int, default=8)
    s.add_argument('--context', type=int, default=400, help='Snippet length near match.')
    s.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    if getattr(args, 'limit', 1) <= 0 or getattr(args,'context',1) <= 0:
        parser.error('--limit and --context must be positive')
    return status(args) if args.command == 'status' else search(args)


if __name__ == '__main__':
    sys.exit(main())
