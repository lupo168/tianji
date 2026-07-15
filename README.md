---
title: 天玑 · 全球商业情报系统
version: v1.2
date: 2026-07-15
author: Hermes Agent + JUN + Claude
license: MIT
description: 天玑是一个开源的全球商业信息采集底座框架。包含框架文档 + 可执行采集管道 + 每日自动日报 + 代码层强制的安全机制（网络白名单、密钥隔离、日报事实过滤、内容层防注入）。
tags: [天玑, 商业情报, 开源, 信息采集, 安全机制]
---

# 🌍 天玑 · 全球商业情报系统

> **天玑 = 眼睛** — 弥补信息差。每天自动采集全球数据，让你知道别人不知道的事。
>
> **开阳 = 大脑** — 弥补认知差。分析数据、判断趋势、给出商业建议。
>
> **玉衡 = 人类** — 做最终决策。机器不能替你判断，但能让你判断得更准。
>
> 架构：天玑(采集) → 开阳(分析) → 玉衡(决策)


## 🚀 一行命令启动

小白买新电脑（Mac / Linux），打开终端，粘贴这一行回车：

```bash
curl -fsSL https://raw.githubusercontent.com/lupo168/tianji/main/quickstart.sh | bash
```

**自动完成：**
- ✅ 检查Python环境
- ✅ 下载天玑代码
- ✅ 创建数据目录
- ✅ 首次采集运行（汇率 / RSS新闻 / Hacker News / 政府数据等）
- ✅ 生成第一份日报
- ✅ 可选：设置每天08:00自动运行

之后每天早上，日报自动出现在 `~/tianji-data/reports/daily-*.md`

```bash
# 随时手动运行
cd ~/tianji/scripts
python3 tianji_runner.py

# 查看日报
cat ~/tianji-data/reports/daily-$(date +%Y-%m-%d).md
```

---

## 🗺️ 功能地图

> 天玑覆盖 **7大商业情报维度**，每个维度包含多个具体数据源。
> 颜色标识：🟢 免费·无需注册  🔵 免费·需注册API  🟡 付费（用户自选）  🧠 需人脑判断（留给开阳）

---

### 📈 ① 汇率与宏观经济

| 数据内容 | 数据源 | 成本 | 获取方式 | 状态 |
|---------|-------|------|---------|------|
| USD/CNY等多币种汇率 | CBR俄罗斯央行 | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 欧元/英镑/日元/韩元等 | ExchangeRate-API | 🔵 免费(1000次/月) | 需注册key | ⏳ 待配置 |
| 美联储利率/经济指标 | FRED | 🔵 免费 | 需注册key | ⏳ 待配置 |
| IMF全球经济数据 | IMF API | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| World Bank发展数据 | World Bank API | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 英国/挪威/瑞典央行 | BoE/Norges/Riksbank | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |

### 📰 ② 新闻与行业动态

| 数据内容 | 数据源 | 成本 | 获取方式 | 状态 |
|---------|-------|------|---------|------|
| 全球商业新闻 | Google News RSS | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 国际要闻/科技 | BBC News RSS | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 财经新闻 | Google/BBC Business | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 亚洲动态 | Nikkei Asia | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 美国监管动态 | FTC News RSS | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |

### 🔥 ③ 科技趋势与创新

| 数据内容 | 数据源 | 成本 | 获取方式 | 状态 |
|---------|-------|------|---------|------|
| 科技创业热门 | Hacker News | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 全球热门话题 | Wikipedia | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 专利动态 | Google Patents | 🟢 免费 | API已验证 | ⏳ 待实现 |
| AI搜索增强 | Tavily | 🔵 免费1000/月 | 需注册key | ⏳ 待接入 |
| 社交数据(220+端点) | UnifAPI | 🟡 $0.001/条 | 需注册key | ⏳ 待接入 |
| OSINT情报(27源) | Crucix | 🟢 免费(自建) | 需自托管 | ⏳ 待评估 |

### 🏛️ ④ 政府监管与合规

