---
title: "Stack Analyzer"
description: "Analyze your supplement stack for synergies, conflicts, timing issues, and gaps. Get personalized recommendations based on your goals."
layout: "analyzer"
---

## What the Stack Analyzer does

The Stack Analyzer takes the supplements you're already taking — or considering — and checks them against a database of 80+ evidence-backed entries to surface four things:

- **Synergies** — pairs that work *better together* than alone (e.g., Vitamin D + K2 for calcium routing, Magnesium + B6 for absorption).
- **Conflicts** — pairs that should be **separated** in time, or avoided entirely (e.g., Calcium blocking Iron and Zinc absorption, Green Tea Extract reducing non-heme iron uptake).
- **Timing issues** — supplements that compete for the same transporter or shouldn't share a meal window.
- **Gaps** — common supporting nutrients missing from your stack given your goals (e.g., taking high-dose Zinc without any Copper).

It also produces an **optimal timing schedule** (AM / with-meal / PM / fasting) so you stop accidentally cancelling out your own stack.

## How to use it

1. **Search and add** each supplement you take in the box above. Autocomplete matches common names and the most popular forms (e.g., "magnesium glycinate" → Magnesium).
2. **Pick a goal** (sleep, energy, recovery, longevity, etc.) — the analyzer biases its gap suggestions toward your goal.
3. **Read the results panel.** Synergies are highlighted in green, conflicts in red, timing notes in amber.
4. **Use the generated schedule** as a starting point. The analyzer groups items into AM / with-meal / PM / fasting slots based on each item's absorption profile.
5. **Iterate.** Drop or add items and the analysis updates live — no page reload needed.

## Examples

**Example 1 — A common "more is better" stack that's quietly cancelling itself**

Inputs: *Multivitamin (with iron), Calcium 1,000 mg, Zinc 30 mg, Magnesium 400 mg, all taken together at breakfast.*

What the analyzer flags:
- Calcium blocks ~50% of the iron in the multivitamin when taken in the same window.
- Zinc and Calcium compete for the same transporter — taking both at once drops Zinc absorption.
- Magnesium is fine to take with food, but combining all four turns a 30 mg Zinc dose into roughly an effective 12–15 mg.

Recommended split: multivitamin + Zinc at breakfast, Calcium + Magnesium at dinner.

**Example 2 — Sleep stack with a hidden gap**

Inputs: *Magnesium Glycinate 400 mg PM, L-Theanine 200 mg PM, Melatonin 0.5 mg.*

What the analyzer flags:
- Strong synergy: Magnesium + L-Theanine + Melatonin is one of the most evidence-backed sleep stacks.
- Gap: no GABA-pathway support beyond L-Theanine — Apigenin (50 mg) or Glycine (3 g) are common additions if onset latency is still long.
- Timing: take Melatonin **30 minutes** before bed, not at lights-out.

## FAQ

<details>
<summary>Is this medical advice?</summary>
No. The analyzer surfaces evidence-backed interactions and gaps, but it doesn't know your labs, medications, or conditions. Talk to your doctor or pharmacist before adding anything new, especially if you take prescription medication.
</details>

<details>
<summary>What if a supplement I take isn't in the database?</summary>
Search by the active ingredient (e.g., "ashwagandha" rather than a brand name). Most stack issues are at the ingredient level — if the active is in the database, the analyzer can reason about it. If you find a real gap, let us know via the <a href="/contact/">contact page</a>.
</details>

<details>
<summary>Why does the schedule split things into so many slots?</summary>
Because the alternative is wasted money. Fat-soluble vitamins (A, D, E, K) need dietary fat. Iron is blocked by Calcium, Zinc, and tannins (coffee/tea). Magnesium relaxes — it belongs in the evening. Lumping everything into one "with breakfast" dose can cut absorption by a third or more.
</details>

<details>
<summary>How accurate are the synergy and conflict calls?</summary>
Each interaction in the database is tagged with the strength of the underlying evidence (clinical trial, mechanism-only, or observational). The analyzer shows the strength inline so you can weight your decisions. We update the database as new research lands.
</details>

<details>
<summary>Can I save my stack?</summary>
The analyzer state lives in your browser. Save the URL after building a stack to come back to it. We don't store anything server-side.
</details>

## Related

- [Browse supplements by goal](/goals/)
- [Supplement Comparison Tool](/supplement-comparison/) — compare forms (e.g., Magnesium Glycinate vs Citrate)
- [Cost Calculator](/cost-calculator/) — once your stack is dialed, see what it'll cost monthly
- [Medication Checker](/medication-checker/) — make sure your stack is safe with any prescriptions
