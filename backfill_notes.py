"""Backfill `notes` field on supplements that lack one.

Notes are short (one short sentence, occasionally two), actionable, clinical.
Style matches existing entries: practical tip, deficiency caveat, or interaction flag.
"""
import json
from pathlib import Path

# Concise clinical notes — one practical tip per supplement.
NOTES = {
    "vitamin-d3": "Get 25-OH vitamin D tested first; target serum 40-60 ng/mL. Pair with K2 if dosing >2000 IU daily.",
    "magnesium": "Glycinate or threonate forms are best tolerated. Oxide is poorly absorbed and laxative-only.",
    "omega-3": "Look for TG (triglyceride) form and a combined EPA+DHA total — not just fish oil mg. Refrigerate to prevent rancidity.",
    "vitamin-k2": "MK-7 form has a longer half-life than MK-4; 100-200 mcg daily is plenty. Avoid if on warfarin.",
    "zinc": "Long-term dosing >25 mg/day depletes copper — add 1-2 mg copper if supplementing chronically.",
    "b-complex": "Choose methylated forms (methylfolate, methylcobalamin) if you have MTHFR variants or sensitivity to standard B-complex.",
    "vitamin-c": "Liposomal or split dosing improves absorption above 500 mg. Megadoses (>2g) can cause GI upset.",
    "ashwagandha": "KSM-66 and Sensoril are the studied extracts — generic root powder is much weaker. Cycle off every 8-12 weeks.",
    "creatine": "Skip the loading phase; 5 g/day reaches saturation in ~4 weeks with less bloating. Monohydrate is the only form with strong evidence.",
    "l-theanine": "Stacks well with caffeine at a 2:1 ratio (200 mg theanine : 100 mg caffeine) for clean focus.",
    "coq10": "Use ubiquinol (not ubiquinone) over age 40 — much better absorbed. Statin users especially benefit.",
    "probiotics": "Strain specificity matters more than CFU count. Refrigerated, multi-strain products outperform shelf-stable in most studies.",
    "collagen": "Take with vitamin C to support collagen synthesis. Hydrolyzed peptides (2-5 kDa) absorb best.",
    "alpha-lipoic-acid": "R-ALA form is more bioactive than racemic. Take on an empty stomach away from minerals (chelates them).",
    "rhodiola": "Look for SHR-5 extract standardized to 3% rosavins / 1% salidroside. Best taken in the morning — can be stimulating.",
    "nac": "Take on an empty stomach for best absorption. May reduce zinc and copper over time — monitor if dosing long-term.",
    "selenium": "Toxic above 400 mcg/day — stick to 100-200 mcg. Brazil nuts (1-2/day) are a food alternative.",
    "berberine": "Split into 500 mg doses 2-3x daily with meals — short half-life. Don't combine with metformin without a doctor.",
    "lions-mane": "Effects on cognition build slowly — 8-12 weeks for noticeable changes. Dual-extract (water + alcohol) products are most complete.",
    "glycine": "3 g before bed improves sleep onset and quality. Tastes sweet, dissolves well in water.",
    "acetyl-l-carnitine": "Take in the morning — can be stimulating. The acetyl form crosses the blood-brain barrier better than plain L-carnitine.",
    "alpha-gpc": "More bioavailable than CDP-choline but has a slight depressive mood effect in some users at high doses (>600 mg).",
    "apigenin": "50 mg before bed improves sleep depth. Found naturally in chamomile and parsley but supplemental doses are much higher.",
    "astaxanthin": "Fat-soluble — must take with a meal containing fat. 4-12 mg daily; the most potent natural antioxidant by some measures.",
    "boron": "3-10 mg daily supports hormone balance and bone health. Megadoses (>20 mg) can disrupt hormones in the other direction.",
    "cdp-choline": "Citicoline form raises both choline and uridine. Better tolerated than alpha-GPC at high doses.",
    "chlorella": "Choose broken-cell-wall chlorella for absorption. May bind to heavy metals — useful for detox protocols but check sourcing for contamination.",
    "chromium": "Picolinate form is best studied for glucose support. Effects are modest — diet and exercise matter more.",
    "citrulline": "L-citrulline malate at 6-8 g pre-workout raises arginine more effectively than arginine itself. Take 30-60 min before training.",
    "digestive-enzymes": "Take with the first bite of the meal. Useful for specific issues (pancreatic insufficiency, lactose intolerance) — not a daily multi-enzyme habit.",
    "fenugreek": "May lower blood sugar — caution with diabetes meds. Body odor side effect (maple syrup smell) is common.",
    "ginseng": "Korean (Panax) is stimulating; American is calming. Cycle 8 weeks on, 2 weeks off to avoid tolerance.",
    "glucosamine": "Sulfate form has stronger evidence than HCl. Allow 4-8 weeks for joint benefits; not all responders.",
    "glutamine": "Most beneficial for gut healing and high-stress states; healthy people get enough from diet. 5-10 g daily for therapeutic use.",
    "hmb": "Most effective in untrained, older, or catabolic states. Take 3 g daily, split into 3 doses around training/meals.",
    "holy-basil": "Tulsi extract supports cortisol balance. Often combined with ashwagandha for adaptogen stacks.",
    "lutein-zeaxanthin": "10 mg lutein + 2 mg zeaxanthin is the standard combo. Take with a fat-containing meal for absorption.",
    "maca": "Gelatinized maca is easier to digest than raw. Effects on libido and energy take 4-8 weeks of consistent use.",
    "manganese": "Easy to over-supplement — most people get enough from diet. Excess is neurotoxic; keep total intake under 11 mg/day.",
    "milk-thistle": "Standardize to 80% silymarin. Useful liver support but not a license to drink — protective, not curative.",
    "msm": "Often stacked with glucosamine and chondroitin for joints. Sulfur smell/taste is normal; mix with juice if needed.",
    "nmn": "Sublingual or liposomal forms may bypass intestinal degradation. Evidence in humans is still early — NR has more clinical data.",
    "phosphatidylserine": "Sunflower-derived is preferred over soy. 100-300 mg before bed lowers cortisol; morning dose supports focus.",
    "pqq": "Synergizes strongly with CoQ10 for mitochondrial biogenesis. 10-20 mg/day is the typical dose.",
    "saw-palmetto": "Standardized extract (85-95% fatty acids) is the studied form. Allow 8-12 weeks for prostate benefits.",
    "spirulina": "Source matters — choose tested brands (heavy metal contamination is common in cheap spirulina). 3-5 g daily.",
    "taurine": "3-6 g daily — much higher than the small doses in energy drinks. Excellent for cardiovascular and recovery support.",
    "tongkat-ali": "Look for standardized extracts (Physta, LJ100) at 200-400 mg. Cycle 5 days on, 2 days off to maintain sensitivity.",
    "vitamin-b5-pantothenic-acid": "Generally well-tolerated. High doses (>1g) historically used for acne but evidence is weak.",
    "magnesium-l-threonate": "The only magnesium form that meaningfully raises brain magnesium. 2 g (144 mg elemental Mg) is the studied dose.",
    "reishi-mushroom": "Dual-extracted (water + alcohol) tinctures or extracts beat plain powder. Bitter taste — capsules preferred.",
    "cordyceps-mushroom": "CS-4 strain is most studied. Take in the morning — can be stimulating for some users.",
    "chaga-mushroom": "Wild-harvested can contain high oxalates — limit to 1-2 g daily if prone to kidney stones.",
    "turkey-tail-mushroom": "PSK and PSP fractions have the strongest immune evidence. Look for hot-water-extracted products.",
    "urolithin-a": "Most people don't convert ellagitannins to urolithin A efficiently — direct supplementation bypasses this. Mitopure is the studied brand.",
    "ginger": "Standardize to gingerols. Effective for nausea and inflammation — 1-2 g daily extract or 4 g fresh root.",
    "moringa": "Nutrient-dense whole-food supplement. Don't use during pregnancy (root and bark especially).",
    "prenatal-vitamins": "Methylfolate (not folic acid) is preferred for women with MTHFR variants. Start 3 months before conception.",
    "tart-cherry": "Concentrate (1-2 oz) before bed for sleep and recovery. Higher dose pre-workout reduces muscle soreness.",
    "l-carnitine": "L-tartrate form is best for exercise recovery; acetyl form for cognition. Take with carbs to enhance muscle uptake.",
    "fisetin": "Senolytic dosing protocol is 20 mg/kg for 2 consecutive days monthly — much higher than daily-use doses.",
    "spermidine": "Wheat germ extract is the typical source. Effects on autophagy are slow — measured in months, not weeks.",
    "choline": "Most adults are deficient. Eggs are the best food source; supplemental choline bitartrate is cheap but less bioavailable than alpha-GPC or CDP-choline.",
    "carnosine": "Beta-alanine is a more cost-effective precursor for raising muscle carnosine. Direct carnosine supplementation is better for cognitive/longevity goals.",
    "maitake-mushroom": "D-fraction is the studied immune-modulating component. Hot-water extraction required for active polysaccharides.",
    "shiitake-mushroom": "Lentinan is the active compound. Culinary doses are too low for therapeutic effect — use extracts.",
    "hawthorn": "Can potentiate blood pressure medications — stack carefully. Effects on cardiac function build over 4-12 weeks.",
    "tmg-betaine": "Lowers homocysteine alongside B12 and folate. 1-3 g daily; also a useful pre-workout for power output.",
    "red-yeast-rice": "Contains naturally occurring monacolin K (lovastatin) — treat like a statin. Pair with CoQ10 and avoid combining with prescription statins.",
    "pomegranate-extract": "Standardize to punicalagins (40%+). Supports cardiovascular and prostate health; juice is also effective but high in sugar.",
    "l-arginine": "Citrulline raises arginine more effectively than arginine itself due to first-pass metabolism. Skip arginine — use citrulline.",
    "schisandra": "Adaptogen supporting liver and stress response. Bitter — capsules preferred over tincture.",
    "gotu-kola": "Supports circulation, skin, and cognition. Triterpenes are the active fraction — look for standardized extracts.",
    "benfotiamine": "Fat-soluble thiamine analog. Much better absorbed than standard B1; particularly useful for diabetic neuropathy support.",
    "tribulus-terrestris": "Despite the marketing, evidence for testosterone elevation in healthy men is weak. May support libido through other mechanisms.",
    "horny-goat-weed": "Icariin is the active compound — standardize to 20%+. Mild PDE5 inhibition.",
    "nicotinamide-riboside": "Niagen is the patented, well-studied form. Raises NAD+ more reliably in humans than NMN currently does.",
}


def main():
    path = Path("data/supplements.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    skipped = 0
    missing_in_dict = []

    for supp in data["supplements"]:
        sid = supp["id"]
        if "notes" in supp and supp["notes"]:
            continue
        if sid in NOTES:
            supp["notes"] = NOTES[sid]
            updated += 1
        else:
            missing_in_dict.append(sid)
            skipped += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Updated {updated} entries with notes.")
    if missing_in_dict:
        print(f"Still missing notes ({len(missing_in_dict)}): {missing_in_dict}")
    total_with = sum(1 for s in data["supplements"] if s.get("notes"))
    print(f"Total with notes now: {total_with}/{len(data['supplements'])}")


if __name__ == "__main__":
    main()
