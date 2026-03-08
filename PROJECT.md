# Supplement Guide Website Project

## Project Vision
A comprehensive, blog-style educational website about supplements, vitamins, and peptides. The go-to resource for people wanting to learn:
- What each supplement does
- How supplements interact/combine with each other
- What to expect when taking them (effects, timeline)
- What to take alongside specific medications

**Monetization**: Amway/Nutrilite affiliate links

## Design Aesthetic
- **Inspired by**: Thrive Market
- **Colors**: Natural greens (#2D5A27), earth tones, cream backgrounds (#FDFBF7)
- **Typography**: Plus Jakarta Sans (headings), Inter (body)
- **Feel**: Clean, organic, trustworthy, wellness-focused

## Tech Stack
- **Framework**: Hugo static site generator
- **Hosting**: Netlify (free tier with subdomain until domain purchased)
- **Affiliate**: Amway/Nutrilite only

## Project Location
`C:\Users\altst\supplement-guide`

---

## Current Status: Phase 2 Complete

### Phase 1: Foundation ✅
- [x] Hugo project structure created
- [x] Custom theme built (Thrive Market inspired)
- [x] Content type templates (supplements, stacks, medications, goals, comparisons)
- [x] Site configuration (hugo.toml)
- [x] Layouts for all content types
- [x] CSS styling complete
- [x] JavaScript (mobile menu, search, TOC)
- [x] Netlify deployment config

### Phase 2: Core Content ✅
- [x] 25 supplement articles
- [x] 5 stack/combination guides
- [x] 7 medication guides
- [x] 5 comparison articles
- [x] 6 goal-based guides
- [x] About, Methodology, Disclaimer, Privacy pages

**Total: ~48 articles**

### Phase 3: Launch & Monetize (TODO)
- [ ] Choose domain name
- [ ] Set up Amway affiliate account
- [ ] Update all affiliate links with real Amway URLs
- [ ] Deploy to Netlify
- [ ] Basic SEO setup (meta tags, sitemap)
- [ ] Test all pages

### Phase 4: Growth (TODO)
- [ ] Add more content (target 100+ articles)
- [ ] Optional quiz feature
- [ ] Email newsletter signup
- [ ] Social media presence

---

## Content Structure

### Supplements (`/content/supplements/`)
Individual deep-dives with:
- Quick facts (dosage, timing, form, results timeline)
- Benefits, mechanism of action
- Best forms comparison
- Side effects, interactions
- Research summary

**Current articles**: vitamin-d3, magnesium, omega-3, zinc, ashwagandha, creatine, nac, lions-mane, b-complex, vitamin-c, l-theanine, vitamin-k2, iron, selenium, coq10, probiotics, curcumin, berberine, rhodiola, alpha-lipoic-acid, melatonin, collagen, vitamin-e, potassium, glycine

### Stacks (`/content/stacks/`)
Combination guides:
- magnesium-vitamin-d
- caffeine-l-theanine
- zinc-copper-balance
- supplements-not-to-combine
- sleep-stack

### Medications (`/content/medications/`)
Supplement support for medications:
- adderall-supplements
- ssri-support
- birth-control-nutrients
- metformin-supplements
- statin-supplements
- ppi-supplements
- blood-pressure-supplements

### Goals (`/content/goals/`)
Goal-based recommendations:
- energy-supplements
- sleep-supplements
- focus-supplements
- anxiety-supplements
- immune-supplements
- muscle-building-supplements

### Comparisons (`/content/comparisons/`)
Side-by-side comparisons:
- magnesium-forms
- fish-oil-vs-krill-oil
- vitamin-d2-vs-d3
- ashwagandha-ksm66-vs-sensoril
- methylated-vs-regular-b-vitamins

---

## Commands

### Local Development
```bash
cd C:\Users\altst\supplement-guide
hugo server -D
```
Visit: http://localhost:1313

### Build for Production
```bash
hugo --gc --minify
```

### Create New Content
```bash
hugo new supplements/new-supplement.md
hugo new stacks/new-stack.md
hugo new medications/new-medication.md
hugo new goals/new-goal.md
hugo new comparisons/new-comparison.md
```

---

## Next Steps (Priority Order)

1. **Preview locally** - Run `hugo server -D` to see the site
2. **Review content** - Check articles for accuracy, fix any issues
3. **Add more supplements** - Target high-search-volume supplements
4. **Set up Amway affiliate** - Get real affiliate links
5. **Deploy to Netlify** - Free hosting with yoursite.netlify.app
6. **Buy domain when ready** - Connect to Netlify

---

## Content Ideas for Future

### More Supplements
- Vitamin A, Vitamin B1/B2/B5/B6/B7/B9/B12 (individual)
- Calcium, Chromium, Copper, Iodine, Manganese
- DHEA, Pregnenolone, Tongkat Ali, Fadogia
- Quercetin, Resveratrol, Pterostilbene
- GABA, 5-HTP, Tryptophan
- Choline, Alpha-GPC, CDP-Choline
- Milk Thistle, Dandelion, Artichoke

### More Medication Guides
- Thyroid medications
- Antibiotics
- Painkillers/NSAIDs
- Antihistamines
- Chemotherapy support

### More Goals
- Skin health
- Hair growth
- Longevity/anti-aging
- Gut health
- Hormone balance
- Athletic performance (endurance vs strength)

### More Comparisons
- Whey vs Casein vs Plant protein
- Different probiotic strains
- Synthetic vs natural vitamins
- Capsules vs powders vs liquids
