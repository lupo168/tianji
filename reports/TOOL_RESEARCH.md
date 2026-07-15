---
title: Tool Research Report — Tavily / Horizon / Crucix / UnifAPI
version: v1.0
date: 2026-07-14
license: MIT
description: Detailed evaluation of Tavily, Horizon Data Wave, Crucix, and UnifAPI for business intelligence use.
---

# 工具调研报告 — 天玑(Tianji)全球商业情报系统候选工具

> 调研日期: 2026-07-14
> 调研范围: Tavily, Horizon Data Wave, Crucix, UnifAPI

---

## 一、全景对比表

| 维度 | **Tavily** | **Horizon Data Wave** | **Crucix** | **UnifAPI** |
|---|---|---|---|---|
| **类型** | AI搜索引擎API | LinkedIn/社交数据API | 开源OSINT情报引擎 (自建) | 公开数据API平台 |
| **官网** | tavily.com | horizondatawave.ai | crucix.live | unifapi.com |
| **官方API?** | ✅ 是 | ✅ 是 | ❌ 无中心API (自收集27个数据源) | ✅ 是 |
| **API文档** | docs.tavily.com | api.horizondatawave.ai/redoc | N/A (GitHub: github.com/calesthio/Crucix) | docs.unifapi.com |
| **免费额度** | 1,000 credits/月 (无信用卡) | 100 请求/月 | 完全免费 (开源, 需自建) | 500 credits 一次性试用 |
| **付费模式** | $0.008/credit, 或 $30~$123/月 | $0.025/请求, Pay-as-you-go | 免费 (仅需部分数据源的免费API key) | $0.001/credit, 按用量付费 |
| **企业方案** | ✅ 定制报价 | ✅ 定制报价 | N/A (自建) | ✅ 定制报价 |
| **数据源范围** | 全网公开网页 (新闻/技术文档/实时事件) | LinkedIn个人资料/公司/职位/邮箱 | 27个OSINT源 (卫星/航班/辐射/经济/冲突/制裁/社交) | 16个平台 × 220+端点 (TikTok/LinkedIn/IG/YouTube/X/Reddit等) |
| **速率限制** | Dev 100 RPM, Prod 1,000 RPM | 未公开具体数值 | 取决于各数据源自身限制 | 按credits计费, 无硬性RPM限制 |
| **MCP支持** | ✅ 有 (mcp.tavily.com) | ❌ 未明确支持 | 🟡 可通过LLM配置使用 | ✅ 有 (mcp.unifapi.com) |
| **Agent集成** | LangChain/LlamaIndex原生, Python/JS SDK | Python SDK (2行代码) | Claude Code/OpenAI Codex集成 | MCP Server + HTTP REST + 8种语言SDK |
| **竞品对比** | 对标Exa, You.com, Parallel; 赢在LangChain生态 | 对标Coresignal, ZoomInfo; 更便宜但数据范围窄 | 无直接竞品; 独树一帜的社区OSINT方案 | 对标Anysite, Bright Data; 赢在MCP原生+按记录付费 |

> **注意:** "Crucix"域名 crucix.com 是宗教网站; 正确产品在 crucix.live 和 GitHub上。
> **注意:** "Uniflo" (uniflo.io) 不是一个活跃产品; 正确产品是 **UnifAPI** (unifapi.com)。

---

## 二、各工具详细分析

### 1️⃣ Tavily

**是什么?**
专为AI Agent设计的搜索API。把传统搜索引擎的原始HTML/SERP结果转换成结构化的、LLM友好的JSON输出。当前被2M+开发者使用, 已被Nebius收购。

**核心能力:**
- `/search` — 语义搜索, 返回排名+评分的结构化结果
- `/extract` — 从任意URL提取结构化内容 (无需JS渲染)
- `/crawl` — 网站爬取和站点地图
- `/research` — 深度研究模式 (多步自主调查)

**定价:**
- Free: 1,000 credits/月 (无信用卡)
- Pay-as-you-go: $0.008/credit
- Project: $30~$123/月 (滑条调节, 含4,000~X credits)
- Enterprise: 定制 (SLA, 安全, 隐私)

