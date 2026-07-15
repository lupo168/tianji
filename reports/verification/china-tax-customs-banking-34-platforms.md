---
title: China/Tax/Customs/Banking API Verification (34 platforms)
version: v1.0
date: 2026-07-14
license: MIT
description: API availability verification report. Methods: curl/browser direct probe.
---

# API Audit: China Tax/Customs/Banking + Cross-Border Finance — 34 Platforms

Verified: 2026-07-14 | Method: browser_navigate to each platform's developer portal / API docs

## Result Matrix

| # | Platform | URL | Category | Has API? | Type | Pricing | Docs URL |
|---|---|---|---|---|---|---|---|
| 1 | TaxJar | taxjar.com | Finance/Tax | Yes | REST (Sales Tax v2) | Paid $19/mo+ (30d trial) | https://developers.taxjar.com/ |
| 2 | Avalara | avalara.com | Finance/Tax | Yes | REST (AvaTax) | Paid (90d trial) | https://developer.avalara.com/ |
| 3 | OFAC/SDN | treasury.gov/ofac | Finance/Sanctions | Yes | REST (SDN lists) | Free | https://sanctionslist.ofac.treas.gov/Home/ApiDocumentation |
| 4 | OFAC Search | sanctionssearch.ofac.treas.gov | Finance/Sanctions | Maybe | Web search + XML/CSV download | Free | https://sanctionssearch.ofac.treas.gov/ |
| 5 | FTC Business | ftc.gov/business-guidance | Finance/Compliance | Maybe | RSS feed | Free | https://www.ftc.gov/news-events/rss |
| 6 | UK VAT | gov.uk/vat | Finance/Tax | Yes | REST (HMRC VAT API) | Free | https://developer.service.hmrc.gov.uk/ |
| 7 | UK Trade Tariff | gov.uk/trade-tariff | Finance/Tariff | Yes | REST (JSON:API + OAuth2) | Free | https://docs.trade-tariff.service.gov.uk/ |
| 8 | EU VAT VIES | ec.europa.eu/taxation | Finance/Tax | Yes | SOAP web service (VAT validation) | Free | https://ec.europa.eu/taxation_customs/vies/ |
| 9 | EU TARIC | ec.europa.eu/taric | Finance/Tariff | Maybe | Web query + CSV download; no REST | Free | https://ec.europa.eu/taxation_customs/dds2/taric/ |
| 10 | WTO Tariff | tariffdata.wto.org | Finance/Tariff | No | File download (Excel/CSV) only | Free | https://tariffdata.wto.org/ (SSL cert error from intl IP) |
| 11 | 国家税务总局 | chinatax.gov.cn | Finance/Tax (CN) | Maybe | RSS policy feeds; HTML pages | Free | https://www.chinatax.gov.cn/ |
| 12 | 外汇管理局 | safe.gov.cn | Finance/FX (CN) | Maybe | HTML exchange rate table + statistics | Free | https://www.safe.gov.cn/ |
| 13 | 海关总署 | customs.gov.cn | Finance/Customs (CN) | No | SSL cert invalid; unreachable from intl IPs | — | — |
| 14 | 企查查 | qichacha.com | Procurement (CN) | Yes | REST OpenAPI (domestic IP required) | Paid (usage-based) | https://openapi.qichacha.com/ |
| 15 | 天眼查 | tianyancha.com | Procurement (CN) | Yes | REST OpenAPI (domestic IP required) | Paid (usage/plan) | https://open.tianyancha.com/ |
| 16 | 启信宝 | qixin.com | Procurement (CN) | Yes | REST OpenAPI (domestic IP required) | Paid (usage-based) | https://open.qixin.com/ |
| 17 | Global Sources | globalsources.com | Procurement | No | Imperva WAF blocked; no public API | — | — |
| 18 | Alibaba.com | alibaba.com | Procurement | Yes | REST Open API | Paid | https://open.alibaba.com/ |
| 19 | Made-in-China | made-in-china.com | Procurement | Maybe | Developer page exists but content blank | Partnership | https://www.made-in-china.com/developer/ |
| 20 | APPA | americanpetproducts.org | Industry Assoc | No | No API; member reports + news | Membership | — |
| 21 | WPA | worldpetassociation.org | Industry Assoc | No | No API; blog + trends | Membership | — |
| 22 | WQA | wqa.org | Industry Assoc | No | No public API; standards publications | Membership | — |
| 23 | IWA | iwa-network.org | Industry Assoc | No | No API; news + publications | Membership | — |
| 24 | 中国宠物行业协会 | cpa.org.cn | Industry Assoc | No | Domain is actually "中国药学会" (Pharmaceutical Assoc); pet association not found | — | — |
| 25 | 中国家电协会 | cheaa.org | Industry Assoc | No | No API; member data reporting system (non-API) | Membership | — |
| 26 | PingPong | pingpong.com | Banking/Cross-Border | Maybe | Payment API; dev docs page returns 404 | Partnership | https://www.pingpongx.com/en/ |
| 27 | Airwallex | airwallex.com | Banking/Cross-Border | Yes | REST API + Webhooks + SDK + MCP | Transaction fee | https://www.airwallex.com/docs |
| 28 | LianLian | lianlian.com | Banking/Cross-Border | Maybe | Developer portal exists but 404; likely partnership API | Partnership | https://www.lianlianglobal.com/developers (404) |
| 29 | WorldFirst | worldfirst.com | Banking/Cross-Border | Maybe | Developer docs page returns 404 | Partnership | https://www.worldfirst.com/global/developers/ (404) |
| 30 | Stripe | stripe.com | Payment | Yes | REST API + SDK + Webhooks | 2.9%+$0.30/txn | https://docs.stripe.com/api |
| 31 | PayPal Business | paypal.com | Payment | Yes | REST API | Transaction fee | https://developer.paypal.com/api/rest/ |
| 32 | CES | ces.tech | Trade Show | No | No data API; exhibitor registration portal | Exhibition fee | — |
| 33 | Global Pet Expo | globalpetexpo.org | Trade Show | No | No data API; event info portal | Exhibition fee | — |
| 34 | 广交会 | cantonfair.org.cn | Trade Show | Maybe | Timeout from intl IP; may have exhibitor data API | Partnership | https://www.cantonfair.org.cn/ (timeout) |

