---
title: 天玑 · 全球商业情报系统
version: v1.5
date: 2026-07-24
author: Hermes Agent + JUN + Claude
license: MIT
description: 天玑是一个开源的全球商业信息采集底座框架。包含框架文档 + 可执行采集管道 + 每日自动日报 + 代码层强制的安全机制（网络白名单、密钥隔离、日报事实过滤、内容层防注入）+ 真实性自检机制（每次运行自动生成结构化执行结果manifest）。
tags: [天玑, 商业情报, 开源, 信息采集, 安全机制, 真实性自检]
---

# 🌍 天玑 · 全球商业情报系统

> **天玑 = 眼睛** — 弥补信息差。每天自动采集全球数据，让你知道别人不知道的事。
>
> **开阳 = 大脑** — 弥补认知差。分析数据、判断趋势、给出商业建议。
>
> **玉衡 = 人类** — 做最终决策。机器不能替你判断，但能让你判断得更准。
>
> 架构：天玑(采集) → 开阳(分析) → 玉衡(决策)
> 边界：**天玑只回答"发生了什么"，开阳回答"这意味着什么，我该怎么办"。** 详见 `PRD.md`。

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

> **真实性自检（新增）**：每次运行`tianji_runner.py`后，会在`~/tianji-data/manifests/run-{时间戳}.json`生成一份结构化的"本次真实执行结果清单"——哪些采集器真正成功、哪些失败、耗时多久，以及本次是否触发了新的白名单外域名请求。**判断"天玑到底有没有覆盖某个数据源"，以这份manifest为准，不要以README的状态标记为准**——文档和代码会自然不同步，manifest是唯一自动生成、不需要人工维护就能反映真实状态的记录。

---

## 🗺️ 维度全景图（外眼9域 + 内镜6域）

> 天玑内部分两个子系统：**外眼**采集外部公开信息（任何人理论上都能拿到，价值在于"比别人快、比别人系统"）；**内镜**接入自身经营的内部数据（私域/渠道后台/供应链履约等，完全独占，规划中，尚未启动）。下表为外眼9域的实测状态，2026-07-23核实。

| 域 | 覆盖状态 | 建议监控类型 | 对应采集器/说明 |
|---|---|---|---|
| ① 宏观经济与货币金融 | ✅ 覆盖较好 | 周期为主（部分触发式） | `fx_collector.py`（汇率）、`commodity_collector.py`（大宗商品）；IMF/World Bank/BoE/挪威/瑞典央行经`gov_open_data_collector.py`覆盖 |
| ② 政治与地缘博弈 | 🔴 研究完成，未实现 | 触发式为主 | GDELT/ACLED/ReliefWeb/OFAC/OpenSanctions等11个OSINT源已研究（见`reports/TOOL_RESEARCH.md`），尚无采集器 |
| ③ 政策法规与认证合规 | ✅ 覆盖较好 | 触发式+周期兜底 | `gov_open_data_collector.py`：FDA/FCC/CPSC/USPTO/EPA/GOV.UK/UKIPO/EU Open Data。SASO/MOIAT/CNCA/NSF等认证已验证API但未实现采集 |
| ④ 贸易、关税与海关 | ✅ 本版新增 | 触发式为主 | `customs_trade_collector.py`：UK Trade Tariff、OFAC/SDN制裁名单确认可用；WTO/EU TARIC仅做可达性检查；中国海关总署已知境外IP不可达，如实记录 |
| ⑤ 需求与市场情报 | ⚠️ 部分覆盖 | 周期为主 | `hn_trends_collector.py`、`wiki_trends_collector.py`、`reddit_collector.py`；电商平台（Amazon/Shopee/Lazada等）需注册开发者账号，未实现 |
| ⑥ 竞争格局 | ✅ 覆盖较好 | 周期+触发式兼有 | `pricing_monitor_collector.py`、`company_intel_collector.py`、`etsy_collector.py`、`producthunt_collector.py` |
| ⑦ 供应链与生产 | ⚠️ 部分覆盖 | 周期为主 | `commodity_collector.py`覆盖原材料价格；B2B询价（如1688类）、国际物流运价指数仍缺 |
| ⑧ 渠道、平台与传播生态 | ✅ 覆盖较好 | 周期为主 | `channel_policy_collector.py`、`seo_geo_collector.py`、`marketing_intel_collector.py`、`reputation_capital_collector.py`、`youtube_collector.py`、`telegram_collector.py`、`agentreach_collector.py` |
| ⑨ 支付与金融基础设施 | ✅ 本版新增 | 周期为主（政策变更触发式） | `payment_finance_policy_collector.py`：Stripe/PayPal/Airwallex/Wise/Payoneer公开政策与费率页监控（仅可达性+内容对比，不解析具体费率数字） |

