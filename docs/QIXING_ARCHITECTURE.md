# 七星 · 商业情报系统架构报告

> 版本：v1.0 | 2026-07-20 | 基于实际基建状态

---

## 架构总览

```
┌─────────────────────────────────────────────────────────┐
│                      玉衡（人类）                         │
│              JUN LIU · 最终决策者                         │
│         输入：开阳分析报告 · 输出：战略决策                  │
├─────────────────────────────────────────────────────────┤
│                    开阳（AI 分析层）                        │
│    底层：24 大思维框架 + agency-agents 专家人格               │
│    职责：把天玑的原始数据变成可执行的商业建议                   │
├─────────────────────────────────────────────────────────┤
│                    天玑（数据采集层）                        │
│    6 层采集漏斗：RSS → Agent Reach → 官方API → AnySearch   │
│    职责：从 14 国 335 平台自动采集原始数据                     │
└─────────────────────────────────────────────────────────┘
```

---

## 一、天玑（数据采集层）

### 定位
**眼睛。** 不分析、不建议、不决策。只做一件事：按固定周期从已审核的公开信源采集数据，写入数据库，出事实性日报。

### 采集工具链（6 层漏斗）

```
优先级 ↓

1. RSS / Atom 公开源
   ├── Google News, BBC, NRK, Yle, CBC...
   ├── 各平台 Developer Blog RSS
   └── 工具: Agent Reach (feedparser) / curl

2. Agent Reach（平台内容直读）
   ├── YouTube 字幕 (yt-dlp)
   ├── Web 网页 (Jina Reader)
   ├── RSS (feedparser)
   ├── 语义搜索 (mcporter + Exa)
   └── 待解锁: Twitter/X, Reddit, 小红书 (需 Cookie)

3. 官方 API（有 Key 的）
   ├── Etsy Open API v3        ✅ 5K QPD
   ├── YouTube Data API v3     免费 10K/日
   ├── Reddit API              免费 60/min
   ├── Telegram Bot API        免费
   ├── GitHub API              免费 5K/hr
   ├── FRED (美联储)            免费
   ├── CBR (俄罗斯央行)         免费
   ├── Wikipedia API           免费
   ├── Hacker News (Algolia)   免费
   ├── ProductHunt GraphQL     免费
   └── 待接入: Amazon SP-API, Shopify, Mercado Libre...

4. CLI-Anything（官方 harness）
   ├── exa — AI 语义搜索
   ├── intelwatch — 竞争情报/OSINT
   ├── browser-cdp — Chrome 浏览器自动化爬虫
   └── anygen — 文档/报告自动生成

5. AnySearch（通用搜索引擎）
   └── 兜底：以上都拿不到时用

6. 第三方聚合（付费）
   ├── TrendRadar Pro ($9.99/月) — AI 市场情报
   ├── Apify ($0→$29/月) — 2500+ 预制爬虫
   ├── Oxylabs ($49/月起) — 电商数据聚合
   ├── RedFox (已付费) — 国内社媒全平台
   └── KeyAPI (需询价) — 海外社媒聚合
```

### 18 个采集器现状