| 数据内容 | 数据源 | 成本 | 获取方式 | 状态 |
|---------|-------|------|---------|------|
| FDA认证/召回 | OpenFDA | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 消费品安全(CPSC) | CPSC RSS | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 电子产品认证(FCC) | FCC API | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 商标查询(USPTO/UKIPO) | USPTO/UKIPO | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 英国公司注册 | Companies House | 🔵 免费(需注册) | 已实现采集器 | ✅ 每日自动 |
| 英国政府政策 | GOV.UK | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 欧盟法规 | EU Open Data | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 沙特标准(SASO) | SASO | 🔵 免费(需注册) | 已验证API | ⏳ 待实现 |
| 阿联酋标准(MOIAT) | MOIAT | 🟢 免费 | Open Data API | ⏳ 待实现 |
| 中国CCC/CQC认证 | CNCA云桥 | 🔵 免费(需注册) | REST API | ⏳ 待实现 |
| OFAC制裁名单 | Treasury | 🟢 免费 | REST API | ⏳ 待实现 |
| NSF/UL/SIRIM等 | — | ⚪ 无公开API | 网页监控 | ⏳ 待实现 |

### 🛒 ⑤ 电商与市场情报

| 数据内容 | 数据源 | 成本 | 获取方式 | 状态 |
|---------|-------|------|---------|------|
| Amazon排名/评论 | Amazon SP-API | 🟡 付费(按调用) | 需注册开发者 | ⏳ 待实现 |
| eBay定价 | eBay API | 🔵 免费(有额度) | 需注册 | ⏳ 待实现 |
| Shopify店铺数据 | Shopify API | 🔵 免费(有店) | 需创建App | ⏳ 待实现 |
| 东南亚(Shopee/Lazada) | Shopee/Lazada | 🔵 免费(需申请) | 需注册卖家 | ⏳ 待实现 |
| 俄罗斯(Ozon/WB) | Ozon/Wildberries | 🔵 免费(卖家) | 需注册卖家 | ⏳ 待实现 |
| 拉美(Mercado Libre) | Mercado Libre | 🔵 免费 | 需注册App | ⏳ 待实现 |
| 中东(Noon/Salla) | Noon/Salla/Zid | 🔵 免费(需注册) | 需注册商户 | ⏳ 待实现 |
| 韩国(Coupang) | Coupang Wing | 🟡 付费(需商务) | 需韩国法人 | ⏳ 待实现 |
| 竞品SKU/定价 | 定时爬虫 | 🟢 免费 | 需自建爬虫 | ⏳ 待实现 |

### 📢 ⑥ 营销广告与KOL ← 新增维度

| 数据内容 | 数据源 | 成本 | 获取方式 | 状态 |
|---------|-------|------|---------|------|
| 竞品FB广告素材 | FB Ad Library | 🟢 免费(公开) | v2采集器 | ✅ 每日自动 |
| 竞品Google广告 | Google Ads透明度 | 🟢 免费(公开) | v2采集器 | ✅ 每日自动 |
| KOL/红人追踪 | AnySearch+社媒 | 🟢 免费 | v2采集器 | ✅ 每日自动 |
| 广告政策变更 | FB/Google/TikTok | 🟢 免费 | v2采集器 | ✅ 每日自动 |
| 竞品社媒数据 | 各平台公开数据 | 🟢 免费 | v2采集器 | ✅ 每日自动 |
| TikTok广告情报 | TikTok Ad Library | 🟢 免费(公开) | ⏳ 待实现 |
| 红人数据库 | Modash/Upfluence | 🟡 $99+/月 | 用户自选 | ⏳ 待实现 |

### 🤖 ⑦ SEO与GEO搜索 ← 新增维度

| 数据内容 | 数据源 | 成本 | 获取方式 | 状态 |
|---------|-------|------|---------|------|
| GEO可见性评分 | AnySearch搜索分析 | 🟢 免费 | v2采集器 | ✅ 每日自动 |
| 关键词趋势 | Google Trends | 🟢 免费(公开) | v2采集器 | ✅ 每日自动 |
| 长尾关键词机会 | AnySearch搜索 | 🟢 免费 | v2采集器 | ✅ 每日自动 |
| 关键词排名追踪 | Ahrefs/SEMrush | 🟡 $99+/月 | 用户自选 | ⏳ 待定 |
| 竞品SEO流量 | SimilarWeb | 🟡 $199+/月 | 用户自选 | ⏳ 待定 |
| AI搜索引用监控 | Perplexity/ChatGPT | 🧠 需人脑 | 留给开阳 | ⏳ 待定 |

### 🏪 ⑧ 渠道与平台政策

