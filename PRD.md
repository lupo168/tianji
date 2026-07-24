| title | 天玑 · 商业情报采集底座 PRD |
|---|---|
| version | v2.3 |
| date | 2026-07-24 |
| author | JUN + Claude（基于 tianji_kaiyang_foundation_v0.md 地基文档 + 仓库实测核实整合） |
| license | MIT（与仓库现有license保持一致） |
| description | 天玑（天枢系统底座层）的完整PRD，整合边界定义、外眼/内镜/接口管理/数据合规四层架构、功能模块、目录结构、维度全景图（9外眼+6内镜）、安全红线与已知缺口路线图。本版基于对github.com/lupo168/tianji的直接代码核实产出，而非沿用历史文档的自我描述。 |
| tags | 天玑 \| PRD \| 商业情报底座 \| 外眼内镜 \| 安全机制 \| 真实性自检 |

> 本PRD裁定关系：本文档为天玑当前权威PRD，取代`PRD.md`中与本文档冲突的部分（尤其第1.2/1.4节对开阳的旧定义，已由`docs/开阳-PRD.md`裁定，本文档同步采纳）。`README.md`中的采集器状态描述以本文档"6. 功能模块"一节的实测结果为准。

---

## 0. 定位：天玑在天枢三层架构中的位置

```
天枢系统三层架构：

天玑（本文档）  →  开阳（AI分析层） →  玉衡（人类决策层）
   采集              分析+呈现矛盾         人类判断
   原始事实            不决策不执行          唯一有权拍板的节点
   不可污染            不可越权代做决策       定方向+可执行
```

**核心边界定义**：

> 天玑只回答"发生了什么"，开阳回答"这意味着什么，我该怎么办"。

天玑是天枢系统的**事实层**，唯一职责是把"发生了什么"变成结构化、可信、可追溯的数据。天玑不做任何解读、不做优先级判断、不做决策建议——这些都属于开阳的职责范围。详细边界见第3节。

---

## 1. 产品概述

### 1.1 一句话定义

天玑是一个开源的全球商业信息采集底座框架，包含可执行采集管道 + 每日自动日报 + 代码层强制的安全机制（网络白名单、密钥隔离、内容防注入、日报事实过滤），为天枢系统的分析层（开阳）和决策层（玉衡）提供唯一可信的事实输入源。

### 1.2 核心原则

| 原则 | 说明 |
|---|---|
| 只采集，不解读 | 任何涉及"这意味着什么"的判断一律不在天玑层产生，交给开阳 |
| 不可污染 | 天玑记录一旦入库，任何角色（含人类）不可直接篡改，异议走标注流程；技术强制（白名单/密钥隔离/防注入）与流程约束（角色权限）两层同时保障，缺一不可（详见基础地基文档1.5节） |
| 真实性优先于完整性 | 宁可少采、明确标注"暂无法采集"，也不伪装成功、不假装能解析实际做不到的数据 |
| 事实分层，外眼/内镜并行不混淆 | 外部公开数据与内部业务数据分开建设、分开管理权限，交叉分析是开阳的职责，不是天玑的职责 |

---

## 2. 天玑双子系统架构

### 2.1 为什么分两个子系统

信息差有两个方向：**外部信息差**（别人知道、你不知道的事）和**内部信息差**（自己经营中正在发生、但没被系统性看见的事）。两者都属于事实层，但数据来源、采集方式、独占性完全不同，必须分开建设。

### 2.2 天玑-外眼（已实现，覆盖9大域）

采集外部公开可得信息，任何第三方理论上都能采到同样数据，不具备独占性，但具备"时间差"价值。当前通过爬虫/公开API/RSS实现，代码层强制走域名白名单。

### 2.3 天玑-内镜（规划中，尚未实现）

接入自身经营体系内部数据（私域用户行为、各渠道后台真实数据、供应商履约记录、内部财务健康度、客服/社群一手反馈、组织执行记录）。这一层数据完全独占，是外部竞争对手无法复制的资产。**当前状态：0%实现**，需要业务方梳理内部系统接口/导出权限后才能启动，属于下一阶段路线图，不在本版本范围内。

### 2.4 横向支撑层：接口/工具管理（不是第三个子系统）

