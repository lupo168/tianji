# 开阳 · AI 分析层 — PRD

> 版本：v1.0 | 创建：2026-07-20
> 作者：JUN LIU / Claude
> 状态：初稿 · 待确认
> **本文档裁定了 PRD.md 与 QIXING_ARCHITECTURE.md 对"开阳"定义的冲突**——见第 0 节

---

## 0. 定义裁定（先解决历史遗留矛盾）

现有仓库里，`PRD.md` 把开阳定义为"自动化执行层……接收天玑日报→自动分析→响应/升级"，`QIXING_ARCHITECTURE.md` 把开阳定义为纯"AI 分析层"，只出建议不执行。本 PRD **采用 QIXING_ARCHITECTURE.md 的定义**：

> **开阳只判断，不执行。** 所有需要产生真实副作用的动作（调价、下单、发消息、改库存、发邮件），一律由独立的、写死规则的执行脚本完成，开阳最多产出一条"建议执行 XX 动作"的结构化请求，动作本身不由开阳直接触发。

**理由**：
1. 单人运营，没有余力去调试一个会自动操作的系统出的错，出错成本（比如自动调错价）远高于收益
2. 这是 2026 年主流多 agent 架构里"决策编排 + 确定性执行器分离"的标准做法——agent 判断该做什么，具体怎么做交给一段可测试的代码去做，避免 LLM 临场决定操作细节
3. 给未来留口子：如果以后真的要让开阳能触发部分低风险动作，架构上是往"结构化请求→独立执行模块"这个方向加一层，而不是让开阳直接获得写权限

**待办**：`PRD.md` 第 1.2、1.4 节需要同步改成本节的定义，避免继续误导。

---

## 1. 产品概述

### 1.1 一句话定义

开阳是天枢系统的**AI 分析层**，把天玑采集的原始数据转化为可执行的商业建议，通过多专家视角并行分析 + 独立仲裁呈现矛盾点，交给玉衡（JUN）做最终决策。开阳本身**不做决策，不执行操作**。

### 1.2 定位

```
天枢系统三层架构：

天玑（底座）    →    开阳（分析层）    →    玉衡（决策层）
  采集               分析+呈现矛盾           人类判断
  原始               不决策不执行            定方向+可执行
  不可污染            不可越权代做决策         唯一有权拍板的节点
```

### 1.3 核心原则

| 原则 | 说明 |
|------|------|
| 只判断，不执行 | 任何有副作用的操作走独立执行脚本，开阳没有写权限 |
| 呈现矛盾，不调和矛盾 | 多视角分歧必须原样呈现给玉衡，不允许悄悄压平成"统一建议" |
| 分层独立产出 | 专家 Agent 之间互不可见对方输出，避免随大流 |
| 结构化输出 | 禁止自由文本结论，所有输出走固定 JSON schema |
| 可回溯校准 | 每条建议记录"是否被采纳"，用于未来评估各专家 Agent 的可靠性 |

### 1.4 用户画像

| 用户 | 角色 | 使用方式 |
|------|------|---------|
| 天玑 | 数据提供方 | 定时产出结构化数据，开阳按需读取 |
| 开阳自身 | AI 分析层 | Tier1 分领域产出观点 → Tier2 仲裁呈现矛盾 |
| JUN（玉衡） | 唯一决策者 | 审阅矛盾点摘要 → 做 Go/No-Go 决策 → 反馈影响未来天玑采集重点 |

---

## 2. 架构设计

### 2.1 两层结构

```
                     ┌──────────────────────────────┐
                     │  Tier 2：综合仲裁层（1个Agent）  │
                     │  不绑定任何思维框架，专职仲裁      │
                     │  职责：标出矛盾点，不解决矛盾      │
                     └───────────────┬────────────────┘
                                      │ 汇总
        ┌──────────┬──────────┬──────┴───┬──────────┬──────────┐
        │          │          │          │          │          │
   ┌────▼───┐ ┌────▼───┐ ┌────▼───┐ ┌────▼───┐ ┌────▼───┐  ...(共10个)
   │Market  │ │Competitor│ │Pricing │ │Risk    │ │Trend   │
   │Sizer   │ │Analyst  │ │Strategist│Scanner │ │Spotter │
   └────┬───┘ └────┬───┘ └────┬───┘ └────┬───┘ └────┬───┘
        │          │          │          │          │
        └──────────┴──────────┴──────────┴──────────┘
                     Tier 1：分析师层（互不可见彼此输出）
                              ↑
                          天玑数据
```

### 2.2 Tier 1：专家 Agent 层（10 个）

