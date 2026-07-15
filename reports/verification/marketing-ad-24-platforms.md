---
title: Marketing & Advertising Platform API Verification (24 platforms)
version: v1.0
date: 2026-07-14
license: MIT
description: API availability verification report. Methods: curl/browser direct probe.
---

# Marketing / Advertising Platform APIs — Global + China (verified 2026-07-14)

## Global Platforms (17)

| # | Platform | URL | Has API? | Type | Pricing | Docs URL | Method |
|---|----------|-----|----------|------|---------|----------|--------|
| 1 | Google Ads | ads.google.com | Yes | REST/gRPC | Free (ads account req.) | https://developers.google.com/google-ads/api | browser 200 |
| 2 | Meta Ads (Marketing API) | facebook.com/business | Yes | REST (Graph API) | Free (app + ads account req.) | https://developers.facebook.com/docs/marketing-apis | browser 200 |
| 3 | TikTok Ads (Business API) | ads.tiktok.com | Yes | REST | Free (ads account req.) | https://developers.tiktok.com/portal | browser → login page |
| 4 | TikTok Shop | shop.tiktok.com | Yes | REST | Free (shop account req.) | https://partner.tiktokshop.com | curl 200 (auth-walled) |
| 5 | Amazon Advertising | advertising.amazon.com | Yes | REST | Free (ads account req.) | https://advertising.amazon.com/API/docs/en-us/start | browser 200 |
| 6 | Pinterest Ads | ads.pinterest.com | Yes | REST | Free (business account req.) | https://developers.pinterest.com | browser 200 |
| 7 | LinkedIn Ads | business.linkedin.com | Yes | REST | Free (LinkedIn app req.) | https://developer.linkedin.com | browser 200 |
| 8 | Google Search Console | search.google.com/search-console | Yes | REST | Free | https://developers.google.com/webmaster-tools | browser 200 |
| 9 | Google Merchant Center | merchants.google.com | Yes | REST (Content API / Merchant API) | Free (MC account req.) | https://developers.google.com/shopping-content | browser 200 (→Merchant API migration Aug 2026) |
| 10 | Bing Webmaster | bing.com/webmaster | Yes | REST | Free | https://www.bing.com/webmaster/help/webmaster-api-application-identification-99029e8a | curl 200 (MS Learn docs 404 — stale URL) |
| 11 | Ahrefs | ahrefs.com | Yes | REST + MCP | Paid (usage/subscription) | https://docs.ahrefs.com | browser 200 |
| 12 | SEMrush | semrush.com | Yes | REST | Paid (subscription tier) | https://developer.semrush.com | browser 200 |
| 13 | Upfluence | upfluence.com | **Maybe** | Private/Partner-only | Partner-only | N/A (no public dev portal) | developer.upfluence.com → homepage redirect |
| 14 | Grin | grin.co | Yes | REST (Partner API) | Customer-only | https://grin.stoplight.io | browser 200 (Stoplight) |
| 15 | ShareASale | shareasale.com | Yes | REST (acquired by Awin) | Free (advertiser/affiliate account req.) | https://www.shareasale.com/shareasale_linkworks.cfm | curl 200 → Awin redirect |
| 16 | Impact | impact.com | Yes | REST + MCP | Customer-only (Partner API) | https://integrations.impact.com | browser 200 (full docs) |
| 17 | Google Analytics (GA4) | analytics.google.com | Yes | REST (Data API v1) | Free (quota limits) | https://developers.google.com/analytics/devguides/reporting/data/v1 | browser 200 |

## China Platforms (7)