**定位澄清**：外眼/内镜的分类轴是"数据归属"（外部公开 vs 只有自己有），接口管理的分类轴是"怎么拿到数据"（API/RSS/爬虫/搜索聚合/MCP/CLI/内部系统对接/人工录入）。两条轴互相正交，**不能把接口管理提升成和外眼、内镜平级的"第三个子系统"**——那样会破坏MECE。正确定位：接口管理是外眼和内镜共用的横向基础设施，长在两者下面，服务于两者。

**当前实现**：天玑外眼已有采集器统一通过 `scripts/security/safe_requests.py` 走网络白名单（见第7节），这是接口管理层的"网络统一出口"部分。接口类型分类、每信源接口元数据（获取方式/选择理由/稳定性风险/重新评估触发条件/归属子系统/负责人）需在初始化阶段落地，对应地基文档2.5节。

### 2.5 横向支撑层：数据合规边界

内镜涉及的内部数据（尤其客户数据）一旦跨越法域边界流动（如从私域系统流向分析/存储系统），可能直接触发数据出境合规义务——这不是"要不要采集"的技术决策，是"能不能这样存、这样传"的法律边界，比一般的数据隐私权限更重，单独立一节。

**当前状态：占位待确认。** 内镜启动前必须确认以下通用问题（对应地基文档2.6节）：内镜每个域的数据物理存储/处理所在法域；数据主体（客户）所在法域是否对个人信息出境有特殊要求；是否需要脱敏/匿名化处理后才能跨法域流动，脱敏发生在哪一层。

> 外眼采集的合规风险主要是"目标网站/平台的访问条款"（体现在"合规爬虫"和域名白名单机制），内镜的合规风险主要是"数据主体所在法域对个人信息跨境流动的限制"——两者都要管，但不是同一类风险，不能用同一套检查清单。

---

## 3. 天玑 × 开阳 边界表

| 天玑做 | 天玑不做 |
|---|---|
| 定时/按需采集原始数据 | 解读数据含义 |
| 结构化入库，带时间戳/来源标注 | 判断"重要不重要" |
| 按透明阈值触发信号/告警 | 决定信号该不该升级为行动 |
| 记录采集失败、数据健康度 | 自动修复业务问题 |

判断测试：**这条内容能不能脱离具体处境，被独立验证真假？** 能——归天玑；需要结合处境/目标/风险偏好才能成立——归开阳。

---

## 4. 天玑维度全景图（9外眼 + 6内镜，MECE版）

### 4.1 外眼9域 × 实测覆盖状态（2026-07-23核实）

| 域 | 定义 | 覆盖状态 | 建议监控类型 | 对应采集器 |
|---|---|---|---|
| ①宏观经济与货币金融 | 汇率、大宗商品、通胀等 | ✅ 覆盖较好 | 周期为主（部分触发式） | `fx_collector.py`、`commodity_collector.py`；IMF/World Bank/BoE等央行数据经`gov_open_data_collector.py`覆盖 |
| ②政治与地缘博弈 | 地缘政治动态、大国关系、公开政策博弈 | 🔴 研究完成，未实现 | 触发式为主 | 无（`reports/TOOL_RESEARCH.md`已列11个OSINT源：GDELT/ACLED/ReliefWeb等，待转化） |
| ③政策法规与认证合规 | 行业标准、产品认证要求 | ✅ 覆盖较好 | 触发式+周期兜底 | `gov_open_data_collector.py`（FDA/FCC/CPSC/USPTO/EPA/GOV.UK/UKIPO等） |
| ④贸易、关税与海关 | 关税税则、出口退税、贸易调查 | ✅ 本版新增 | 触发式为主 | `customs_trade_collector.py`（UK Trade Tariff、OFAC/SDN已确认可用；WTO/EU TARIC仅可达性检查；中国海关总署已知限制如实记录） |
| ⑤需求与市场情报 | 品类规模趋势、未满足需求信号 | ⚠️ 部分覆盖 | 周期为主 | `hn_trends_collector.py`、`wiki_trends_collector.py`、`reddit_collector.py` |
| ⑥竞争格局 | 定价促销、新品、资本动向、口碑缺陷 | ✅ 覆盖较好 | 周期+触发式兼有 | `pricing_monitor_collector.py`、`company_intel_collector.py`、`etsy_collector.py`、`producthunt_collector.py`（营销投放归⑧，属跨域共享字段，见地基文档6.4） |
| ⑦供应链与生产 | 原材料价格、B2B询价、物流运价 | ⚠️ 部分覆盖 | 周期为主 | `commodity_collector.py`（原材料价格）；B2B询价/物流运价指数仍缺 |
| ⑧渠道、平台与传播生态 | 平台规则、SEO、广告、KOL、外部舆情 | ✅ 覆盖较好 | 周期为主 | `channel_policy_collector.py`、`seo_geo_collector.py`、`marketing_intel_collector.py`、`reputation_capital_collector.py`、`youtube_collector.py`、`telegram_collector.py`、`agentreach_collector.py` |
| ⑨支付与金融基础设施 | 收单/支付平台费率与政策 | ✅ 本版新增 | 周期为主（政策变更触发式） | `payment_finance_policy_collector.py`（Stripe/PayPal/Airwallex/Wise/Payoneer公开政策监控） |

