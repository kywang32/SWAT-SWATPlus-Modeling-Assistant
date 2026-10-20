# Reference manuals (local installation only)

This directory deliberately contains **no third-party PDF files** in the public GitHub release. Source documents are not automatically licensed for redistribution just because they are openly downloadable.

Download legitimate copies for your own use, save them here, and consult [`../lookup/knowledge-index.json`](../lookup/knowledge-index.json) for the exact expected filenames, model domains, and source links.

| Local filename | Domain | Source / notes |
| --- | --- | --- |
| `swat2009-theory.pdf` | classic SWAT | [Official 2009 theory PDF](https://swat.tamu.edu/media/99192/swat2009-theory.pdf) |
| `swat-io-documentation-2012.pdf` | classic SWAT | [Official 2012 input/output PDF](https://swat.tamu.edu/media/69296/SWAT-IO-Documentation-2012.pdf) |
| `QSWATPlus Manual_v3.0.pdf` | SWAT+ / QSWAT+ | [Official QSWAT+ project](https://github.com/swat-model/QSWATPlus); locate a legally accessible **v3.0** manual, not an unrelated newer or older edition |
| `SWAT+ Documentation.pdf` | SWAT+ | **Optional historical PDF snapshot**, not a guaranteed downloadable official file; see [current SWAT+ documentation](https://docs.swat.tamu.edu/) |
| `SWAT+ Installation & Help.pdf` | SWAT+ | **Optional historical PDF snapshot**, not a guaranteed downloadable official file; see [current SWAT+ installation documentation](https://docs.swat.tamu.edu/getting-started/install/) |

**You do not need all five files to start.** For example, providing the two classic-SWAT manuals enables searching those documents locally; for SWAT+ you can use current online documentation if your agent has browsing access. If you make a different PDF capture of the online pages, use a **distinct filename** and update the catalog's version/title; do not pretend it is the 2025 source snapshot.

## Setup

After placing local PDFs here:

```bash
# From the skill directory (the one containing SKILL.md)
python scripts/reference_lookup.py status

# Fast local PDF text search
python scripts/reference_lookup.py search --model swat --query "curve number" --match phrase
python scripts/reference_lookup.py search --model swatplus --query "reservoir" --match all
```

The search script uses a local `pdftotext` executable if available; otherwise install the optional Python library:

```bash
python -m pip install -r scripts/requirements.txt
```

For more detail, refer to the project-level README. Mere presence of a PDF does **not** mean the ChatGPT plugin product will automatically ingest it or that a cloud agent can read files stored only on your own computer.

## Adding an additional manual

1. Put a legally obtained PDF into this directory.
2. Add a record in `../lookup/knowledge-index.json` using a unique `id`, correct `model` (`swat` or `swatplus`), exact relative `file` path, accurate `title` and `version`, and a provenance `source_url` if known.
3. Run `python scripts/reference_lookup.py status` and `search` to verify local readability. Cite the **actual** source/version used.
4. Keep uploaded and downloaded PDFs out of your public GitHub commit. The repository's `.gitignore` excludes the `references/` PDF files.