| 数据内容 | 数据源 | 成本 | 获取方式 | 状态 |
|---------|-------|------|---------|------|
| Amazon卖家政策 | Amazon Seller Central | 🟢 免费(公开) | 已实现采集器 | ✅ 每日自动 |
| Shopify更新 | Shopify Changelog | 🟢 免费(公开) | 已实现采集器 | ✅ 每日自动 |
| eBay/Walmart政策 | 各平台公告 | 🟢 免费(公开) | 已实现采集器 | ✅ 每日自动 |
| 平台费用变化 | 各平台费用页 | 🟢 免费 | 定时监控 | ⏳ 待实现 |

### 📦 ⑨ 物流与供应链

| 数据内容 | 数据源 | 成本 | 获取方式 | 状态 |
|---------|-------|------|---------|------|
| 国际快递运费 | UPS/FedEx/DHL | 🟡 付费(有免费额) | 需注册开发者 | ⏳ 待实现 |
| 集装箱运价 | Freightos | 🟡 付费 | API订阅 | ⏳ 待实现 |
| 代发货(CJ) | CJ Dropshipping | 🔵 免费(有账户) | 需注册 | ⏳ 待实现 |
| 原材料价格 | LME/期货 | 🟡 付费(部分免费) | API订阅 | ⏳ 待实现 |

### 🏷️ ⑩ 品牌声誉与舆情 ← 新增维度

| 数据内容 | 数据源 | 成本 | 获取方式 | 状态 |
|---------|-------|------|---------|------|
| 品牌新闻动态 | AnySearch新闻搜索 | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 融资/收购情报 | 新闻搜索 | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 合作伙伴动态 | 新闻搜索 | 🟢 免费 | 已实现采集器 | ✅ 每日自动 |
| 消费者评价 | Trustpilot/BBB | 🔵 免费(有额度) | 需注册 | ⏳ 待实现 |
| 社媒舆论监控 | Brandwatch等 | 🟡 付费 | 用户自选 | ⏳ 待定 |
| 危机预警 | 综合信号分析 | 🧠 需人脑 | 留给开阳 | ⏳ 待定 |

### 💰 ⑪ 支付与金融

| 数据内容 | 数据源 | 成本 | 获取方式 | 状态 |
|---------|-------|------|---------|------|
| PayPal费率变化 | PayPal Developer | 🟢 免费(公开) | 页面监控 | ⏳ 待实现 |
| Stripe政策更新 | Stripe Changelog | 🟢 免费(公开) | 页面监控 | ⏳ 待实现 |
| 跨境收款费率 | PingPong/连连 | 🟡 需商务对接 | 用户自选 | ⏳ 待定 |
| BNPL趋势 | Klarna/Tabby | 🔵 免费(API) | 需注册 | ⏳ 待实现 |

### 🧠 ⑫ 商业决策（开阳层）← 未来规划

| 需要什么 | 谁来处理 | 何时实现 |
|---------|---------|---------|
| 竞品战略判断 | 开阳(人+AI) | Phase 4 |
| 市场机会评估 | 开阳(人+AI) | Phase 4 |
| 风险预警决策 | 开阳(人+AI) | Phase 4 |
| 定价策略建议 | 开阳(人+AI) | Phase 4 |
| 营销策略优化 | 开阳(人+AI) | Phase 4 |

---

### 📊 功能汇总

| 维度 | 🟢免费 | 🔵免费(需注册) | 🟡付费(自选) | ⚪无API | 🧠需人脑 |
|------|-------|---------------|-------------|---------|---------|
| ① 汇率经济 | 6 | 2 | 0 | 0 | 0 |
| ② 新闻动态 | 5 | 0 | 0 | 0 | 0 |
| ③ 科技趋势 | 3 | 1 | 1 | 0 | 0 |
| ④ 政府监管 | 10 | 3 | 0 | 3 | 0 |
| ⑤ 电商情报 | 1 | 5 | 2 | 0 | 0 |
| ⑥ 营销广告 | 5 | 0 | 1 | 0 | 0 |
| ⑦ SEO/GEO | 3 | 0 | 2 | 0 | 1 |
| ⑧ 渠道政策 | 4 | 0 | 0 | 0 | 0 |
| ⑨ 物流供应 | 0 | 1 | 3 | 0 | 0 |
| ⑩ 品牌声誉 | 3 | 1 | 1 | 0 | 1 |
| ⑪ 支付金融 | 2 | 1 | 1 | 0 | 0 |
| ⑫ 开阳决策 | 0 | 0 | 0 | 0 | 全部 |
| **合计** | **42** | **14** | **11** | **3** | **2** |

