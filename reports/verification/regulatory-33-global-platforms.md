---
title: Global Regulatory & Certification API Verification (33 platforms)
version: v1.0
date: 2026-07-14
license: MIT
description: API availability verification report. Methods: curl/browser direct probe.
---

# Verified API Status: 33 Regulatory Platforms (Canada, Mexico, Korea, Malaysia, Thailand, Saudi, UAE, China)

**Verified:** 2026-07-14 | **Method:** AnySearch batch_search + browser direct verification

## Summary

| Region | Count | Yes | Maybe | No |
|--------|-------|-----|-------|----|
| 🇨🇦 Canada | 5 | 2 | 0 | 3 |
| 🇲🇽 Mexico | 4 | 2 | 0 | 2 |
| 🇰🇷 Korea | 4 | 3 | 1 | 0 |
| 🇲🇾 Malaysia | 4 | 1 | 0 | 3 |
| 🇹🇭 Thailand | 4 | 2 | 0 | 2 |
| 🇸🇦 Saudi | 2 | 2 | 0 | 0 |
| 🇦🇪 UAE | 4 | 3 | 1 | 0 |
| 🇨🇳 China | 6 | 1 | 1 | 4 |
| **Total** | **33** | **16** | **3** | **14** |

## Verified Entries

| # | Platform | URL | Country | Has API? | Type | Docs URL |
|---|----------|-----|---------|----------|------|---------|
| 1 | Standards Council of Canada (SCC) | scc.ca | 🇨🇦 | No | — | Standards Hub is member-only; no public API |
| 2 | CGSB | tpsgc-pwgsc.gc.ca/cgsb | 🇨🇦 | No | — | CGSB absorbed into Canada.ca; no standalone API |
| 3 | Measurement Canada | ic.gc.ca/mc | 🇨🇦 | No | — | Site behind bot-blocker (ISED); no known API |
| 4 | CFIA | inspection.gc.ca | 🇨🇦 | Yes | Open Data CSV | https://open.canada.ca/data/en/dataset?publisher=cfia |
| 5 | Environment Canada | canada.ca/environment | 🇨🇦 | Yes | OGC API (GeoMet) | https://api.weather.gc.ca/ |
| 6 | DGN | gob.mx/dgn | 🇲🇽 | No | — | NOM standards published via DOF; no API |
| 7 | CONUEE | conuee.gob.mx | 🇲🇽 | Yes | Open Data (datos.gob.mx) | https://www.datos.gob.mx/organization/conuee |
| 8 | PROFECO | gob.mx/profeco | 🇲🇽 | Yes | REST API (JSON) | https://datos.profeco.gob.mx/api.php |
| 9 | EMA | ema.org.mx | 🇲🇽 | No | — | Accreditation body website only |
| 10 | KTL | ktl.re.kr | 🇰🇷 | Yes | OpenAPI (data.go.kr) | https://www.data.go.kr/data/15124605/fileData.do |
| 11 | KTR | ktr.or.kr | 🇰🇷 | Maybe | Possibly via data.go.kr | Search data.go.kr for "KTR" |
| 12 | MFDS | mfds.go.kr | 🇰🇷 | Yes | REST API (JSON+XML) | https://www.data.go.kr/en/data/15058273/openapi.do |
| 13 | NIER | nier.go.kr | 🇰🇷 | Yes | GEMS Open-API (REST) | https://nesc.nier.go.kr/en/html/svc/openapi/explain.do |
| 14 | SIRIM | sirim.my | 🇲🇾 | No | — | Commercial certification body |
| 15 | JSM | jsm.gov.my | 🇲🇾 | No | — | MySOL + e-Accreditation web systems only |
| 16 | DVS | dvs.gov.my | 🇲🇾 | Yes | Open Data (data.gov.my) | https://www.dvs.gov.my/index.php/pages/view/1340 |
| 17 | ST (Energy Commission) | st.gov.my | 🇲🇾 | No | — | Regulatory web portal only |
| 18 | TISI | tis.go.th | 🇹🇭 | Yes | Open Data Portal | https://opendata.tisi.go.th/ |
| 19 | Thai FDA | fda.moph.go.th | 🇹🇭 | Yes | SOAP Web Service | https://porta.fda.moph.go.th/FDA_SEARCH_ALL/WS_LICENSE_SEARCH.asmx |
| 20 | DLD | did.go.th | 🇹🇭 | No | — | e-Service portal only |
| 21 | PCD | pcd.go.th | 🇹🇭 | Yes | JSON API (Air4Thai) | http://air4thai.pcd.go.th/services/getNewAQI_JSON.php |
| 22 | SFDA | sfda.gov.sa | 🇸🇦 | Yes | REST API (OAuth) | https://developer.sfda.gov.sa/ |
| 23 | Ministry of Commerce | mc.gov.sa | 🇸🇦 | Yes | REST API (SharePoint) | https://mc.gov.sa/en/About/Statistics/Pages/GISInfo.aspx |
| 24 | ESMA | esma.gov.ae | 🇦🇪 | Maybe | Merged into MOIAT | https://moiat.gov.ae/en/open-data/open-data-apis |
| 25 | MOIAT | moiat.gov.ae | 🇦🇪 | Yes | REST API (Open Data) | https://moiat.gov.ae/en/open-data/open-data-apis |
| 26 | Federal Customs (FCA/ICP) | fca.gov.ae | 🇦🇪 | Yes | REST API (Dubai Pulse) | https://www.dubaipulse.gov.ae/ |
| 27 | Dubai Municipality | dm.gov.ae | 🇦🇪 | Yes | REST API (Dubai Pulse) | https://www.dm.gov.ae/open-data2/ |
| 28 | CQC | cqc.com.cn | 🇨🇳 | No | — | CCC cert web query only |
| 29 | CNAS | cnas.org.cn | 🇨🇳 | No | — | Accreditation web system only |
| 30 | SAC | sac.gov.cn | 🇨🇳 | Maybe | Web search (std.samr.gov.cn) | https://std.samr.gov.cn/ |
| 31 | NIFDC | nifdc.org.cn | 🇨🇳 | No | — | Data query pages only |
| 32 | openstd.samr.gov.cn | openstd.samr.gov.cn | 🇨🇳 | No | — | Web-only GB standard search; community spider exists (openstd_spider) but no official API |
| 33 | CNCA (云桥) | cx.cnca.cn | 🇨🇳 | Yes | REST API (认证认可云桥) | https://yunqiao.cnca.cn/CNCACB |

