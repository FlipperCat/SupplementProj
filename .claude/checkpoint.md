# Checkpoint — 2026-05-11 (PM)

## Done (this session)

- Backfilled `notes` field on all 77 supplements that lacked one in `data/supplements.json`. Stack Analyzer DB is now 119/119 with notes (full coverage).
- Wrote concise, clinical, actionable one-liners per entry (dosing tips, form preferences, interaction caveats, deficiency cautions). Style matches existing entries.
- Created `backfill_notes.py` as a reusable helper (in repo root).
- Updated `PROJECT-STATUS.md` richness section + crossed off the notes task in Outstanding work.
- Verified `hugo` build is clean (1530 pages, 2.3s, exit 0).

## Next obvious step

- **Fill in `conflicts` arrays** — still only 15/119. This is now the thinnest data quality area and the Stack Analyzer's killer feature is conflict detection. Best leverage is on the high-traffic entries (vitamin-d3, magnesium, omega-3 already have conflicts — focus on zinc, calcium, iron, k2, b-complex interactions with common meds).
- After that: `MedicalSupplement` schema.org structured data on supplement pages (SEO leverage, low-competition).

## Earlier outstanding (carried forward)

- ~~75-file uncommitted backlog~~ — working tree is now clean (previous backlog appears to have been committed). Skip.
- Replace placeholder analytics IDs in `hugo.toml` (`G-XXXXXXXXXX`, `YOUR_GSC_VERIFICATION_ID`) — needs real values from user.

## In flight

None — task shipped end-to-end.

## Gotchas discovered

- `data/supplements.json` em-dash bytes survive — Python writes UTF-8 cleanly when `encoding='utf-8'` is explicit AND `ensure_ascii=False` is passed to `json.dump`. Without the latter, you get `—` escapes which still load fine but bloat the file.
- Windows terminal will mojibake em-dashes on stdout (cp1252 default) — the file itself is fine; only console display is affected.
