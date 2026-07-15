---
title: 天玑 · 数据源接入成本总表
version: v1.0
date: 2026-07-14
license: MIT
description: 350+平台的数据源接入成本全景，含免费/需注册/付费/无API四种类型。
---

# 天玑 · 数据源接入成本总表

> 图例: ✅免费 💲付费 ❌无API 📡RSS

---

## 一、免费·无需注册（~60个）

### 央行/汇率
| 数据源 | API类型 | 说明 |
|--------|---------|------|
| CBR俄罗斯央行 | REST/SOAP | 实时汇率，境外可访 |
| Bank of England | REST | 英国央行利率/汇率 |
| Norges Bank (挪威) | REST | 挪威央行汇率 |
| Sveriges Riksbank (瑞典) | REST | 瑞典央行汇率 |
| IMF | REST | 全球经济数据 |
| World Bank | REST | 全球发展数据 |

### 美国政府
| 数据源 | API类型 | 说明 |
|--------|---------|------|
| FDA (OpenFDA) | REST | 食品/药品/医疗器械认证及召回 |
| FCC | REST/API | 电子设备认证 |
| CPSC | RSS | 消费品安全召回 |
| USPTO | REST | 商标/专利查询 |
| EPA | REST | 环保法规 |
| FTC | RSS | 消费者保护/竞争法 |
| BLS | REST | 就业/CPI统计数据 |
| BEA | REST | 经济数据 |
| FRED (美联储) | REST | 经济指标(需注册免费key) |

### 英国政府
| 数据源 | API类型 | 说明 |
|--------|---------|------|
| GOV.UK | REST | 政府综合信息 |
| Companies House | REST | 公司注册查询(需注册免费key) |
| UKIPO | REST | 商标/专利 |
| HMRC | REST | 税务/关税(需注册) |

### 国际组织
| 数据源 | API类型 | 说明 |
|--------|---------|------|
| EU Open Data | REST | 欧盟开放数据 |
| WTO | 文件下载 | 全球关税数据 |
| WIPO | REST | 国际知识产权 |

### 新闻/RSS免费
| 数据源 | 类型 | 说明 |
|--------|------|------|
| Google News | RSS | 聚合新闻 |
| BBC News | RSS | 国际新闻 |
| Reuters | RSS | 财经新闻(部分) |
| Nikkei Asia | RSS | 亚洲财经 |

### 科技/趋势
| 数据源 | API类型 | 说明 |
|--------|---------|------|
| Hacker News | REST | 科技创业趋势 |
| Wikipedia | REST | 热门话题/知识库 |
| Google Patents | REST | 全球专利搜索 |

---

## 二、免费·需注册API key（~40个）

| 数据源 | 免费额度 | 注册难度 |
|--------|---------|---------|
| ExchangeRate-API | 1000次/月 | ⭐ 简单 |
| YouTube Data | 10,000额度/日 | ⭐⭐ 需Google Cloud |
| Reddit | 60 req/min | ⭐⭐ 需注册OAuth App |
| Telegram Bot | 无限制 | ⭐ 创建Bot即可 |
| Tavily | 1000credits/月 | ⭐ 简单 |
| GitHub | 5000次/小时 | ⭐ 简单 |
| eBay | 有额度 | ⭐⭐ 需注册开发者 |
| Mercado Libre | 免费 | ⭐⭐ 需注册App |
| Ozon (俄罗斯) | 卖家免费 | ⭐⭐ 需注册卖家 |
| Wildberries | 卖家免费 | ⭐⭐ 需注册卖家 |
| Etsy | 免费 | ⭐⭐ 需注册开发者 |
| Shopify | 免费(有店) | ⭐⭐ 需创建App |
| PayPal | 免费 | ⭐ 简单 |
| Stripe | 免费 | ⭐ 简单 |
| Klarna | 免费 | ⭐⭐ 需申请 |
| Salla (沙特) | 免费 | ⭐⭐ 需注册 |

---

## 三、付费（~30个）

| 数据源 | 费用 | 说明 |
|--------|------|------|
| X/Twitter Basic | $100/月 | 最低档 |
| X/Twitter Pro | $5,000/月 | 高端 |
| Amazon SP-API | 按调用量 | 卖家必备 |
| Walmart API | 需商务 | 需审核签约 |
| Coupang Wing | 需商务 | 需韩国法人 |
| UnifAPI | $0.001/条 | 220+社交端点 |
| 4PX / 云途 / 燕文 | 需商务 | 物流商API |
| PingPong / 连连 | 需商务 | 跨境收款 |
| UPS / FedEx / DHL | 有免费额度 | 物流API |

---

## 四、无公开API（~20个）

只能网页监控或爬虫：

NSF / SIRIM / 各国标准机构 / 行业协会 / 部分展会 / 部分监管机构

---

## 五、自建开源

| 项目 | 说明 | 成本 |
|------|------|------|
| Crucix | 27个OSINT源聚合引擎 | 免费(需自托管) |
| AnySearch | 统一搜索API | 免费(匿名可用) |
