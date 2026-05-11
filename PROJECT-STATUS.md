# Supplement Guide (VitaWise) — Project Status

**Site:** https://vitawise.life/ (Hugo + Netlify)
**Repo:** https://github.com/FlipperCat/SupplementProj
**Last refreshed:** 2026-05-11

## Overview
Evidence-based supplement information site. Hugo static site, Netlify auto-deploy on push to `main`. Affiliate model via Amway/Nutrilite.

## Current content

| Section | Count |
|---|---|
| Supplements (markdown) | 119 |
| Supplements in Stack Analyzer JSON | **119 — full parity** ✅ |
| Comparisons | 24 |
| Goals | 7 |
| Guides | 16 |
| Medications | 17 (added NSAIDs + antihistamines 2026-05-11) |
| Stacks | 11 |
| Timelines | 4 |

The Stack Analyzer DB is in 1:1 sync with the markdown catalog — each entry has the full schema (`id`, `name`, `type`, `category`, `dosage{min/typical/max/unit}`, `timing`, `withFood`, `withFat`, `benefits`, `goals`, `synergies`, `conflicts`, `absorptionCompetitors`, `depletedBy`, `amwayProduct`, `resultsTimeline`).

**JSON richness:**
- 119/119 have `synergies` populated
- 42/119 have `notes` field (added on the 6 new entries 2026-05-11)
- 23/119 are linked to a specific Amway product (affiliate)
- **15/119 have `conflicts` populated** (added 6 new with conflicts 2026-05-11) ← still thinnest area

## Uncommitted git state ⚠️

There's a substantial uncommitted backlog from the 2026-03-16 VitaWise cleanup that has never been pushed:

- 37 untracked files
- 26 modified files
- 12 deleted files

Run `git status` to inspect. Likely safe to commit + push as one cleanup batch — but eyeball the deletions first.

## Outstanding work

### High value
1. **Push the VitaWise cleanup commit.** 75 files of pending changes have been sitting since 2026-03-16. Site is live but the local repo and GitHub have drifted.
2. **Fill in `conflicts` arrays.** Only 9/113 entries flag drug or supplement conflicts. The Stack Analyzer's value is in catching these — gap is real.
3. **Replace placeholder analytics IDs** in `hugo.toml` (`G-XXXXXXXXXX`, `YOUR_GSC_VERIFICATION_ID`).

### Medium
4. Add structured data (`MedicalSupplement` schema.org) on supplement pages — no other supplement site does this well, and rich-results eligibility is real SEO leverage.
5. Add more entries to the `medications/` interaction guides (currently 8).
6. Quality pass on the 77 entries without a `notes` field — short clinical note where warranted.

### Optional / low priority
- More comparison articles (only 6 right now).
- Email capture / newsletter integration.
- `interactions.synergies` / `interactions.conflicts` top-level arrays in JSON for cross-supplement metadata that doesn't fit on a single entry.

## Architecture pointers
- `data/supplements.json` — Stack Analyzer DB (~111 KB, 113 entries)
- `layouts/_default/analyzer.html` (or `stack-generator.html`) — Stack Analyzer UI + logic
- `content/supplements/<slug>.md` — individual supplement articles
- `hugo.toml` — site config + analytics + affiliate URLs
- `netlify.toml` — build settings

## Quick commands
```bash
cd C:/Users/altst/supplement-guide

# Inspect uncommitted state
git status

# Build + serve locally (if Hugo installed)
hugo server -D

# Validate JSON
python -c "import json; print(len(json.load(open('data/supplements.json'))['supplements']))"
```

## Notes for future agents
- The catalog grew from 24 → 113 entries between March and May 2026 — old status docs that claim "Stack Analyzer broken / 24 supplements" are stale.
- Amway is the only affiliate currently wired; 23 entries link to specific products.
- `notes` is freeform and uses real em-dashes (—). Don't pass through any "fix mojibake" pass — the file is clean UTF-8.