| 采集器 | 数据源 | 安全层 | 可靠性 |
|--------|--------|:---:|:---:|
| etsy_collector | Etsy API | NEW ✅ | ⭐⭐⭐⭐⭐ |
| producthunt_collector | ProductHunt GraphQL | NEW ✅ | ⭐⭐⭐⭐ |
| agentreach_collector | Agent Reach | 🔴 subprocess | ⭐⭐⭐ (未测试) |
| youtube_collector | YouTube API | OLD | ⭐⭐⭐⭐ |
| reddit_collector | Reddit API | OLD | ⭐⭐ (需 OAuth) |
| fx_collector | CBR + FRED + ExchangeRate | OLD | ⭐⭐⭐⭐ (CBR 已修复) |
| hn_trends_collector | Hacker News | OLD | ⭐⭐⭐⭐⭐ |
| wiki_trends_collector | Wikipedia | OLD | ⭐⭐⭐⭐⭐ |
| telegram_collector | Telegram | OLD | ⭐⭐⭐⭐ |
| rss_news_collector | Google News | OLD | ⭐⭐⭐⭐ |
| gov_open_data_collector | 政府开放数据 | OLD | ⭐⭐⭐⭐ |
| commodity_collector | 大宗商品 | OLD | ⭐⭐⭐ |
| channel_policy_collector | 渠道政策 | OLD | ⭐⭐ (AnySearch) |
| marketing_intel_collector | 营销情报 | OLD | ⭐⭐ (AnySearch) |
| seo_geo_collector | SEO/GEO | OLD | ⭐⭐ (AnySearch) |
| reputation_capital_collector | 品牌声誉 | 🟡 none | ⭐ (AnySearch) |
| pricing_monitor_collector | 竞品定价 | 🔴 subprocess | ⭐⭐ (正则抓价) |
| company_intel_collector | 公司情报 | 🔴 subprocess | ⭐⭐ (关键词匹配) |

---

## 二、开阳（AI 分析层）

### 定位
**大脑。** 把天玑的原始数据变成可执行的商业建议。跨源关联、趋势判断、风险评估、策略推演。

### 双层架构

```
┌──────────────────────────────────────┐
│  第二层：agency-agents 专家人格         │
│  Market Analyst / Competitor Intel    │
│  Risk Assessor / Pricing Strategist   │
│  → 把分析过程结构化、可复用              │
├──────────────────────────────────────┤
│  第一层：24 大思维框架                  │
│  巴菲特的复利 / 芒格的多元思维模型       │
│  达利欧的大周期 / 张一鸣的延迟满足       │
│  → 给分析注入不同的思考视角               │
└──────────────────────────────────────┘
```

### 第一层：24 大思维框架

| 框架 | 适用场景 |
|------|---------|
| **Warren Buffett** | 护城河识别、长期价值判断、定价权分析 |
| **Charlie Munger** | 多元思维模型、误判心理学、逆向思考 |
| **Peter Thiel** | 垄断判断、0→1 机会识别、秘密发现 |
| **Ray Dalio** | 大周期判断、债务周期、宏观风险 |
| **Ben Graham** | 安全边际、内在价值、市场情绪 |
| **Naval Ravikant** | 杠杆思维、复利效应、长期博弈 |
| **Jeff Bezos** | 飞轮效应、长期主义、客户至上 |
| **Steve Jobs** | 产品直觉、极简主义、现实扭曲力场 |
| **Elon Musk** | 第一性原理、物理极限、指数思维 |
| **Sam Altman** | 指数增长、AI 时代、长期乐观 |
| **Zhang Yiming** | 延迟满足、算法驱动、信息效率 |
| **Ren Zhengfei** | 灰度管理、艰苦奋斗、自我批判 |
| **Christensen** | 颠覆式创新、JTBD、价值网络 |
| **Porter / Helmer** | 五力分析、7种战略力量 |
| **Sunzi** | 知己知彼、不战而胜、形势判断 |
| **Kahneman** | 前景理论、系统 1/2、认知偏差 |
| **Taleb** | 黑天鹅、反脆弱、skin in the game |
| **Damodaran** | 估值、叙事经济学 |
| **Druckenmiller** | 资本配置、非对称下注 |
| **Soros** | 反身性、市场认知偏差 |
| **Dalio** | 原则系统、可信度加权 |
| **Graham (Paul)** | 创业思维、做不规模化的事 |
| **Fei Xiaotong** | 差序格局、中国社会结构 |
| **Wu Xiaobo** | 中国商业史、改革开放周期 |

### 第二层：开阳专家 Agent 原型