**外眼综合：9域中6域已实现（①③④⑥⑧⑨），2域部分实现（⑤⑦），1域研究完成待实现（②）。**

> **关于"建议监控类型"**：这是每个域按时间特性应有的处理方式（详见`PRD.md`第4.1节）。其中标注"触发式"的域（如②地缘、④关税）一旦发生必须第一时间知道——但当前所有采集器统一按每日周期运行，尚无独立的触发式基础设施，存在窗口期错过风险，已列入路线图。

内镜6域（客户关系与行为 / 渠道运营真实数据 / 供应链内部履约记录 / 内部财务健康度 / 内部一手反馈 / 组织与执行记录）目前均为规划状态，依赖业务方梳理内部系统接口权限后启动，详见`PRD.md`第2.3节。

> 完整的域定义、优先级/监控频率标准、方法论详见 `PRD.md`。历史版本的12维度框架描述（`reports/DIMENSION_AUDIT.md`等）部分内容已过时，以本README和`PRD.md`为准。

---

## 📊 当前采集器（20个，均零成本·无需付费）

| 分组 | 采集器 | 频率 |
|---|---|---|
| 宏观经济 | `fx_collector.py`、`commodity_collector.py` | 每日 |
| 政策法规 | `gov_open_data_collector.py` | 每日 |
| 贸易关税 *(新增)* | `customs_trade_collector.py` | 每日 |
| 支付金融 *(新增)* | `payment_finance_policy_collector.py` | 每日 |
| 需求趋势 | `hn_trends_collector.py`、`wiki_trends_collector.py`、`reddit_collector.py` | 每日 |
| 竞争情报 | `pricing_monitor_collector.py`、`company_intel_collector.py`、`etsy_collector.py`、`producthunt_collector.py` | 每日 |
| 渠道传播 | `channel_policy_collector.py`、`seo_geo_collector.py`、`marketing_intel_collector.py`、`reputation_capital_collector.py`、`youtube_collector.py`、`telegram_collector.py`、`agentreach_collector.py` | 每日 |
| 新闻资讯 | `rss_news_collector.py` | 每日 |

> 状态标记以本表和`tianji_runner.py`实际调用列表为准，不要以某份历史审计文档的手写标记为准——文档和代码会自然地不同步，出现分歧时以直接跑一次`tianji_runner.py`的真实输出为准。

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
| 密钥管理 | 密钥不进入 Hermes 的对话上下文，验证不经过模型 | `scripts/security/verify_key.sh`、`env_loader.py` |
| 提交前拦截 | 防止密钥被 commit、防止采集器绕过白名单层 | `.pre-commit-config.yaml` + `check_no_key_print.py` + `check_no_raw_requests.py` |
| 日报事实过滤 | 拦截"建议""预测"等结论性语言，保证天玑产出止步于事实 | `scripts/security/report_filter.py` |
| 内容层防注入 | 聚合搜索（AnySearch等）返回的网页内容可能藏着写给AI看的指令，需剥离并显式标记为"数据非指令" | `scripts/security/content_sanitizer.py` + `review_suspicious_content.py` |

安装和集成步骤见 `SETUP_SECURITY.md`。

> **已知待办**：`scripts/safe_requests.py`与`scripts/security/safe_requests.py`当前存在同名文件，建议统一到一处，避免后续维护时改错文件。

---

## 📚 文档索引

| 文档 | 说明 |
|------|------|
| `PRD.md` | 天玑产品需求文档（v2.3，含边界定义/外眼内镜+接口管理+数据合规四层架构/维度全景图含建议监控类型/方法论落地/路线图） |
| `docs/开阳-PRD.md` | 开阳（AI分析层）产品需求文档 |
| `docs/QIXING_ARCHITECTURE.md` | 天枢三层架构总览 |
| `SOP.md` | 全流程标准作业程序 |
| `TOOLCHAIN.md` | 工具链选型指南 |
| `SOUL.md` | 天玑身份定义（system prompt，每次任务注入上下文最前面） |
| `RULES.md` | 红线规范，能做什么/不能做什么，每条配代码层强制点 |
| `SETUP_SECURITY.md` | 安全机制安装与集成说明 |
| `DEV_SECURITY_STANDARD.md` | 开发安全规范，任何人/agent向仓库提交代码前必须遵守 |
| `.env.example` | 环境变量配置示例 |
| `reports/API_VERIFICATION_METHODOLOGY.md` | API验证方法学 |
| `reports/verification/` | 11份平台API验证报告，约300+平台（部分尚未转化为采集器，见`PRD.md`路线图） |

