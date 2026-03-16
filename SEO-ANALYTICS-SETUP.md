# VitaWise SEO & Analytics Setup Guide

## Quick Start - Essential Setup (First 24 Hours)

### 1. Google Analytics 4
- Account URL: https://analytics.google.com
- Property Name: "VitaWise"
- Website: https://vitawise.life
- Copy your tracking ID (G-XXXXXXXXXX)
- Add to every page `<head>` tag

### 2. Google Search Console
- Verify at: https://search.google.com/search-console
- Add sitemap: /sitemap.xml
- Monitor "Coverage" tab for indexing

### 3. Schema Markup
- Add to each article (already templated in `/static/schema-markup.json`)
- Validate at: https://validator.schema.org
- Test: `Article`, `Breadcrumb`, `Organization` schemas

### 4. Robots.txt
- Already created at `/static/robots.txt`
- Update sitemap URLs in robots.txt

---

## Analytics Setup Details

### Google Analytics 4 Configuration

**Events to Track:**
- `affiliate_click` - Amway/Amazon links
- `scroll_depth` - How far users scroll
- `cta_click` - Newsletter signup, buttons
- `page_view` - Standard page views
- `conversion` - Any monetization action

**Conversion Goals:**
1. Affiliate click → $0.50-2.00 value
2. Email signup → $5.00 value (lifetime)
3. Page visit → $0.05 value
4. Time on page >30s → $0.10 value

### Google Search Console

**Key Reports to Monitor:**
- **Performance:** Click-through rate, impressions, rankings
- **Coverage:** How many pages indexed (target: 95%+)
- **Core Web Vitals:** Page speed, stability
- **Mobile Usability:** Mobile-friendly status

**Weekly Monitoring:**
- Check for crawl errors (fix immediately)
- Review top 10 performing keywords
- Monitor impressions/click trends

---

## SEO Metadata Standards

### Page Title Template
`[Primary Keyword] | [Subcategory] - VitaWise` (55-60 chars)

Examples:
- "Best Multivitamins Comparison | Supplements - VitaWise"
- "Supplements for Weight Loss | Weight Management - VitaWise"

### Meta Description Template
`[Keyword benefit]. [Specific coverage]. [CTA]` (150-160 chars)

Examples:
- "Complete multivitamin comparison: 6 brands ranked by quality, cost-per-dose, bioavailability. Best supplements for your budget."
- "Weight loss supplement protocol: metabolism support, appetite control, fat burning. Evidence-based stacks, 4-8 week results."

### Open Graph Tags (Social Sharing)
```html
<meta property="og:title" content="[Page Title]">
<meta property="og:description" content="[Meta Description]">
<meta property="og:image" content="[Image URL]">
<meta property="og:type" content="article">
<meta property="og:url" content="[Page URL]">
```

---

## Keyword Research by Content Type

### Goal Guide Keywords (Primary)
- "Supplements for [goal]" (8k-80k searches)
- "Best supplements for [goal]" (secondary)
- "[Goal] supplement stack" (tertiary)

### Medication Guide Keywords
- "Supplements with [medication]" (1k-5k)
- "[Medication] nutrient depletion" (500-2k)
- "Safe supplements [medication]" (1k-3k)

### Comparison Article Keywords
- "Best [supplement] supplements" (5k-20k)
- "[Supplement] comparison" (2k-10k)
- "[Supplement] vs [supplement]" (1k-5k)

### Condition Guide Keywords
- "Supplements for [condition]" (5k-40k)
- "[Condition] natural treatment" (2k-10k)
- "[Condition] supplement protocol" (500-2k)

---

## Internal Linking Strategy

