---
title: "Google Analytics 4 & Search Console Implementation Guide"
date: 2026-03-15
description: "Step-by-step guide to deploy GA4 tracking and Google Search Console for vitawise.life"
---

# GA4 & GSC Implementation Guide

## Phase 1: Google Analytics 4 Setup (15 minutes)

### Step 1: Create GA4 Property
1. Go to [Google Analytics](https://analytics.google.com)
2. Sign in with your Google account
3. Click **"+ Create"** in the left sidebar
4. Select **"Account"**
   - Account name: "VitaWise"
   - Data sharing: Leave defaults (recommended)
   - Click **"Next"**

5. Create Property:
   - Property name: "vitawise.life"
   - Reporting timezone: Select your timezone (or US/Eastern)
   - Currency: USD
   - Click **"Next"**

6. Select Business Information:
   - Business type: Small business (or appropriate)
   - Business objectives: E-commerce, lead generation
   - Click **"Create"**

### Step 2: Get Your GA4 Tracking ID
1. After property is created, you'll see your **Measurement ID**
2. Copy the ID (format: `G-XXXXXXXXXX`)
3. Save this ID - you'll need it for the next step

### Step 3: Add Tracking ID to Hugo Config
1. Open `hugo.toml` in the repository
2. Find the line: `ga4 = "G-XXXXXXXXXX"`
3. Replace `G-XXXXXXXXXX` with your actual GA4 ID
4. Save the file

Example:
```toml
[params.analytics]
  ga4 = "G-ABC123DEF45"  # Your actual ID
```

### Step 4: Deploy Changes
Run these commands:
```bash
cd C:\Users\altst\supplement-guide
git add hugo.toml layouts/partials/analytics.html
git commit -m "Add GA4 tracking ID and custom event tracking"
git push origin main
```

Netlify will automatically deploy. Wait 2-5 minutes for deployment to complete.

### Step 5: Verify GA4 is Working
1. Go to your website: https://vitawise.life
2. Return to [Google Analytics](https://analytics.google.com)
3. In left sidebar, click **"Real Time"**
4. If you see active users, GA4 is working! ✓

**Note:** It may take 24 hours to see data in other GA4 reports.

---

## Phase 2: Google Search Console Setup (15 minutes)

### Step 1: Create GSC Property
1. Go to [Google Search Console](https://search.google.com/search-console)
2. Sign in with your Google account
3. Click **"Add property"**
4. Enter URL: `https://vitawise.life`
5. Click **"Continue"**

### Step 2: Verify Ownership (Choose Method)

#### Option A: HTML Tag (Recommended - Easiest)
1. GSC shows: `<meta name="google-site-verification" content="YOUR_VERIFICATION_CODE" />`
2. Copy the verification code (the long string after `content="`)
3. Open `hugo.toml`
4. Find: `gsc_verification = "YOUR_GSC_VERIFICATION_ID"`
5. Replace with your verification code

Example:
```toml
gsc_verification = "abc123xyz789abc123xyz789abc123"
```

6. Save and deploy:
```bash
git add hugo.toml
git commit -m "Add GSC verification code"
git push origin main
```

7. Wait 2-5 minutes for Netlify to deploy
8. Return to GSC and click **"Verify"**

#### Option B: DNS Record (Alternative)
If you have DNS access:
1. GSC shows DNS CNAME record
2. Add to your domain's DNS settings
3. Wait for DNS propagation (up to 48 hours)
4. Return to GSC and click "Verify"

**Recommended:** Use Option A (HTML tag) for faster verification.

### Step 3: Submit Sitemap
1. In GSC, left sidebar → **"Sitemaps"**
2. Enter: `sitemap.xml`
3. Click **"Submit"**
4. Also submit additional sitemaps (optional):
   - `sitemap-articles.xml`
   - `sitemap-comparisons.xml`

GSC will now crawl and index your site.

### Step 4: Monitor Coverage
1. Left sidebar → **"Coverage"**
2. Check status:
   - **Valid:** Pages indexed successfully ✓
   - **Excluded:** Pages with noindex (intentional)
   - **Error:** Fix immediately
   - **Submitted not indexed:** Needs time to index

**Target:** 80%+ indexed within 30 days

---

## Phase 3: Verify Setup (Checklist)

### Google Analytics 4 ✓
- [ ] GA4 property created
- [ ] Tracking ID in hugo.toml
- [ ] Changes deployed to production
- [ ] Real-time users showing in GA4
- [ ] Custom events firing (affiliate clicks, scroll depth)

### Google Search Console ✓
- [ ] Property verified (HTML tag or DNS)
- [ ] Sitemaps submitted
- [ ] Coverage report showing pages
- [ ] No critical errors

### Schema Markup ✓
- [ ] Schema partial templates exist (`schema/article.html`, etc.)
- [ ] Included in baseof.html template
- [ ] Test at [Schema Validator](https://validator.schema.org)

---

## What Gets Tracked Now

### Google Analytics 4 Custom Events

| Event | Trigger | Purpose |
|-------|---------|---------|
| `affiliate_click` | User clicks Amway/Amazon link | Track conversions |
| `scroll_25` | User scrolls 25% down page | Engagement metric |
| `scroll_50` | User scrolls 50% down page | Engagement metric |
| `scroll_75` | User scrolls 75% down page | Engagement metric |
| `cta_click` | User clicks newsletter/CTA button | Conversion tracking |
| `time_on_page` | User spends 30+ seconds on page | Engagement metric |
| `page_view` | Page is loaded | Standard tracking |

### Conversion Goals to Monitor
1. **Affiliate Click** → High value (revenue)
2. **Email Signup** → Medium value (list growth)
3. **Time on Page (30s+)** → Low value (engagement)
4. **Scroll Depth (50%+)** → Low value (content quality)

---

## Monitoring Dashboard Setup

### Daily Metrics (Check in GA4)
1. **Real-time users** - Should show activity
2. **Affiliate clicks** (Events → affiliate_click)
3. **Conversion rate** (affiliate clicks / page views)

### Weekly Metrics (Check Sunday evening)
1. **Organic traffic** - Should grow week-over-week
2. **Page views by source**
3. **Top 5 performing pages**
4. **Bounce rate**
5. **Average session duration**

### Monthly Metrics (1st of month)
1. **Total organic traffic** - Track growth
2. **Total affiliate clicks** - Revenue potential
3. **New vs returning users**
4. **Conversion funnel**
5. **Top keywords (from GSC)**

### Google Search Console Weekly
1. **Coverage report** - Indexation progress
2. **Performance** - Impressions and clicks
3. **Top pages** - Which content performs best
4. **Errors** - Fix any crawl issues

---

## Expected Timeline & Results

### Days 1-7
- ✓ GA4 tracking active (real-time data visible)
- ✓ GSC property verified and crawling
- ⏳ Initial indexing beginning (5-10% of pages)
- Expected: <100 affiliate clicks

### Days 8-30
- ✓ Most pages indexed (70-80%)
- ✓ Organic impressions starting to appear in GSC
- ✓ Custom events tracked in GA4
- Expected: 100-300 affiliate clicks, 200-500 organic impressions

### Months 2-3
- ✓ 85-95% of pages indexed
- ✓ Keyword rankings improving (top 50-100 range)
- ✓ Organic traffic: 500-1,500/month
- Expected: 500+ affiliate clicks cumulative

---

## Troubleshooting

### GA4 Not Showing Data
1. Check Real-time (should show users in seconds)
2. Verify tracking ID in hugo.toml (must match GA4 property)
3. Deploy changes to production (changes pushed to GitHub)
4. Wait 5 minutes for Netlify deployment
5. Hard refresh website (Ctrl+Shift+R)
6. Open developer console (F12) → Network tab
7. Look for `googletagmanager.com` requests (should succeed)

### GSC Not Verifying
1. Check HTML tag added correctly to `hugo.toml`
2. Deploy changes and wait 2-5 minutes
3. Visit website and view page source (Ctrl+U)
4. Search for `google-site-verification` - should be present
5. Return to GSC and click "Verify" again
6. If still fails, use DNS record method instead

### Pages Not Indexed
1. Check GSC Coverage tab for errors
2. Fix any reported issues (robots.txt blocking, etc.)
3. Request indexing manually (Coverage → Valid → Select URL → "Request Indexing")
4. Wait up to 2 weeks for indexing

---

## SEO Best Practices Going Forward

### Weekly
- [ ] Check GA4 Real-time for traffic anomalies
- [ ] Monitor GSC Coverage for new errors
- [ ] Review top 10 performing pages
- [ ] Check affiliate click conversion rate

### Monthly
- [ ] Analyze GA4 traffic sources and pages
- [ ] Review GSC Performance (impressions, CTR)
- [ ] Identify underperforming pages (<100 views)
- [ ] Check Core Web Vitals
- [ ] Optimize 1-2 underperforming pages

### Quarterly
- [ ] Full SEO audit (all pages)
- [ ] Competitor analysis
- [ ] Keyword research update
- [ ] Internal link optimization
- [ ] Content gap analysis

---

## Key Metrics to Focus On

### Revenue Metrics (Most Important)
1. **Affiliate click conversion rate** - Goal: 2-4%
2. **Cost per affiliate click** - Lower is better
3. **Affiliate revenue per 1,000 views** - Goal: $5-10 CPM

### Traffic Metrics
1. **Organic traffic growth** - Goal: +20% month-over-month
2. **Keyword rankings** - Goal: 100+ keywords in top 50
3. **Total pageviews** - Goal: 3,000-8,000/month by month 6

### Engagement Metrics
1. **Scroll depth (50%+)** - Goal: >60% of users
2. **Time on page (30s+)** - Goal: >50% of users
3. **Pages per session** - Goal: >1.5
4. **Bounce rate** - Goal: <60%

---

## Common Questions

**Q: When will I see organic traffic?**
A: First users in days 2-7. Meaningful traffic in weeks 3-4. Significant traffic in months 2-3.

**Q: How long does indexing take?**
A: Fast (high-quality sites): 3-7 days for 80%+. Normal: 2-4 weeks for 90%+. Slow: 4+ weeks.

**Q: What's a good conversion rate?**
A: 2-4% (affiliate click from page view) is excellent for health content.

**Q: Should I use Google Analytics or Search Console?**
A: Both. GA4 tracks user behavior; GSC tracks search performance.

**Q: Can I see real-time affiliate clicks?**
A: Yes, in GA4 → Real-time → Events → affiliate_click

---

## Files Modified

✓ `hugo.toml` - Added GA4 ID and GSC verification
✓ `layouts/partials/analytics.html` - Enhanced with custom events
✓ `layouts/_default/baseof.html` - Added GSC verification meta tag

---

## Support & Resources

- [Google Analytics Help](https://support.google.com/analytics)
- [Google Search Console Help](https://support.google.com/webmasters)
- [Schema.org Validator](https://validator.schema.org)
- [Core Web Vitals Guide](https://web.dev/vitals)

---

## Next Steps

1. ✓ Complete GA4 setup (Phase 1)
2. ✓ Complete GSC setup (Phase 2)
3. Monitor Real-time data (Days 1-7)
4. Submit sitemap (Phase 2, Step 3)
5. Wait for indexing (Weeks 1-4)
6. Monitor performance metrics weekly
7. Optimize underperforming pages (Month 1+)
8. Create additional content based on search data (Month 2+)

---

**Setup Complete!** Your website is now ready to be analyzed and optimized for search engines and conversions.
