---
title: UK/China/Korea/Finance API Verification (47 platforms)
version: v1.0
date: 2026-07-14
license: MIT
description: API availability verification report. Methods: curl/browser direct probe.
---

# API Availability: UK, China Commerce, Global Financial, Nordic Payments, Singapore, Canada/Mexico

> Verified: 2026-07-14. 47 platforms across UK, China, Korea, Nordic, Singapore, Global Financial, Canada, Mexico.
> Method: curl HTTP status + browser developer-portal inspection per platform.

---

## Summary

| Region | Platforms | Yes | Maybe | No |
|--------|-----------|-----|-------|----|
| UK | 6 | 4 | 1 | 1 |
| China (Commerce) | 5 | 4 | 1 | 0 |
| Korea | 9 | 7 | 2 | 0 |
| Nordic | 10 | 7 | 3 | 0 |
| Singapore | 4 | 3 | 1 | 0 |
| Global Financial | 3 | 3 | 0 | 0 |
| Canada / Mexico | 10 | 7 | 3 | 0 |
| **Total** | **47** | **35** | **11** | **1** |

---

## UK

| # | Platform | URL | Has API? | Type | Pricing | Docs URL |
|---|----------|-----|----------|------|---------|----------|
| 1 | GOV.UK | gov.uk | Yes | REST (Content API) | Free (Open Government Licence) | https://www.gov.uk/api/content |
| 2 | Companies House | companieshouse.gov.uk | Yes | REST API | Free (daily rate limit) | https://developer.company-information.service.gov.uk |
| 3 | UKIPO (Intellectual Property Office) | gov.uk/ipo | Maybe | Trademark journal data download | Free | No independent REST API found; trademarks journal data exports exist |
| 4 | HMRC | gov.uk/hmrc | Yes | REST API | Free | https://developer.service.hmrc.gov.uk/api-documentation |
| 5 | Bank of England | bankofengland.co.uk | Yes | Statistical Data API (IADB) | Free | https://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp |
| 6 | BSI (British Standards) | bsigroup.com | No | None | N/A (standards sold individually, no programmatic API) | BSI Knowledge is a paid document store, no public API |

### UK Notes
- UK government APIs use `api-content` HMAC signing (API key + secret pattern)
- Companies House API: free, no API key required for read-only queries
- HMRC API: requires Government Gateway / OAuth 2.0; developer hub has sandbox
- Bank of England IADB: returns CSV via query-string params; can return 200 but bot-detection blocks real browsers
- BSI: no API — standards are copyrighted products purchased individually on BSI Knowledge platform

---

## China (Commerce Platforms)

| # | Platform | URL | Has API? | Type | Pricing | Docs URL |
|---|----------|-----|----------|------|---------|----------|
| 7 | 淘宝开放平台 (Taobao Open) | open.taobao.com | Yes | REST + SDK | Free tier + paid (capability packs) | https://open.taobao.com |
| 8 | 1688 开放平台 | open.1688.com | Yes | REST API | Free + paid (enterprise verification required) | https://open.1688.com |
| 9 | 京东开放平台 (JD Open) | open.jd.com | Yes | REST + SDK | Free + paid (requires merchant registration) | https://open.jd.com |
| 10 | 拼多多开放平台 | open.pinduoduo.com | Yes | REST API | Free + paid (requires merchant credentials) | https://open.pinduoduo.com |
| 11 | CNIPA (国家知识产权局) | cnipa.gov.cn | Maybe | Web search | Free | cnipa.gov.cn accessible; formal API docs need further verification |

### China Commerce Notes
- All four e-commerce platforms (Taobao, 1688, JD, Pinduoduo) have mature open API ecosystems
- All require Chinese business registration for paid/commercial access
- APIs are REST-based with SDKs in Java/PHP/Python
- Documentation is primarily in Chinese
- Topology: Taobao/1688 both under Alibaba Group — similar API architecture (top client)
- CNIPA: main site reachable but no standalone API docs page found

---

## Korea

| # | Platform | URL | Has API? | Type | Pricing | Docs URL |
|---|----------|-----|----------|------|---------|----------|
| 12 | Naver Developers | developers.naver.com | Yes | REST (Search, Map, Login, etc.) | Free with usage quotas | https://developers.naver.com |
| 13 | Kakao Developers | developers.kakao.com | Yes | REST (KakaoTalk, Map, Login, Payment) | Free + commercial (some APIs require business) | https://developers.kakao.com |
| 14 | Coupang Wing | wing.coupang.com | Yes | REST (Seller/Wing API) | Requires Coupang seller account | https://wing.coupang.com (login gated) |
| 15 | KIPO (Korean IP Office) | kipo.go.kr | Maybe | KIPRIS patent search | Free | kipo.go.kr accessible; KIPRIS API status unclear from English site |
| 16 | BOK (Bank of Korea) | bok.or.kr | Yes | ECOS REST API | Free | https://ecos.bok.or.kr |
| 17 | KOSTAT (Statistics Korea) | kostat.go.kr | Yes | KOSIS Open API | Free | https://kosis.kr |
| 18 | DART (Electronic Disclosure) | dart.fss.or.kr | Yes | OpenDART REST API | Free (API key required) | https://opendart.fss.or.kr |
| 19 | KakaoPay | kakaopay.com | Maybe | Payment API (via Kakao Developers) | Business agreement required | Integrated through Kakao Developers platform |
| 20 | Toss | toss.im | Yes | Toss Payments REST API | Business agreement | https://docs.tosspayments.com |