**外眼综合覆盖：9域中6域已有实现（①③④⑥⑧⑨），2域部分覆盖（⑤⑦），1域研究完成待实现（②）。**

> **监控类型 vs 当前实现的差距（诚实标注，对应地基文档6.3）**：上表"建议监控类型"是该域按时间特性应有的处理方式——其中②地缘、④关税这类**触发式为主**的域，一旦发生必须第一时间知道。但天玑当前所有采集器统一挂在 `tianji_runner.py` 的**每日周期任务**上，尚无独立的异常检测/关键词监听基础设施。也就是说：被判定为"触发式"的域，目前实际仍按周期式运行，存在"窗口期错过"的风险。这是地基文档6.3明确警告要避免、但当前实现尚未覆盖的缺口，已列入第8节路线图。

### 4.2 内镜6域（规划中，0%实现）

| 域 | 定义 | 状态 |
|---|---|---|
| ①客户关系与行为 | 私域用户行为轨迹、复购、流失信号 | 待初始化 |
| ②渠道运营真实数据 | 各渠道后台真实流量成本/转化率 | 待初始化 |
| ③供应链内部履约记录 | 实际交期vs承诺交期、质量记录 | 待初始化 |
| ④内部财务健康度 | 现金流、真实ROI | 待初始化 |
| ⑤内部一手反馈 | 客服工单、社群反馈 | 待初始化 |
| ⑥组织与执行记录 | 内部协作系统执行留痕 | 待初始化 |

---

## 5. 功能模块

### 5.1 采集调度模块

| 模块 | 文件 | 功能 |
|---|---|---|
| 主调度器 | `scripts/tianji_runner.py` | 按daily/weekly/monthly频率批量调用采集器，是唯一的执行入口；v2起每次运行自动生成结构化执行结果manifest |
| 真实性自检manifest（本版新增，已实现） | `~/tianji-data/manifests/run-{时间戳}.json` | 对应地基文档方法一：记录每个采集器本次真实成功/失败/耗时，判断"到底有没有覆盖某数据源"以此为准，不看README的手写状态标记 |
| 日报生成 | `scripts/tianji_daily_report.py` | 汇总当日各采集器输出，生成结构化日报 |
| 初始化脚本 | `scripts/tianji_setup.py` | 环境初始化 |

### 5.2 采集器模块（20个，按域分组）

| 分组 | 采集器文件 |
|---|---|
| 宏观经济 | `fx_collector.py`、`commodity_collector.py` |
| 政策法规 | `gov_open_data_collector.py` |
| 贸易关税（新增） | `customs_trade_collector.py` |
| 支付金融（新增） | `payment_finance_policy_collector.py` |
| 需求趋势 | `hn_trends_collector.py`、`wiki_trends_collector.py`、`reddit_collector.py` |
| 竞争情报 | `pricing_monitor_collector.py`、`company_intel_collector.py`、`etsy_collector.py`、`producthunt_collector.py` |
| 渠道传播 | `channel_policy_collector.py`、`seo_geo_collector.py`、`marketing_intel_collector.py`、`reputation_capital_collector.py`、`youtube_collector.py`、`telegram_collector.py`、`agentreach_collector.py` |
| 新闻资讯 | `rss_news_collector.py` |

### 5.3 安全层模块

