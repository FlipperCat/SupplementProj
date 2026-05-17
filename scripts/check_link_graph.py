#!/usr/bin/env python3
"""Audit internal cross-links on supplement pages.

For every ``content/supplements/*.md`` (excluding ``_index.md``) verify that
the page links to:

* at least 3 other supplement pages
* at least 1 stack page
* at least 1 medication-interaction page (under ``content/medications/`` or
  ``content/interactions/``)

Supports both Hugo shortcodes (``{{< ref "..." >}}`` / ``{{< relref "..." >}}``)
and standard markdown links ``[text](url)``.

CLI:
    check_link_graph.py [--root REPO_ROOT] [--report-md PATH] [--fix]

Exit code 0 if every page passes, 1 if any page fails. With ``--fix`` failing
pages get an appended ``## Related supplements`` section with enough links to
satisfy the rule.

Stdlib-only. Deterministic ordering throughout.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

SHORTCODE_RE = re.compile(r"{{[%<]\s*(?:ref|relref)\s+\"([^\"]+)\"\s*[%>]}}")
MD_LINK_RE = re.compile(r"(?<!\!)\[([^\]\n]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^\s*```")
TITLE_RE = re.compile(r'^\s*title\s*:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)

MEDICATION_SECTIONS = {"medications", "interactions", "medication-interactions"}


@dataclass
class PageReport:
    slug: str
    path: Path
    supplements: list[str] = field(default_factory=list)
    stacks: list[str] = field(default_factory=list)
    medications: list[str] = field(default_factory=list)

    @property
    def passes(self) -> bool:
        return (
            len(self.supplements) >= 3
            and len(self.stacks) >= 1
            and len(self.medications) >= 1
        )

    def short_line(self) -> str:
        s_ok = "OK" if len(self.supplements) >= 3 else f"(need 3)"
        st_ok = "OK" if len(self.stacks) >= 1 else f"(need 1)"
        m_ok = "OK" if len(self.medications) >= 1 else f"(need 1)"
        return (
            f"{self.path.name}: "
            f"supp={len(self.supplements)} {s_ok}, "
            f"stack={len(self.stacks)} {st_ok}, "
            f"med={len(self.medications)} {m_ok}"
        )


def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for candidate in (cur, *cur.parents):
        if (candidate / "hugo.toml").exists() or (candidate / "config.toml").exists():
            return candidate
    raise SystemExit(f"could not find hugo.toml/config.toml above {start}")


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip() != "---":
        return "", text
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            return "".join(lines[: i + 1]), "".join(lines[i + 1 :])
    return "", text


def strip_code_fences(body: str) -> str:
    out: list[str] = []
    in_fence = False
    for line in body.splitlines(keepends=True):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "".join(out)


def _normalize_target(target: str) -> str:
    t = target.split("#", 1)[0].split("?", 1)[0].replace("\\", "/")
    if t.endswith(".md"):
        t = t[:-3]
    return t.strip("/")


def classify_target(
    target: str,
    current_slug: str,
    current_section: str,
) -> tuple[str, str] | None:
    norm = _normalize_target(target)
    if not norm:
        return None
    parts = norm.split("/")
    if parts and parts[0] == "content":
        parts = parts[1:]
    if not parts:
        return None
    if len(parts) == 1:
        section = current_section
        slug = parts[0]
    else:
        section = parts[0]
        slug = parts[-1]
    slug = slug.lower()
    if not slug or slug == "_index":
        return None
    if section == "supplements":
        if slug == current_slug:
            return None
        return ("supplement", slug)
    if section == "stacks":
        return ("stack", slug)
    if section in MEDICATION_SECTIONS:
        return ("medication", slug)
    return None


def extract_links(
    body: str, current_slug: str, current_section: str
) -> list[tuple[str, str]]:
    cleaned = strip_code_fences(body)
    raw_targets: list[str] = list(SHORTCODE_RE.findall(cleaned))
    for _text, url in MD_LINK_RE.findall(cleaned):
        if url.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            continue
        raw_targets.append(url)
    found: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for t in raw_targets:
        c = classify_target(t, current_slug, current_section)
        if c and c not in seen:
            seen.add(c)
            found.append(c)
    return found


def humanize(slug: str) -> str:
    return " ".join(word.capitalize() for word in slug.split("-"))


def page_title(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return humanize(path.stem)
    fm, _ = split_frontmatter(text)
    m = TITLE_RE.search(fm)
    if m:
        return m.group(1).strip()
    return humanize(path.stem)


# ---------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------


def audit_pages(repo_root: Path) -> list[PageReport]:
    supp_dir = repo_root / "content" / "supplements"
    if not supp_dir.is_dir():
        raise SystemExit(f"missing {supp_dir}")
    reports: list[PageReport] = []
    for path in sorted(supp_dir.glob("*.md")):
        if path.name == "_index.md":
            continue
        slug = path.stem.lower()
        text = path.read_text(encoding="utf-8")
        _fm, body = split_frontmatter(text)
        links = extract_links(body, slug, "supplements")
        rep = PageReport(slug=slug, path=path)
        for kind, target_slug in links:
            if kind == "supplement":
                rep.supplements.append(target_slug)
            elif kind == "stack":
                rep.stacks.append(target_slug)
            elif kind == "medication":
                rep.medications.append(target_slug)
        reports.append(rep)
    return reports


def render_report(
    reports: list[PageReport], as_markdown: bool
) -> str:
    failing = [r for r in reports if not r.passes]
    passing = len(reports) - len(failing)
    lines: list[str] = []
    if as_markdown:
        lines.append("# Link graph audit")
        lines.append("")
        lines.append(
            f"- Pages scanned: **{len(reports)}**"
        )
        lines.append(
            f"- Passing (supp>=3, stack>=1, med>=1): **{passing}**"
        )
        lines.append(f"- Failing: **{len(failing)}**")
        lines.append("")
        if failing:
            lines.append("## Failing pages")
            lines.append("")
            for r in failing:
                rel = r.path.relative_to(r.path.parents[2]).as_posix()
                lines.append(f"- `{rel}` -- {r.short_line()}")
            lines.append("")
        else:
            lines.append("All pages pass.")
    else:
        lines.append(f"Pages scanned: {len(reports)}")
        lines.append(f"Passing: {passing}")
        lines.append(f"Failing: {len(failing)}")
        if failing:
            lines.append("")
            lines.append("Failing pages:")
            for r in failing:
                lines.append(f"  {r.short_line()}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Fix mode
# ---------------------------------------------------------------------------


@dataclass
class FixSources:
    interactions: dict
    stack_map: dict[str, list[str]]
    supplement_slugs: list[str]
    supplement_titles: dict[str, str]
    stack_slugs: list[str]
    stack_titles: dict[str, str]
    # medication key (e.g. "ssri") -> (url, display_name)
    medication_pages: dict[str, tuple[str, str]]
    # supplement slug -> list of medication keys mentioning it
    medications_for_supp: dict[str, list[str]]
    # supplement slug -> list of co-occurring supplement slugs (deterministic)
    supp_co_occurrence: dict[str, list[str]]
    stack_map_missing: bool


def load_fix_sources(repo_root: Path) -> FixSources:
    data_dir = repo_root / "data"
    interactions_path = data_dir / "interactions.json"
    interactions = json.loads(interactions_path.read_text(encoding="utf-8"))

    stack_map_path = data_dir / "stack_map.json"
    stack_map_missing = not stack_map_path.exists()
    if stack_map_missing:
        stack_map: dict[str, list[str]] = {}
    else:
        stack_map = json.loads(stack_map_path.read_text(encoding="utf-8"))

    supp_dir = repo_root / "content" / "supplements"
    supplement_slugs = sorted(
        p.stem.lower() for p in supp_dir.glob("*.md") if p.name != "_index.md"
    )
    supplement_titles = {
        slug: page_title(supp_dir / f"{slug}.md") for slug in supplement_slugs
    }

    stacks_dir = repo_root / "content" / "stacks"
    stack_slugs = sorted(
        p.stem.lower() for p in stacks_dir.glob("*.md") if p.name != "_index.md"
    )
    stack_titles = {
        slug: page_title(stacks_dir / f"{slug}.md") for slug in stack_slugs
    }

    # Build medication page index. interactions.json has medication keys with
    # an optional guide_url. We accept the guide_url when present and point to
    # a real content page; otherwise probe the common naming conventions.
    medication_pages: dict[str, tuple[str, str]] = {}
    medications = interactions.get("medications", {})
    for key, entry in sorted(medications.items()):
        name = entry.get("name", humanize(key))
        url: str | None = None
        guide_url = (entry.get("guide_url") or "").strip()
        if guide_url:
            cand_path = _url_to_content_path(repo_root, guide_url)
            if cand_path and cand_path.exists():
                url = _content_path_to_url(repo_root, cand_path)
        if not url:
            for folder, suffix in (
                ("interactions", "-supplements"),
                ("medications", "-supplements"),
                ("medications", "-support"),
                ("medications", "-nutrients"),
                ("medications", "-medication-supplements"),
                ("interactions", ""),
                ("medications", ""),
            ):
                cand = repo_root / "content" / folder / f"{key}{suffix}.md"
                if cand.exists():
                    url = f"/{folder}/{key}{suffix}/"
                    break
        if url:
            medication_pages[key] = (url, name)

    medications_for_supp: dict[str, list[str]] = {}
    supp_co_occurrence: dict[str, set[str]] = {}
    for key, entry in medications.items():
        slugs_here: set[str] = set()
        for bucket in ("safe", "caution", "avoid"):
            for item in entry.get(bucket, []):
                slug = (item.get("slug") or "").lower()
                if slug:
                    slugs_here.add(slug)
        for slug in slugs_here:
            medications_for_supp.setdefault(slug, []).append(key)
            others = slugs_here - {slug}
            supp_co_occurrence.setdefault(slug, set()).update(others)
    medications_for_supp = {
        k: sorted(set(v)) for k, v in medications_for_supp.items()
    }
    supp_co_occurrence_sorted = {
        k: sorted(v) for k, v in supp_co_occurrence.items()
    }

    return FixSources(
        interactions=interactions,
        stack_map=stack_map,
        supplement_slugs=supplement_slugs,
        supplement_titles=supplement_titles,
        stack_slugs=stack_slugs,
        stack_titles=stack_titles,
        medication_pages=medication_pages,
        medications_for_supp=medications_for_supp,
        supp_co_occurrence=supp_co_occurrence_sorted,
        stack_map_missing=stack_map_missing,
    )


def _url_to_content_path(repo_root: Path, url: str) -> Path | None:
    norm = _normalize_target(url)
    if not norm:
        return None
    return repo_root / "content" / (norm + ".md")


def _content_path_to_url(repo_root: Path, path: Path) -> str:
    rel = path.relative_to(repo_root / "content").as_posix()
    if rel.endswith(".md"):
        rel = rel[:-3]
    return "/" + rel + "/"


def choose_supplement_fixes(
    rep: PageReport,
    sources: FixSources,
    needed: int,
    already: set[tuple[str, str]],
) -> list[tuple[str, str, str]]:
    """Return list of (slug, url, display_name) for supplements to add."""
    picks: list[tuple[str, str, str]] = []
    used_slugs: set[str] = {s for kind, s in already if kind == "supplement"}
    used_slugs.add(rep.slug)

    def try_add(slug: str) -> bool:
        if slug in used_slugs:
            return False
        if slug not in sources.supplement_titles:
            return False
        title = sources.supplement_titles[slug]
        picks.append((slug, f"/supplements/{slug}/", title))
        used_slugs.add(slug)
        return len(picks) >= needed

    for candidate in sources.supp_co_occurrence.get(rep.slug, []):
        if try_add(candidate):
            return picks
    for candidate in sources.supplement_slugs:
        if try_add(candidate):
            return picks
    return picks


def choose_stack_fix(
    rep: PageReport,
    sources: FixSources,
    already: set[tuple[str, str]],
    warnings: list[str],
) -> tuple[str, str, str] | None:
    used_slugs = {s for kind, s in already if kind == "stack"}
    mapped = sources.stack_map.get(rep.slug, [])
    for candidate in mapped:
        c = candidate.lower()
        if c not in used_slugs and c in sources.stack_titles:
            return (c, f"/stacks/{c}/", sources.stack_titles[c])
    if not mapped:
        if sources.stack_map_missing:
            warnings.append(
                f"stack_map.json missing -- using alphabetical fallback for {rep.slug}"
            )
        else:
            warnings.append(
                f"no stack_map entry for {rep.slug} -- using alphabetical fallback"
            )
    for candidate in sources.stack_slugs:
        if candidate not in used_slugs:
            return (candidate, f"/stacks/{candidate}/", sources.stack_titles[candidate])
    return None


def choose_medication_fix(
    rep: PageReport,
    sources: FixSources,
    already: set[tuple[str, str]],
) -> tuple[str, str, str] | None:
    used_slugs = {s for kind, s in already if kind == "medication"}
    keys = sources.medications_for_supp.get(rep.slug, [])
    for key in keys:
        page = sources.medication_pages.get(key)
        if not page:
            continue
        url, name = page
        # Derive a slug from the URL's final segment so we can dedupe across
        # both markdown and shortcode link forms.
        page_slug = _normalize_target(url).split("/")[-1]
        if page_slug in used_slugs:
            continue
        return (page_slug, url, name)
    # Fallback: any medication page not already linked, alphabetical.
    for key in sorted(sources.medication_pages.keys()):
        url, name = sources.medication_pages[key]
        page_slug = _normalize_target(url).split("/")[-1]
        if page_slug not in used_slugs:
            return (page_slug, url, name)
    return None


HAS_RELATED_RE = re.compile(r"^##\s+Related supplements\b", re.MULTILINE)


def apply_fix(rep: PageReport, sources: FixSources, warnings: list[str]) -> bool:
    """Append a Related section to rep.path if needed. Return True if changed."""
    text = rep.path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    if HAS_RELATED_RE.search(body):
        return False
    already: set[tuple[str, str]] = set()
    for s in rep.supplements:
        already.add(("supplement", s))
    for s in rep.stacks:
        already.add(("stack", s))
    for s in rep.medications:
        already.add(("medication", s))

    supp_needed = max(0, 3 - len(rep.supplements))
    stack_needed = max(0, 1 - len(rep.stacks))
    med_needed = max(0, 1 - len(rep.medications))

    supps = choose_supplement_fixes(rep, sources, supp_needed, already)
    for slug, _url, _name in supps:
        already.add(("supplement", slug))

    stack: tuple[str, str, str] | None = None
    if stack_needed:
        stack = choose_stack_fix(rep, sources, already, warnings)
        if stack:
            already.add(("stack", stack[0]))

    med: tuple[str, str, str] | None = None
    if med_needed:
        med = choose_medication_fix(rep, sources, already)
        if med:
            already.add(("medication", med[0]))

    if not (supps or stack or med):
        return False

    section_lines = ["", "## Related supplements", ""]
    if supps:
        section_lines.append("**Other supplements:**")
        section_lines.append("")
        for _slug, url, name in supps:
            section_lines.append(f"- [{name}]({url})")
        section_lines.append("")
    if stack:
        _slug, url, name = stack
        section_lines.append(f"**Stack:** [{name}]({url})")
        section_lines.append("")
    if med:
        _slug, url, name = med
        section_lines.append(f"**Medication interactions:** [{name}]({url})")
        section_lines.append("")

    new_body = body
    if not new_body.endswith("\n"):
        new_body += "\n"
    new_body += "\n".join(section_lines).rstrip() + "\n"
    rep.path.write_text(fm + new_body, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=None, help="repo root override")
    parser.add_argument("--fix", action="store_true", help="append Related sections to failing pages")
    parser.add_argument("--report-md", type=Path, default=None, help="write markdown report here instead of stdout")
    args = parser.parse_args(argv)

    repo_root = args.root.resolve() if args.root else find_repo_root(Path.cwd())

    reports = audit_pages(repo_root)
    warnings: list[str] = []

    if args.fix:
        sources = load_fix_sources(repo_root)
        for rep in reports:
            if rep.passes:
                continue
            changed = apply_fix(rep, sources, warnings)
            if changed:
                # Re-scan that page so the report reflects post-fix state.
                text = rep.path.read_text(encoding="utf-8")
                _fm, body = split_frontmatter(text)
                links = extract_links(body, rep.slug, "supplements")
                rep.supplements = [s for k, s in links if k == "supplement"]
                rep.stacks = [s for k, s in links if k == "stack"]
                rep.medications = [s for k, s in links if k == "medication"]

    body = render_report(reports, as_markdown=bool(args.report_md))
    if warnings:
        warn_block = "\n".join(f"WARNING: {w}" for w in warnings) + "\n"
        if args.report_md:
            body += "\n## Warnings\n\n" + "\n".join(f"- {w}" for w in warnings) + "\n"
        else:
            body = warn_block + body

    if args.report_md:
        args.report_md.parent.mkdir(parents=True, exist_ok=True)
        args.report_md.write_text(body, encoding="utf-8")
    else:
        sys.stdout.write(body)

    return 0 if all(r.passes for r in reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
