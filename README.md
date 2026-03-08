# Supplement Guide

Evidence-based supplement, vitamin, and peptide information website.

## Getting Started

### Prerequisites
- [Hugo](https://gohugo.io/installation/) (v0.121.1 or later)

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/supplement-guide.git
cd supplement-guide

# Start the development server
hugo server -D

# Build for production
hugo --gc --minify
```

Visit `http://localhost:1313` to see the site.

## Project Structure

```
supplement-guide/
├── archetypes/          # Content templates
├── content/
│   ├── supplements/     # Individual supplement guides
│   ├── stacks/          # Combination guides
│   ├── medications/     # Medication support guides
│   ├── goals/           # Goal-based guides
│   └── comparisons/     # Comparison articles
├── layouts/             # Hugo templates
├── static/
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript
│   └── images/          # Static images
└── hugo.toml            # Site configuration
```

## Content Types

### Supplements
Individual supplement deep-dives with:
- Quick facts (dosage, timing, form)
- Results timeline
- Benefits and mechanism
- Side effects and interactions
- Affiliate links

### Stacks
Combination guides showing:
- Why supplements work together
- Optimal dosing protocols
- Timing recommendations

### Medication Guides
Support for medication users:
- Nutrient depletions
- Supportive supplements
- Dangerous interactions to avoid

### Goals
Goal-oriented recommendations:
- Best supplements for energy
- Sleep support
- Focus enhancement
- Stress relief

### Comparisons
Side-by-side comparisons:
- Different forms (e.g., magnesium types)
- Similar supplements
- Brand comparisons

## Creating Content

### New Supplement
```bash
hugo new supplements/your-supplement-name.md
```

### New Stack Guide
```bash
hugo new stacks/your-stack-name.md
```

## Deployment

### Netlify
1. Connect your GitHub repository to Netlify
2. Build settings are in `netlify.toml`
3. Deploy automatically on push

### Manual
```bash
hugo --gc --minify
# Upload 'public' folder to your host
```

## Affiliate Setup

Update affiliate codes in `hugo.toml`:
```toml
[params.affiliates]
  iherb = "YOUR_IHERB_CODE"
  amazon = "YOUR_AMAZON_TAG"
```

## Design

Inspired by Thrive Market with:
- Natural greens and earth tones
- Clean, organic aesthetic
- High readability typography
- Research-backed trust signals

## License

All rights reserved.