**速率限制:**
- Dev环境: 100 RPM (search/extract)
- Prod环境: 1,000 RPM
- Crawl: 100 RPM (dev/prod相同)
- Research: 20 RPM

**MCP集成:**
- MCP Server: `https://mcp.tavily.com/mcp/`
- 支持keyless模式 (无需API key即可测试)
- 提供 `tavily-search` 和 `tavily-extract` 工具

**天玑适配性评估: ⭐⭐⭐⭐⭐ (强烈推荐)**
- ✅ 最成熟的Agent搜索API, 社区最大
- ✅ 免费额度充裕, 上手成本极低
- ✅ LangChain/LlamaIndex原生集成
- ✅ 刚被Nebius收购, 生态持续增长
- ❌ 偏重通用网页搜索, 对结构化B2B数据支持有限
- ❌ Research endpoint速率较低 (20 RPM)

---

### 2️⃣ Horizon Data Wave

**是什么?**
聚焦LinkedIn数据的社交数据API, 专门为AI Agent和自动化场景设计。不仅提供数据查询, 还支持通过API执行社交操作 (发送消息、添加联系人、发布内容)。

**核心能力:**
- LinkedIn个人资料查询 (工作经验、教育、技能、认证)
- 邮箱发现 (通过邮箱查资料 / 从资料提取邮箱)
- 职位情报 (关键词、经验级别、行业筛选)
- 公司情报 (地点、员工数、成立日期)
- 社交自动化 (发送消息、添加联系人、发布帖子)

**定价:**
- Starter: 0元/月 (100请求)
- Pay-and-Go: $0.025~0.02/请求
- Enterprise: 定制 (自定义数据源+Agent+支持)

**数据源:**
- LinkedIn (个人资料、公司、职位)
- 邮箱数据
- 暂无其他社交平台

**MCP/Agent集成:**
- Python SDK: "2行代码集成"
- 文档: api.horizondatawave.ai/redoc
- 没有明确MCP支持

**天玑适配性评估: ⭐⭐⭐ (可选)**
- ✅ 价格透明, 100免费请求
- ✅ LinkedIn数据对商业情报有价值
- ⚠️ 数据范围窄 (仅LinkedIn)
- ❌ 无MCP, 无明确速率限制文档
- ❌ 产品相对早期, 社区较小

---

### 3️⃣ Crucix

**是什么?**
一个开源的**自建**情报聚合引擎 (AGPL v3), GitHub上10.4K+星标的爆款项目。聚合27个公开OSINT数据源, 每15分钟刷新, 渲染在Jarvis风格仪表盘上。

**⚠️ 重要: Crucix不是一个商业API产品, 而是一个自托管(自建)的开源项目。**

**核心架构:**
```
git clone → npm install → npm run dev → http://localhost:3117
```

**27个数据源覆盖:**
| 类别 | 源数量 | 具体源 |
|---|---|---|
| 地缘政治/OSINT | 11 | GDELT, OpenSky, ADS-B Exchange, NASA FIRMS, Maritime AIS, Safecast, ACLED, ReliefWeb, WHO, OFAC, OpenSanctions |
| 经济/金融 | 7 | FRED, US Treasury, BLS, EIA, GSCPI, USAspending, UN Comtrade |
| 环境/社交/SIGINT | 7 | NOAA, EPA RadNet, USPTO, Bluesky, Reddit, Telegram, KiwiSDR |
| 太空 | 1 | CelesTrak |
| 市场 | 1 | Yahoo Finance |

**免费额度:** 完全免费 (开源), 部分数据源需要免费API key (FRED, FIRMS, EIA等)

**LLM集成:**
- 支持 Anthropic Claude, OpenAI, Google Gemini, OpenAI Codex
- LLM故障不阻塞sweep循环 (优雅降级)
- 可生成AI交易想法和简报

**天玑适配性评估: ⭐⭐⭐⭐ (高价值参考)**
- ✅ 27种OSINT数据源, 对全球情报采集极有价值
- ✅ 完全免费, 自建可控
- ✅ 可嵌入天玑作为数据采集层之一
- ✅ GitHub社区活跃, 20+贡献者
- ❌ 需要Node.js 22+ 自建基础设施
- ❌ 部分数据源API key需自行申请
- ❌ 不是商业API, 没有SLA
- 💡 **建议:** 把Crucix的数据采集逻辑作为天玑的一个模块/数据管道引入