| Agent 名称 | 绑定框架 | 输入 | 输出 |
|-----------|---------|------|------|
| **Market Sizer** | Damodaran + Bezos | Etsy/Amazon BSR 数据 | TAM/SAM/SOM 测算 |
| **Competitor Analyst** | Porter + Sunzi | 竞品定价、新品、评论 | 竞争五力图 + 攻防建议 |
| **Pricing Strategist** | Buffett + Thiel | 成本 + 竞品价 + 历史 | 最优定价区间 |
| **Risk Scanner** | Taleb + Dalio | FDA/CPSC 法规、汇率 | 风险矩阵 + 对冲策略 |
| **Trend Spotter** | Altman + Bezos | 社媒趋势、专利、融资 | 未来 6-12 月趋势判断 |
| **Channel Strategist** | Zhang Yiming + Naval | 平台政策、Region 物流 | 渠道优先级矩阵 |
| **Copy & Content** | Steve Jobs + 营销 | 竞品文案、热搜词 | 本地化文案建议 |
| **M&A Scout** | Munger + Graham | 融资信号、专利动态 | 收购目标短名单 |
| **Crisis Responder** | Ren Zhengfei + Taleb | 负面舆情、供应链断裂 | 应急响应方案 |
| **Portfolio Optimizer** | Druckenmiller + Dalio | 全业务线数据 | 资源分配权重建议 |

### 工作流示例

```
天玑采集: Etsy "pet water fountain" 358 条，avg $83.35，重力式最热

↓ 开阳分析（三视角并行）

视角1: Peter Thiel（垄断思维）
→ 重力式净水器是 Etsy 上被忽略的 niche
→ 建议: Macallan 以 Berkey 兼容木支架切入，建立品类垄断

视角2: Charlie Munger（多元思维模型）
→ 木工 + 净水器 + Etsy SEO = 三个能力圈的交叉点
→ 建议: 不要做全品类，只做"实木 + 净水器配件"这一个交叉点

视角3: Naval Ravikant（杠杆思维）
→ 木支架 $265 × 0 边际成本(按需定制)
→ 建议: 用 3D 打印 STL 文件($5)做引流，木支架做利润

↓ 玉衡决策

JUN 根据三视角分析做出最终选择
```

---

## 三、玉衡（人类决策层）

### 定位
**决策者。** 机器不能替你判断，但能让你判断得更准。

玉衡的输入是开阳的多视角分析报告，输出是战略决策。玉衡的职责：

- 审阅开阳的「矛盾点」（两个框架给出相反建议的地方）
- 注入机器无法获取的信息（行业人脉、直觉、风险偏好）
- 做最终 Go/No-Go 决策
- 反馈给天玑「接下来重点采集什么」

---

## 四、当前基建与缺口

### ✅ 已就绪

| 层 | 组件 | 状态 |
|----|------|:---:|
| 天玑 | 18 采集器 | ✅ |
| 天玑 | 6 层采集漏斗 | ✅ |
| 天玑 | 安全层 + 白名单 145 域 | 🟡 待合并 |
| 天玑 | Etsy API + Agent Reach + CLI-Anything | ✅ |
| 开阳 | 24 大思维框架（Nuwa Skills） | ✅ 已装 |
| 玉衡 | JUN LIU | ✅ |

### 🔲 待建设

| 层 | 缺口 | 优先级 |
|----|------|:---:|
| 天玑 | 安全层合并（OLD → NEW） | P0 |
| 天玑 | 日报引擎跑通 | P0 |
| 天玑 | 定时任务恢复 | P0 |
| 天玑 | Agent Reach 采集器验证 | P1 |
| 天玑 | CLI-Anything 接入采集器 | P1 |
| 天玑 | 6 个 AnySearch 换皮改为独立 API | P1 |
| 天玑 | SQLite 替代散落 JSON | P2 |
| 开阳 | **开阳核心引擎（0% → 可运行）** | P0 |
| 开阳 | 10 个专家 Agent 原型 | P1 |
| 开阳 | 多视角分析流水线 | P2 |
| 玉衡 | 天玑→开阳→玉衡 数据管道 | P2 |
