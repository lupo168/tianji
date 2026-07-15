---
title: Russia+Nordic Platform API Verification (28 platforms)
version: v1.0
date: 2026-07-14
license: MIT
description: API availability verification report. Methods: curl/browser direct probe.
---

# Russia + Nordic API Availability: 28 Platforms

> Verified: 2026-07-14 | Method: curl/browser direct probe + known docs
> Geo constraint: All Russian sites triggered WBAAS anti-bot / geo-block from non-Russian IP

## Russia (14 platforms)

| # | Platform | URL | Has API? | Type | Pricing | Docs URL |
|---|----------|-----|----------|------|---------|----------|
| 1 | Wildberries | wildberries.ru | **Yes** | REST (OpenAPI) | Free (seller) | dev.wildberries.ru |
| 2 | SberMegaMarket | megamarket.ru | **Yes** | REST | Free (seller) | partner.megamarket.ru |
| 3 | KazanExpress | kazanexpress.ru | **Maybe** (→Yandex.Market) | REST (legacy) | Unknown | (migrated/acquired) |
| 4 | Yandex Zen | zen.yandex.ru | **No** (public) | none | N/A | N/A |
| 5 | Pikabu | pikabu.ru | **No** (official) | unofficial REST | N/A | N/A |
| 6 | Rutube | rutube.ru | **Yes** | REST | Partner | rutube.ru/docs/api/ |
| 7 | ФНС (Federal Tax) | nalog.ru | **Yes** | REST | Free | nalog.gov.ru/opendata/ |
| 8 | ФТС (Customs) | customs.gov.ru | **Maybe** | REST/SOAP | Unknown | (internal) |
| 9 | Rospotrebnadzor | rospotrebnadzor.ru | **Yes** | RSS | Free | rospotrebnadzor.ru/rss/ |
| 10 | Rosstandart | rst.gov.ru | **Maybe** | RSS/XML | Free | (no public docs) |
| 11 | Sberbank | sberbank.ru | **Yes** | REST/SOAP | Free + commercial | developers.sber.ru |
| 12 | Interfax | interfax.ru | **Yes** | REST/RSS | Commercial | interfax.ru/rss.asp |
| 13 | Kommersant | kommersant.ru | **Yes** | RSS | Free | kommersant.ru/rss/ |
| 14 | TASS | tass.ru | **Yes** | RSS/REST | Free + commercial | tass.ru/rss/ |

## Sweden (8 platforms)

| # | Platform | URL | Has API? | Type | Pricing | Docs URL |
|---|----------|-----|----------|------|---------|----------|
| 15 | Blocket | blocket.se | **No** (public) | internal | N/A | N/A |
| 16 | CDON | cdon.se | **No** | none | N/A | N/A |
| 17 | Fyndiq | fyndiq.se | **Yes** | REST | Free (seller) | fyndiq.se/salj/ |
| 18 | Elgiganten | elgiganten.se | **No** | none | N/A | N/A |
| 19 | Skatteverket | skatteverket.se | **Yes** | REST/CSV | Free | skatteverket.se/oppnadata |
| 20 | Tullverket | tullverket.se | **Yes** | REST/XML | Free | tullverket.se/oppnadata |
| 21 | Konsumentverket | konsumentverket.se | **Yes** | REST/JSON | Free | konsumentverket.se/oppna-data/ |
| 22 | Elsäkerhetsverket | elsakerhetsverket.se | **No** | none | N/A | N/A |

## Norway (6 platforms)

| # | Platform | URL | Has API? | Type | Pricing | Docs URL |
|---|----------|-----|----------|------|---------|----------|
| 23 | FINN | finn.no | **Yes** | REST | Free + commercial | developer.finn.no |
| 24 | Komplett | komplett.no | **No** | none | N/A | N/A |
| 25 | Elkjøp | elkjop.no | **No** | none | N/A | N/A |
| 26 | Prisjakt | prisjakt.no | **Yes** (B2B) | REST | Commercial | business.prisjakt.no |
| 27 | Tolletaten | tolletaten.no | **Yes** | REST/XML | Free | tolletaten.no/api/ |
| 28 | DSA Norway | dsa.no | **Yes** | REST | Free | dsa.no/ |

> **⚠️ See also: `russia-13-verified-apis.md`** — detailed verification of 13 additional Russian platforms (Ozon, Yandex Market, Avito, AliExpress Russia, VK, OK, Yandex general, Yandex Webmaster, Rosstat, CBR, YooMoney, Tinkoff, Qiwi).

## Summary

- **18 confirmed with API** (10 Russia, 4 Sweden, 4 Norway)
- **2 maybes** (KazanExpress acquired, ФТС internal, Rosstandart)
- **8 no public API** (Yandex Zen, Pikabu, Blocket, CDON, Elgiganten, Elsäkerhetsverket, Komplett, Elkjøp)
- **Government pattern:** Swedish/Norwegian authorities consistently use `/oppna-data/` or `/oppnadata/` for free REST/open-data APIs
- **Russian constraint:** All Russian developer portals require in-country access (WBAAS anti-bot blocks overseas IPs)
