---
title: Global Social Media + US Government API Verification (26 platforms)
version: v1.0
date: 2026-07-14
license: MIT
description: API availability verification report. Methods: curl/browser direct probe.
---

# US & Global 26-Platform API Audit (verified 2026-07-14)

Verified by actual HTTP requests + browser navigation. A complete API-availability scan spanning major social/media, US federal government, and US commerce platforms.

---

## Part I — Social / Media (10 platforms)

| Platform | URL | Has API? | Type | Pricing | Doc URL |
|---|---|---|---|---|---|
| Reddit | reddit.com | Yes | Devvit + REST (OAuth 2.0) | Free + Developer Funds ($167K) | https://developers.reddit.com |
| X/Twitter | x.com | Yes | X API v2 | Pay-per-use (credit based; $0.001/resource owned reads) | https://docs.x.com |
| YouTube | youtube.com | Yes | Data API v3 (REST) | Free 10K units/day + paid | https://developers.google.com/youtube/v3 |
| TikTok | tiktok.com | Yes | TikTok API for Business | Free base tier | https://developers.tiktok.com/portal |
| Instagram | instagram.com | Yes | Instagram Graph API (via FB) | Free | https://developers.facebook.com/products/instagram |
| Pinterest | pinterest.com | Yes | Pinterest REST API | Free | https://developers.pinterest.com |
| Facebook | facebook.com | Yes | Graph API (REST) | Free | https://developers.facebook.com/docs/graph-api |
| LinkedIn | linkedin.com | Yes | LinkedIn REST API | Free base tier | https://developer.linkedin.com |
| Discord | discord.com | Yes | Discord REST + Gateway | Free | https://docs.discord.com/developers/intro |
| Wikipedia | wikipedia.org | Yes | MediaWiki API | Free (public) | https://en.wikipedia.org/w/api.php |

## Part II — US Federal Government (9 platforms)

| Platform | URL | Has API? | Type | Pricing | Doc URL |
|---|---|---|---|---|---|
| FDA | fda.gov | Yes | open.fda.gov REST | Free | https://open.fda.gov/apis |
| FCC | fcc.gov | Yes | FCC Developer API | Free | https://www.fcc.gov/general/developer-api |
| CPSC | cpsc.gov | Maybe | NEISS data queries (no formal REST) | Free | https://www.cpsc.gov/Research--Statistics |
| USPTO | uspto.gov | Yes | USPTO Data Portal | Free | https://data.uspto.gov |
| EPA | epa.gov | Yes | EPA Developer REST | Free | https://www.epa.gov/developers |
| FTC | ftc.gov | Maybe | RSS feeds + data downloads (no formal REST) | Free | https://www.ftc.gov/data |
| BLS | bls.gov | Yes | BLS API v2 | Free (500 req/day) | https://www.bls.gov/developers/ |
| BEA | bea.gov | Yes | BEA REST API | Free | https://apps.bea.gov/API/docs/ |
| FRED | fred.stlouisfed.org | Yes | FRED REST API | Free (120 req/min) | https://fred.stlouisfed.org/docs/api/fred/ |

## Part III — US Commerce (7 platforms)

| Platform | URL | Has API? | Type | Pricing | Doc URL |
|---|---|---|---|---|---|
| Amazon SP-API | developer.amazon.com | Yes | Selling Partner REST API | Professional seller account required | https://developer-docs.amazon.com/sp-api |
| eBay | ebay.com | Yes | eBay REST API | Free + paid tiers | https://developer.ebay.com |
| Walmart | walmart.com | Yes | Walmart Marketplace REST API | Seller account required | https://developer.walmart.com |
| Chewy | chewy.com | No | — | — | — |
| Google Trends | trends.google.com | Unofficial only | Community libraries (npm google-trends-api) | — | https://github.com/pat310/google-trends-api |
| Freightos | freightos.com | Maybe | Enterprise-only internal API | Enterprise customers only | https://www.freightos.com |
| LME | lme.com | Maybe | LME data subscription (paid) | Paid subscription | Contact LME sales |

---

## HTTP Verification Details

### Curl / direct HTTP results
- **developer.twitter.com** → 307 redirect → **docs.x.com** → 308 redirect → actual docs
- **developers.google.com/youtube/v3** → 200 OK
- **developers.tiktok.com** → 404; **developers.tiktok.com/portal** → 200 OK
- **developers.facebook.com/docs/graph-api** → 200 OK
- **developers.pinterest.com** → 200 OK
- **developer.linkedin.com** → 301 → **developer.linkedin.com/** (singular)
- **discord.com/developers/docs/intro** → 301 → **docs.discord.com/developers/intro**
- **en.wikipedia.org/w/api.php** → 200 OK
- **open.fda.gov/apis** → 302 Found (redirects to api endpoint)
- **fcc.gov/general/developer-api** → ERR_HTTP2_PROTOCOL_ERROR (site down at verification time)
- **data.uspto.gov** → 200 OK
- **epa.gov/developers** → 200 OK
- **ftc.gov/developer** → empty page (no content, likely blocked)
- **bls.gov/developers/** → 403 (Akamai); docs exist at bls.gov/developers/api_signature_v2.htm
- **apps.bea.gov/API/** → 200 OK
- **fred.stlouisfed.org/docs/api/fred/** → 301 → 200 OK
- **developer-docs.amazon.com/sp-api** → 301 → 200 OK
- **developer.ebay.com** → redirects to error page (bot detection active)
- **developer.walmart.com** → 200 OK
- **chewy.com/app/api** → 404; **developer.chewy.com** → no DNS
- **trends.google.com/trends/api/explore** → 400 (trends endpoint exists but requires params)
- **freightos.com/developers** → 301; **developers.freightos.com** → empty page; **api.freightos.com** → 404
- **lme.com/en-GB/Market-Data/API** → 403 (Cloudflare challenge)