> **零成本起步：** 42个数据源完全免费，一行命令直接开跑。
> **扩展方向：** 注册14个免费API key可扩展至56个数据源。
> **付费可选：** 11个付费工具标明了价格，用户自愿采购。
> **开阳层：** 需要人脑判断的留给未来AI分析层。这套系统才完整。`
| ① 汇率与经济 | **7** | **2** | 0 | 0 |
| ② 新闻动态 | **6** | 0 | 0 | 0 |
| ③ 科技趋势 | **4** | **2** | 0 | 0 |
| ④ 政府监管 | **11** | **3** | 0 | **3** |
| ⑤ 电商情报 | 0 | **6** | **3** | **1** |
| ⑥ 物流供应 | **1** | **2** | **4** | 0 |
| ⑦ 社媒洞察 | **1** | **3** | **2** | **1** |
| **合计** | **30** | **18** | **9** | **5** |

> **零成本起步：** 30个数据源完全免费，无需注册任何账号，一行命令直接开跑。
> **扩展方向：** 注册18个免费API key可扩展至48个数据源。
> **完整覆盖：** 接入62个数据源即可覆盖核心商业情报需求。

---

---

## 📊 当前采集器（零成本·无需注册）

| 采集器 | 数据源 | 频率 |
|--------|-------|------|
| 汇率采集 | CBR俄罗斯央行 | 每日 |
| RSS新闻 | Google News / BBC / FTC | 每日 |
| 科技趋势 | Hacker News | 每日 |
| 政府开放数据 | FDA / World Bank / UKIPO / BoE 等 | 每日 |

---

## 🔧 工具生态 / 插件

天玑不是封闭系统，它整合了一系列独立工具作为采集和分析的"插件"。每个工具解决一类问题：

### 搜索与采集

| 工具 | 用途 | 官网 | 费用 | 状态 |
|------|------|------|------|------|
| **AnySearch** | 统一实时搜索（支持垂直领域搜索） | [anysearch.com](https://anysearch.com) | 匿名免费 | ✅ 已集成 |
| **last30days** | 海外社媒研究（Reddit/X/TikTok/YouTube/IG） | [Hermes社区](https://github.com/stansz/hermes-community-pulse) | 自带API key | ✅ 可用 |
| **last30days-cn** | 国内社媒研究（小红书/知乎/B站/微博/抖音） | [Hermes社区](https://github.com/stansz/hermes-community-pulse) | 自带RedFox key | ✅ 可用 |
| **RedFox** | 国内社媒API桥接（小红书/抖音/微博/知乎等） | [redfox.hk](https://redfox.hk) | 付费 | ✅ 可用 |
| **DDGS** | DuckDuckGo搜索（回退搜索引擎） | [duckduckgo.com](https://duckduckgo.com) | 免费 | ✅ 可用 |
| **ScrapeCreators** | 爬虫服务（页面抓取） | [scrapecreators.com](https://scrapecreators.com) | 付费 | ✅ 可用 |
| **Tavily** | AI Agent搜索引擎（结构化输出） | [tavily.com](https://tavily.com) | 1000credits/月免费 | ⏳ 待接入 |
| **UnifAPI** | 社交平台公开数据聚合（220+端点×16平台） | [unifapi.com](https://unifapi.com) | $0.001/条, 500试用 | ⏳ 待接入 |
| **Crucix** | 开源OSINT情报引擎（27个数据源） | [crucix.live](https://crucix.live) | 免费(需自建) | ⏳ 待评估 |

### 数据处理与验证

| 工具 | 用途 | 官网 | 费用 | 状态 |
|------|------|------|------|------|
| **DashScope (qwen-vl-max)** | 阿里云视觉识别（看图分析） | [aliyun.com/product/bailian](https://www.aliyun.com/product/bailian) | 按量付费 | ✅ 可用 |
| **Context7** | 文档/API新鲜度验证 | [context7.com](https://context7.com) | 免费 | ✅ 可用 |
| **source-verifier** | 信源可靠性研判（NATO情报级） | [Hermes社区](https://github.com/stansz/hermes-community-pulse) | 内置 | ✅ 可用 |
| **PostgreSQL** | 结构化数据存储与查询 | [postgresql.org](https://postgresql.org) | 免费 | ⏳ 待部署 |

### 分析框架

| 工具 | 用途 |
|------|------|
| **ecommerce-data-analyst** | VPE/ROI/GMV/盈亏/RFM计算 |
| **ecommerce-store-analyzer** | 6维15项竞争分析 |
| **industry-analysis** | 行业生命周期/市场规模 |
| **market-analysis** | PEST/五力/SWOT/竞争格局 |
| **competitor-analysis** | 竞品方法论 |
| **pricing-science** | 定价策略/价值感知 |
| **pmp-mastery** | 项目管理 |

---

## 🔑 需注册免费API key

| 采集器 | 免费额度 | 说明 |
|--------|---------|------|
| ExchangeRate-API | 1000次/月 | 多币种汇率 |
| FRED | 免费 | 美联储经济数据 |
| YouTube Data | 10,000额度/日 | 视频/趋势数据 |
| Reddit | 60req/min | 消费者讨论 |
| Tavily | 1000credits/月 | AI搜索 |
| Telegram Bot | 免费(无限制) | 行业群监控 |

---

## 🔒 安全机制

天玑的价值在于给开阳和玉衡提供一份"无条件可信"的事实层——这个信任一旦被越权执行、密钥泄露或内容层面的间接注入污染过一次，后面所有分析和决策都建立在不可信的地基上。所以下面这套机制不是可选项，是天玑架构的一部分：

| 层 | 解决什么问题 | 对应文件 |
|---|---|---|
| 身份定义 | 天玑该怎么想、遇到不确定情况怎么办 | `SOUL.md` |
| 红线规范 | 天玑能做什么/不能做什么，每条配代码层强制点 | `RULES.md` |
| 网络白名单 | 禁止访问未审核域名、禁止一切写操作 | `scripts/security/safe_requests.py` + `domain_whitelist.yaml` |
| 待审核域名队列 | 遇到白名单外的域名，记录而非擅自访问；开阳可评估，只有人能批准 | `scripts/security/pending_domains.yaml` + `review_pending_domains.py` |
| 密钥管理 | 密钥不进入 Hermes 的对话上下文，验证不经过模型 | `scripts/security/verify_key.sh` |
| 提交前拦截 | 防止密钥被 commit、防止采集器绕过白名单层 | `.pre-commit-config.yaml` + `check_no_key_print.py` + `check_no_raw_requests.py` |
| 日报事实过滤 | 拦截"建议""预测"等结论性语言，保证天玑产出止步于事实 | `scripts/security/report_filter.py` |
| 内容层防注入 | 聚合搜索（AnySearch等）返回的网页内容可能藏着写给AI看的指令，需剥离并显式标记为"数据非指令" | `scripts/security/content_sanitizer.py` + `review_suspicious_content.py` |

安装和集成步骤见 `SETUP_SECURITY.md`。

---

## 📚 文档索引

| 文档 | 说明 |
|------|------|
| `PRD.md` | 产品需求文档 |
| `SOP.md` | 全流程标准作业程序 |
| `TOOLCHAIN.md` | 工具链选型指南 |
| `BUSINESS_AUDIT_FRAMEWORK.md` | 商业审计框架 |
| `SOUL.md` | 天玑身份定义（system prompt，每次任务注入上下文最前面） |
| `RULES.md` | 红线规范，能做什么/不能做什么，每条配代码层强制点 |
| `SETUP_SECURITY.md` | 安全机制安装与集成说明 |
| `DEV_SECURITY_STANDARD.md` | 开发安全规范，任何人/agent向仓库提交代码前必须遵守 |
| `.env.example` | 环境变量配置示例 |
| `reports/API_VERIFICATION_METHODOLOGY.md` | API验证方法学 |

## 📂 目录结构

```
tianji/
├── README.md                    ← 你现在看的
├── PRD.md                       ← 系统设计文档
├── SOP.md                       ← 操作流程
├── TOOLCHAIN.md                 ← 工具链
├── BUSINESS_AUDIT_FRAMEWORK.md  ← 审计框架
├── SOUL.md                      ← 天玑身份定义（system prompt）
├── RULES.md                     ← 红线规范（代码层强制点对照）
├── SETUP_SECURITY.md            ← 安全机制安装说明
├── DEV_SECURITY_STANDARD.md     ← 开发安全规范（贡献代码前必读）
├── .env.example                 ← 环境变量配置示例
├── .pre-commit-config.yaml      ← 提交前自动检查配置
├── .gitignore
├── scripts/
│   ├── tianji_runner.py         ← 一键运行所有采集器
│   ├── tianji_setup.py          ← 初始化向导
│   ├── tianji_daily_report.py   ← 日报生成器
│   ├── collectors/
│   │   ├── fx_collector.py           ← 汇率采集
│   │   ├── rss_news_collector.py     ← RSS新闻
│   │   ├── hn_trends_collector.py    ← Hacker News
│   │   ├── wiki_trends_collector.py  ← Wikipedia
│   │   ├── gov_open_data_collector.py ← 政府开放数据
│   │   ├── commodity_collector.py    ← 大宗商品
│   │   ├── marketing_intel_collector.py ← 营销广告/KOL
│   │   ├── seo_geo_collector.py      ← SEO/GEO
│   │   ├── reputation_capital_collector.py ← 品牌声誉/舆情
│   │   ├── channel_policy_collector.py ← 渠道与平台政策
│   │   ├── reddit_collector.py       ← Reddit社媒
│   │   ├── telegram_collector.py     ← Telegram监控
│   │   └── youtube_collector.py      ← YouTube趋势
│   └── security/                ← 安全机制（新增）
│       ├── safe_requests.py            ← 网络白名单强制层，禁止写操作
│       ├── env_loader.py               ← 极简.env加载器，替代明文JSON配置
│       ├── safe_search.py              ← AnySearch调用的统一安全封装
│       ├── domain_whitelist.yaml       ← 白名单域名配置
│       ├── pending_domains.yaml        ← 待审核域名队列（运行时生成，不提交）
│       ├── verify_key.sh               ← 密钥验证，不经过模型上下文
│       ├── check_no_raw_requests.py    ← pre-commit：禁止绕过白名单层
│       ├── check_no_key_print.py       ← pre-commit：禁止打印密钥明文
│       ├── report_filter.py            ← 日报事实层过滤器
│       ├── content_sanitizer.py        ← 内容层防注入过滤器
│       ├── review_pending_domains.py   ← 待审核域名队列查看/审批工具
│       └── review_suspicious_content.py ← 可疑内容审计日志查看工具
└── reports/
    ├── API_VERIFICATION_METHODOLOGY.md
    ├── COVERAGE_AUDIT.md
    ├── DIMENSION_AUDIT.md
    ├── TOOL_RESEARCH.md
    ├── product-intelligence-demo.md
    └── verification/