| 模块 | 文件 | 功能 |
|---|---|---|
| 网络白名单强制 | `scripts/security/safe_requests.py` + `domain_whitelist.yaml` | 采集器只能访问白名单域名，新增域名必须人工手动添加，代码不能自行决定 |
| 内容防注入过滤 | `scripts/security/content_sanitizer.py` | 检测间接prompt注入模式，给外部内容加"不可信数据"显式包裹 |
| 安全搜索封装 | `scripts/security/safe_search.py` | 统一封装AnySearch等搜索调用，自动过内容防注入过滤 |
| 密钥隔离 | `scripts/security/env_loader.py` | 密钥不进模型上下文 |
| 日报事实过滤 | `scripts/security/report_filter.py` | 日报生成前过滤，防止污染内容混入最终输出 |
| 待审域名队列 | `scripts/security/review_pending_domains.py` + `pending_domains.yaml` | 被拒绝的新域名进入待人工审核队列 |
| 可疑内容复核 | `scripts/security/review_suspicious_content.py` + `suspicious_content_log.yaml` | 人工复核被标记的可疑内容 |
| 代码层强制检查 | `scripts/security/check_no_key_print.py`、`check_no_raw_requests.py` | pre-commit钩子，防止密钥打印、防止绕过safe_requests直连 |

### 5.4 待建模块（本版尚未实现，属于路线图）

| 模块 | 对应方法论 | 说明 |
|---|---|---|
| 决策贡献度记录接口 | 地基文档方法论6.2 | 天玑侧只需提供"该数据被开阳引用次数"的原始记录字段，真正的贡献度评分在开阳/复盘流程完成 |
| 信源可信度分级字段 | 地基文档方法论6.8 | 每个信源的历史准确率记录，暂未在数据模型里落地 |
| 数据TTL标注 | 地基文档方法论6.9 | 各类情报点的有效期阈值，暂未实现 |
| 内镜接入层 | 第2.3节 | 内部系统API对接/ETL，待业务方梳理内部系统权限后启动 |

---

## 6. 目录结构（实测，2026-07-23）

```
tianji/
├── .env.example
├── .pre-commit-config.yaml          # 代码层强制安全检查钩子
├── README.md
├── PRD.md                            # 天玑早期PRD（部分内容已被本文档取代）
├── ROADMAP.md
├── RULES.md                          # 安全红线规则
├── SOUL.md                           # 治理原则
├── SOP.md
├── DEV_SECURITY_STANDARD.md
├── SETUP_SECURITY.md
├── TOOLCHAIN.md
├── API_COST_MATRIX.md
├── BUSINESS_AUDIT_FRAMEWORK.md       # 历史审计文档①（部分内容已过时，见诊断报告）
├── STRATEGIC_AUDIT.md                # 历史审计文档②
├── quickstart.sh
│
├── config/
│   └── DOMAIN_WHITELIST.json         # 域名白名单（展示层，实际强制以scripts/security/domain_whitelist.yaml为准）
│
├── docs/
│   ├── QIXING_ARCHITECTURE.md        # 七星/三层架构总览
│   ├── 开阳-PRD.md                   # 开阳PRD（已存在，v1.0）
│   ├── FULL_INTERFACE_INVENTORY.md   # 全量接口清单研究
│   ├── OVERSEAS_API_AGGREGATORS.md
│   └── PLATFORM_MAP_14_COUNTRIES.md  # 14国平台地图研究
│
├── reports/
│   ├── DIMENSION_AUDIT.md            # 历史审计文档③（已过时，见诊断报告第2节）
│   ├── COVERAGE_AUDIT.md             # 历史审计文档④（已过时）
│   ├── TOOL_RESEARCH.md              # OSINT/政治地缘等工具研究
│   ├── API_VERIFICATION_METHODOLOGY.md
│   ├── product-intelligence-demo.md
│   └── verification/                 # 11份平台API验证报告（约1700行，300+平台）
│       ├── china-tax-customs-banking-34-platforms.md
│       ├── logistics-customer-service-27-platforms.md
│       ├── marketing-ad-24-platforms.md
│       ├── regulatory-33-global-platforms.md
│       ├── north-america-middle-east-28-platforms.md
│       ├── ru-nordic-28-platforms.md
│       ├── russia-13-verified-apis.md
│       ├── russia-nordic-uk-regulatory-24-platforms.md
│       ├── sea-28-platforms.md
│       ├── uk-china-finance-47-platforms.md
│       └── us-26-global-platforms.md
│
└── scripts/
    ├── tianji_runner.py               # 主调度器
    ├── tianji_daily_report.py         # 日报生成
    ├── tianji_setup.py                # 初始化
    ├── env_loader.py
    ├── safe_requests.py               # 注：与security/下同名文件重复，建议后续统一，见第9节
    │
    ├── collectors/                    # 20个采集器（18已有+2本版新增）
    │   ├── fx_collector.py
    │   ├── commodity_collector.py
    │   ├── gov_open_data_collector.py
    │   ├── customs_trade_collector.py          # 本版新增
    │   ├── payment_finance_policy_collector.py # 本版新增
    │   ├── hn_trends_collector.py
    │   ├── wiki_trends_collector.py
    │   ├── reddit_collector.py
    │   ├── pricing_monitor_collector.py
    │   ├── company_intel_collector.py
    │   ├── etsy_collector.py
    │   ├── producthunt_collector.py
    │   ├── channel_policy_collector.py
    │   ├── seo_geo_collector.py
    │   ├── marketing_intel_collector.py
    │   ├── reputation_capital_collector.py
    │   ├── youtube_collector.py
    │   ├── telegram_collector.py
    │   ├── agentreach_collector.py
    │   └── rss_news_collector.py
    │
    └── security/                      # 安全层
        ├── safe_requests.py            # 网络白名单强制（采集器实际调用的版本）
        ├── domain_whitelist.yaml       # 白名单，人工维护
        ├── pending_domains.yaml        # 待审域名队列
        ├── content_sanitizer.py        # 内容防注入
        ├── suspicious_content_log.yaml
        ├── safe_search.py
        ├── env_loader.py
        ├── report_filter.py
        ├── review_pending_domains.py
        ├── review_suspicious_content.py
        ├── check_no_key_print.py       # pre-commit检查
        ├── check_no_raw_requests.py    # pre-commit检查
        └── verify_key.sh
```