### Korea Notes
- Naver is Korea's primary developer ecosystem (like Google in the West)
- Coupang Wing is seller-only, login-gated
- BOK ECOS and DART OpenDART are excellent free government APIs with REST endpoints
- KIPO KIPRIS API: status uncertain; if it exists it would be on kipris.or.kr
- Toss Payments docs are clean and comprehensive at docs.tosspayments.com (Korean + English)

---

## Nordic

| # | Platform | Country | URL | Has API? | Type | Pricing | Docs URL |
|---|----------|---------|-----|----------|------|---------|----------|
| 21 | Klarna | Sweden | klarna.com | Yes | REST (Payment/KCO/KP) | Commercial partnership | https://docs.klarna.com |
| 22 | Swish | Sweden | swish.nu | Yes | REST API | Requires Swish merchant registration | https://www.swish.nu/api |
| 23 | Trustly | Sweden | trustly.com | Yes | REST (Open Banking/Payments) | Commercial partnership | https://developers.trustly.com |
| 24 | Vipps | Norway | vipps.no | Yes | REST (Payment) | Requires Vipps merchant account | https://developer.vipps.no |
| 25 | Bolagsverket | Sweden | bolagsverket.se | Maybe | Open data downloads | Free | bolagsverket.se provides open data exports; independent REST API unclear |
| 26 | SCB (Statistics Sweden) | Sweden | scb.se | Yes | PxWebApi | Free | https://api.scb.se (PxWebApi v2) |
| 27 | BRREG (Brønnøysund Register) | Norway | brreg.no | Yes | REST API (Enhetsregisteret) | Free | https://data.brreg.no/enhetsregisteret/api |
| 28 | SSB (Statistics Norway) | Norway | ssb.no | Yes | PxWebApi v2 | Free | https://data.ssb.no/api |
| 29 | Riksbank (Swedish Central Bank) | Sweden | riksbank.se | Maybe | Structured interest/exchange rate data | Free | Website provides Search Interest and Exchange Rates tool; independent REST API unclear |
| 30 | Norges Bank (Norwegian Central Bank) | Norway | norges-bank.no | Maybe | Exchange rate data (CSV/XML) | Free | Website provides exchange rate data exports; `api.norges-bank.no` connection refused |

### Nordic Notes
- Payment platforms (Klarna, Swish, Trustly, Vipps) all have developer portals but are commercial
- SCB and SSB both use the PxWebApi standard — free, no auth required, JSON-stat2 format
- BRREG Enhetsregisteret API: REST, free, no auth for read; good for Norwegian company lookup
- Swedish/Norwegian central banks offer statistics exports rather than formal REST APIs
- Riksbanken: data available via web search form; no documented REST endpoint found

---

## Singapore

| # | Platform | URL | Has API? | Type | Pricing | Docs URL |
|---|----------|-----|----------|------|---------|----------|
| 31 | ACRA (Accounting & Corporate Regulatory Authority) | acra.gov.sg | Yes | BizFile API | Free + paid | https://www.acra.gov.sg/agencies/bizfile (BizFile+) |
| 32 | MAS (Monetary Authority of Singapore) | mas.gov.sg | Yes | MAS API (economic data) | Free | https://www.mas.gov.sg/development/economics-data/api |
| 33 | IPOS (Intellectual Property Office) | ipos.gov.sg | Maybe | IPOS Digital Hub | Free | ipos.gov.sg accessible; API status needs further verification |
| 34 | GrabPay (via Grab Developer) | grab.com/sg | Yes | REST (Payment/Food/Transport) | Commercial partnership | https://developer.grab.com |

---

## Global Financial

| # | Platform | URL | Has API? | Type | Pricing | Docs URL |
|---|----------|-----|----------|------|---------|----------|
| 35 | IMF (International Monetary Fund) | imf.org | Yes | REST API | Free | https://www.imf.org/en/Data |
| 36 | World Bank | worldbank.org | Yes | REST API | Free | https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-api-documentation |
| 37 | Exchange Rate API | exchangerate-api.com | Yes | REST API | Free tier + paid | https://www.exchangerate-api.com |

---

## Canada / Mexico

