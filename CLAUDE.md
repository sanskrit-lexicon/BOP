# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**BOP** is the corrections and research repository for the Cologne digitization of Bopp's *Glossarium Sanscritum* (1830). The canonical source lives in `csl-orig/v02/bop/bop.txt`.

## Architecture

| Directory | Purpose |
|---|---|
| `issues/` | Per-issue correction workflows (`issueNNN/` pattern) |
| `greek/` | Greek loanword and citation research in Bopp entries |

### Issue correction pattern (`issues/issueNNN/`)

Each issue folder follows the standard workflow:
1. Copy current `bop.txt` to a local `temp_bop_0.txt` (not tracked by git)
2. Apply corrections incrementally as `temp_bop_1.txt`, `temp_bop_2.txt`, etc.
3. Rebuild XML with `generate_dict.sh` and validate with `xmlchk_xampp.sh`
4. Commit the corrected file to `csl-orig`, then sync to Cologne
5. Commit issue documentation back here

## Common Commands

### Apply line-level corrections
```bash
python updateByLine.py <input_file> <changein_file> <output_file>
```

### Rebuild and validate XML (from `csl-pywork/v02/`)
```bash
sh generate_dict.sh bop ../../BOPScan/2020
sh xmlchk_xampp.sh bop
```

## Dependencies

- **Python 3**
- **bop.txt** — in `$BASE/cologne/csl-orig/v02/bop/bop.txt`

## Data format

Bopp entries use standard CDSL Sanskrit-lexicography markup, with **Latin** glosses.

| Tag | Role | Example |
|---|---|---|
| `<L>NNNN` | Entry begin, with `<pc>` print page-column ref | `<L>1<pc>001-a` |
| `<k1>`, `<k2>` | Primary / secondary headword (SLP1) | `<k1>a<k2>a` |
| `<h>N` | Homonym number | `<h>1` |
| `<LEND>` | Entry end | |
| `{#…#}` | Sanskrit text (SLP1) | `{#a#}` |
| `{%…%}` | Latin gloss / italic display | `{%stirps%}` |

Annotated example — the first entry of `bop.txt`:
```
<L>1<pc>001-a<k1>a<k2>a<h>1        # entry 1; print page 001 col a; headword "a"; homonym 1
1. {#a#}¦ stirps demonstrativa; v. gr. 270.   # SLP1 headword ¦ Latin gloss
<LEND>                             # entry end
```

## GitHub Issue Conventions

This repository uses the Cologne dictionary-repo issue taxonomy. Every issue has exactly one **type**, one **severity**, and one **milestone**:

- **Type** (9): link-target, link-splitting, markup, text-correction, content-enhancement, encoding, scan-quality, bug, question
- **Severity** (3): minor, medium, hard
- **Milestone** (4): Dictionary to Book, Digitization Quality, Structured Data, Major Enhancements

See the [Cologne issue runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-issue-runbook.md) for label definitions and the type→milestone mapping.
