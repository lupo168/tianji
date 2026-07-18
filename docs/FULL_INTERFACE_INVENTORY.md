# 天玑 · 全接口清单

> 覆盖：API / Token / MCP / CLI / RSS  
> 维度：免费/付费 | 开源/闭源 | 配额/限额  
> 更新：2026-07-18

---

## 一、已接入或可直接接入 ✅

| # | 平台 | 接口类型 | 认证方式 | 费用 | 开源 | 配额 | 采集器状态 |
|---|------|---------|---------|------|------|------|----------|
| 1 | Etsy Open API v3 | REST API | API Key | 免费 | 闭源 | 5 QPS / 5K QPD | ✅ 已接入 |
| 2 | Etsy MCP Server | MCP (HTTP) | 无 | 免费 | 闭源 | 不限 | ✅ 家里已配 |
| 3 | ProductHunt | GraphQL API | 无 | 免费 | 闭源 | 不限(无官方限流) | ✅ 已接入 |
| 4 | YouTube Data API v3 | REST API | API Key | 免费 | 闭源 | 10K 配额/日 | ✅ 已接入 |
| 5 | Reddit API | REST API | OAuth2 | 免费 | 部分开源 | 60 req/min | ✅ 已接入 |
| 6 | Telegram Bot API | REST API | Bot Token | 免费 | 开源 | 30 msg/sec | ✅ 已接入 |
| 7 | Hacker News (Algolia) | REST API | 无 | 免费 | 开源 | 不限 | ✅ 已接入 |
| 8 | Wikipedia / Wikimedia | REST API | 无 | 免费 | 开源 | 不限 | ✅ 已接入 |
| 9 | CBR (俄罗斯央行) | REST API | 无 | 免费 | 闭源 | 不限 | ✅ 已接入 |
| 10 | Google News | RSS | 无 | 免费 | 闭源 | 不限 | ✅ 已接入 |
| 11 | FRED (美联储) | REST API | API Key | 免费 | 闭源 | 120 req/min | ✅ 已接入 |
| 12 | Frankfurter (汇率) | REST API | 无 | 免费 | 开源 | 不限 | ✅ 已接入 |
| 13 | GitHub API | REST API | Token (PAT) | 免费 | 部分开源 | 5K req/hr | ✅ 已用(天玑仓库) |
| 14 | AnySearch | CLI / REST API | API Key | 免费 | 闭源 | 匿名额度 | ✅ 已接入 |

---

## 二、天玑采集器已有但需完善 🔧

| # | 平台 | 接口类型 | 认证方式 | 费用 | 问题 |
|---|------|---------|---------|------|------|
| 15 | Reddit | OAuth2 | 已淘汰 → v2 | 免费 | 需迁移到 v2 API |
| 16 | SEO/GEO 采集 | AnySearch wrapper | — | 免费 | 需改为独立 API (Google Trends/Google Search) |
| 17 | 营销情报 | AnySearch wrapper | — | 免费 | 需改为 Meta Ads Library API |
| 18 | 品牌声誉 | AnySearch wrapper | — | 免费 | 需改为 TrustPilot / Google Reviews API |
| 19 | 渠道政策 | AnySearch wrapper | — | 免费 | 需接入各平台 Developer Blog RSS |
| 20 | 公司情报 | AnySearch wrapper | — | 免费 | 需改为 Crunchbase / CB Insights API |

---

## 三、海外社媒 API

