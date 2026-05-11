# Checkpoint — 2026-05-11

## Done (this session, headless dispatcher run)

- Added 6 new supplement markdown articles to `content/supplements/`:
  - `dhea.md`
  - `pregnenolone.md`
  - `fadogia-agrestis.md`
  - `pterostilbene.md`
  - `dandelion-root.md`
  - `artichoke-extract.md`
- Added matching entries (all with `notes` and `conflicts` populated) to `data/supplements.json`. Total now 119 supplements.
- Added 3 new comparison articles to `content/comparisons/`:
  - `nmn-vs-nr.md`
  - `pterostilbene-vs-resveratrol.md`
  - `tongkat-ali-vs-fadogia.md`
- Added 2 new medication interaction guides to `content/medications/`:
  - `nsaid-supplements.md`
  - `antihistamine-supplements.md`
- Updated `PROJECT-STATUS.md` counts (119 supplements, 24 comparisons, 17 medications).

## Next

- Substantial uncommitted backlog (75+ files) — review and commit when human is available. Don't auto-commit; user wants eyeball check first.
- Fill in `conflicts` arrays on the remaining supplements without them (still ~104 entries lack conflict data).
- Add schema.org `MedicalSupplement` structured data on supplement pages — solid SEO leverage; no competitor doing it well.
- Replace placeholder analytics IDs in `hugo.toml` (`G-XXXXXXXXXX`, `YOUR_GSC_VERIFICATION_ID`) — needs real values.
- Quality pass on the ~77 entries without a `notes` field.

## In flight

None — all targeted work completed in this run.

## Gotchas discovered

- `data/supplements.json` requires UTF-8 explicit on Windows Python (default cp1252 codec fails on em-dashes).
- Hugo isn't installed locally (no quick `hugo --quiet` validation possible from this session) — relying on Netlify build to catch any frontmatter issues.
- Added `notes` field to every new supplement to set a quality bar; the existing entries that lack notes are mostly the older bulk-import batch.