> 注：`scripts/safe_requests.py`与`scripts/security/safe_requests.py`同名文件存在于两个位置，建议下一步统一到一处，避免后续维护时改错文件、产生"改了没生效"的隐性bug。

---

## 7. 安全红线（不可触碰）

| 红线 | 保护措施 |
|---|---|
| 采集器不可访问白名单外域名 | `safe_requests.py`强制校验，拒绝并记入`pending_domains.yaml` |
| 新增信源域名不可由代码自行决定 | 必须人工手动写入`domain_whitelist.yaml`，无自动化写入通道 |
| 天玑不可执行任何写操作 | `safe_requests.py`对POST/PUT/DELETE硬拒绝，不区分域名 |
| 外部抓取内容不可未经过滤直接下传 | 强制走`content_sanitizer.py`，标记可疑注入模式 |
| 密钥不可进入模型上下文 | `env_loader.py`隔离，`check_no_key_print.py`做pre-commit拦截 |

---

## 8. 已知缺口与路线图

| 优先级 | 事项 | 状态 |
|---|---|---|
| 已完成 | 关税/海关/贸易域采集器 | 本版新增`customs_trade_collector.py`，已接入runner |
| 已完成 | 支付/跨境金融政策采集器 | 本版新增`payment_finance_policy_collector.py`，已接入runner |
| 已完成 | 真实性自检机制 | `tianji_runner.py` v2每次运行自动生成执行结果manifest，取代人工维护README状态 |
| 待办 | 政治/地缘博弈域采集器 | 研究已完成（11个OSINT源），未实现，优先级低于前两项 |
| 待办 | 供应链域补齐 | B2B询价、物流运价指数仍缺 |
| 待办 | 需求/市场域精度提升 | 现有覆盖偏泛，未做细分未满足需求文本挖掘 |
| 待办 | 内镜子系统启动 | 依赖业务方梳理内部系统接口权限，非天玑代码本身能推进 |
| 待办 | 每个采集器的负责人分配 | 对应地基文档2.5节，防止长期无人维护 |
| 待办 | 信源可信度分级、数据TTL标注 | 对应地基文档6.8/6.9节，暂未落地到数据模型 |
| 待办 | 内镜跨境数据合规确认 | 对应地基文档2.6节，需在内镜启动前而非启动后确认 |
| 待办 | 历史审计文档归档标注 | `DIMENSION_AUDIT.md`、`COVERAGE_AUDIT.md`等需标注"已过时，以本PRD为准"，不建议直接删除（保留历史脉络） |
| 待办 | `scripts/safe_requests.py`与`scripts/security/safe_requests.py`重复文件统一 | 维护风险点 |
| 待办 | 触发式监控基础设施 | 对应地基文档6.3：当前所有采集器统一挂每日周期任务，②地缘/④关税等"触发式为主"的域存在窗口期错过风险。需独立的异常检测/关键词监听通道，不能和周期式共用调度逻辑 |
| 待办 | 内镜数据权限与脱敏规范 | 对应地基文档2.4/2.6：内镜启动前需确认"谁能访问哪类内部数据""脱敏规则""数据主体法域出境限制"。本版2.5节已占位，待业务初始化时落地具体规范 |
| 待办 | HUMINT人工渠道录入接口 | 对应地基文档6.7：人力情报（内部圈子/非公开讨论）天然无法自动化采集，需提供结构化的人工录入接口，让人工获得的事实能与自动采集的事实一起被开阳使用。并非自动化目标 |
| 待办 | 反馈闭环协议（跨天玑-开阳-玉衡） | 对应地基文档第4节：当前三层为单向管道（采集→分析→决策），缺反向学习机制。需天玑/开阳/玉衡三方共同确认"决策结果如何反过来调整采集优先级"。非天玑单独可推进，本文档占位 |

