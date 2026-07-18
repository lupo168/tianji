# 海外版"RedFox" — 多源数据聚合平台完整对比

> RedFox.hk = 国内社媒/电商统一 API 接口  
> 以下为海外对标方案，按类型分组

---

## 一、统一社媒 API（最接近 RedFox）

| 平台 | 覆盖 | 价格 | 特点 |
|------|------|------|------|
| **KeyAPI.ai** | TikTok/Instagram/YouTube/X/Reddit/LinkedIn/Facebook/Pinterest/Amazon/Threads/Discord/Snapchat 等 20+ | ❓未见公开定价（需联系） | ⭐ 最像 RedFox。单一 REST API，一个 key 通吃，<500ms 延迟，AI Agent 优先设计，含 MCP 集成 |
| **Datashake** | 150+ 来源（社媒+评价+电商+论坛+App Store） | 企业定制 | 数据清洗+标准化，一个 schema 输出，98.3% 可用性，偏企业级 |

| 对比维度 | RedFox (国内) | KeyAPI (海外) |
|----------|--------------|---------------|
| 覆盖平台 | 小红书/抖音/微信/微博/知乎/B站/快手 | TikTok/IG/YT/X/Reddit/LinkedIn/Amazon |
| 计费模式 | 按量付费 | 按量/月费 |
| 适合我们 | ✅ 国内 14 平台 | ❓ 需询价 |

---

## 二、电商数据聚合

| 平台 | 覆盖 | 起步价 | 特点 |
|------|------|--------|------|
| **Oxylabs E-Commerce Scraper** | Amazon/Walmart/Shopee/任意电商站 | **$49/月** (98K条) | 预建爬虫+自定义 parser，195 国家，JS 渲染 |
| **Oxylabs E-Commerce Platform** | Amazon/Walmart/Shopee 等 | 企业定制 | 产品数据库，按需刷新，GTIN 查询 |
| **Bright Data** | 全电商 + 任意网站 | 按量计费 | 代理网络 + 预建爬虫 + 自定义函数，最底层 |
| **Apify** | 2,500+ 预制 Actor | **免费** ($5额度) → $29/月 | 最灵活，社区 Actor 市场，按计算单元计费 |

---

## 三、通用爬虫 / 底层设施

| 平台 | 起步价 | 特点 |
|------|--------|------|
| **ScrapingBee** | $49/月 | 专注浏览器渲染，反检测 |
| **ScrapingDog** | $20/月 | 低价，含代理轮换 |
| **ZenRows** | $69/月 | 反机器检测最强 |
| **ScraperAPI** | $49/月 | 代理+CAPTCHA，简单直接 |

---

## 四、企业情报平台（最贵但最全）

| 平台 | 覆盖 | 起步价 | 特点 |
|------|------|--------|------|
| **SimilarWeb** | 网站流量/电商/广告/社媒 | ~$1,000+/月 | 全行业流量分析，竞品对标 |
| **DataForSEO** | SEO/关键词/排名/竞品 | $50/月 | SERP 数据聚合，覆盖 Google/Bing/Yandex |
| **Diffbot** | 全 Web 结构化抽取 | $299/月 | AI 驱动的页面理解，自动提取实体 |

---

## 五、对我们来说

### 天玑当前路线：自建采集器

| 优势 | 劣势 |
|------|------|
| 免费（API key 成本低） | 每个平台要写代码 |
| 完全控制数据流 | 反爬维护成本 |
| 已接入 17 个 | 扩展 300+ 平台需要时间 |

### 如果采购第三方

| 方案 | 月费 | 能替代哪些采集器 |
|------|------|-----------------|
| **Apify Free** | $0 | ProductHunt + 部分社媒 |
| **Apify Starter** | $29 | + 电商基础数据 |
| **KeyAPI** | ❓ | 替代所有社媒采集器（TikTok/IG/YT/X/Reddit） |
| **Oxylabs E-Commerce** | $49 | 替代 Amazon/Shopee 等电商采集器 |
| **Bright Data** | 按量 | 最灵活的兜底方案 |

### 推荐策略

```
P0 免费用：Apify Free（$5 额度）→ 验证可行性
P1 低价：Apify $29/月 → 覆盖电商+部分社媒
P2 按需：KeyAPI（覆盖海外社媒全矩阵） + Oxylabs（电商） 
P3 自建兜底：天玑采集器覆盖长尾和特殊需求
```

**核心结论**：海外没有 RedFox 那样"一家通吃国内全部平台"的单一方案。海外平台更分散，通常需要**组合使用**——一个社媒聚合（KeyAPI/Datashake）+ 一个电商聚合（Oxylabs/Bright Data）+ 自建长尾采集器。
