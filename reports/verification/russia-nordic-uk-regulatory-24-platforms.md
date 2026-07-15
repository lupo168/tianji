---
title: Russia/Nordic/UK Regulatory API Verification (24 platforms)
version: v1.0
date: 2026-07-14
license: MIT
description: API availability verification report. Methods: curl/browser direct probe.
---

# Russia + Nordic + UK: 24 Regulatory/Certification Platforms — API Audit (2026-07-14)

Coverage: Russia(5) + Sweden(6) + Norway(6) + UK(7) = 24 platforms.
Focus: government regulatory bodies, accreditation agencies, standards bodies, certification registries, food/drug/chemical/product safety authorities, customs/trade agencies.

## Results Matrix

| # | Platform | URL | Country | Has API? | Type | Docs URL |
|---|----------|-----|---------|----------|------|----------|
| **Russia** |
| 1 | Eurasian Economic Commission | eurasiancommission.org | Russia | **Yes** | OData (REST/JSON/Atom) | https://portal.eaeunion.org/sites/odata/odata/Pages/default.aspx |
| 2 | RusAccreditation | fsa.gov.ru | Russia | **Maybe** | Internal ФГИС API (VPN-only) | https://fgis2.fsa.gov.ru (non-public, VPN needed) |
| 3 | GOST Database (Rosstandart) | gost.ru | Russia | **RSS** | Open data CSV/HTML + RSS | https://www.gost.ru/portal/gost/home/activity/informationfacility |
| 4 | Rospatent | rospatent.gov.ru | Russia | **Yes** | REST API (OpenAPI/Swagger) | https://online.rospatent.gov.ru/open-data/open-api |
| 5 | Federal Customs Service (ФТС) | customs.gov.ru | Russia | **Yes** | Open data CSV + ТНВЭД queries | https://customs.ru/opendata |
| **Sweden** |
| 6 | Swedac | swedac.se | Sweden | **Yes** | REST API (JSON/XML, no key) | https://www.swedac.se/psidata/ |
| 7 | Kemikalieinspektionen | kemi.se | Sweden | **Maybe** | REST API (planned, not released) | https://www.kemi.se/bkmreg (future REST API) |
| 8 | Livsmedelsverket | livsmedelsverket.se | Sweden | **Yes** | REST API (Swagger/JSON) | https://dataportal.livsmedelsverket.se/livsmedel/swagger/index.html |
| 9 | PTS (Post- och telestyrelsen) | pts.se | Sweden | **Yes** | REST API (JSON, operator lookup) | https://catalog.pts.se/dokumentation/operator.html |
| 10 | SIS (Swedish Standards) | sis.se | Sweden | **No** | Commercial sales, no public API | N/A (SS12000 education data exchange standard exists) |
| 11 | Arbetsmiljöverket | av.se | Sweden | **RSS** | RSS news/events | https://www.av.se/om-oss/om-webbplatsen/rss-prenumerera/ |
| **Norway** |
| 12 | Norsk Akkreditering | akkreditert.no | Norway | **No** | Web search only | https://www.akkreditert.no/en/akkrediterte-organisasjoner/ |
| 13 | Mattilsynet | mattilsynet.no | Norway | **Yes** | REST API + open data | https://data.norge.no/datasets/... (meat inspection API + matvaretabellen.no) |
| 14 | Nkom | nkom.no | Norway | **Yes** | Open data JSON/XML (data.norge.no) | https://nkom.no/om-nkom/vare-opne-radata |
| 15 | Standard Norge | standard.no | Norway | **No** | Commercial sales, no public API | N/A |
| 16 | DSB (Direktoratet for samfunnssikkerhet) | dsb.no | Norway | **No** | Internal system (FAST, Altinn login) | N/A |
| 17 | Norsk Vann | norskvann.no | Norway | **No** | Trade association, not a regulator | N/A |
| **UK** |
| 18 | UKAS | ukas.com | UK | **Yes** | CertCheck (online verification DB) | https://www.ukas.com/certcheck/ |
| 19 | OPSS | gov.uk/opss | UK | **Maybe** | Product Safety DB (registration req.) | https://www.product-safety-database.service.gov.uk/ |
| 20 | Trading Standards | tradingstandards.uk | UK | **No** | Industry body (CTSI), no API | N/A (gov API directory: https://www.api.gov.uk/) |
| 21 | UK Trade Remedies | trade-remedies.service.gov.uk | UK | **Maybe** | Public case listings (web UI) | https://www.trade-remedies.service.gov.uk/public/cases/ |
| 22 | Drinking Water Inspectorate | dwi.gov.uk | UK | **No** | PDF/CSV annual reports only | https://www.dwi.gov.uk/what-we-do/annual-report/ |
| 23 | DEFRA | gov.uk/defra | UK | **Yes** | REST API (Linked Data APIs) | https://environment.data.gov.uk/apiportal |
| 24 | APHA | gov.uk/apha | UK | **Maybe** | Tableau dashboards + data.gov.uk | https://www.gov.uk/guidance/view-apha-surveillance-reports-publications-and-data |

## Summary

| Status | Count | Platforms |
|--------|-------|-----------|
| **Yes** (formal API) | 11 | EEC, Rospatent, Customs, Swedac, Livsmedelsverket, PTS, Mattilsynet, Nkom, UKAS, DEFRA |
| **Maybe** (limited/planned/restricted) | 5 | FSA, Kemi, OPSS, Trade Remedies, APHA |
| **RSS** (feeds + data downloads) | 2 | GOST, AV |
| **No** (no API) | 6 | SIS, Standard Norge, DSB, Norsk Vann, Norsk Akkreditering, Trading Standards, DWI |
| **Total** | **24** | |

## Key Patterns

### Russian regulatory sites
- EEC uses OData protocol at a dedicated portal (portal.eaeunion.org/sites/odata/)
- Rospatent has a dedicated OpenAPI platform (online.rospatent.gov.ru/open-data/open-api)
- FSA (RusAccreditation) requires corporate VPN (VipNet) — completely locked down; only third parties (apicrafter.ru, kontur.ru) provide access
- GOST's FGIS subsystems (BEREZA, ARSHIN) are internal-only with no public API
- Customs publishes open data as CSV dumps at customs.ru/opendata/

### Swedish authorities
- Most Swedish agencies have "Öppna data" (open data) portals — Swedac, Livsmedelsverket, PTS all offer free REST APIs with no API key required
- Swedac: JSON/XML, no key needed, new version coming mid-2025 (breaking changes)
- Kemi: pesticide register API is planned but not yet available
- Livsmedelsverket: Swagger-documented REST API with Creative Commons license
- PTS: operator lookup API at catalog.pts.se; admin endpoints behind auth

### Norwegian authorities
- Many open data sets published through the unified **data.norge.no** portal
- Mattilsynet: meat inspection APIs (Swagger), food composition API (matvaretabellen.no), and ephyto exchange on GitHub
- Nkom: JSON/XML open data feeds (authorizations, number plans, equipment registrations)
- DSB: Internal FAST system requiring Altinn login — no public data access
- Norsk Akkreditering: web search only, no API

### UK authorities
- DEFRA leads: comprehensive environment.data.gov.uk/apiportal with 12+ API categories (flood monitoring, water quality, ecology, tide gauges, etc.)
- OPSS: Product Safety Database exists but requires registration — not self-service
- UKAS: CertCheck online database — web interface, no documented REST API
- APHA: Tableau dashboards (embeddable) + data.gov.uk CSV/PDF downloads
- DWI: Raw water quality data not publicly released (only FOI-accessible)
- Trading Standards (CTSI): industry association, not a direct regulator with API

## Geo-Access Notes
- Russian sites (gost.ru, eurasiancommission.org) are slow or intermittent from non-Russian IPs
- PTS (pts.se) returns 403 to curl; API docs found via search engine results
- All Swedish, Norwegian, and UK sites were reachable from international IPs
- Standard bodies (SIS, Standard Norge) universally have no public APIs — standards are copyrighted, sold by subscription