---

### 4️⃣ UnifAPI

**是什么?**
面向AI Agent的公开数据API平台。提供220+个标准化JSON端点, 覆盖16个社交/媒体平台。通过一个MCP Server和统一计费体系运营。

> 注: uniflo.io 和 getuniflo.com 不是本调研目标; 正确产品为 UnifAPI (unifapi.com)

**定价:**
- 试用: 500 credits 一次性赠送 (无需信用卡)
- Pay-as-you-go: $0.001/credit
- 大部分记录 = 1 credit ($0.001)
- Search类: 10 credits/次 ($0.01)
- Analytics类: 50 credits/次 ($0.05)
- Premium类: 500 credits/次 ($0.50)
- Enterprise: 定制 (年约, SLA, SSO, 审计日志)

**16个平台 × 220+端点:**
| 平台 | 端点数量 (部分) | 数据类型 |
|---|---|---|
| TikTok | 20 | 视频、创作者、评论、标签、音乐 |
| LinkedIn | 多端点 | 个人资料、公司、职位 |
| Instagram | 多端点 | 探索、位置、内容 |
| YouTube | 多端点 | 频道、视频、搜索 |
| Twitter/X | 多端点 | 推文、用户、趋势 |
| Reddit | 多端点 | 帖子、评论、社区 |
| Threads | 多端点 | 帖子、用户 |
| 其他 | GEO/Maps/News/SEO/浏览器 | 地理位置、地图、新闻、SEO |

**MCP集成: ⭐⭐⭐⭐⭐ (最佳)**
- MCP Server: `https://mcp.unifapi.com`
- OAuth认证, Streamable HTTP传输
- 支持Skills (预封装的任务工作流)
- 提供自然语言查询 (`/ask` 端点)
- 同时支持HTTP REST + MCP双模式

**天玑适配性评估: ⭐⭐⭐⭐ (强烈推荐)**
- ✅ 220+标准化端点, 覆盖社交/媒体/地理/SEO
- ✅ MCP原生支持, 与天玑的Agent架构高度匹配
- ✅ 按记录计费, 成本可预测 ($0.001/记录)
- ✅ SDK覆盖8种语言
- ❌ 产品相对新 (500 credits试用)
- ❌ 不覆盖企业B2B数据 (LinkedIn个人资料不如Horizon深)
- ❌ 不覆盖深层OSINT/卫星/经济指标数据

---

## 三、天玑整合建议

| 天玑数据需求 | 推荐工具 | 理由 |
|---|---|---|
| **通用网页搜索 + Agent实时信息** | Tavily ⭐⭐⭐⭐⭐ | Agent搜索黄金标准, LangChain/MCP生态 |
| **LinkedIn/社交自动化数据** | Horizon Data Wave ⭐⭐⭐ | 价格透明, 但范围窄; 可做辅助数据源 |
| **全球OSINT情报 (卫星/航班/辐射/冲突/制裁)** | Crucix (开源自建) ⭐⭐⭐⭐ | 27个数据源免费聚合, 建议作为数据管道模块引入 |
| **社交平台公开数据 (TikTok/YT/IG/X/Reddit)** | UnifAPI ⭐⭐⭐⭐⭐ | 220+标准化端点, MCP原生, 按记录计费 |
| **企业B2B深度数据 (公司/员工)** | 目前缺口 → 建议补充调研 Coresignal/ZoomInfo | Tavily/UnifAPI不覆盖结构化企业数据 |

### 短期行动建议

1. **立即接入: Tavily** — 免费额度充裕, LangChain生态, MCP支持
2. **优先评估: UnifAPI** — MCP原生, 220+社交数据端点, 与天玑架构最匹配
3. **中期整合: Crucix数据管道** — 把27个OSINT源的数据采集逻辑抽取为天玑模块
4. **按需选用: Horizon Data Wave** — 如果需要深度LinkedIn自动化 (发消息/加好友)
5. **补充调研缺口:** 企业B2B数据层 (Coresignal, ZoomInfo, Apollo.io)

---

*报告生成: Hermes Agent | 数据来源: 各工具官网/文档/GitHub/公开评测*