| # | 平台 | 接口类型 | 认证 | 费用 | 开源 | 配额 |
|---|------|---------|------|------|------|------|
| 21 | X / Twitter API v2 | REST API | OAuth2 / Bearer | **Basic $100/月** | 闭源 | Basic: 10K帖/月, Pro: 1M帖/月 |
| 22 | TikTok API | REST API | OAuth2 | 免费(Research) | 闭源 | 需申请, 审核严格 |
| 23 | Instagram Graph API | REST API | OAuth2 + FB审核 | 免费 | 闭源 | 需 FB App 审核 |
| 24 | Facebook Graph API | REST API | OAuth2 | 免费→付费 | 闭源 | 按 App 类型分配 |
| 25 | LinkedIn API | REST API | OAuth2 | 免费(极有限) | 闭源 | 非常受限 |
| 26 | Pinterest API | REST API | OAuth2 | 免费 | 闭源 | 1K req/hr |
| 27 | Snapchat API | REST API | OAuth2 | 免费(受限) | 闭源 | 非常受限 |
| 28 | Discord API | REST API + WebSocket | Bot Token | 免费 | 开源 | 50 req/sec |
| 29 | Threads API | — | — | 未开放 | — | 无公开 API |
| 30 | Bluesky | REST API + WebSocket | App Password | 免费 | 开源 | 不限(AT Protocol) |
| 31 | Mastodon | REST API | OAuth2 | 免费 | 开源 | 取决于实例 |
| 32 | Twitch API | REST API | OAuth2 | 免费 | 闭源 | 800 req/min |

---

## 四、俄罗斯/独联体平台

| # | 平台 | 接口类型 | 认证 | 费用 | 开源 |
|---|------|---------|------|------|------|
| 33 | VK API | REST API | Access Token | 免费 | 闭源 |
| 34 | Odnoklassniki API | REST API | OAuth2 | 免费 | 闭源 |
| 35 | Yandex Market API | REST API | OAuth2 | 免费 | 闭源 |
| 36 | Wildberries API | REST API | API Key | 免费 | 闭源 |
| 37 | Ozon API | REST API | API Key + OAuth | 免费 | 闭源 |
| 38 | Yandex Search API | REST API | API Key | 付费(~$10/1K req) | 闭源 |
| 39 | Yandex Translate | REST API | API Key | 免费→付费 | 闭源 |

---

## 五、韩国平台

| # | 平台 | 接口类型 | 认证 | 费用 | 开源 |
|---|------|---------|------|------|------|
| 40 | Naver API (搜索/购物/地图) | REST API | API Key | 免费(额度) | 闭源 |
| 41 | Kakao API (通讯/支付/地图) | REST API | API Key | 免费 | 闭源 |
| 42 | Coupang API | REST API | Partner Key | 需入驻 | 闭源 |
| 43 | data.go.kr (政府开放数据) | REST API | API Key | 免费 | 开源数据 |

---

## 六、东南亚平台

| # | 平台 | 接口类型 | 认证 | 费用 | 开源 |
|---|------|---------|------|------|------|
| 44 | Shopee Open API | REST API | Partner Key | 免费(需入驻) | 闭源 |
| 45 | Lazada Open API | REST API | App Key | 免费(需入驻) | 闭源 |
| 46 | LINE API | REST API + Messaging | Channel Token | 免费 | 闭源 |
| 47 | Grab API | REST API | Partner | 需合作 | 闭源 |
| 48 | data.gov.sg | REST API | API Key | 免费 | 开源 |
| 49 | data.gov.my | REST API | 无 | 免费 | 开源 |
| 50 | data.go.th | REST API | 无 | 免费 | 开源 |

---

## 七、中东平台

| # | 平台 | 接口类型 | 认证 | 费用 | 开源 |
|---|------|---------|------|------|------|
| 51 | Amazon SP-API (覆盖 .sa / .ae) | REST API | IAM + OAuth | 免费(需入驻) | 闭源 |
| 52 | Noon API | — | — | 无公开 API | 闭源 |
| 53 | Salla API | REST API | API Key | 免费→付费 | 闭源 |
| 54 | Zid API | REST API | API Key | 免费 | 闭源 |
| 55 | Tabby API (BNPL) | REST API | API Key | 需合作 | 闭源 |
| 56 | Tamara API (BNPL) | REST API | API Key | 需合作 | 闭源 |
| 57 | UAE Open Data | REST API | 无 | 免费 | 开源 |
| 58 | Saudi Open Data | REST API | 无 | 免费 | 开源 |

---

## 八、拉美/北美补充