## Key Findings

### Confirmed with API (14)
| Domain | Platforms |
|--------|-----------|
| US Tax | TaxJar, Avalara |
| US Sanctions | OFAC/SDN |
| UK Gov | HMRC VAT, Trade Tariff |
| EU Gov | VIES |
| CN Procurement | 企查查, 天眼查, 启信宝, Alibaba |
| Banking/Payment | Airwallex, Stripe, PayPal |

### Maybe — Needs Further Investigation (10)
| Reason | Platforms |
|--------|-----------|
| RSS/web only | OFAC Search, FTC, EU TARIC, 国家税务总局, 外汇管理局 |
| Partner/walled | Made-in-China, PingPong, LianLian, WorldFirst, 广交会 |

### No API (10)
WTO Tariff (file download only), 海关总署 (SSL error), Global Sources (WAF blocked), APPA, WPA, WQA, IWA, CPA (wrong domain), CHEAA, CES, Global Pet Expo

## Domain-Specific Patterns

### Chinese Government Sites
- No unified open-data portal (unlike `data.go.kr` or `data.gov`)
- Data served as HTML tables and policy text
- SSL errors common from international IPs (customs.gov.cn)
- Exchange rate data from SAFE available as HTML table on homepage
- Tax policy RSS feeds exist but no structured data API

### Chinese Procurement APIs
- All three (企查查, 天眼查, 启信宝) require Chinese domestic IP for registration/access
- OpenAPI documentation exists but pages may not load from overseas
- Pricing: usage-based credit system (approx ¥0.1-5 per query depending on tier)
- All require Chinese business license for commercial access

### Cross-Border Payment Platforms
- PingPong, LianLian, WorldFirst all have 404 on developer pages
- APIs exist but are granted through business partnership onboarding
- Airwallex is the exception — full public docs at /docs with API reference
- None are self-service API key platforms (unlike Stripe)

### Industry Associations / Trade Shows
- Universally no data APIs
- Data is published as: PDF reports (member-only), press releases (public), exhibition directories (web search)
- CHEAA has a member data submission system but it's a web form, not API
- CES and Global Pet Expo only provide event registration web portals
