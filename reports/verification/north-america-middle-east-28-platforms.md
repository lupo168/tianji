---
title: North America + Middle East Platform API Verification (28 platforms)
version: v1.0
date: 2026-07-14
license: MIT
description: API verification for Canada, Mexico, Saudi Arabia, UAE platforms.
---

# 天玑(Tianji) API可用性验证报告

**生成时间**: 2026-07-14  
**验证方法**: 浏览器访问 + 任意搜索 + curl HTTP探测  
**覆盖范围**: 28个平台，涵盖加拿大、墨西哥、沙特、阿联酋及全球平台

---

## 综合结果表

| # | 平台 | 国家/地区 | URL | 有API? | API类型 | 定价 | 文档地址 |
|---|------|----------|-----|--------|---------|------|---------|
| 1 | Canada Revenue Agency (CRA) | 加拿大 | canada.ca/cra | Maybe | XML Schema/IFT (非REST) | 免费(需注册CRA账户) | https://www.canada.ca/en/revenue-agency/services/e-services/filing-information-returns-electronically-t4-t5-other-types-returns-overview/xml-specs.html |
| 2 | CBSA (边境服务局) | 加拿大 | cbsa-asfc.gc.ca | **Yes** | REST API (Swagger) | 免费(CARM系统) | https://ccp-pcc.cbsa-asfc.cloud-nuage.canada.ca/en/carm-api |
| 3 | Competition Bureau | 加拿大 | competitionbureau.gc.ca | **No** | — | — | — |
| 4 | Innovation Canada (ISED) | 加拿大 | ised-isde.canada.ca | **Yes** | REST API (OpenAPI) | 免费(需订阅API Plan) | https://api.ised-isde.canada.ca/en |
| 5 | Kijiji | 加拿大 | kijiji.ca | **No** | — | — | — |
| 6 | Walmart México | 墨西哥 | walmart.com.mx | **Yes** | REST API | 需注册为Walmart卖家 | https://developer.walmart.com/mx-marketplace |
| 7 | Coppel | 墨西哥 | coppel.com | **No** | — | — | — |
| 8 | Linio | 墨西哥 | linio.com.mx | **Yes** | REST API | 需注册为Seller Center用户 | https://developers.falabella.com |
| 9 | SAT (税务管理局) | 墨西哥 | sat.gob.mx | **Yes** | SOAP Web Services | 免费(需e.Firma/CIEC认证) | https://www.sat.gob.mx (CFDI Web Services文档) |
| 10 | SE Economía (经济部) | 墨西哥 | gob.mx/se | **Maybe** | VUCEM Web Services / Open Data | 免费(部分贸易服务需注册) | https://www.ventanillaunica.gob.mx (VUCEM) |
| 11 | COFEPRIS (卫生安全) | 墨西哥 | gob.mx/cofepris | **Yes** | SOAP Web Services | 免费(通过VUCEM) | https://www.ventanillaunica.gob.mx |
| 12 | IMPI (知识产权局) | 墨西哥 | gob.mx/impi | **Maybe** | SOAP Web Service (有限) | 免费 | https://www.impi.gob.mx/servicios/_vti_bin/search.asmx |
| 13 | Noon Saudi | 沙特 | noon.com/sa | **Yes** | REST API (JWT) | 需Noon卖家账户 | https://noon-docs.noonpartners.dev/ |
| 14 | Extra (电子零售) | 沙特 | extra.com | **No** | — | — | — |
| 15 | Haraj | 沙特 | haraj.com.sa | **Maybe** | GraphQL (内部,无官方文档) | 免费(非官方,需爬虫) | N/A |
| 16 | CMA (资本市场局) | 沙特 | cma.org.sa | **Yes** | REST API (Swagger/Open Data) | 免费(开放数据) | https://opendataapi.cma.gov.sa/swagger/ |
| 17 | Saudi Customs (ZATCA/海关) | 沙特 | customs.gov.sa | **Yes** | REST API (Open Data) | 免费(开放数据) | https://zatca.gov.sa/en/e-participation/PublicData/Pages/APIs.aspx |
| 18 | Argaam (金融数据) | 沙特 | argaam.com | **Maybe** | Data Feeds (订阅制) | SAR 7,500-40,000/年 | https://www.argaam.com (无公开API文档) |
| 19 | SPA (沙特通讯社) | 沙特 | spa.gov.sa | **No** | — | — | — |
| 20 | Noon UAE | 阿联酋 | noon.com/uae | **Yes** | REST API (JWT) | 需Noon卖家账户 | https://noon-docs.noonpartners.dev/ |
| 21 | Dubizzle | 阿联酋 | dubizzle.com | **No** | — | — | — |
| 22 | Dubai DED (经济发展局) | 阿联酋 | ded.ae | **Yes** | REST API (Open Data) | 免费(需API Key) | https://www.dubaipulse.gov.ae/data/ded-registration/ |
| 23 | DFM (迪拜金融市场) | 阿联酋 | dfm.ae | **Yes** | REST API | 需授权数据供应商 | https://api.dfm.ae |
| 24 | WAM (阿联酋通讯社) | 阿联酋 | wam.ae | **No** | — | — | — |
| 25 | Careem | 阿联酋 | careem.com | **Yes** | REST API (Careem Pay/API) | 需注册Careem Pay商家 | https://engineering.careem.com/tech/developerhub |
| 26 | Shopee Malaysia | 马来西亚 | shopee.com.my | **Yes** | REST API v2 | 需注册为开发者/卖家 | https://open.shopee.com (与SG同一平台) |
| 27 | SHFE (上海期货交易所) | 中国 | shfe.com.cn | **Yes** | C++ TraderAPI/MduserAPI (FTD) | 需交易所会员资格 | https://www.shfe.com.cn/eng/services/Technology/TechnicalSpecificationResource/ |
| 28 | Etsy | 全球 | etsy.com | **Yes** | REST API (Open API v3) | 免费(需注册App) | https://developers.etsy.com/documentation/ |