### Linking Best Practices
✓ Descriptive anchor text (not "click here")
✓ 5-7 internal links per 2,000-word article
✓ Link to related content (contextually relevant)
✓ Mix of footer links + body links
✓ Vary anchor text (don't repeat exact phrase)

### Link Distribution Per Article
- 2-3 related goal guides
- 1-2 comparison articles (if applicable)
- 1-2 medication guides (if medication-related)
- 1 timeline article (for supplement timing)
- Category/index page links

### High-Value Linking Targets
1. Best-performing comparison articles (monetization)
2. High-volume goal guides (traffic drivers)
3. Medication guides (unique, hard-to-find content)
4. Category landing pages (internal authority)

---

## Technical SEO Checklist

### Before Launch
- [ ] GA4 tracking code on all pages
- [ ] GSC property verified
- [ ] Robots.txt live (/static/robots.txt)
- [ ] Sitemap generated (/sitemap.xml)
- [ ] Schema markup on all articles
- [ ] Meta titles optimized (all pages)
- [ ] Meta descriptions unique (no duplicates)
- [ ] Open Graph tags added
- [ ] Internal links strategically placed
- [ ] 301 redirects configured (if applicable)

### Performance Targets
- Page load time: <3 seconds
- Largest Contentful Paint: <2.5 seconds
- Cumulative Layout Shift: <0.1
- First Input Delay: <100ms
- Mobile-friendly: 100% pages

### Ongoing Monitoring
- Weekly: Check GSC for errors
- Weekly: Monitor top keywords
- Monthly: Review GA4 reports
- Monthly: Update underperforming content
- Quarterly: Full SEO audit

---

## Expected Timeline & Results

### Month 1
- Indexation: 50-70% of pages
- Organic traffic: 100-200/month
- Affiliate clicks: 10-30/month

### Month 3
- Indexation: 80-90% of pages
- Organic traffic: 500-1,000/month
- Affiliate clicks: 100-300/month
- Keywords in top 10: 20-40

### Month 6
- Indexation: 95%+ of pages
- Organic traffic: 1,500-3,000/month
- Affiliate clicks: 300-800/month
- Keywords in top 10: 50-100

### Month 12
- Indexation: 98%+ of pages
- Organic traffic: 3,000-8,000/month
- Affiliate clicks: 1,000-2,500/month
- Keywords in top 3: 50-100+

---

## Quick Reference Links

### Tools (Free)
- [Google Analytics 4](https://analytics.google.com)
- [Google Search Console](https://search.google.com/search-console)
- [Schema Validator](https://validator.schema.org)
- [PageSpeed Insights](https://pagespeed.web.dev)
- [Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)

### Learning Resources
- [Google SEO Starter Guide](https://developers.google.com/search/docs)
- [Schema.org Documentation](https://schema.org)
- [Hugo SEO Guide](https://gohugo.io/templates/output-formats/)

---

## Files Created for This Setup

✓ `/static/google-analytics.js` - GA4 tracking script
✓ `/static/schema-markup.json` - Schema.org templates
✓ `/static/robots.txt` - Search engine crawling rules
✓ `/config/seo-config.toml` - SEO configuration
✓ `SEO-ANALYTICS-SETUP.md` - This setup guide

---

## Next Steps

1. **This Week:**
   - Setup GA4 property
   - Verify GSC ownership
   - Deploy tracking code
   - Submit sitemap to GSC

2. **Next Week:**
   - Add schema markup to templates
   - Audit meta descriptions
   - Test Core Web Vitals
   - Setup conversion tracking

3. **Month 2:**
   - Monitor organic traffic
   - Optimize top content
   - Build internal links
   - Create new content based on search data

4. **Ongoing:**
   - Monitor GA4 & GSC weekly
   - Optimize underperforming pages
   - Track keyword rankings
   - Update content regularly

---

## Content Gap Analysis

**Current Strength:** 86 comprehensive articles across 6 categories
**Target Keywords:** 100+ primary keywords
**Estimated Potential:** 3,000-8,000 organic visits/month

**High-Priority Content Gaps:**
- "Supplements side effects" (high volume, not covered)
- "[Supplement] dosage" guides (specific dosing questions)
- "[Supplement] benefits" individual breakdowns
- "Drug-supplement interactions" more depth

**Recommended Next:** Create 20-30 more targeted long-tail articles focusing on specific supplement + benefit combinations.
