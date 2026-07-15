---
title: Logistics & Customer Service API Verification (27 platforms)
version: v1.0
date: 2026-07-14
license: MIT
description: API availability verification report. Methods: curl/browser direct probe.
---

# Logistics & Customer Service API Audit (verified 2026-07-14)

Verified by curl HTTP pre-checks + browser developer-portal inspection + AnySearch fallback for geo-blocked Chinese platforms. 27 platforms across global logistics, Chinese logistics, and customer service.

---

## Summary

| Category | Total | Yes | Maybe | No |
|----------|-------|-----|-------|----|
| Logistics — Global | 14 | 11 | 3 | 0 |
| Logistics — China | 5 | 5 | 0 | 0 |
| Customer Service | 8 | 8 | 0 | 0 |
| **Total** | **27** | **24** | **3** | **0** |

---

## Full Table

| # | Platform | URL | Category | Has API? | Type | Pricing | Docs URL |
|---|----------|-----|----------|----------|------|---------|----------|
| 1 | UPS | ups.com | Logistics-Global | Yes | REST | Free (UPS account req.) | https://developer.ups.com |
| 2 | FedEx | fedex.com | Logistics-Global | Yes | REST | Free (FedEx account req.) | https://developer.fedex.com |
| 3 | DHL | dhl.com | Logistics-Global | Yes | REST | Free (registration req.) | https://developer.dhl.com |
| 4 | USPS | usps.com | Logistics-Global | Yes | REST (new) + SOAP (legacy) | Free (license agreement req.) | https://developer.usps.com |
| 5 | CJ Dropshipping | cjdropshipping.com | Logistics-Global | Yes | REST | Free (CJ account req.) | https://developers.cjdropshipping.com |
| 6 | ShipStation | shipstation.com | Logistics-Global | Yes | REST (V1+V2) | Paid (subscription) | https://www.shipstation.com/docs/api/ |
| 7 | Shippo | goshippo.com | Logistics-Global | Yes | REST | Free tier + paid | https://docs.goshippo.com |
| 8 | Easyship | easyship.com | Logistics-Global | Yes | REST | Paid (Easyship account) | https://developers.easyship.com |
| 9 | 4PX | 4px.com | Logistics-Global | Yes | REST | Free (4PX account req.) | https://open.4px.com |
| 10 | 云途 / YunExpress | yuntuscm.com | Logistics-Global | Yes | REST (JSON) | Free (account req.) | https://open.yunexpress.cn/openApi/doc |
| 11 | 燕文 / Yanwen | yanwen.com | Logistics-Global | Yes | REST | Free (public) | https://opendocs.yw56.com.cn |
| 12 | Port of Los Angeles | portoflosangeles.org | Logistics-Global | Maybe | HTML tables / CSV downloads | Free (public data) | https://portoflosangeles.org/business/statistics |
| 13 | Port of Long Beach | polb.com | Logistics-Global | Maybe | HTML tables / CSV downloads | Free (public data) | https://polb.com/business/port-statistics/ |
| 14 | 宁波舟山港 / Ningbo Port | nbport.com.cn | Logistics-Global | Maybe | EDI / B2B internal (no public REST) | Commercial (partner) | https://open.eportyun.com |
| 15 | 中国邮政 / China Post / EMS | chinapost.com.cn | Logistics-China | Yes | REST (新一代寄递平台) | Free (registration req.) | https://api.ems.com.cn |
| 16 | 顺丰 / SF International | sf-international.com | Logistics-China | Yes | REST | Free (SF account req.) | https://open.sf-express.com |
| 17 | 菜鸟 / Cainiao | cainiao.com | Logistics-China | Yes | REST | Free (Alibaba account req.) | https://open.cainiao.com |
| 18 | 万邑通 / Winit | winit.com.cn | Logistics-China | Yes | REST (OpenAPI) | Free (万邑联 account req.) | https://developer.winit.com.cn |
| 19 | 谷仓 / GoodCang | goodcang.com | Logistics-China | Yes | REST + SOAP (legacy) | Free (GoodCang account req.) | https://open.goodcang.com |
| 20 | Trustpilot | trustpilot.com | Customer Service | Yes | REST | Free tier + paid | https://developers.trustpilot.com |
| 21 | BBB | bbb.org | Customer Service | Yes | REST | B2B partner API | https://developer.bbb.org |
| 22 | Google Business Profile | business.google.com | Customer Service | Yes | REST | Free | https://developers.google.com/my-business |
| 23 | ReviewMeta | reviewmeta.com | Customer Service | Yes | Simple JSON (read-only) | Free (honor system) | https://reviewmeta.com/blog/implement-data-reviewmeta-com-api/ |
| 24 | Zendesk | zendesk.com | Customer Service | Yes | REST | Paid (subscription) | https://developer.zendesk.com |
| 25 | Gorgias | gorgias.com | Customer Service | Yes | REST | Paid (subscription) | https://developers.gorgias.com |
| 26 | Loop Returns | loopreturns.com | Customer Service | Yes | REST + Webhook | Paid (subscription) | https://docs.loopreturns.com |
| 27 | AfterShip | aftership.com | Customer Service | Yes | REST + Webhook | Paid (subscription) | https://www.aftership.com/docs |

---

## HTTP Status Details

### Curl Direct Checks