| Agent 名称 | 绑定框架 | 输入 | 输出字段 |
|-----------|---------|------|---------|
| Market Sizer | Damodaran + Bezos | Etsy/Amazon BSR 数据 | TAM/SAM/SOM 测算 |
| Competitor Analyst | Porter + Sunzi | 竞品定价、新品、评论 | 竞争五力图 + 攻防建议 |
| Pricing Strategist | Buffett + Thiel | 成本 + 竞品价 + 历史 | 最优定价区间 |
| Risk Scanner | Taleb + Dalio | 法规、汇率数据 | 风险矩阵 + 对冲策略 |
| Trend Spotter | Altman + Bezos | 社媒趋势、专利、融资 | 6-12月趋势判断 |
| Channel Strategist | Zhang Yiming + Naval | 平台政策、物流 | 渠道优先级矩阵 |
| Copy & Content | Steve Jobs + 营销 | 竞品文案、热搜词 | 本地化文案建议 |
| M&A Scout | Munger + Graham | 融资信号、专利动态 | 收购目标短名单 |
| Crisis Responder | Ren Zhengfei + Taleb | 负面舆情、供应链中断 | 应急响应方案 |
| Portfolio Optimizer | Druckenmiller + Dalio | 全业务线数据 | 资源分配权重建议 |

**每个 Agent 的输出必须是固定 JSON schema，不接受自由文本：**

```json
{
  "agent": "Pricing Strategist",
  "framework": ["Buffett", "Thiel"],
  "input_ref": "天玑数据源ID列表",
  "conclusion": "一句话结论",
  "supporting_evidence": ["依据1", "依据2"],
  "confidence": 0.0,
  "counter_argument": "反对本结论最有力的理由是什么",
  "recommended_action": "建议的下一步动作（不是自动执行，只是文字建议）",
  "generated_at": "ISO8601时间戳"
}
```

**约束**：Tier1 各 Agent 之间**不共享上下文**，同一批天玑数据分发给 10 个 Agent 是并行独立调用，不是链式传递——避免后调用的 Agent 被前面的结论带偏。

### 2.3 Tier 2：综合仲裁层（1 个）

- 不绑定任何思维框架，人设是"中立仲裁者"，唯一职责是**发现矛盾、呈现矛盾**，不允许输出"综合以上意见，建议……"这种把分歧压平的结论
- 输入：Tier1 全部 10 份 JSON 输出
- 输出结构：

```json
{
  "report_date": "YYYY-MM-DD",
  "topic": "本次分析主题",
  "consensus_points": ["多数Agent一致认同的判断"],
  "conflict_points": [
    {
      "issue": "冲突焦点是什么",
      "position_a": {"agent": "...", "stance": "..."},
      "position_b": {"agent": "...", "stance": "..."},
      "why_it_matters": "这个分歧对决策的实际影响"
    }
  ],
  "confidence_weighted_summary": "按各Agent置信度加权后的简要陈述，不是最终建议",
  "escalate_to_yuheng": true
}
```

- **仲裁层不能做的事**：不能因为某个 Agent 置信度高就直接采纳其结论作为"最终答案"；不能省略共识度低的少数派意见；不能把"多数意见"包装成"正确答案"

---

## 3. 数据流转与存储

### 3.1 输入源

| 数据 | 来源 | 格式 |
|------|------|------|
| 结构化情报数据 | 天玑 `tianji_structured` 表 | PostgreSQL |
| 业务上下文（成本结构、产品类目等） | JUN 手工录入 | 见 3.3 |

### 3.2 输出存储（新增表，追加在天玑 schema 之后）

```sql
-- Tier1 专家分析表
CREATE TABLE kaiyang_tier1_analysis (
    id BIGSERIAL PRIMARY KEY,
    agent_name VARCHAR(50) NOT NULL,
    framework VARCHAR(100),
    input_ref JSONB,                    -- 引用的天玑数据ID
    conclusion TEXT NOT NULL,
    supporting_evidence JSONB,
    confidence DECIMAL(3,2),
    counter_argument TEXT,
    recommended_action TEXT,
    generated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tier2 仲裁报告表
CREATE TABLE kaiyang_tier2_report (
    id BIGSERIAL PRIMARY KEY,
    report_date DATE NOT NULL,
    topic VARCHAR(200),
    consensus_points JSONB,
    conflict_points JSONB,
    confidence_weighted_summary TEXT,
    tier1_refs BIGINT[],                -- 引用的 tier1 分析 id 列表
    generated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 玉衡决策反馈表（用于未来校准各 Agent 可靠性）
CREATE TABLE yuheng_decision_log (
    id BIGSERIAL PRIMARY KEY,
    tier2_report_id BIGINT REFERENCES kaiyang_tier2_report(id),
    decision TEXT NOT NULL,             -- JUN的最终决策
    adopted_agent_names VARCHAR[],      -- 采纳了哪些Agent的意见
    rejected_agent_names VARCHAR[],     -- 否决了哪些Agent的意见
    rationale TEXT,                     -- JUN注入的判断依据（人脉/直觉/风险偏好）
    decided_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 3.3 业务上下文注入（P0 前置依赖）

开阳分析必须有 JUN 的业务上下文才有意义，否则只是通用商业评论。上线前需要先把这些录入一个配置文件（不是每次分析都问）：

```yaml
# kaiyang_business_context.yaml
product_lines:
  - name: 宠物饮水机
    entity: FURRY BABY LTD
    bom_cost: 110  # CNY
    shipping_cost: 50
    platform_fee_pct: 15
  - name: 家用净水器
    entity: Macallan Inc.
    bom_cost: ...
