# SWAT/SWAT+ Modeling Assistant Gen II

**A portable, documentation-grounded Agent Skill and plugin for classic SWAT and SWAT+ watershed modeling.**

**Author:** Kunyang Wang · **License:** MIT (project-authored content only) · **Release:** v1.0.0 (portable public edition)

This open-source research assistant helps hydrologists, students, and environmental scientists make **model-version-aware, evidence-based** decisions about watershed setup, HRUs, routing, reservoirs, water balance, calibration, validation, and troubleshooting. It explicitly separates **classic SWAT** from **SWAT+** so terminology and parameter rules from one model are not casually applied to the other.

**It is not the SWAT/SWAT+ model executable, a trained or fine-tuned model, a calibration engine, or a bundled collection of copyrighted manuals.** The assistant requires access to actual authoritative sources (local PDF documents, accessible online manuals, or user-provided excerpts) before it can provide source-grounded technical claims.

## What changed in the public edition

- Replaced non-portable `file-...` document IDs with human-readable titles, documented versions, and relative file paths in `lookup/knowledge-index.json`.
- Removed **all five third-party PDFs** pending explicit redistribution authorization. Added official source links and local setup instructions instead.
- Added a working **on-demand PDF page search** helper (`scripts/reference_lookup.py`) supporting classic-SWAT-only, SWAT+-only, and dual-model queries.
- Removed the unsupported claim that uploaded PDFs are automatically processed into persistent vector/keyword databases. The included helper is **local text search**, not a vector database.
- Preserved model-generation isolation, source citations, cautious missing-source behavior, and technical troubleshooting workflows.
- Added a standard root-level `plugin.json` for portable Agent Plugins, while preserving `.codex-plugin/plugin.json` compatibility metadata. The skill can also be packaged independently.

## Research workflow and boundaries

| Request | Evidence and rules |
| --- | --- |
| Classic SWAT / SWAT2009 / SWAT2012 / ArcSWAT | Search only the **classic SWAT** documents for generation-specific claims |
| SWAT+ / SWAT+ Editor / QSWAT+ | Search only the **SWAT+** domain, with interface/model version checks |
| SWAT versus SWAT+ comparison | Search **both domains independently**, clearly separating each claim and source |
| Unqualified “SWAT” in a version-dependent question | Ask for model generation, or explicitly describe both branches |
| A PDF cannot be read or a claim lacks evidence | State what evidence is unavailable. **No invented page numbers or parameters** |

The answering priorities remain: **practical model implementation and debugging first; physical/mathematical explanation second**. Responses should cite a verified document title, version, section (if verified), and **PDF page number**, or an accessible official documentation URL and page heading.

## Files in this GitHub repository

```text
SWAT-SWATPlus-Modeling-Assistant-Gen-II/
├── plugin.json                            # Portable Agent Plugins manifest
├── .codex-plugin/plugin.json              # Compatibility manifest
├── .gitignore                             # Prevents commits of users' local PDFs
├── README.md
├── LICENSE
├── assets/gpt-icon.png                    # Existing project icon
└── skills/swat-swatplus-modeling/
    ├── SKILL.md                           # Portable skill rules and retrieval procedure
    ├── agents/openai.yaml                  # Agent-facing skill metadata
    ├── lookup/knowledge-index.json        # Manual metadata, not a vector index
    ├── references/README.md               # How to obtain and place local manuals
    └── scripts/
        ├── reference_lookup.py            # Local PDF status and page-text search
        └── requirements.txt               # Optional Python fallback: pypdf
```

There are **no PDF manuals** in this public repository. There is **no automatic PDF download** or automated rebuilding of hosted knowledge stores.

## Quick start: local use (Codex / shell-enabled agent)

