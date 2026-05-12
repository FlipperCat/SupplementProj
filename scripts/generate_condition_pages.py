"""Generate /content/for/<slug>/index.md pages from data/symptoms.json.

Each page is data-driven: an intro that acknowledges the symptom + mainstream
context, then a generated narrative summary. The bulk of the dynamic content
(supplement list, related goals, related conditions) is rendered by the
layout at layouts/for/single.html.

Run from repo root:
    python scripts/generate_condition_pages.py
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SYMPTOMS_FILE = REPO / "data" / "symptoms.json"
SUPPLEMENTS_FILE = REPO / "data" / "supplements.json"
OUT_DIR = REPO / "content" / "for"


def load_data():
    with SYMPTOMS_FILE.open(encoding="utf-8") as f:
        symptoms = json.load(f)["symptoms"]
    with SUPPLEMENTS_FILE.open(encoding="utf-8") as f:
        supplements = {s["id"]: s for s in json.load(f)["supplements"]}
    return symptoms, supplements


CATEGORY_BLURB = {
    "Energy & Focus": "Energy and focus complaints rarely have a single cause. Sleep debt, nutrient gaps, thyroid function, stress, and lifestyle inputs like caffeine and screens all interact.",
    "Sleep": "Sleep complaints are usually multi-factorial. Stress, light exposure, blood-sugar swings, alcohol, and irregular schedules each affect sleep architecture independent of supplements.",
    "Mood": "Mood-related symptoms are influenced by sleep, light exposure, exercise, social connection, gut health, and hormones — supplements work best as one input among several.",
    "Digestion": "Digestive symptoms commonly reflect the interaction of food choices, microbiome, motility, and stress. A short food-symptom diary often surfaces patterns faster than supplements alone.",
    "Pain & Inflammation": "Pain and inflammation respond to mechanical, nutritional, and lifestyle inputs. Supplements may complement — but do not replace — appropriate diagnosis and physical care.",
    "Hormonal": "Hormonal symptoms often shift with sleep, body composition, stress, training, and age. Lab work (when appropriate) usually beats guessing.",
    "Skin & Hair": "Skin and hair are visible outputs of internal status — protein intake, iron, micronutrients, hormones, and topical care all matter. Patience helps; hair and skin turnover is slow.",
    "Metabolic": "Metabolic markers respond first to nutrition, body composition, sleep, and movement. Supplements may add a marginal edge once those basics are in place.",
    "Other": "This concern can stem from several systems. The framing below is informational, not diagnostic.",
}


def intro_paragraph(symptom: dict, supplements: dict) -> str:
    """Build the long intro section: ~600 words of cautious, framing-aware text."""
    name = symptom["display_name"]
    cname = symptom["conventional_name"]
    desc = symptom["description"]
    cat = symptom["category"]
    cat_blurb = CATEGORY_BLURB.get(cat, CATEGORY_BLURB["Other"])

    # Pick top 3 supplements for the lede
    sup_objs = [supplements[s] for s in symptom["supplements"] if s in supplements][:3]
    sup_names = [s["name"] for s in sup_objs]
    sup_inline = (
        ", ".join(sup_names[:-1]) + ", and " + sup_names[-1]
        if len(sup_names) > 1
        else sup_names[0]
    )

    return f"""## Understanding {name}

{name} — also discussed clinically as {cname.lower()} — is a concern that brings people to supplement research every day. {desc} It is not a single diagnosis and not every case has the same underlying driver, which is one reason a one-size-fits-all "best supplement for {name.lower()}" answer rarely exists.

{cat_blurb} That context matters because supplements work best when stacked on top of the basics — adequate sleep, reasonable nutrition, movement, and stress management — rather than substituting for them.

### What users commonly research

People searching for help with {name.lower()} most often look into a small set of supplements: {sup_inline}, along with a few others detailed below. These show up repeatedly in user discussions, traditional use, and the more accessible research literature. That is not the same as clinical proof for any one person — many of these supplements have mixed or modest evidence, and individual response varies.

The cautious framing in this guide is intentional. Phrases like *may support*, *research suggests*, and *users commonly consider* reflect the uncertainty that is honest about most supplement research, especially for symptom-based use rather than diagnosed disease.

### When supplements are not the right first move

A few situations call for medical evaluation before — or instead of — experimenting with supplements:

- The symptom is new, severe, or worsening quickly.
- It interferes meaningfully with daily life, sleep, or work.
- It accompanies other concerning signs (chest pain, neurological changes, fever, blood in stool or urine, unexplained weight loss).
- You take prescription medications that could interact with common supplements (blood thinners, antidepressants, immune-modulating drugs, thyroid medication, and many others).
- The underlying issue is likely structural (e.g., a slipped disc, a thyroid tumor, anemia from blood loss) rather than nutritional.

