_Created: 22-05-2026 · Last updated: 05-09-2026_

### Location

Counterpart of https://github.com/sanskrit-lexicon/PWG/issues/175 (PWG) and https://github.com/sanskrit-lexicon/PWK/issues/113 (PWK) for `bop.txt`.

I ran the same two-job recipe over `csl-orig/v02/bop/bop.txt`: auto-fix the few things with a single safe resolution; audit everything else with line refs. Added `08_markup_fix.py` plus outputs to a new `issues/markup_fix/` folder on the branch `markup-fix-audit`.

@funderburkjim @Andhrabharati — please review the findings listed below.

## Markup fixer + audit for `bop.txt`

### What it auto-fixes

| Pattern | Result |
|---|---|
| `<ab><ab>X</ab> Y</ab>` | `<ab>X Y</ab>` |
| `<lang> word </lang>` | `<lang>word</lang>` |
| `<sup> word </sup>` | `<sup>word</sup>` |
| `<F> word </F>` | `<F>word</F>` |

Whitespace trimming applies to all 3 paired tag(s) in `bop.txt`: `<lang>`, `<sup>`, `<F>`. The original file is never modified — output goes to `bop_fixed.txt`, with the full diff in `markup_fix_changes.txt` (updateByLine format). 39 line(s) changed.

### Closing-tag inventory in current `bop.txt`

| Tag | Count |
|---|---:|
| `</lang>` | 1 |
| `</479)>` | ? |
| `</sup>` | 59 |
| `</F>` | 59 |

### What it found in current `bop.txt`

- 39 whitespace trims applied: leading/trailing spaces inside `<lang>` tags (44 leading + 1 trailing from scan).
- 0 adjacent `</ab> <ab>` — no `<ab>` tag in bop.txt.
- 0 `<ab n="…">` attributes — no abbreviation markup in bop.txt.
- 0 correction records.

### Usage

```
cd issues/markup_fix
python 08_markup_fix.py                        # uses csl-orig/v02/bop/bop.txt by default
python 08_markup_fix.py IN.txt OUT.txt         # custom paths
```

Outputs: `bop_fixed.txt`, `markup_fix_changes.txt`, `markup_audit.txt`.

### Summary

No <ab> or <ls> tags; <lang> is the primary paired tag.

### Severity

`minor`

_Dr. Mārcis Gasūns_