```

## 📄 许可

MIT License — 自由使用、修改、分发。


---

## 📋 项目规划

查看完整发展规划 → [ROADMAP.md](ROADMAP.md) | 当前阶段：Phase 2（告警与通知）

当前进度：Phase 1（数据层）100% ✅ → Phase 2（告警层）20% 🔄 → Phase 3（可视化）0% → Phase 4（AI分析）0%

---

## 🎯 实战案例：天玑如何挖出两个品类的商业情报

> 场景：你想了解"宠物喷泉饮水机"和"家用净水器"两个市场，但不想手动搜几十个网页。
> 耗时：**30秒** | 成本：**$0** | 数据源：全部公开免费

### 背景

2026年7月14日，我们用天玑对两个品类做了一次快速商业情报调研，目标是了解：
- 市场上有哪些主要竞品，定价多少
- 消费者的痛点和投诉是什么
- 有什么准入门槛（认证/法规）
- 有没有值得注意的行业趋势

### 数据来源

这份情报来自于**两类采集**的配合——天玑的自动日报 + 按需定向搜索：

| 来源 | 采集方式 | 成本 | 采集了什么 |
|------|---------|------|-----------|
| **🇷🇺 CBR俄罗斯央行** 汇率API | ① 天玑自动日报 ✅ | API直连·$0 | USD/CNY实时汇率 |
| **🏛️ FDA** 公开召回数据 | ① 天玑自动日报 ✅ | API直连·$0 | 当日食品药品召回 |
| **⚖️ FTC** 新闻RSS | ① 天玑自动日报 ✅ | RSS·$0 | 消费者保护执法动态 |
| **🔥 Hacker News** 科技趋势 | ① 天玑自动日报 ✅ | Firebase API·$0 | 科技商业热门讨论 |
| **Amazon Best Sellers** | ② AnySearch实时搜索 | 搜索聚合·$0 | 宠物喷泉TOP20排名/定价/评分 |
| **CNET/Forbes/Wirecutter** 评测 | ② AnySearch + RSS | 搜索聚合·$0 | 2026最佳产品评测 |
| **消费者博客/论坛** 真实反馈 | ② AnySearch实时搜索 | 搜索聚合·$0 | 用户投诉、痛点、使用体验 |
| **NSF认证标准** | ② AnySearch实时搜索 | 搜索聚合·$0 | 净水器必须的认证类型和要求 |

> ① = 天玑**自动采集器**（定时任务，无需手动触发）
> ② = 天玑**按需搜索**（AnySearch聚合搜索引擎）

### 执行过程

```bash
# ───── 第一层：自动采集（已经每天在跑，不需要你手动） ─────