In those cases, a clinician visit, basic labs, and an actual diagnosis save time and prevent misplaced confidence in any single supplement.

### How to read the supplement list below

For each supplement we surface:

- **What it is commonly explored for** — the cluster of benefits people associate with it.
- **The typical research-cited dose range** — a starting reference, not a prescription.
- **Usual timing** — morning, evening, with food, etc.
- **Who should be cautious or avoid** — known interactions, particularly with prescription drugs.
- **A short note** — practical context, what to look for in a product, what tends to disappoint.
- **A link to the full supplement page** — every supplement here has a deeper guide.

None of this is medical advice. None of it replaces the conversation you should have with a clinician or pharmacist if you are on prescriptions, pregnant, breastfeeding, managing a chronic condition, or about to start something new.

### A note on expectations

Supplements that influence neurotransmitters, hormones, or inflammation usually need weeks — sometimes a few months — to show their full effect. The most common reason people decide a supplement "did not work" is that they tried it for ten days, at an arbitrary dose, alongside everything else that was going wrong with their sleep, stress, or schedule. A more useful experiment is one variable at a time, a realistic dose, and a written record of how you feel over four to eight weeks.

With that context, here is what users commonly consider when researching {name.lower()}."""


def front_matter(symptom: dict) -> str:
    name = symptom["display_name"]
    cname = symptom["conventional_name"]
    slug = symptom["slug"]
    tags = [slug, symptom["category"].lower().replace(" & ", "-").replace(" ", "-")]
    # add a couple supplement-tag breadcrumbs
    tags.extend(symptom["supplements"][:3])
    tag_lines = "\n".join(f'  - "{t}"' for t in tags)

    return f"""---
title: "Supplements Commonly Considered for {name}"
date: 2025-01-15
draft: false
tagline: "What people research when looking into {name.lower()} ({cname.lower()}) — cautious, evidence-aware overview."
description: "An educational overview of supplements users commonly research for {name.lower()}. Not medical advice. Includes typical doses, timing, and who should be cautious."
symptom_slug: "{slug}"
tags:
{tag_lines}
aliases:
  - "/for/{slug}/"
---
"""


def write_page(symptom: dict, supplements: dict):
    slug = symptom["slug"]
    page_dir = OUT_DIR / slug
    page_dir.mkdir(parents=True, exist_ok=True)
    page = page_dir / "index.md"

    body = front_matter(symptom) + "\n" + intro_paragraph(symptom, supplements) + "\n"
    page.write_text(body, encoding="utf-8")


def write_section_index(symptoms):
    """Build content/for/_index.md grouped by category."""
    groups: dict[str, list] = {}
    for s in symptoms:
        groups.setdefault(s["category"], []).append(s)

    order = [
        "Energy & Focus",
        "Sleep",
        "Mood",
        "Digestion",
        "Pain & Inflammation",
        "Hormonal",
        "Skin & Hair",
        "Metabolic",
        "Other",
    ]

    lines = [
        "---",
        'title: "Supplement Guides by Symptom and Condition"',
        'description: "50 condition and symptom pages explaining what users commonly research, with cautious supplement notes — not medical advice."',
        'tagline: "Find research-aware supplement notes by what you are actually dealing with."',
        "---",
        "",
        "## Browse by Concern",
        "",
        "Pages are organized by what people search for rather than by clinical taxonomy. Every page surfaces the supplements users commonly consider, typical doses, who should be cautious, and links to the full supplement guides. None of this is medical advice.",
        "",
    ]

    for cat in order:
        if cat not in groups:
            continue
        lines.append(f"### {cat}")
        lines.append("")
        for s in sorted(groups[cat], key=lambda x: x["display_name"]):
            lines.append(
                f"- **[{s['display_name']}](/for/{s['slug']}/)** — {s['description'][:120].rstrip('.').rstrip(',')}…"
            )
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            "## How to Use These Pages",
            "",
            "1. **Start with the concern you actually have**, not the supplement you already heard about.",
            "2. **Read the framing** at the top — most symptoms are multi-factorial and supplements are one of several inputs.",
            "3. **Check the cautions** if you take prescription medication.",
            "4. **Pick one supplement at a time** and give it a realistic trial (typically 4–8 weeks).",
            "5. **Talk to a clinician** if a symptom is new, severe, persistent, or accompanied by red-flag signs.",
            "",
        ]
    )

    (OUT_DIR / "_index.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    symptoms, supplements = load_data()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for sym in symptoms:
        write_page(sym, supplements)
    write_section_index(symptoms)
    print(f"Generated {len(symptoms)} condition pages + index.")


if __name__ == "__main__":
    main()