| # | 平台 | 接口类型 | 认证 | 费用 | 开源 |
|---|------|---------|------|------|------|
| 59 | Mercado Libre API | REST API | OAuth2 | 免费 | 闭源 |
| 60 | Amazon SP-API (US/CA/MX) | REST API | IAM + OAuth | 免费(需入驻) | 闭源 |
| 61 | Walmart API | REST API | API Key | 免费(需申请) | 闭源 |
| 62 | eBay API | REST API | OAuth2 | 免费 | 闭源 |
| 63 | Shopify Admin API | GraphQL + REST | OAuth2 | 免费(自店) | 闭源 |
| 64 | AliExpress API | REST API | App Key | 需入驻 | 闭源 |
| 65 | Statistics Canada | REST API | 无 | 免费 | 开源 |
| 66 | INEGI (墨西哥统计) | REST API | 无 | 免费 | 开源 |

---

## 九、欧洲/北欧补充

| # | 平台 | 接口类型 | 认证 | 费用 | 开源 |
|---|------|---------|------|------|------|
| 67 | Bolagsverket (瑞典公司) | REST API | 无 | 免费 | 开源 |
| 68 | Brreg (挪威公司) | REST API | 无 | 免费 | 开源 |
| 69 | SCB (瑞典统计) | REST API | 无 | 免费 | 开源 |
| 70 | SSB (挪威统计) | REST API | 无 | 免费 | 开源 |
| 71 | Companies House UK | REST API | API Key | 免费 | 开源 |
| 72 | UK Gov APIs | REST API | 部分需 Key | 多数免费 | 开源 |
| 73 | EU Open Data Portal | REST API + SPARQL | 无 | 免费 | 开源 |
| 74 | Allegro API (波兰) | REST API | OAuth2 | 免费(需入驻) | 闭源 |
| 75 | Klarna API | REST API | API Key | 需合作 | 闭源 |
| 76 | Swish API | REST API | Certificate | 需合作 | 闭源 |
| 77 | Vipps API | REST API | API Key | 需合作 | 闭源 |
| 78 | Tink API | REST API | OAuth2 | 需合作 | 闭源 |

---

## 十、政府/监管/合规

| # | 平台 | 接口类型 | 认证 | 费用 | 开源 |
|---|------|---------|------|------|------|
| 79 | openFDA (美国药监) | REST API | API Key(可选) | 免费 | 开源 |
| 80 | FCC API | REST API | 无 | 免费 | 开源 |
| 81 | CPSC (消费品安全) | RSS | 无 | 免费 | 开源 |
| 82 | USPTO (专利商标) | REST API | 无 | 免费 | 开源 |
| 83 | EUIPO (欧盟商标) | REST API | 无 | 免费 | 开源 |
| 84 | WIPO (世界知产) | REST API | 无 | 免费 | 开源 |
| 85 | CBP (美国海关) | — | — | 无公开 API | — |
| 86 | UKIPO (英国知产) | REST API | 无 | 免费 | 开源 |

---

## 十一、金融/宏观经济

| # | 平台 | 接口类型 | 认证 | 费用 | 开源 | 配额 |
|---|------|---------|------|------|------|------|
| 87 | CBR (俄央行) | REST API | 无 | 免费 | 闭源 | 不限 |
| 88 | FRED (美联储) | REST API | API Key | 免费 | 闭源 | 120/min |
| 89 | Frankfurter (汇率) | REST API | 无 | 免费 | 开源 | 不限 |
| 90 | World Bank API | REST API | 无 | 免费 | 开源 | 不限 |
| 91 | IMF Data API | REST API | 无 | 免费 | 开源 | 不限 |
| 92 | Trading Economics | REST API | API Key | **$300+/月** | 闭源 | 按套餐 |
| 93 | BEA (美国经济) | REST API | API Key | 免费 | 开源 | 不限 |
| 94 | BLS (劳工统计) | REST API | API Key | 免费 | 开源 | 不限 |
| 95 | BNM (马来央行) | REST API | 无 | 免费 | 开源 | 不限 |
| 96 | BOT (泰国央行) | REST API | 无 | 免费 | 开源 | 不限 |
| 97 | SAMA (沙特央行) | — | — | 无公开 API | — | — |

---

## 十二、支付基础设施

