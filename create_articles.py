import os

articles = {
    'hawthorn.md': '''---
title: Hawthorn
date: 2025-03-15
draft: false
supplement_type: Herbal
tagline: The heart-supporting herbal that strengthens cardiac muscle and improves blood flow
research_backed: true
dosage: 300-900 mg
dosage_unit: mg
dosage_min: 300
dosage_typical: 600
dosage_max: 1500
timing: With meals
form: Capsules or extract
results_timeline: 4-12 weeks
synergies:
  - CoQ10
  - L-Arginine
  - Omega-3
  - Magnesium
tags:
  - cardiovascular
  - heart health
  - blood flow
  - cardiac function
  - herbal
warnings: Generally very safe. May lower blood pressure if on BP medications. Pregnant women consult doctor.
interactions: Safe with most supplements. May have additive effects with BP medications.
---

**What it is:** Hawthorn is a traditional herbal medicine from the Crataegus plant used for centuries to strengthen the heart. It contains flavonoids and proanthocyanidins that enhance cardiac contractility, improve blood flow, and support cardiovascular function.

## Benefits

### Cardiac Strength
- Increases cardiac contractility (force of heart contraction)
- Improves cardiac output and exercise tolerance
- Supports heart function in aging
- Enhances overall cardiovascular resilience

### Blood Flow & Circulation
- Enhances vasodilation and blood vessel widening
- Improves coronary blood flow to heart muscle
- Supports peripheral circulation
- Reduces blood pressure (5-10 mmHg typical)
- Supports endothelial function

### Antioxidant Protection
- Reduces oxidative stress in heart tissue
- Protects cardiac cells from damage
- Anti-inflammatory in cardiovascular system
- Supports mitochondrial function

### Exercise Tolerance
- Improved exercise tolerance and endurance
- Better oxygen delivery during exertion
- Enhanced cardiovascular resilience
- Faster post-exercise recovery

## Dosage

**Cardiovascular support:** 300-600 mg daily (300 mg twice daily)
**Enhanced:** 600-900 mg daily
**Full spectrum:** 900-1,500 mg daily
**Timing:** With meals
**Duration:** 4-12 weeks initial; 12+ weeks full benefits

## Best Forms

**Hawthorn Extract** (Recommended)
- Concentrated, standardized form
- More potent than whole herb
- Better absorption
- Most research uses extract

**Hawthorn Berries** (Whole)
- More economical
- Can be used as tea

## Research

- Multiple trials show improved cardiac contractility
- Consistent 5-10 mmHg blood pressure reductions
- Improved exercise capacity in those with cardiac aging
- Excellent safety record with few side effects

## Safety

Excellent safety profile with very rare side effects.

## Stacking

**Comprehensive cardiac:**
- Hawthorn 600 mg + CoQ10 200 mg + L-Arginine 3g + Magnesium 300 mg

**Blood pressure support:**
- Hawthorn 600 mg + Magnesium 300 mg + Omega-3 2g

**Exercise performance:**
- Hawthorn 600 mg + L-Arginine 3g + Carnosine 1g

## Bottom Line

Hawthorn strengthens cardiac muscle and improves blood flow. Strong evidence for cardiac aging, blood pressure support, and cardiovascular health. Key takeaways:
- Strengthens cardiac contractility and blood flow
- Dose: 300-900 mg daily
- Results in 4-8 weeks; full benefits 12+ weeks
- Excellent safety
- Synergizes with CoQ10, L-Arginine, Magnesium
- Valuable for cardiac aging and cardiovascular optimization
''',
    'red-yeast-rice.md': '''---
title: Red Yeast Rice
date: 2025-03-15
draft: false
supplement_type: Herbal
tagline: The traditional fermented rice that supports healthy cholesterol levels through natural statin-like compounds
research_backed: true
dosage: 1200-2400 mg
dosage_unit: mg
dosage_min: 1200
dosage_typical: 1500
dosage_max: 2400
timing: With meals
form: Capsules
results_timeline: 4-8 weeks
synergies:
  - CoQ10
  - Niacin
  - Plant Sterols
  - Omega-3
tags:
  - cardiovascular
  - cholesterol
  - herbal
  - lipid support
warnings: May cause mild muscle discomfort. Those on statin drugs should consult doctor (potential interaction). Not for pregnant women.
interactions: May have additive cholesterol-lowering effects with statins.
---

**What it is:** Red yeast rice is fermented rice containing naturally-occurring statins (monacolin compounds) that support healthy cholesterol levels. Used in traditional Chinese medicine for centuries, modern research confirms its cholesterol-lowering effects through mechanisms similar to pharmaceutical statins but from natural compounds.

## Benefits

### Cholesterol Support
- Reduces LDL cholesterol 15-30%
- May increase HDL cholesterol
- Supports cardiovascular lipid profiles
- Natural alternative to statins

### Cardiovascular Health
- Reduces cardiovascular disease risk
- Anti-inflammatory in cardiovascular system
- Supports arterial health
- Antioxidant protection of lipids

### CoQ10 Preservation
- Unlike statins, may not deplete CoQ10
- Supports mitochondrial function
- Maintains cellular energy

## Dosage

**Cholesterol support:** 1,200-1,500 mg daily
**Enhanced:** 1,500-2,000 mg daily
**Maximum:** 2,400 mg daily
**Timing:** With meals containing fat
**Duration:** 4-8 weeks for cholesterol effects

## Best Forms

**Red Yeast Rice Extract**
- Standardized to monacolin content
- Consistent potency
- Recommended choice

## Research

- Multiple trials show 15-30% LDL reduction
- Comparable to pharmaceutical statin alternatives
- Natural compounds with similar mechanisms
- Excellent safety record

## Safety

Generally safe. Very rare muscle discomfort (compared to statins).

## Stacking

**Comprehensive cholesterol:**
- Red Yeast Rice 1,500 mg + CoQ10 200 mg + Plant Sterols 2g + Omega-3 2g

**Cardiovascular support:**
- Red Yeast Rice 1,500 mg + Niacin 500 mg + Hawthorn 600 mg

## Bottom Line

Red yeast rice naturally supports healthy cholesterol through monacolin compounds. Strong evidence for lipid support, natural statin alternative. Key takeaways:
- Natural statin-like cholesterol support
- Dose: 1,200-2,400 mg daily with meals
- Results in 4-8 weeks
- Excellent safety profile
- Synergizes with CoQ10, niacin, plant sterols
- Valuable alternative to pharmaceutical statins
''',
}

base_path = 'content/supplements'
for filename, content in articles.items():
    filepath = os.path.join(base_path, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created {filename}')
    
print('All articles created!')
