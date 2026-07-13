# BOP Correction Manual

_Created: 11-07-2026 · Last updated: 11-07-2026_

The operator manual for correction and enrichment work on Bopp's *Glossarium
Sanscritum* (1847, Sanskrit→Latin, 8,961 entries): the correction pipeline
self-contained (change file → `updateByLine.py` → rebuild → validate →
batched delivery), the Greek-text campaign (`greek/`), the per-issue
workspaces, and the completed prefaces OCR. The per-directory `readme.txt`
files are working logs; this manual is the runbook layer over them.

Companion metadoc: [docs/CORRECTION_MANUAL.meta.md](https://github.com/sanskrit-lexicon/BOP/blob/main/docs/CORRECTION_MANUAL.meta.md).

---

## 1. Cheat-sheet — one correction, end to end

```bash
# layout: BOP + csl-orig + csl-pywork as siblings (the $BASE/cologne convention)

# 1. snapshot the canonical text (never edit it in place)
cp $BASE/cologne/csl-orig/v02/bop/bop.txt temp_bop_0.txt

# 2. write the change file (paired lines, ';' comments)
#    NNN old <exact current line>
#    NNN new <replacement line>          (also: ins = insert after, del = delete)

# 3. apply
python updateByLine.py temp_bop_0.txt change_bop_N.txt temp_bop_1.txt

# 4. rebuild + validate (from csl-pywork/v02/; watch for "All records parsed by ET")
sh generate_dict.sh bop ../../BOPScan/2020
sh xmlchk_xampp.sh bop

# 5. DELIVER — org agents: park in the correction queue, ship in the ONE
#    consolidated csl-orig PR ~monthly (/cologne-correction-queue +
#    /cologne-batch-pr). Direct csl-orig commits = upstream maintainers only.
#    Audit trail: diff_to_changes_dict.py before/after -> csl-corrections batch.
```

The full 8-stage discipline with every gotcha (BOM, `<LEND>`, CRLF,
line-count mismatch, line-number drift, python3/xmllint setup) is canonical
in [csl-corrections/docs/correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)
— this manual applies it to BOP and adds the repo's own campaigns.

## 2. Data-flow diagram

```
csl-orig/v02/bop/bop.txt   (canonical; SLP1 {#…#} + LATIN glosses {%…%};
│                           metaline <L>N<pc>PPP-c<k1>…<k2>…<h>N)
│
├── issues/issueNNN/  — per-defect correction workspaces (§4)
│     issue4 (proofread Greek) · issue5 (Slavonic: extract_slav.py + the
│     strings files) · issue6 (BOP-Main-L2 batch) · markup_fix (the
│     PWG-issue174-family fixer + synthetic tests)
│
├── greek/  — THE GREEK-TEXT CAMPAIGN (issue #1 lineage, §3)
│     temp_bop_ab_0.txt   ← Andhrabharati's re-keyboarding, WITH Greek
│     │  ab_convert_1.py         (line endings, tab→newline)
│     │  transcode/deva.py       (Devanagari → SLP1, invertibility-checked;
│     │                           the 4-line residue = issue #2 anomaly)
│     │  prep1.py                (metaline alignment vs Cologne text —
│     │                           found the 3593.1 'Ra' phantom headword,
│     │                           commented out; 282 metaline diffs triaged)
│     ▼
│     change_1..10.txt chain (+ make_change_*.py generators, proof.py
│     proofing pass → proof_greek.txt) applied via updateByLine.py
│     → Greek citations now live in bop.txt as UTF-8 Greek
│
├── prefaces/  — front-matter OCR, COMPLETE (5 pages: title, 2-pp. preface,
│     2-pp. SIGLORUM EXPLICATIO; Latin source + EN/RU; build_combined.py)
│
▼  csl-pywork build → bop.xml → Cologne display / csl-app
```

## 3. The Greek-text campaign (`greek/`) — how Bopp got its Greek back

**The problem:** the original Cologne keyboarding of Bopp omitted the Greek
script in his comparative citations. Andhrabharati's independent
re-keyboarding (posted on
[csl-devanagari #40](https://github.com/sanskrit-lexicon/csl-devanagari/issues/40))
carried the Greek — so the campaign merged it in, without importing the AB
text wholesale. The chain
([greek/readme.txt](https://github.com/sanskrit-lexicon/BOP/blob/main/greek/readme.txt)
is the log):

1. **Normalize the AB text**: `ab_convert_1.py` (Unix line endings,
   tab→newline: 19,923 lines → 37,845 records).
2. **Transcode**: `transcode/deva.py deva,slp1` converts the AB Devanāgarī
   to SLP1, then the **invertibility check** (slp1→deva round-trip diffed
   against the input) proves the transcoding is lossless — the 4-line
   residue became [issue #2](https://github.com/sanskrit-lexicon/BOP/issues/2)
   (deva↔slp1 anomaly, still open).
3. **Align**: `prep1.py` pairs both texts' entries by metaline. Findings of
   record: entry counts 8,960 vs 8,961 — the AB extra is `3593.1`, the
   cerebral nasal `Ra` counted as a headword only by AB (commented out to
   align); 282 metaline differences triaged.
4. **Extract + apply**: the `make_change_*.py` generators produce the
   numbered `change_1..10.txt` files (each one topic: pc corrections,
   Greek insertions per letter range, punctuation via `punct.py`), applied
   with `updateByLine.py`; `proof.py` renders the Greek-bearing lines for
   the human proofreading pass (`proof_greek.txt`, closed as
   [issue #4](https://github.com/sanskrit-lexicon/BOP/issues/4)).

**Status: completed campaign.** Greek citations are in the canonical text;
the numbered change files + readme are the replayable provenance. The same
pattern was repeated for **Slavonic** in
[issues/issue5/](https://github.com/sanskrit-lexicon/BOP/tree/main/issues/issue5)
(`extract_slav.py` + the `*.strings.txt` proofing files).

## 4. Per-issue corrections (`issues/issueNNN/`)

The standard Cologne pattern applied to BOP: pin `temp_bop_0.txt` from
csl-orig, transform incrementally (`temp_bop_1.txt`, …), keep the change
files + a `readme.txt` of commands run, rebuild + validate, deliver per §1
step 5, commit the documentation here. Existing workspaces: `issue4`
(Greek proofread), `issue5` (Slavonic), `issue6` (the BOP-Main-L2 external
correction batch), `markup_fix` (the org-wide markup-oddities fixer family —
PWG issue174 port with synthetic tests, closed as
[issue #8](https://github.com/sanskrit-lexicon/BOP/issues/8)).

## 5. Environment & prerequisites

- **Python 3** + `sh` (Git Bash on Windows); no pip installs (transcoders
  bundled in `greek/transcode/`).
- **Sibling repos:** csl-orig (canonical `bop.txt`), csl-pywork (build +
  validation), csl-corrections (audit trail + the queue). Scan images:
  `BOPScan/2020` (the `generate_dict.sh` second argument).
- The historical logs use the maintainer XAMPP layout
  (`/c/xampp/htdocs/cologne/...`); substitute your clone paths.

## 6. Symptom → cause → cure

| Symptom | Cause | Cure |
|---|---|---|
| CLAUDE.md says Bopp 1830, README says 1847 | Two editions of the Glossarium; the digitized edition is the expanded **1847** (title page MDCCCXLVII, per the prefaces OCR) | Trust README/CITATION; CLAUDE.md's 1830 needs a one-word fix |
| deva→slp1 round-trip diff is not zero | The known 4-line anomaly ([issue #2](https://github.com/sanskrit-lexicon/BOP/issues/2), open) | Expected residue; don't "fix" blindly — it is a tracked encoding question |
| Entry counts disagree with AB text (8,960 vs 8,961) | AB counts the `3593.1` cerebral-nasal letter head as an entry | Historic alignment decision: commented out on the AB side (§3.3) |
| `updateByLine.py` line-count/text mismatch | Change file built against a different bop.txt state | Re-pull csl-orig, re-snapshot, rebuild the change file |
| Greek renders as mojibake somewhere downstream | A consumer assumed Latin-1/ASCII; the Greek is UTF-8 by design | Fix the consumer; the source encoding is correct |
| `generate_dict.sh bop` fails on your machine | csl-pywork/BOPScan siblings missing, or `python3`/`xmllint` absent | §5 layout + the canonical doc's setup gotchas |
| Tempted to commit a fix straight to csl-orig | The no-noise delivery rule | Queue it; ONE batched PR ~monthly (§1 step 5) |
| An old issue's fix seems obvious | It may already be adjudicated | Check csl-corrections CFR/batch history first (the canonical preflight) |
| Latin gloss looks wrong but matches the print | Bopp's 1847 Latin, not a digitization error | Print divergences are `printchange` territory, and only for clear print errors |

## 7. Glossary

| Term | Meaning |
|---|---|
| Glossarium Sanscritum | Bopp's Sanskrit→Latin dictionary (Berlin 1847, expanded edition) — glosses in **Latin**, comparative forms in Greek/Old-Persian/Lithuanian/Slavic/Celtic |
| AB version | Andhrabharati's independent re-keyboarding, the source of the Greek text |
| invertibility check | Round-tripping deva→slp1→deva and diffing — the campaign's transcoding-losslessness proof |
| `3593.1` | The AB-only phantom headword (cerebral nasal `Ra` as a letter head) found by prep1 alignment |
| metaline | `<L>N<pc>PPP-c<k1>…<k2>…<h>N` — entry id, print page-column, headwords, homonym number |
| `{#…#}` / `{%…%}` | SLP1 Sanskrit / Latin-gloss italic display markup |
| SIGLORUM EXPLICATIO | The abbreviation list of the 1847 front matter (prefaces pages 04–05) |
| change file | Line-addressed `NNN old` / `NNN new` (+ `ins`/`del`) edit record — the auditable unit |
| batched PR | The agent delivery unit into csl-orig: everything queued, one consolidated PR ~monthly |
| proof file | A rendered extraction (`proof_greek.txt`, the Slavonic strings files) for human proofreading |

## 8. Maintainer appendix

- **Live vs finished:** open = [issue #2](https://github.com/sanskrit-lexicon/BOP/issues/2)
  (the deva↔slp1 anomaly). Finished campaigns = Greek insertion +
  proofreading (#1/#4), Slavonic (#5), the L2 batch (#6), markup oddities
  (#8), prefaces. The `greek/` change-file chain is replayable provenance —
  don't clean it up.
- **Observed quirks** (11-07-2026, while writing this manual): (1) the
  1830-vs-1847 date split between CLAUDE.md and README/CITATION (§6 row 1);
  (2) `greek/readme.txt` is a dense working log whose command paths are
  XAMPP-absolute — this manual is the portable layer; (3) the
  `change_3a`/`change_7`… numbering gaps in `greek/` reflect abandoned
  rounds — the readme, not the numbering, is the sequence of record.
- **Cross-repo edges:** csl-orig (canonical text), csl-pywork (+ BOPScan
  images) for build/validation, csl-corrections (audit + queue),
  csl-devanagari #40 (the AB source thread), the markup_fix family shared
  with PWG/PWK/LRV.
- **Issue taxonomy:** dictionary-repo taxonomy — see
  [CLAUDE.md](https://github.com/sanskrit-lexicon/BOP/blob/main/CLAUDE.md)
  and the README's label tables.

---

_Dr. Mārcis Gasūns_