## Key Regional Patterns

### 🇨🇦 Canada
- **CFIA** and most federal data goes through unified **open.canada.ca** portal (CKAN-based, CSV downloads, not REST API)
- **Environment Canada** is the exception — has a proper **MSC GeoMet OGC API** (`api.weather.gc.ca`) for weather/climate/water data
- Many gov sites (ISED, CFIA) use aggressive WAF blocking — detect via HTTP 403 `"The URL you requested has been blocked"` with Attack ID

### 🇲🇽 Mexico
- **PROFECO** has its own API subdomain (`datos.profeco.gob.mx`) — separate from the main `gob.mx` profile page, with GET-based JSON API + catalog endpoints
- **CONUEE** data goes through `datos.gob.mx` (unified Mexican open data portal)
- **EMA** (accreditation body) is a private non-profit — no public data API

### 🇰🇷 Korea (supplements sea-28-platforms.md)
- Most Korean agencies publish via **data.go.kr** (unified public data portal) — requires service key registration
- **MFDS** has the richest API ecosystem: imported food license info, drug info, nutritional DB — all REST JSON+XML
- **NIER** has its own GEMS Open-API for environmental satellite data (key application required, 7-day approval)
- **KTL/KTR** use data.go.kr for file data; direct site APIs are absent (they're testing labs, not data publishers)

### 🇲🇾 Malaysia (supplements sea-28-platforms.md)
- **DVS** publishes open data through the Malaysian data.gov.my portal
- **SIRIM, JSM, ST** are regulatory/commercial bodies with web portals only — no public APIs
- JSM's MySOL system sells MS standards online but offers no API

### 🇹🇭 Thailand (supplements sea-28-platforms.md)
- **Thai FDA** has a SOAP web service at `porta.fda.moph.go.th` for license search — WS_LICENSE_SEARCH.asmx
- **PCD** has the Air4Thai JSON API — no auth, free, returns real-time AQI data from hundreds of stations
- **DLD** has e-Service systems (e-Movement, e-Regist, e-Certify) but these are government internal platforms, not public APIs

### 🇸🇦 Saudi Arabia
- **SFDA** has an excellent developer portal at `developer.sfda.gov.sa` with Food, Drug, Medical Device, Cosmetics REST APIs (OAuth bearer token)
- **Ministry of Commerce** has SharePoint REST API for CR (commercial register) GIS data — API docs available as PDF on their site

### 🇦🇪 UAE
- **MOIAT** (which absorbed ESMA) has a clean Open Data API at `api.moiat.gov.ae` — GetIndustrialLicensesList, GetNotifiedBodiesList, GetRecalledProductsList — no auth required
- **Dubai Municipality** + **Federal Customs** data available through **Dubai Pulse** (`dubaipulse.gov.ae`) — CKAN-based, API key + secret required
- ESMA brand is legacy — all functions now under MOIAT

### 🇨🇳 China
- **CNCA 云桥** (Yunqiao) is the only formal API — certification data sharing platform with REST interfaces for CCC/organic/management system certificates
- Most others (CQC, CNAS, SAC, NIFDC) are web-only query systems
- **openstd.samr.gov.cn** (国家标准全文公开系统) has no official API, but the community `openstd_spider` Python library reverse-engineers the search/download endpoints
- Chinese sites often require captchas, Baidu analytics, and complex login portals

## Detection Patterns

### Government Open Data Portals (Common)
- `/opendata/`, `/open-data/`, `/datos-abiertos/` — check navigation
- Unified national portals: `open.canada.ca`, `datos.gob.mx`, `data.go.kr`, `data.gov.my`, `opendata.tisi.go.th`
- CKAN-based portals (open.canada.ca, dubaipulse.gov.ae) expose CKAN API at `/api/action/` → can list packages, resources, and data programmatically

### Latin American Government Sites
- Main site (`gob.mx/entidad`) is often a profile page — look for `datos.entidad.gob.mx` or `datos.gob.mx/organization/entidad`
- Mexico: PROFECO data lives at `datos.profeco.gob.mx`, NOT `profeco.gob.mx`

### Middle East Government Sites
- Saudi: `developer.sfda.gov.sa` is a full Apigee-style developer portal
- UAE: MOIAT has clean REST at `api.moiat.gov.ae` — test with curl before assuming auth needed
- UAE: Dubai Pulse (`dubaipulse.gov.ae`) is the central data marketplace — requires registration but many datasets are free

### East Asian Government Sites
- Korea: always check `data.go.kr` first — it's the unified OpenAPI gateway
- China: Most gov sites are web-only. Only CNCA has a formal API. Check `yunqiao.cnca.cn` for certification data
- Thailand: Thai FDA has SOAP (legacy), PCD has REST (modern) — unusual mix in same country
