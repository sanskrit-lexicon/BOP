# CORRECTION_MANUAL.md — metadoc

_Created: 11-07-2026 · Last updated: 11-07-2026_

Companion record for
[docs/CORRECTION_MANUAL.md](https://github.com/sanskrit-lexicon/BOP/blob/main/docs/CORRECTION_MANUAL.md).

## Purpose

The runbook over BOP's working logs: the correction pipeline applied to
Bopp (change file → updateByLine → rebuild → validate → batched delivery),
the Greek-text campaign as replayable provenance (AB merge with
invertibility check and metaline alignment), the per-issue pattern, and the
completed prefaces OCR.

## Audience

- An operator preparing a BOP correction for the monthly batch.
- A scholar tracing how the Greek (or Slavonic) text entered `bop.txt`.
- A contributor picking up the open deva↔slp1 anomaly (issue #2).

## Provenance

Authored 11-07-2026 by Fable 5 (`claude-fable-5`) under handoff
[H516-Fable_BOP_correction_pipeline_manual_10.07.26](https://github.com/gasyoun/Uprava/blob/main/handoffs/H516-Fable_BOP_correction_pipeline_manual_10.07.26.md)
(the H501–H531 per-repo manuals programme, Litpam-Indexator MANUAL.md gold
standard). Content read from `greek/readme.txt` (the campaign log),
`issues/*/readme.txt`, README/CLAUDE.md/prefaces, and the canonical
correction-workflow doc — none invented.

## Ranked improvement backlog

| # | Item | Status |
|---|---|---|
| 1 | Fix CLAUDE.md's "1830" → 1847 (title page MDCCCXLVII; README/CITATION already correct) | open |
| 2 | Close the deva↔slp1 4-line anomaly ([issue #2](https://github.com/sanskrit-lexicon/BOP/issues/2)) — the campaign's one open thread | open (owned by issue) |
| 3 | A short `greek/` index note mapping each `change_N` to its topic (currently reconstructed from the log; numbering has gaps from abandoned rounds) | open |
| 4 | Portable-path variables in the issue readme conventions (XAMPP-absolute paths recur) | open |

## Known limitations

- The Greek campaign is documented at replay/provenance level; per-decision
  detail (which entry got which citation) lives in the change files
  themselves.
- The Latin-philology adjudications (gloss corrections vs Bopp's own usage)
  are scholarly territory outside this manual.
- The build internals are the canonical workflow doc's + csl-pywork's to
  document; this manual stops at the interface.

## Related documents

- [README.md](https://github.com/sanskrit-lexicon/BOP/blob/main/README.md) — repo overview + verified change-file usage example
- [CLAUDE.md](https://github.com/sanskrit-lexicon/BOP/blob/main/CLAUDE.md) — data-format reference (one stale date, backlog #1)
- [greek/readme.txt](https://github.com/sanskrit-lexicon/BOP/blob/main/greek/readme.txt) — the Greek-campaign working log
- [prefaces/README.md](https://github.com/sanskrit-lexicon/BOP/blob/main/prefaces/README.md) — front-matter conventions
- [csl-corrections/docs/correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md) — the canonical 8-stage reference
- Sibling manual: [csl-orig docs/CORRECTION_MANUAL.md](https://github.com/sanskrit-lexicon/csl-orig/blob/main/docs/CORRECTION_MANUAL.md) (H515) — the delivery-side view

## Revision history

| Date | Change | By |
|---|---|---|
| 11-07-2026 | Initial version (H516) | Fable 5 (`claude-fable-5`) |

---

_Dr. Mārcis Gasūns_