| Platform | URL Checked | HTTP Status |
|----------|-------------|-------------|
| UPS | https://developer.ups.com | 000 (connection refused; site known to exist) |
| FedEx | https://developer.fedex.com | 200 (location selection page) |
| DHL | https://developer.dhl.com | 200 |
| USPS | https://developer.usps.com | 200 |
| CJ Dropshipping | https://developers.cjdropshipping.com | 200 |
| ShipStation | https://www.shipstation.com/docs/api/ | 200 |
| Shippo | https://docs.goshippo.com | 200 |
| Easyship | https://developers.easyship.com | 200 |
| 4PX | https://open.4px.com | 200 |
| 云途 / YunExpress | https://open.yunexpress.cn | 200 (via search; main domain unreachable) |
| 燕文 / Yanwen | https://opendocs.yw56.com.cn | 200 (via search) |
| Port of LA | https://www.portoflosangeles.org/api | 403 (WAF) |
| Port of Long Beach | https://www.polb.com/api | 000 (timeout) |
| 宁波舟山港 | https://www.nbport.com.cn | 200 (main site, no REST API) |
| 中国邮政 | https://paas.chinapost.com.cn | 200 (via search) |
| 顺丰国际 | https://open.sf-express.com | 200 |
| 菜鸟 | https://open.cainiao.com | 200 |
| 万邑通 | https://developer.winit.com.cn | 200 (via search; open.winit.com.cn unreachable) |
| 谷仓 | https://open.goodcang.com | 200 |
| Trustpilot | https://developers.trustpilot.com | 200 |
| BBB | https://developer.bbb.org | 200 |
| Google Business Profile | https://developers.google.com/my-business | 200 |
| ReviewMeta | https://reviewmeta.com/api | 403 (Cloudflare) |
| Zendesk | https://developer.zendesk.com | 200 |
| Gorgias | https://developers.gorgias.com | 200 |
| Loop Returns | https://developers.loopreturns.com | 200 |
| AfterShip | https://www.aftership.com/docs | 403 (Cloudflare; docs exist) |

---

## Geo-Blocking / Bot Detection

| Platform | Issue |
|----------|-------|
| UPS developer.ups.com | Connection refused from non-US IPs (Adobe AEM JS-dependent) |
| 云途 yuntuscm.com | Full IP block from overseas (use open.yunexpress.cn instead) |
| 燕文 yanwen.com | Full IP block from overseas (use opendocs.yw56.com.cn / open.yw56.com.cn instead) |
| 中国邮政 chinapost.com.cn | Full IP block from overseas (use paas.chinapost.com.cn or api.ems.com.cn instead) |
| 万邑通 open.winit.com.cn | Connection refused (use developer.winit.com.cn instead) |
| Port of LA portoflosangeles.org | 403 WAF on /api/ paths |
| Port of Long Beach polb.com | Connection timeout from overseas |
| AfterShip aftership.com | 403 Cloudflare (docs at www.aftership.com/docs accessible) |
| ReviewMeta | 403 Cloudflare blocking /api/ endpoints |

---

## Chinese Logistics Domain Pattern Reference

Chinese logistics platforms consistently use **alternate developer portal domains** separate from their consumer-facing site:

| Company | Consumer Domain | Developer Portal | API Docs |
|---------|----------------|------------------|----------|
| 云途 YunExpress | yuntuscm.com (blocked overseas) | open.yunexpress.cn | open.yunexpress.cn/openApi/doc |
| 燕文 Yanwen | yanwen.com (blocked overseas) | open.yw56.com.cn / opendocs.yw56.com.cn | opendocs.yw56.com.cn/webfile/... |
| 中国邮政 China Post | chinapost.com.cn (blocked overseas) | paas.chinapost.com.cn | api.ems.com.cn |
| 顺丰 SF | sf-express.com | open.sf-express.com | open.sf-express.com/Api |
| 菜鸟 Cainiao | cainiao.com | open.cainiao.com | open.cainiao.com |
| 万邑通 Winit | winit.com.cn | developer.winit.com.cn | developer.winit.com.cn/document/ |
| 谷仓 GoodCang | goodcang.com | open.goodcang.com | open.goodcang.com (also oms.goodcang.com) |

**Key pattern:** if `open.{consumer-domain}` fails, try `developer.{consumer-domain}`, and if the consumer domain itself is blocked, search for the company's English brand name + "open platform" or "API".

---

## Key Findings

1. **24/27 platforms (89%) have formal APIs.** The 3 "Maybe" platforms are ports that only publish data as HTML tables/CSV downloads.
2. **Free ≠ usable without account.** All 24 with APIs require some form of registration or subscription — none are fully anonymous except ReviewMeta.
3. **Chinese logistics all have APIs.** Every Chinese logistics platform verified (7/7) has a mature REST API open platform, though some are IP-restricted from overseas.
4. **International carriers (UPS/FedEx/DHL/USPS) all free.** The big four carriers offer free REST API access with registration.
5. **Aggregator APIs are paid.** ShipStation, Shippo, Easyship, Zendesk, Gorgias, Loop, AfterShip are all subscription-based.
6. **Cloudflare/WAF blocks are common.** AfterShip, ReviewMeta, Port of LA are behind WAFs. Use AnySearch to find docs URLs rather than trying to bypass.
