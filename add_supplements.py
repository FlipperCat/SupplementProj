import json

new_supplements = [
    {
        "id": "magnesium-l-threonate",
        "name": "Magnesium L-Threonate",
        "type": "mineral",
        "category": "nootropic",
        "dosage": {"min": 1500, "typical": 2000, "max": 2000, "unit": "mg"},
        "timing": "morning or evening",
        "withFood": True,
        "withFat": False,
        "benefits": ["brain health", "memory", "cognitive function", "neuroprotection", "sleep"],
        "goals": ["brain", "memory", "focus", "sleep"],
        "synergies": ["omega-3", "lions-mane", "b-complex"],
        "conflicts": [],
        "absorptionCompetitors": ["calcium"],
        "depletedBy": [],
        "amwayProduct": None,
        "resultsTimeline": "4-8 weeks"
    },
    {
        "id": "reishi-mushroom",
        "name": "Reishi Mushroom",
        "type": "mushroom",
        "category": "adaptogen",
        "dosage": {"min": 1000, "typical": 1500, "max": 2000, "unit": "mg"},
        "timing": "evening",
        "withFood": True,
        "withFat": False,
        "benefits": ["sleep", "stress relief", "anxiety", "immune support", "longevity"],
        "goals": ["sleep", "stress", "anxiety", "immunity", "longevity"],
        "synergies": ["magnesium", "apigenin", "glycine"],
        "conflicts": [],
        "absorptionCompetitors": [],
        "depletedBy": [],
        "amwayProduct": None,
        "resultsTimeline": "2-4 weeks"
    },
    {
        "id": "cordyceps-mushroom",
        "name": "Cordyceps Mushroom",
        "type": "mushroom",
        "category": "performance",
        "dosage": {"min": 1500, "typical": 2000, "max": 3000, "unit": "mg"},
        "timing": "morning",
        "withFood": True,
        "withFat": False,
        "benefits": ["energy", "endurance", "athletic performance", "ATP production", "recovery"],
        "goals": ["energy", "performance", "endurance", "muscle"],
        "synergies": ["creatine", "beta-alanine", "coq10"],
        "conflicts": [],
        "absorptionCompetitors": [],
        "depletedBy": [],
        "amwayProduct": None,
        "resultsTimeline": "1-4 weeks"
    },
    {
        "id": "chaga-mushroom",
        "name": "Chaga Mushroom",
        "type": "mushroom",
        "category": "antioxidant",
        "dosage": {"min": 1000, "typical": 2000, "max": 3000, "unit": "mg"},
        "timing": "morning",
        "withFood": True,
        "withFat": False,
        "benefits": ["antioxidant", "immune support", "longevity", "anti-inflammatory"],
        "goals": ["antioxidant", "immunity", "longevity", "anti-aging"],
        "synergies": ["vitamin-c", "quercetin", "green-tea-extract"],
        "conflicts": [],
        "absorptionCompetitors": [],
        "depletedBy": [],
        "amwayProduct": None,
        "resultsTimeline": "2-8 weeks"
    },
    {
        "id": "turkey-tail-mushroom",
        "name": "Turkey Tail Mushroom",
        "type": "mushroom",
        "category": "prebiotic",
        "dosage": {"min": 1000, "typical": 1500, "max": 3000, "unit": "mg"},
        "timing": "morning",
        "withFood": True,
        "withFat": False,
        "benefits": ["gut health", "prebiotic", "immune support", "microbiome", "digestive"],
        "goals": ["gut", "immunity", "digestion"],
        "synergies": ["probiotics", "glutamine", "vitamin-d3"],
        "conflicts": [],
        "absorptionCompetitors": [],
        "depletedBy": [],
        "amwayProduct": None,
        "resultsTimeline": "2-8 weeks"
    },
    {
        "id": "urolithin-a",
        "name": "Urolithin A",
        "type": "metabolite",
        "category": "longevity",
        "dosage": {"min": 500, "typical": 500, "max": 1000, "unit": "mg"},
        "timing": "morning",
        "withFood": True,
        "withFat": False,
        "benefits": ["mitochondrial renewal", "muscle function", "longevity", "ATP production"],
        "goals": ["longevity", "energy", "muscle", "anti-aging"],
        "synergies": ["nmn", "coq10", "resveratrol"],
        "conflicts": [],
        "absorptionCompetitors": [],
        "depletedBy": [],
        "amwayProduct": None,
        "resultsTimeline": "8-12 weeks"
    }
]

with open('data/supplements.json', 'r') as f:
    data = json.load(f)

data['supplements'].extend(new_supplements)

with open('data/supplements.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Added {len(new_supplements)} supplements. Total now: {len(data['supplements'])}")