# 天玑每天08:00自动运行的采集器：
#   fx_collector.py          → 🇷🇺 CBR央行汇率（API直连，非搜索引擎）
#   rss_news_collector.py    → 📰 Google News / BBC / FTC（RSS源直连）
#   hn_trends_collector.py   → 🔥 Hacker News（Firebase API直连）
#   gov_open_data_collector.py → 🏛️ FDA/World Bank/UKIPO（政府API直连）

# 查看今早自动生成的日报：
cat ~/tianji-data/reports/daily-$(date +%Y-%m-%d).md

# ───── 第二层：按需定向搜索（针对特定品类的深度调研） ─────

# 3条命令，30秒，挖出两个品类的竞品情报：
python anysearch_cli.py search "pet water fountain best seller 2026 price review"
python anysearch_cli.py search "water filter purifier best seller 2026 NSF certification"
python anysearch_cli.py search "pet water fountain complaints problems cleaning difficulty"

# ───── 整合产出 ─────
# 自动日报的数据 + 定向搜索的发现 → 合并成一份情报报告
```

> **解释：** AnySearch是一个搜索聚合工具，但你看到的日报数据（汇率、FDH召回、FTC新闻、Hacker News）来自天玑独立的**9个采集器**，每个采集器直连不同的API/RSS源，不是通过AnySearch拿的。
>
> 天玑的采集体系 = 9个直连采集器（每日自动） + 1个搜索聚合（按需调用）

### 发现的核心情报

#### 宠物喷泉市场

| 发现 | 数据来源 | 商业价值 |
|------|---------|---------|
| Petkit Eversweet Solo SE 卖$25.99，4.3★，13,507条评论 | ① Amazon Best Sellers | 这是你必须对标的入门价位 |
| 消费者#1投诉："水泵内部发霉无法彻底清洗" | ② 消费者博客/评测 | **设计差异化机会**：可拆卸泵仓/全洗碗机安全 |
| #2投诉："清洗困难，有死角" | ② 消费者博客 | **产品改进方向**：极简结构/无死角设计 |
| #3投诉："噪音随时间变大" | ② 消费者博客 | 静音水泵是卖点 |
| 趋势：无线水泵/不锈钢/APP智能控制 | ③ CNET/Forbes评测 | 跟进行业演进方向 |
| Petkit Eversweet 3 Pro (不锈钢版) $62.99 | ① 电商数据 | 高端锚点，中端有空间 |

#### 净水器市场

| 发现 | 数据来源 | 商业价值 |
|------|---------|---------|
| 价格带分布：$37入门→$200中端RO→$500旗舰 | ① Amazon Best Sellers | 定位区间决策依据 |
| Waterdrop 10UA $37.99 月销领先 | ① 电商数据 | 入门级巨大市场 |
| NSF/ANSI 42/53/58/372是必须认证 | ④ NSF标准 | 准入门槛，不是可选 |
| 智能龙头（TDS显示）已成中端标配 | ③ Wirecutter评测 | 功能差异化方向 |

### 如果没有天玑

你需要手动：
1. 打开Google搜索 → 打开20个链接
2. 逐页阅读Amazon产品页 → 记录价格、评分
3. 搜产品投诉 → 打开10篇博客 → 手动归纳
4. 搜NSF认证要求 → 打开官方网站 → 阅读标准文档
5. 查汇率 → 打开汇率网站
6. 把所有数据手动整理成表格

**总耗时：2-3小时。有天玑：30秒。**

### 关键结论

> 天玑不能替代人的商业判断，但它能把调研时间从**几小时压缩到几十秒**。
> 采集是自动的，整理是结构化的，你要做的只剩**决策**。

完整的产出报告见：`reports/product-intelligence-demo.md`
