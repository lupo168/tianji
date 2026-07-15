---
title: Russia Confirmed APIs (13 platforms)
version: v1.0
date: 2026-07-14
license: MIT
description: API availability verification report. Methods: curl/browser direct probe.
---

# Russia API Availability: 13 Platforms (Verified)

> Verified: 2026-07-14 | Method: AnySearch + curl/browser probe
> Geo constraint: Russian sites are geo-blocked from non-Russian IPs (WBAAS/anti-bot). Results based on AnySearch web index + selective curl endpoint tests.

| # | Platform | URL | Has API? | Type | Pricing | Docs URL | Method Used |
|---|----------|-----|----------|------|---------|----------|------------|
| 1 | Ozon Seller API | ozon.ru | **Yes** | REST (OpenAPI v3) | Free with seller account | docs.ozon.ru/api/seller/ | AnySearch + GitHub client refs → confirmed |
| 2 | Yandex Market | market.yandex.ru | **Yes** | REST (OpenAPI) | Free with seller account | yandex.ru/dev/market/partner-api/doc/en/ | AnySearch → official docs found |
| 3 | Avito | avito.ru | **Yes** | REST (OAuth2) | Free with paid tariff (Базовый/Расширенный/Максимальный) | developers.avito.ru | AnySearch → developer portal confirmed |
| 4 | AliExpress Russia | aliexpress.ru | **Yes** | REST | Free with seller account | business.aliexpress.ru/docs | AnySearch → official docs found |
| 5 | VK | vk.com | **Yes** | REST API | Free (with app registration) | dev.vk.com (site under maintenance, classic docs at vk.com/dev) | AnySearch + curl (dev.vk.com returns 200) |
| 6 | Odnoklassniki | ok.ru | **Yes** | REST | Free (with app registration) | apiok.ru/en/dev/methods/ | AnySearch → official docs confirmed |
| 7 | Yandex (general) | yandex.ru | **Yes** | Multiple (REST/SOAP) | Mixed free/commercial | yandex.com/dev/ | AnySearch + curl (200) → confirmed |
| 8 | Yandex Webmaster | webmaster.yandex.ru | **Yes** | REST | Free | yandex.com/dev/webmaster/ | AnySearch → official docs confirmed |
| 9 | Rosstat | rosstat.gov.ru | **Yes** (commercial) | REST (SOAP/XML also) | Commercial (paid) — 8,070–274,956 RUB/year | gmcgks.ru/720 (via GMC subsidiary) | AnySearch → GMC portal with pricing confirmed |
| 10 | CBR | cbr.ru | **Yes** | SOAP + XML/REST | Free | cbr.ru/scripts/XML_daily.asp + cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL | curl → verified live XML data + SOAP WSDL |
| 11 | YooMoney | yoomoney.ru | **Yes** | REST (OAuth2) | Free + commercial (YooKassa) | yoomoney.ru/docs/wallet | AnySearch → official docs confirmed |
| 12 | Tinkoff | tinkoff.ru | **Yes** | REST (OpenAPI) | Commercial (contract needed) | developer.tinkoff.ru | AnySearch → official dev portal confirmed |
| 13 | Qiwi | qiwi.com | **Yes** | REST (OAuth2) | Commercial (B2B contract) | developer.qiwi.com | AnySearch + curl (200) → confirmed |

## Summary

- **13/13 have APIs** — all confirmed with official documentation
- **Pricing ranges:**
  - **Free:** CBR, Yandex Webmaster, Yandex general, VK, OK
  - **Free with seller/account:** Ozon, Yandex Market, Avito (paid tariff required), AliExpress Russia, YooMoney (wallet)
  - **Commercial (paid/contract):** Rosstat (GMC, 8k-275k RUB/year), Tinkoff (contract), Qiwi (B2B)
- **API types:** Predominantly REST (12/13), CBR uses SOAP + legacy XML
- **Key finding:** All platforms have well-documented APIs. Rosstat's main site (rosstat.gov.ru) also provides free CSV/Excel downloads but programmatic API access is through their commercial GMC subsidiary.