target_markets: [US, UK, SEA]
private_domain_users: 120000
suppliers: [汇纳海, 盛泰滤材]
```

---

## 4. 输出设计（呈现给玉衡的报告）

```
开阳分析报告 — YYYY-MM-DD
=======================
主题：宠物饮水机 Etsy 品类机会评估

━━━━ 共识点 ━━━━
✓ 重力式净水器是 Etsy 上被忽略的 niche（10/10 Agent 一致）
✓ 定价区间 $180-280 有空间（8/10 Agent 支持）

━━━━ 矛盾点（需要您判断）━━━━
⚡ 品类策略分歧：
  Peter Thiel视角（Competitor Analyst）→ 建立品类垄断，全品类覆盖
  Munger视角（Portfolio Optimizer）→ 只做"实木+净水器"能力圈交叉点，不要铺开
  → 这个分歧的实际影响：决定您接下来3个月的SKU开发方向

━━━━ 置信度加权摘要 ━━━━
（仅供参考，不是最终建议）...

━━━━ 待您决策 ━━━━
[ ] Go / No-Go
[ ] 若Go，选哪个品类策略
```

---

## 5. 系统架构

### 5.1 技术栈

| 组件 | 选型 | 理由 |
|------|------|------|
| 编程语言 | Python 3.11+ | 与天玑保持一致 |
| LLM 调用 | Claude API | Tier1/Tier2 均为独立 API 调用，无需框架 |
| 输出校验 | pydantic | 强制 JSON schema，拒绝自由文本 |
| 并行调用 | asyncio | Tier1 十个 Agent 并行请求，不是顺序链式 |
| 数据库 | PostgreSQL（复用天玑同一实例） | 新增3张表即可，不需要单独部署 |

**明确不引入**：AutoGen / CrewAI / LangGraph 等重型多 agent 框架。理由：单人维护，10+1 个 Agent 用顺序/并行 API 调用 + JSON schema 约束就能满足现阶段需求，复杂度应该留在 prompt 设计上，不是留在基础设施上。等真的需要动态路由（谁发言、何时升级）再评估引入框架。

### 5.2 执行触发方式

- **不做成自动定时任务**（这点和天玑不同）——开阳分析应该是 JUN 主动触发（"针对某个品类/某个决策点，跑一次开阳分析"），而不是每天自动跑一遍产出无人看的报告
- 触发方式：命令行 `python3 kaiyang_runner.py --topic "宠物饮水机品类策略"`，读取天玑最新相关数据 + business_context.yaml，跑 Tier1→Tier2，输出报告

---

## 6. 实施路线图

### Phase 1：单 Agent 验证（本周）

```
D1：先只做 1 个 Agent（建议从 Pricing Strategist 开始，输入输出最容易验证）
  ├─ 定义 JSON schema（pydantic model）
  ├─ 写 prompt，绑定 Buffett+Thiel 框架
  ├─ 接入天玑一个数据域（比如 Etsy 定价数据）
  └─ 手动跑一次，人工检查输出质量

