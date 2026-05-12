---
description: Audit https://vitawise.life for broken links and Hugo build issues, fix what's auto-fixable, commit and push. Falls back to filing an Obsidian Ideas/ brief if the fix needs judgement.
---

You are running the VitaWise maintenance audit. Goal: keep the site shipped and unbroken without user intervention.

## Steps

1. **Pull latest** from `origin/main` so you're not editing a stale tree:
   `git pull --rebase origin main`

2. **Run the live crawl**:
   `python -X utf8 scripts/crawl.py`
   This writes `.maintenance/<today>-broken.json` and exits non-zero if any broken links found.

3. **Run a local build sanity check**:
   `hugo --gc --minify`
   Any warnings or errors → investigate before touching anything else.

4. **If broken links found**, classify each:

   - **Layout-generated 404 from synergy/conflict label slugification** — already handled by `layouts/partials/related-supplement-link.html`. If new instances appear because a new layout was added, port the same pattern to it.

   - **Removed taxonomy or section references** (`/supplement_types/*`, `/medications/*`) — point them at the right replacement section (e.g. `/browse/` or `/interactions/`).

   - **Short-slug supplement references** (e.g. `/supplements/nac/` → `nac-n-acetylcysteine`) — add a Hugo `aliases:` entry to the canonical `.md` file. There's already a Python pattern in commit `4d2a90e` for this; reuse the approach.

   - **References to supplement pages that legitimately don't exist** (e.g. `/supplements/echinacea/` when there's no echinacea.md) — these are content writing decisions. Don't fabricate articles. Instead, either:
     a) If 1-2 references, edit the source content to remove the link (keep the text) — small, safe fix.
     b) If many references, queue an Obsidian Ideas/ brief titled `vitawise-add-<slug>.md` with `status: ready` so the dispatcher picks it up overnight. Brief should list every page referencing the missing slug.

   - **5xx or network errors** — log them and re-crawl once. If persistent, file an Ideas/ brief flagging a possible infra issue.

5. **After fixes**, rebuild + re-crawl to confirm the count dropped:
   `hugo --gc --minify && python -X utf8 scripts/crawl.py`

6. **If you made changes**, commit + push:
   - Commit message format: `Maintenance YYYY-MM-DD: fix N broken links` (one-line summary, then bullets per fix category)
   - Push to `origin main`
   - Netlify will auto-deploy

7. **If no changes were needed**, write a one-line entry to `.maintenance/<today>.log`: `OK  <crawled> pages, 0 broken.`

## Boundaries

- **Don't** touch `hugo.toml` analytics IDs (user provisions those manually).
- **Don't** create fabricated supplement content. If a page is genuinely missing, file an Ideas/ brief, don't invent it.
- **Don't** force-push or skip hooks.
- **Don't** add new dependencies without checking with the user first.
- If something needs human judgement (layout redesign, content strategy decisions, anything ambiguous), file an Ideas/ brief at `C:\Users\altst\OneDrive\Desktop\OBSIDIAN BRAIN\OBSIDIAN BRAIN\Ideas\vitawise-<slug>.md` with `status: ready` and exit cleanly.

## Sanity checks before push

- `hugo --gc --minify` finishes with 0 warnings
- `python -X utf8 scripts/crawl.py` reports fewer broken than at the start (ideally 0)
- `git diff` shows only intended file changes (no temp files, no `.maintenance/` artifacts staged)