> `BUSINESS_AUDIT_FRAMEWORK.md`、`STRATEGIC_AUDIT.md`、`reports/DIMENSION_AUDIT.md`、`reports/COVERAGE_AUDIT.md` 为历史审计文档，部分内容已与当前代码状态不一致（例如曾标记为"空白"的营销/SEO/品牌声誉域现已实现），建议阅读时以`PRD.md`的实测结论为准。

## 📂 目录结构

```
tianji/
├── README.md                    ← 你现在看的
├── PRD.md                       ← 系统设计文档（v2.0）
├── SOP.md                       ← 操作流程
├── TOOLCHAIN.md                 ← 工具链
├── BUSINESS_AUDIT_FRAMEWORK.md  ← 历史审计文档（部分已过时）
├── STRATEGIC_AUDIT.md           ← 历史审计文档（商业/认知/信息差三维框架）
├── SOUL.md                      ← 天玑身份定义（system prompt）
├── RULES.md                     ← 红线规范（代码层强制点对照）
├── SETUP_SECURITY.md            ← 安全机制安装说明
├── DEV_SECURITY_STANDARD.md     ← 开发安全规范（贡献代码前必读）
├── API_COST_MATRIX.md
├── ROADMAP.md
├── .env.example                 ← 环境变量配置示例
├── .pre-commit-config.yaml      ← 提交前自动检查配置
├── .gitignore
├── quickstart.sh
│
├── config/
│   └── DOMAIN_WHITELIST.json    ← 白名单展示层（实际强制以scripts/security/domain_whitelist.yaml为准）
│
├── docs/
│   ├── QIXING_ARCHITECTURE.md   ← 七星/三层架构总览
│   ├── 开阳-PRD.md              ← 开阳PRD
│   ├── FULL_INTERFACE_INVENTORY.md
│   ├── OVERSEAS_API_AGGREGATORS.md
│   └── PLATFORM_MAP_14_COUNTRIES.md
│
├── scripts/
│   ├── tianji_runner.py         ← 一键运行所有采集器（唯一执行入口）
│   ├── tianji_setup.py          ← 初始化向导
│   ├── tianji_daily_report.py   ← 日报生成器
│   ├── env_loader.py
│   ├── collectors/              ← 20个采集器
│   │   ├── fx_collector.py                   ← 汇率
│   │   ├── commodity_collector.py            ← 大宗商品
│   │   ├── gov_open_data_collector.py        ← 政府开放数据
│   │   ├── customs_trade_collector.py        ← 海关/关税/贸易 *(新增)*
│   │   ├── payment_finance_policy_collector.py ← 支付/跨境金融政策 *(新增)*
│   │   ├── hn_trends_collector.py            ← Hacker News
│   │   ├── wiki_trends_collector.py          ← Wikipedia趋势
│   │   ├── reddit_collector.py               ← Reddit社媒
│   │   ├── pricing_monitor_collector.py      ← 竞品定价监控
│   │   ├── company_intel_collector.py        ← 公司融资情报
│   │   ├── etsy_collector.py                 ← Etsy竞品
│   │   ├── producthunt_collector.py          ← ProductHunt新品
│   │   ├── channel_policy_collector.py       ← 渠道与平台政策
│   │   ├── seo_geo_collector.py              ← SEO/GEO搜索情报
│   │   ├── marketing_intel_collector.py      ← 营销广告/KOL
│   │   ├── reputation_capital_collector.py   ← 品牌声誉/舆情
│   │   ├── youtube_collector.py              ← YouTube趋势
│   │   ├── telegram_collector.py             ← Telegram行业监控
│   │   ├── agentreach_collector.py           ← Agent Reach多源
│   │   └── rss_news_collector.py             ← RSS新闻
│   └── security/                ← 安全机制
│       ├── safe_requests.py            ← 网络白名单强制层，禁止写操作
│       ├── env_loader.py               ← 极简.env加载器，替代明文JSON配置
│       ├── safe_search.py              ← AnySearch调用的统一安全封装
│       ├── domain_whitelist.yaml       ← 白名单域名配置（新增域名须人工手动加入）
│       ├── pending_domains.yaml        ← 待审核域名队列（运行时生成，不提交）
│       ├── verify_key.sh               ← 密钥验证，不经过模型上下文
│       ├── check_no_raw_requests.py    ← pre-commit：禁止绕过白名单层
│       ├── check_no_key_print.py       ← pre-commit：禁止打印密钥明文
│       ├── report_filter.py            ← 日报事实层过滤器
│       ├── content_sanitizer.py        ← 内容层防注入过滤器
│       ├── review_pending_domains.py   ← 待审核域名队列查看/审批工具
│       └── review_suspicious_content.py ← 可疑内容审计日志查看工具
│
└── reports/
    ├── API_VERIFICATION_METHODOLOGY.md
    ├── COVERAGE_AUDIT.md          ← 历史审计文档（部分已过时）
    ├── DIMENSION_AUDIT.md         ← 历史审计文档（部分已过时）
    ├── TOOL_RESEARCH.md           ← OSINT/地缘政治等工具研究
    ├── product-intelligence-demo.md
    └── verification/              ← 11份平台API验证报告，300+平台
```

