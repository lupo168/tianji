---
title: Southeast Asia Platform API Verification (28 platforms)
version: v1.0
date: 2026-07-14
license: MIT
description: API availability verification report. Methods: curl/browser direct probe.
---

# SEA 28-Platform API Audit — July 2026

Korea (10) + Singapore (6) + Malaysia (5) + Thailand (7) = 28 platforms.  
Verification method: curl HTTP status + browser portal inspection from a Windows machine on a commercial ISP.

## Summary

| Rating | Count | Platforms |
|--------|-------|-----------|
| **Yes** | 5 | Auction, Daum, NaverPay, Naver Cafe, IRAS |
| **Maybe** | 14 | Gmarket, 11Street, KCS Customs, KFTC, Qoo10 SG, SG Customs, SSM, Royal Customs MY, MyIPO, Touch 'n Go, DBD, Thai Customs, DIP, TrueMoney |
| **No** | 9 | Interpark, KC Certification, Carousell, Enterprise SG, Spring SG, PG Mall, Central Online, TIS, PromptPay |

## Full Results Table

| # | Platform | Country | URL | Has API? | Type | Pricing | Docs URL | Method |
|---|----------|---------|-----|----------|------|---------|----------|--------|
| 1 | Gmarket | 🇰🇷 | gmarket.co.kr | Maybe | Seller API (ESM) | Seller account required | dev.gmarket.com (tech blog only) | curl 200 → blog, no API portal |
| 2 | 11Street | 🇰🇷 | 11st.co.kr | Maybe | Seller Tool | Seller account required | None | curl 200 → no dev portal found |
| 3 | Interpark | 🇰🇷 | interpark.com | No | — | — | — | developers.interpark.com DNS fail |
| 4 | Auction | 🇰🇷 | auction.co.kr | **Yes** | Open API (REST/SOAP) | Free (registration) | https://developer.auction.co.kr/ | Browser → full portal, notices, API list |
| 5 | Daum | 🇰🇷 | daum.net | **Yes** | REST (Kakao) | Free (daily quota) | https://developers.kakao.com/docs/ko/daum-search/dev-guide | Browser → dev guide confirmed |
| 6 | NaverPay | 🇰🇷 | naverpay.com | **Yes** | Payment REST | Transaction-based | https://developers.pay.naver.com/ | Browser → complete dev center |
| 7 | KCS Customs | 🇰🇷 | customs.go.kr | Maybe | Open Data | Free | https://data.customs.go.kr/ | Timed out (IP blocked) |
| 8 | KC Certification | 🇰🇷 | kats.go.kr | No | — | — | — | kats.go.kr 200, kc.re.kr timeout |
| 9 | KFTC | 🇰🇷 | ftc.go.kr | Maybe | Open Data | Free | https://openapi.ftc.go.kr/ | ftc.go.kr 200, openapi blocked |
| 10 | Naver Cafe | 🇰🇷 | cafe.naver.com | **Yes** | REST | Free (50-200/day) | https://developers.naver.com/ | Naver API list confirms Cafe endpoints |
| 11 | Carousell | 🇸🇬 | carousell.com.sg | No | — | — | — | developers.carousell.com DNS fail |
| 12 | Qoo10 SG | 🇸🇬 | qoo10.sg | Maybe | Seller API | Seller account | — | developer.qoo10.com conn refused |
| 13 | IRAS | 🇸🇬 | iras.gov.sg | **Yes** | REST (OAuth 2.0) | Free (register) | https://apiservices.iras.gov.sg/iras/devportal/ | Browser → API marketplace confirmed |
| 14 | SG Customs | 🇸🇬 | customs.gov.sg | Maybe | TradeNet API | B2B | — | 403 CloudFront; tradexchange.gov.sg blocked |
| 15 | Enterprise SG | 🇸🇬 | enterprisesg.gov.sg | No | — | — | — | 200 → no API/developer section |
| 16 | Spring SG | 🇸🇬 | spring.gov.sg | No | — | — | — | Domain defunct (merged into Enterprise SG) |
| 17 | PG Mall | 🇲🇾 | pgmall.my | No | — | — | — | 403 Forbidden |
| 18 | SSM | 🇲🇾 | ssm.com.my | Maybe | Corporate Data | Paid B2B | https://www.ssm.com.my/ | ssm-einfo.my shows search portal; integration page returns 404 |
| 19 | Royal Customs | 🇲🇾 | customs.gov.my | Maybe | uCustoms B2B | B2B | — | 200 → no API portal |
| 20 | MyIPO | 🇲🇾 | myipo.gov.my | Maybe | IP Search | Likely free | — | Timed out |
| 21 | Touch 'n Go | 🇲🇾 | tngdigital.com.my | Maybe | Payment B2B | B2B | — | 200 (site), developer.tngdigital.com.my conn refused |
| 22 | Central Online | 🇹🇭 | central.co.th | No | — | — | — | Cloudflare blocked |
| 23 | DBD | 🇹🇭 | dbd.go.th | Maybe | Datawarehouse | Likely free | https://www.dbd.go.th/ | 200 → datawarehouse portal |
| 24 | Thai Customs | 🇹🇭 | customs.go.th | Maybe | NSW B2B | B2B | — | GDCC security block |
| 25 | DIP | 🇹🇭 | ipthailand.go.th | Maybe | IP Search | Likely free | — | Imperva hCaptcha block |
| 26 | TIS | 🇹🇭 | tis.go.th | No | — | — | — | Timed out |
| 27 | TrueMoney | 🇹🇭 | truemoney.com | Maybe | Payment B2B | B2B | — | Cloudflare blocked |
| 28 | PromptPay | 🇹🇭 | promptpay.io | No | — | — | — | SSL error; is a payment standard, not platform |

## Key Lessons from This Audit

1. **Naver & Kakao** are the two Korean mega-ecosystems for developer APIs — always check both.
2. **Korean gov (.go.kr)** sites are consistently unreachable from non-Korean IPs. Plan for this from the start.
3. **Singapore gov (.gov.sg)** sites are generally reachable; IRAS is the standout with a full API marketplace.
4. **Thai gov (.go.th)** sites use aggressive security gateways (GDCC, Imperva). Cloudflare-heavy.
5. **PromptPay** is frequently mistaken for an API platform — it's the Thai equivalent of UPI, a *standard* routed through commercial banks.
6. **Commerce platforms** (Gmarket, 11Street, Carousell, PG Mall, Central) rarely have public APIs — note as No or Maybe and qualify.
7. **SSM Malaysia** has a paid B2B corporate data integration service — not free, not self-service.

## HTTP Status Code Reference

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Site reachable | Inspect for API/developer section |
| 403 | WAF/CloudFront blocking | Try alternative URL or country proxy |
| 000 / timeout | Connection refused or blocked | IP-level blocking |
| DNS fail (exit 6) | Subdomain does not exist | No dev portal at that URL |
| Cloudflare page | Bot detection triggered | Note limitation |