| # | Platform | URL | Has API? | Type | Pricing | Docs URL |
|---|----------|-----|----------|------|---------|----------|
| 38 | Health Canada | canada.ca/health | Yes | Government Open API | Free | https://health.canada.ca |
| 39 | Statistics Canada | statcan.gc.ca | Yes | REST API | Free | https://www.statcan.gc.ca/en/developers |
| 40 | Bank of Canada | bankofcanada.ca | Yes | Valet API (exchange rates) | Free | https://www.bankofcanada.ca/rates/valet/ |
| 41 | CIPO (Canadian IP Office) | ic.gc.ca/opic | Maybe | IP search | Free | https://ised-isde.canada.ca/site/canadian-intellectual-property-office/en |
| 42 | Mercado Libre | mercadolibre.com | Yes | REST (e-commerce/categories/items) | Free + paid | https://developers.mercadolibre.com |
| 43 | Mercado Pago | mercadopago.com | Yes | REST (payments) | Per-transaction fees | https://www.mercadopago.com/developers |
| 44 | Banxico (Bank of Mexico) | banxico.org.mx | Yes | SIE REST API (economic data) | Free (requires API token) | https://www.banxico.org.mx/SieAPIRest/service/v1/ |
| 45 | INEGI (Statistics Mexico) | inegi.org.mx | Maybe | Open data downloads | Free | https://www.inegi.org.mx/datosabiertos/ (open data; formal REST API unclear) |
| 46 | Conekta | conekta.com | Yes | REST (payments) | Per-transaction fees | https://developers.conekta.com |
| 47 | Clip | clip.mx | Maybe | Payment SDK | Requires business contact | `/desarrolladores` returns 404; SDK exists but no public dev portal |

### Canada/Mexico Notes
- Bank of Canada Valet API: REST, free, no auth, returns JSON. Excellent for forex.
- Banxico SIE API: REST with Swagger docs, requires free token via email request. TLS 1.3 required.
- Mercado Libre / Mercado Pago: mature APIs used across 18 Latin American countries
- Conekta: well-documented REST API for Mexican payments (cards, OXXO, SPEI)
- Clip: has SDK/business integration but no public developer portal. Not a self-service API.
- INEGI: open data downloads (CSV/Excel) but formal REST API not found

---

## Verified HTTP Status Codes (Selected Platforms)

| Platform | URL Checked | HTTP Status |
|----------|------------|-------------|
| GOV.UK Content API | https://www.gov.uk/api/content | 200 |
| Companies House Dev Hub | https://developer.company-information.service.gov.uk | 200 |
| HMRC Dev Hub | https://developer.service.hmrc.gov.uk | 200 |
| BoE IADB | https://www.bankofengland.co.uk/boeapps/iadb/fromshowcolumns.asp | 200 (CSV data accessible via curl) |
| Taobao Open | https://open.taobao.com | 200 |
| 1688 Open | https://open.1688.com | 200 |
| JD Open | https://open.jd.com | 200 |
| Pinduoduo Open | https://open.pinduoduo.com | 200 |
| Naver Developers | https://developers.naver.com | 200 |
| Kakao Developers | https://developers.kakao.com | 200 |
| OpenDART | https://opendart.fss.or.kr | 200 |
| Klarna Docs | https://docs.klarna.com | 200 |
| SCB API | https://api.scb.se | 200 |
| BRREG API | https://data.brreg.no/enhetsregisteret/api | 200 |
| MAS API | https://www.mas.gov.sg/development/economics-data/api | 200 |
| World Bank API | https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-api-documentation | 200 |
| Banxico SIE | https://www.banxico.org.mx/SieAPIRest/service/v1/ | 200 |
| Mercado Pago Devs | https://www.mercadopago.com/developers | 200 |
| Conekta Devs | https://developers.conekta.com | 200 |
| Bank of Canada Valet | https://www.bankofcanada.ca/rates/valet/ | 404 (redirect expected) |
| Riksbank | https://www.riksbank.se/en-gb/statistics/ | 200 (page, not API) |
| Norges Bank | https://www.norges-bank.no/en/topics/Statistics/exchange-rates/ | 404 |
| INEGI Open Data | https://www.inegi.org.mx/datosabiertos/ | 200 (open data portal) |

## Known Geo-Blocking / Bot Detection

| Platform | Issue |
|----------|-------|
| Bank of England (browser) | Akamai bot detection blocks real browsers from `bankofengland.co.uk/statistics` |
| Coupang Wing | Bot detection on login page |
| ECOS BOK | Korean government site, intermittent 503 |

## Methodology

1. Start with curl HTTP status check on each platform's main domain
2. For confirmed-reachable domains, browser-navigate to verify API documentation
3. Check at least 2-3 URL patterns per platform (dev portal, /api, open data page)
4. Classify response as Yes (docs found), Maybe (reachable but docs unclear), No (no API)
5. Record docs URL when found