---

## 按地区统计

### 🇨🇦 加拿大 (5个)
| 状态 | 数量 | 平台 |
|------|------|------|
| **Yes** | 2 | CBSA, Innovation Canada (ISED) |
| **Maybe** | 1 | CRA (只有XML Schema/IFT, 非REST API) |
| **No** | 2 | Competition Bureau, Kijiji |

### 🇲🇽 墨西哥 (7个)
| 状态 | 数量 | 平台 |
|------|------|------|
| **Yes** | 4 | Walmart MX, Linio, SAT, COFEPRIS |
| **Maybe** | 2 | SE Economía (VUCEM), IMPI (有限SOAP) |
| **No** | 1 | Coppel |

### 🇸🇦 沙特 (7个)
| 状态 | 数量 | 平台 |
|------|------|------|
| **Yes** | 3 | Noon Saudi, CMA, Saudi Customs (ZATCA) |
| **Maybe** | 2 | Haraj (内部GraphQL), Argaam (订阅数据) |
| **No** | 2 | Extra, SPA |

### 🇦🇪 阿联酋 (6个)
| 状态 | 数量 | 平台 |
|------|------|------|
| **Yes** | 4 | Noon UAE, Dubai DED, DFM, Careem |
| **No** | 2 | Dubizzle, WAM |

### 🌐 全球 (3个)
| 状态 | 数量 | 平台 |
|------|------|------|
| **Yes** | 3 | Shopee MY (同SG平台), SHFE, Etsy |

---

## 汇总
- **有API (Yes)**: 16个 (57%)
- **可能有 (Maybe)**: 6个 (21%) — 部分有内部API或有限制接口
- **无API (No)**: 6个 (21%)
- **REST API**: 13个 | **SOAP**: 3个 | **C++/FTD**: 1个 | **订阅制**: 1个 | **XML/EDI**: 1个

## 关键发现
1. **Shopee** 使用统一的Open Platform，马来西亚和新加坡共用同一套API(v2)
2. **Noon** 沙特和阿联酋同一套API，不同国家不同endpoint
3. **Linio** 已被Falabella整合，API通过 `developers.falabella.com` 统一提供
4. **Walmart México** 有独立的墨西哥Marketplace API门户
5. **沙特海关** 通过ZATCA提供RESTful Open Data API
6. **CMA** 提供带Swagger文档的完整Open Data API