1. Download or clone this GitHub repository. Install the plugin using a host that supports the portable root `plugin.json` or the compatibility `.codex-plugin/plugin.json`. Alternatively, install the standalone folder `skills/swat-swatplus-modeling/` as an Agent Skill; that directory contains `SKILL.md` at its root. See [OpenAI Skills](https://developers.openai.com/api/docs/guides/tools-skills) and [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins) for compatible packaging flows.
2. Obtain authorized reference documents yourself (see the next section). Put local PDF files under:

   ```text
   skills/swat-swatplus-modeling/references/
   ```

3. From `skills/swat-swatplus-modeling/`, check availability:

   ```bash
   python scripts/reference_lookup.py status
   ```

4. Search **only** the appropriate model domain:

   ```bash
   # Classic SWAT: find the exact phrase in user-provided local PDFs
   python scripts/reference_lookup.py search --model swat --query "curve number" --match phrase --limit 5

   # SWAT+: find pages containing the term
   python scripts/reference_lookup.py search --model swatplus --query "reservoir" --match all --limit 5

   # Machine-readable results for an agent
   python scripts/reference_lookup.py search --model swatplus --query "routing" --json
   ```

5. Read the surrounding source page before treating a search snippet as supporting evidence. The output uses **1-based PDF viewer page numbers**; these may differ from page numbers printed inside the manual.

The script prefers the local `pdftotext` utility (if available). If it is absent, install the optional PDF reader dependency:

```bash
python -m pip install -r skills/swat-swatplus-modeling/scripts/requirements.txt
```

The script reads PDFs locally and **does not upload, download, or republish them**. No search daemon, external AI API, database, credentials, or model runtime is required for this helper.

### ChatGPT installations without local filesystem/shell access

Installing a skill **does not automatically grant an agent access to files on your personal computer**. If a ChatGPT product cannot run the bundled script or read the `references/` folder, use that product's document upload/knowledge feature if supported, provide relevant excerpts, or ask the assistant to consult official online documentation using its browsing capabilities. Exact behavior depends on the host and workspace. A local-only PDF is not automatically available to a cloud ChatGPT session.

## Five reference documents (not redistributed)

| Model | Expected local filename | Official source / status |
| --- | --- | --- |
| Classic SWAT | `swat2009-theory.pdf` | [SWAT 2009 Theoretical Documentation (official PDF)](https://swat.tamu.edu/media/99192/swat2009-theory.pdf) |
| Classic SWAT | `swat-io-documentation-2012.pdf` | [SWAT 2012 Input/Output Documentation (official PDF)](https://swat.tamu.edu/media/69296/SWAT-IO-Documentation-2012.pdf) |
| SWAT+ (QSWAT+ GUI) | `QSWATPlus Manual_v3.0.pdf` | [QSWAT+ official project](https://github.com/swat-model/QSWATPlus); locate the matching v3.0 edition from an authorized source |
| SWAT+ | `SWAT+ Documentation.pdf` | Optional **2025 historical PDF capture**; current [SWAT+ documentation](https://docs.swat.tamu.edu/) is the authoritative online reference |
| SWAT+ | `SWAT+ Installation & Help.pdf` | Optional **2025 historical PDF capture**; refer to [current SWAT+ installation instructions](https://docs.swat.tamu.edu/getting-started/install/) |

**Important:** The last two names refer to historical local PDF captures, **not** official standardized PDF downloads. Do **not** save a different current web page under the historical filename and claim it is the same version. When using a new PDF edition or your own permitted web-page capture, add a new catalog entry with the real title, date, and filename. **You do not have to download all five** to use the skill, provided your host can access sufficient authoritative documentation for the questions at hand.

The public repository intentionally contains no third-party manual files. Open access for reading does not automatically confer a right to republish a PDF. The project's MIT License covers only material that its author has the right to license, not the external manuals, modeling software, or external trademarks.

## Installing reference documents: troubleshooting

- `status` shows **MISSING**: the matching file was not found under the expected path or does not look like a PDF. Check its exact spelling and directory.
- Search returns **no results**: verify the model domain (`swat` vs `swatplus`), try fewer terms (`--match any`), or use official online documentation.
- Error about `pypdf` / `pdftotext`: install `pypdf` using the command above, or install a supported `pdftotext` executable on your system.
- Search result cites a PDF page but not an internal section: this is intentional; the assistant must verify the printed section or printed page number independently.
- Adding a newer version: update `lookup/knowledge-index.json` to reflect its **real** filename and version. The helper reads the entries dynamically; there is no proprietary file ID to recreate.
- ChatGPT cannot find your PDF: check whether the product actually gives the agent access to that file. Uploading it as host-supported knowledge is different from putting it into a folder on a separate computer.

## Example prompts

```text
I am using classic SWAT2012. Which documentation-backed checks should I perform
before calibrating daily streamflow? Please cite manual sections/pages.

I use SWAT+ with a QSWAT+ project. How should I define reservoirs and routing
objects? Distinguish interface setup from the SWAT+ model revision.

Compare HRU definitions in classic SWAT and SWAT+, using separate sources.

My SWAT+ run fails in channel routing. Tell me what information you need,
which input and output files to inspect, and the evidence for each check.
```

## Scientific and reproducibility notes

- Distinguish observed facts, official model definitions, and modeling recommendations.
- Always report the **model executable version**, and when relevant QSWAT+ and SWAT+ Editor versions.
- PDF-search snippets identify **candidate passages**, not verified calculations or complete procedures.
- Parameter ranges, file column names, units, and process equations may be revision dependent.
- Validate water and constituent mass balances, input assumptions, calibration/validation protocols, spatial and temporal scales, and reproducibility independently.
- No source available means **no invented citations**; host-level browsing/access constraints should be disclosed.

## License and third-party rights

Project-authored instructions and scripts: [MIT License](LICENSE), © 2026 Kunyang Wang. The license does **not** grant rights to third-party reference manuals, model executables, third-party code, or any artwork not owned by the project author. Before public release, verify you own or may distribute the included icon.

**Independent project:** This repository is not an official SWAT, SWAT+, QSWAT+, USDA, or Texas A&M support service.

## Citation, issues, and contributions

If describing this assistant in published work, cite a fixed release/tag or archived snapshot with the actual repository URL. Cite the underlying SWAT/SWAT+ software and documentation independently for any model methods.

> Wang, K. (2026). *SWAT/SWAT+ Modeling Assistant Gen II* (v1.0.0) [Agent Skill and plugin]. GitHub. [Add repository URL after publishing].

Scientific bug reports, documentation corrections, usability improvements, and version-specific references are welcome. Please **do not submit copyrighted third-party PDFs, unpublished model/data files, or credentials** in issues and pull requests.