| # | 平台 | 接口类型 | 认证 | 费用 | 开源 |
|---|------|---------|------|------|------|
| 98 | PayPal API | REST API | OAuth2 | 交易费 | 闭源 |
| 99 | Stripe API | REST API | Secret Key | 交易费 | 开源 SDK |
| 100 | Wise API | REST API | API Key | 转账费 | 闭源 |
| 101 | Airwallex API | REST API | API Key | 按量 | 闭源 |
| 102 | PingPong API | REST API | API Key | 按量 | 闭源 |
| 103 | Payoneer API | REST API | API Key | 按量 | 闭源 |

---

## 十三、第三方聚合 API（RedFox 对标）

| # | 平台 | 接口类型 | 认证 | 费用 | 开源 | 覆盖 |
|---|------|---------|------|------|------|------|
| 104 | **KeyAPI.ai** | REST API | API Key | ❓需询价 | 闭源 | 20+ 社媒 |
| 105 | **Apify** | REST API + CLI + MCP | API Key | **免费→$29/月** | 部分开源 | 2,500+ Actor |
| 106 | **Oxylabs E-Commerce** | REST API | API Key | **$49/月起** | 闭源 | 全电商 |
| 107 | **Bright Data** | REST API + CLI | API Key | 按量计费 | 闭源 | 全 Web |
| 108 | **ScrapingBee** | REST API | API Key | $49/月 | 闭源 | 通用 |
| 109 | **ScrapingDog** | REST API | API Key | $20/月 | 闭源 | 通用 |
| 110 | **ZenRows** | REST API | API Key | $69/月 | 闭源 | 通用 |
| 111 | **ScraperAPI** | REST API | API Key | $49/月 | 闭源 | 通用 |
| 112 | **Diffbot** | REST API | API Key | $299/月 | 闭源 | 全 Web 结构 |
| 113 | **Datashake** | REST API | API Key | 企业定制 | 闭源 | 150+ 来源 |
| 114 | **DataForSEO** | REST API | API Key | $50/月 | 闭源 | SEO/关键词 |
| 115 | **SimilarWeb** | REST API | API Key | ~$1,000+/月 | 闭源 | 流量/竞品 |
| 116 | **EchoTik** | REST API | API Key | ❓ | 闭源 | TikTok 专精 |

---

## 十四、RSS / 无认证公开源（免费捡）

| # | 平台 | 接口类型 | 费用 | 说明 |
|---|------|---------|------|------|
| 117 | Google News RSS | RSS | 免费 | 多语言/地区 |
| 118 | BBC News RSS | RSS | 免费 | 英国 |
| 119 | SVT (瑞典广播) RSS | RSS | 免费 | 瑞典语 |
| 120 | NRK (挪威广播) RSS | RSS | 免费 | 挪威语 |
| 121 | Yle (芬兰广播) RSS | RSS | 免费 | 芬兰语 |
| 122 | CBC (加拿大) RSS | RSS | 免费 | |
| 123 | Yonhap (韩国) RSS | RSS | 免费 | 韩语 |
| 124 | RT / TASS (俄) RSS | RSS | 免费 | 俄语 |
| 125 | Arab News RSS | RSS | 免费 | 沙特 |
| 126 | Gulf News RSS | RSS | 免费 | 阿联酋 |
| 127 | Straits Times RSS | RSS | 免费 | 新加坡 |

---

## 汇总

| 维度 | 数量 |
|------|------|
| 已接入可用 | 14 |
| 需完善 | 6 |
| 海外社媒 API | 12 |
| 俄罗斯/独联体 | 7 |
| 韩国 | 4 |
| 东南亚 | 7 |
| 中东 | 8 |
| 拉美/北美 | 8 |
| 欧洲/北欧 | 12 |
| 政府/合规 | 8 |
| 金融/经济 | 11 |
| 支付 | 6 |
| 第三方聚合 | 13 |
| RSS 公开源 | 11 |
| **总计** | **127** |

> 注：127 是已调查接口明细的源。全部 335 个平台中有大量政府开放数据/信息公开页面没有传统 API（网页为主、PDF 为主、或只有 SPARQL 端点）。实际"有可用编程接口"的约 120-130 个。