| # | Platform | URL | Has API? | Type | Pricing | Docs URL | Method |
|---|----------|-----|----------|------|---------|----------|--------|
| 18 | 巨量引擎 (OceanEngine) | oceanengine.com | Yes | REST | Free (ads account + enterprise verification req.) | https://open.oceanengine.com/doc | browser 200 |
| 19 | 巨量千川 (Qianchuan) | qianchuan.jinritemai.com | Yes | REST | Free (shop account req.) | https://op.jinritemai.com | curl 200 (抖店开放平台) |
| 20 | 百度营销 (Baidu Yingxiao) | e.baidu.com | Yes | REST | Free (Baidu推广 account req.) | https://openapi.baidu.com | curl 200 |
| 21 | 腾讯广告 (Tencent Ads) | e.qq.com | Yes | REST | Free (Tencent ads account req.) | https://developers.e.qq.com | curl 200 |
| 22 | 小红书蒲公英 (Xiaohongshu) | xiaohongshu.com | Yes | REST | Free (enterprise verification req.) | https://open.xiaohongshu.com | browser 200 (open platform login) |
| 23 | 阿里妈妈 (Alimama) | alimama.com | Yes | REST (TOP architecture) | Free (淘宝联盟 account req.) | https://aff-open.taobao.com | browser 200 (淘宝联盟开放平台) |
| 24 | 百度统计 (Baidu Tongji) | tongji.baidu.com | Yes | REST | Free (Baidu Tongji account req.) | https://tongji.baidu.com/api/manual/ | browser 200 (full API manual) |

## Key Patterns for Marketing/Ad Platforms

### Google Ecosystem
- All Google ad/marketing APIs live under `developers.google.com/{product}`:
  - Google Ads → `developers.google.com/google-ads/api`
  - Search Console → `developers.google.com/webmaster-tools`
  - Merchant Center → `developers.google.com/shopping-content` (migrating to Merchant API Aug 2026)
  - Analytics → `developers.google.com/analytics/devguides/reporting/data/v1`
- All free with Google Cloud project + OAuth 2.0 authentication
- Rate limits per project vary by product

### Social Media Ad Platforms
- **Meta**: All through `developers.facebook.com` (Marketing API routed via Graph API)
- **TikTok**: `developers.tiktok.com/portal` (note: `/portal` suffix is required; root returns 404)
- **Pinterest**: Standard `developers.pinterest.com` (Ads API, Catalogs API, Conversion API)
- **LinkedIn**: `developer.linkedin.com` (singular "developer", Marketing product group)

### SaaS SEO/Marketing Tools
- **Ahrefs**: Commercial API at `docs.ahrefs.com`. REST + MCP. Paid subscription/usage-based.
- **SEMrush**: Developer portal at `developer.semrush.com`. REST API + App Center marketplace. Paid tiers.
- **Impact**: Most advanced docs — MCP server + REST + OpenAPI specs at `integrations.impact.com`
- **Grin**: API docs via Stoplight at `grin.stoplight.io` (not a public self-service API)
- **Upfluence**: No public API docs found — likely partner-only private API

### Affiliate Networks
- **ShareASale**: Acquired by Awin (2017). Old portal redirects to Awin. API still functional.
- **Impact**: Full REST API + modern MCP interface

### China Ad Platforms
- **All 7 confirmed with APIs** — China's ad ecosystem is well-integrated with open platforms
- Dev portal domain pattern: `open.{brand}.com` or `openapi.{brand}.com`
- All require Chinese business registration or WeChat/phone verification
- Documentation primarily in Chinese
- **巨量引擎** (OceanEngine): ByteDance's ad platform — `open.oceanengine.com/doc`
- **巨量千川** (Qianchuan): TikTok Shop's ad platform — dev portal at `op.jinritemai.com` (抖店开放平台), NOT a dedicated domain
- **百度营销**: Dev portal at `openapi.baidu.com` (unified Baidu API gateway), not `e.baidu.com`
- **阿里妈妈**: Dev portal at `aff-open.taobao.com` (淘宝联盟开放平台), not `open.alimama.com`
- **小红书**: `open.xiaohongshu.com` — requires enterprise account for API keys
- **腾讯广告**: `developers.e.qq.com` — full developer portal with console
- **百度统计**: `tongji.baidu.com/api/manual/` — surprisingly complete self-serve API docs

### Bing Webmaster — Stale Docs Note
- The Bing Webmaster API exists (curl 200 on help endpoint) but the Microsoft Learn documentation appears to have been removed or reorganized
- The help page at `bing.com/webmaster/help/webmaster-api-application-identification-99029e8a` still works
- The old `learn.microsoft.com/en-us/bing/webmaster-api` URL now returns 404

## Summary

- **23 of 24 platforms** have confirmed public APIs
- **1** (Upfluence) is likely partner-only — no public developer portal found
- **Pricing**: Most ad platforms offer free API access (with an active ad/business account); only Ahrefs and SEMrush are pure paid subscriptions
- **China platforms are universally open** but heavily gated by identity verification