D2：验证输出可用后，补 business_context.yaml 注入
```

### Phase 2：Tier1 全量 + Tier2 仲裁（下周）

```
├─ 补齐剩余 9 个 Agent
├─ 实现并行调用（asyncio）
├─ 写 Tier2 仲裁 Agent，验证"呈现矛盾不调和"这条约束是否被遵守
└─ kaiyang_runner.py 命令行工具跑通
```

### Phase 3：反馈闭环（本月）

```
├─ yuheng_decision_log 表接入，每次决策后手动记录
├─ 跑够 10-20 次分析后，回看哪些 Agent 的建议采纳率高/低
└─ 根据采纳率数据，考虑砍掉长期不准的 Agent 或调整其 prompt
```

### Phase 4（暂不做，留口子）

```
"能执行"能力——仅在 Phase 1-3 稳定运行、且 JUN 明确需要后才评估
架构预留：开阳输出 recommended_action 字段 → 未来可接一个独立的、
规则写死的执行模块，LLM本身不直接获得写权限
```

---

## 7. 成功指标

| 指标 | 目标 | 衡量方式 |
|------|------|---------|
| Tier1 输出 schema 合规率 | 100% | pydantic 校验通过率 |
| 矛盾点呈现完整性 | 不遗漏任何方向性分歧 | 人工抽查 Tier2 输出 vs Tier1 原始输出 |
| 决策反馈记录率 | 每次分析都有 yuheng_decision_log | 手动记录 |
| 建议采纳率可追溯 | 跑够20次后能看出各Agent准确率排名 | 查询 yuheng_decision_log |

北极星指标暂不设（数据量不够前谈"决策覆盖率"没有意义，先跑够样本量）。

---

## 8. 边界与红线

### 红线（不可触碰）

| 红线 | 违反后果 | 保护措施 |
|------|---------|---------|
| 开阳不能直接调用任何有副作用的API | 出错成本不可控 | 代码层不给开阳任何写权限的 API key |
| 开阳不能碰密钥明文 | 和天玑同级别红线 | 复用天玑的 env_loader，密钥不进模型上下文 |
| Tier2 不能把矛盾压平成单一建议 | 剥夺玉衡的判断依据 | Tier2 prompt 明确写死"禁止综合成一个建议"，人工抽查 |
| Tier1 之间不能共享上下文 | 导致随大流、虚假共识 | 架构上强制并行独立调用，不做链式传递 |

### 边界

| 开阳做 | 开阳不做 |
|--------|---------|
| 读取天玑数据做跨源分析 | 直接执行任何操作（天玑同样不做） |
| 按框架视角产出结构化建议 | 替玉衡做 Go/No-Go 决策 |
| 标出多视角矛盾 | 调和/压平矛盾 |
| 记录建议与决策的对应关系 | 自动根据历史决策"学习"改变自己的立场（避免过拟合到JUN过去的偏好而失去独立视角） |

---

## 9. 依赖资源

### 已有资源

| 资源 | 用途 |
|------|------|
| 天玑已产出的结构化数据 | 开阳的唯一输入源 |
| Claude API | Tier1/Tier2 全部调用 |
| PostgreSQL（天玑同实例） | 新增3张表 |
| Claude.ai 已装的约14个人物视角 Skill | 可作为 prompt 设计参考，但需要重写成 API 可调用的 system prompt，不能直接照搬 Claude.ai skill 格式 |

### 需要新建的

| 资源 | 用途 |
|------|------|
| kaiyang_business_context.yaml | 业务上下文配置 |
| kaiyang_runner.py | 命令行触发脚本 |
| 10 个 Tier1 Agent 的 prompt 文件 | 建议单独存放，方便迭代 |
| 1 个 Tier2 仲裁 Agent 的 prompt 文件 | 同上 |

---

## 10. 风险与缓解

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| 10 个 Agent 输出高度雷同，"多视角"沦为形式 | 中 | 高 | Phase 3 用采纳率数据识别雷同/低价值 Agent，及时砍掉 |
| Tier2 仲裁 Agent 偷懒把矛盾压平 | 中 | 高 | prompt 明确禁止 + 人工抽查前 10 次输出 |
| 业务上下文过时导致分析脱离实际 | 高 | 中 | business_context.yaml 需要定期人工更新，建议每月检查一次 |
| 天玑数据质量不足（部分采集器⭐⭐可靠性）拖累开阳分析质量 | 高 | 中 | Tier1 Agent 的 input_ref 必须标注数据源可靠性，低可靠性数据源的结论自动降置信度 |

---

## 11. 附录

### A. 术语表

| 术语 | 定义 |
|------|------|
| 开阳 | 天枢系统的AI分析层，只判断不执行 |
| Tier1 | 10个专家Agent，分领域独立产出观点 |
| Tier2 | 1个仲裁Agent，负责呈现矛盾不调和矛盾 |
| 玉衡 | 人类决策节点，即JUN |
| 矛盾点 | 多个Tier1 Agent方向性冲突的判断 |

### B. 相关文件

| 文件 | 位置 | 用途 |
|------|------|------|
| 天玑PRD | PRD.md | 天玑产品需求（需要同步更新第1.2/1.4节的开阳定义） |
| 七星架构总览 | docs/QIXING_ARCHITECTURE.md | 三层架构总览，本PRD的上位文档 |
| 天玑安全规则 | RULES.md | 开阳的安全红线应参照同一标准 |
| 本PRD | docs/KAIYANG_PRD.md（建议路径） | 开阳产品需求文档 |

### C. Change Log

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-07-20 | 初稿，裁定PRD.md与QIXING_ARCHITECTURE.md的定义冲突，确立"只判断不执行"原则 |
