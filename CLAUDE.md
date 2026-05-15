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