> 注：`scripts/safe_requests.py`与`scripts/security/safe_requests.py`目前是两个位置的同名文件，采集器实际引用的是`scripts.security.safe_requests`，建议后续清理掉顶层那份重复文件。

## 📄 许可

MIT License — 自由使用、修改、分发。

---

## 📋 项目规划

查看完整发展规划 → [ROADMAP.md](ROADMAP.md) | 详细路线图见 `PRD.md` 第8节

当前进度：外眼采集层（Phase 1）核心已实现（9域中6域覆盖，2域部分覆盖，1域研究完成待实现）→ 开阳分析层（Phase 2）已有PRD（`docs/开阳-PRD.md`），Tier1单Agent验证阶段 → 内镜内部数据层：规划中，待业务方梳理内部系统权限

---

## 🎯 实战案例：天玑如何挖出两个品类的商业情报

> 场景：你想了解某个品类的市场，但不想手动搜几十个网页。
> 耗时：**30秒** | 成本：**$0** | 数据源：全部公开免费

### 数据来源

这份情报来自于**两类采集**的配合——天玑的自动日报 + 按需定向搜索：

| 来源 | 采集方式 | 成本 |
|------|---------|------|
| 汇率/政府公开数据/科技趋势/新闻RSS | ① 天玑自动日报 | API/RSS直连·$0 |
| 电商平台排名/评测/消费者论坛反馈/认证标准 | ② AnySearch按需搜索 | 搜索聚合·$0 |

> ① = 天玑**自动采集器**（定时任务，无需手动触发）
> ② = 天玑**按需搜索**（AnySearch聚合搜索引擎，用于自动采集器暂未覆盖的细分调研）

### 如果没有天玑

手动打开搜索引擎、逐页阅读产品页记录价格评分、搜投诉博客手动归纳、查认证要求阅读官方文档、查汇率、手动整理成表格——**总耗时2-3小时。有天玑：30秒。**

完整案例见：`reports/product-intelligence-demo.md`

### 关键结论

> 天玑不能替代人的商业判断，但它能把调研时间从几小时压缩到几十秒。采集是自动的，整理是结构化的，你要做的只剩**决策**——而决策，是开阳和玉衡的工作，不是天玑的工作。

---

## Change Log

| 版本 | 说明 |
|---|---|
| v1.2 | 新增营销广告/KOL、SEO/GEO、品牌声誉三个维度的v2采集器 |
| v1.3 | 修正"功能地图"一节此前重复粘贴、互相矛盾的两张统计表；改用外眼9域/内镜6域的MECE框架替代原12维度描述；新增关税贸易、支付金融两个采集器（20个采集器，非此前的6-13个不等的各版本描述）；目录结构改为实测核实版本；补充`docs/开阳-PRD.md`索引；标注历史审计文档过时风险与`safe_requests.py`重复文件风险 |
| v1.4 | `tianji_runner.py`升级：正式接入关税贸易、支付金融两个采集器（此前只是文件存在，未在runner里注册）；实现真实性自检机制——每次运行生成`~/tianji-data/manifests/run-{时间戳}.json`结构化执行结果清单，并自动检测本次是否触发新的白名单外域名请求 |
| v1.5 | 跟随`PRD.md` v2.2 跨文档对齐：文档索引中PRD引用更新至v2.2（含外眼内镜+接口管理+数据合规四层架构）；维度表⑧渠道传播的`marketing_intel_collector.py`与PRD保持一致（不再重复挂入⑥竞争格局）；IMF/World Bank等央行数据归属①宏观经济（本README此前即如此，本次确认与PRD对齐） |
| v1.6 | 跟随`PRD.md` v2.3：维度表新增"建议监控类型"列（取自地基7.1，落地地基6.3）；文档索引PRD引用更新至v2.3（含维度全景图带建议监控类型/方法论落地/路线图） |