---

## 9. 术语表

| 术语 | 定义 |
|---|---|
| 天玑 | 天枢系统的采集底座层，只回答"发生了什么" |
| 外眼 | 天玑子系统之一，采集外部公开信息 |
| 内镜 | 天玑子系统之一，接入内部业务数据，规划中 |
| 开阳 | 天枢系统的AI分析层，只判断不执行 |
| 玉衡 | 人类决策节点 |
| 白名单强制 | 采集器只能访问预先人工批准的域名，代码本身无权限自行扩展 |
| manifest（真实性自检） | 每次运行 `tianji_runner.py` 自动生成的结构化执行结果清单，记录各采集器真实成功/失败/耗时。判断"是否覆盖某数据源"以此为准，而非手写文档 |
| OSINT | Open-Source Intelligence，开源/公开来源情报。外眼采集的数据均属此类（区别于需要内部权限的 HUMINT/TECHINT） |
| HUMINT | Human Intelligence，人力情报，通过人际关系/内部圈子获得，天然无法自动化采集，需人工录入接口补足（见地基文档6.7） |
| MECE | Mutually Exclusive, Collectively Exhaustive，相互独立、完全穷尽。维度全景图的设计目标，避免同一采集器同时归两个域 |
| TTL | Time-To-Live，情报点建议的有效期阈值。超过TTL未被重新确认的事实应标记为"待复核"，防止过期事实被当作当前事实使用（见地基文档6.9） |
| P0/P1/P2 | 优先级分级标准：P0生死存亡级（触发式为主）、P1增长节奏级（周期式）、P2战略背景板级（低频扫描）。具体归类因业务而异，见地基文档6.6 |

---

## Change Log

| 版本 | 说明 |
|---|---|
| v1.x | 历史版本，见`PRD.md`（部分定义已被本文档裁定/取代） |
| v2.0 | 基于`tianji_kaiyang_foundation_v0.md`地基文档 + 仓库实测核实，整合产出天玑最新PRD：确立外眼/内镜双子系统架构；给出9+6维度全景图与实测覆盖状态；补充功能模块与实测目录结构；新增关税贸易、支付金融两个采集器并计入路线图；标注已知重复文件与过时文档风险点 |
| v2.1 | 真实性自检机制正式实现：`tianji_runner.py` v2接入关税贸易/支付金融两个采集器并生成结构化执行结果manifest，从"待建模块"移至"已实现"；路线图新增负责人分配、信源可信度分级、数据TTL标注、内镜跨境合规确认四项待办（对应地基文档v0.5/v0.6新增内容） |
| v2.2 | 跨文档对齐修订：修正4.1节⑥竞争格局误挂`marketing_intel_collector.py`的MECE破坏（与5.2及README对齐，营销投放明确归⑧渠道传播，标注为跨域共享字段）；修正IMF/World Bank归属（从③政策法规移至①宏观经济，与README一致）；第2节补全2.4接口管理层+2.5数据合规层两个横向支撑层（此前description声称"四层架构"但正文只有两层）；术语表从6条扩充到12条（补manifest/OSINT/HUMINT/MECE/TTL/P0-P2） |
| v2.3 | 方法论落地与路线图补全：4.1节维度表新增"建议监控类型"列（落地地基6.3，取自地基7.1的默认监控类型）；表下诚实标注"当前所有采集器统一挂每日周期任务，触发式基础设施尚未建，②地缘/④关税等触发式域存在窗口期错过风险"；第8节路线图新增四项待办（触发式监控基础设施/内镜数据权限与脱敏规范/HUMINT人工渠道录入接口/反馈闭环协议，分别对应地基6.3/2.4·2.6/6.7/第4节） |
