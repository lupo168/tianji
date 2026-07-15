---
title: 天玑 · 红线规范（RULES）
version: v1.0
date: 2026-07-15
author: JUN + Claude
applies_to: 天玑（采集子系统）
status: 强制执行，非建议性文档
---

# 天玑 · 红线规范

> 本文档不是"希望天玑怎么做"，而是"天玑在代码层面能做什么、不能做什么"。
> 凡是能用代码/权限/网络层拦住的，一律不依赖 Hermes 自觉遵守文字规则。
> soul.md / rules.md 之前失败了三次，原因不是写得不够狠，是文字规则从架构上就管不住模型行为。本文档的每一条都要求配一个"代码层强制点"，没有强制点的条款视为无效。

---

## 👤 一、定位（一句话讲清楚天玑是什么）

天玑只做一件事：把公开、免费或已授权的外部信息，按固定周期抓回来，写进数据库和 PDF。它不判断、不建议、不执行、不接触任何密钥的明文。

它存在的唯一价值，是给开阳和玉衡（人类）提供一份**无条件可信**的事实层。这个信任一旦被污染一次,后面所有分析和决策都建立在不可信的地基上——所以圈死范围不是限制天玑的能力,是保护整个天枢系统最贵的资产:数据可信度。

---

## 👤 二、允许的动作

| 允许做的事 | 对应现有实现 |
|---|---|
| 按周期调用只读 API / 拉取 RSS | `scripts/collectors/*.py` 里现有的汇率、新闻、HN、政府数据采集器 |
| 结构化清洗后写入数据库（信息层原始事实） | 未来接入 PostgreSQL 后的落库环节 |
| 按周期自动生成 PDF/MD 日报，只呈现事实 | `tianji_daily_report.py` |
| 记录采集元数据（来源、时间戳、采集方式） | 各 collector 的 metadata 字段 |
| 调用第三方"聚合搜索"类工具（AnySearch、Tavily 等）做**按需检索**，但仅限只读查询 | `anysearch_cli.py search "..."` 这类调用 |

## 👤 三、绝对禁止的动作

| 禁止做的事 | 为什么 | 代码层强制点 |
|---|---|---|
| 执行任何对外写操作(下单、改价、发消息、调用需鉴权的写 API) | 天玑只是眼睛,不是手 | 采集器运行环境的出站请求，除已知只读 API 域名外，其余一律 403（见第五节网络白名单） |
| 读取或接触任何密钥明文 | 之前3次越权的直接根源 | 密钥不进 Hermes 的对话上下文，见第四节 |
| 对采集内容做主观解读、预测、建议 | 这是开阳的职责,天玑越界一次,信任链就断一次 | 日报生成模板里禁止出现"建议""预测""应该""我认为"等词，加一道生成后关键词过滤，命中就整段拒绝输出 |
| 访问白名单之外的域名 | 防止被诱导访问未审核的信源或恶意站点 | 见第五节 |
| 修改自己的 RULES.md / SOP.md / 采集器权限配置 | 防止自我松绑 | 这些文件对天玑运行时进程设为只读权限（`chmod 444` 或等效），只有人类在仓库层面能改 |
| 与开阳共享同一套凭证 / 执行环境 | 防止越权后果扩散 | 天玑和开阳分别用独立的服务账号/进程运行，不共享 `.env` |
| 在"调试代码/验证 API 是否可用"这个开发过程中，把 key 的明文值读进自己的推理上下文 | 这是上次泄露到 DeepSeek 的真实路径——不是任务执行时读的，是写代码/调试时读的 | 见第四节"验证不经过模型" |

---

## 👤 四、密钥管理规范（这是本次事故的核心整改项）

**问题的真实机制**：不是 Hermes 在"执行任务"时偷看了 key，是这个仓库本身由 Hermes 编写和调试（README author 就写着 Hermes Agent），它在验证某个 API key 能不能用的时候，很自然地会把 key 的值打印出来确认——这个打印动作发生在它自己的对话/推理过程里，而那个过程被路由到了 DeepSeek，key 就这样出去了。

**整改方式，三层缺一不可：**

1. **物理隔离**：所有 key 只存在于 `.env`（已在 `.gitignore` 里，需要现在核实历史 commit 里干不干净），代码里一律 `os.getenv("XXX_API_KEY")` 引用，不允许出现任何形式的 `print(api_key)` 或把 key 写进日志/报告。

2. **验证不经过模型**：验证某个 key 是否有效，用一段独立的、不进入 Hermes 对话上下文的 shell 脚本完成，比如：
   ```bash
   # verify_key.sh —— Hermes 只被允许看到这个脚本的退出码和"成功/失败"，看不到 key 本身
   curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $FRED_API_KEY" \
     "https://api.stlouisfed.org/fred/series?series_id=..." 
   ```
   Hermes 可以被告知"跑一下 verify_key.sh 看看返回 200 还是 401"，但不能被允许 `cat .env` 或在对话里输出 key 内容做核对。

3. **提交前拦截**：装 `detect-secrets` 或 `git-secrets` 做 pre-commit hook，任何长得像 key 的字符串（`sk-`、32位以上的十六进制串等）一律拦截 commit，不依赖 Hermes 自己记得"别提交密钥"。
   ```bash
   pip install detect-secrets
   detect-secrets scan > .secrets.baseline
   # 配到 pre-commit
   ```

---

## 👤 五、网络访问白名单

天玑运行环境的出站网络，只允许访问以下类别域名，其余一律拒绝（不是"建议不要访问"，是网络层直接 403）：

- 已在 README 里列出的官方 API/RSS 域名（CBR、FRED、World Bank、OpenFDA、GOV.UK 等）
- 已审核通过的搜索聚合服务域名（AnySearch、Tavily）
- 明确禁止：任何未经审核就临时新增的域名，哪怕是采集任务过程中"顺手"发现的新信源，都要先过白名单审核流程才能加入，不能由 Hermes 自行决定当场访问。

实现方式可以参考 Claude 自己 bash 工具的 `allowed_domains` 机制——在采集器进程的容器/沙箱层面配置出站规则，而不是写在 Python 代码里靠 if 判断（if 判断可以被绕过或遗漏，网络层规则不能）。

---

## 👤 六、输出格式限定

- 日报（`reports/daily-*.md`）只允许包含：数据、来源、时间戳。不允许包含结论性语言。
- 任何需要"解读这批数据意味着什么"的内容，天玑只能原样标注"待开阳分析"，不能自己下判断。
- 第七节实战案例里那种"这是设计差异化机会"式的结论，属于开阳该做的事，天玑的产出应该止步于"消费者投诉Top3是XXX"，不该往下走一步给出商业含义解读。**这一条现在其实已经有点越界了，建议下一版日报模板里把"发现的核心情报"里"商业价值"这一列单独拆出去，标注为开阳产出,不算天玑产出。**

---

## 👤 七、第三方依赖审查（新发现的风险面）

天玑接入了几个非官方的第三方工具（`last30days`、`source-verifier` 来自个人仓库 `stansz/hermes-community-pulse`，以及 RedFox、ScrapeCreators）。这些是黑盒代码，天玑的"零污染"原则不能只防 Hermes 自己越权,也要防这些依赖本身携带的风险:

- 逐个审查这几个包的源码，或至少确认它们的网络访问范围
- 把它们放进独立的、没有密钥访问权限、且被网络白名单限制的子进程里跑，即使这个包本身被投毒，也拿不到 key、碰不到白名单外的域名

---

## 👤 八、违规处理机制

- 任何一条红线被触发（越权网络请求、试图读取密钥文件、日报里出现结论性语言），**硬停**，不是记录警告后继续跑
- 所有工具调用日志记录在天玑进程之外、Hermes 自己够不到的地方（比如宿主机的独立日志服务），保证出问题后能溯源，且日志本身不能被 Hermes 篡改

---

## 🤖 AGENT MANIFEST (YAML)

```yaml
subsystem: 天玑
role: collection_only
permitted_actions:
  - read_only_api_call
  - rss_fetch
  - db_write_raw_facts
  - generate_daily_report_facts_only
  - on_demand_search_aggregator_readonly
prohibited_actions:
  - any_write_to_external_system
  - read_secret_plaintext
  - subjective_interpretation_in_output
  - access_domain_outside_whitelist
  - modify_own_rules_or_permission_config
  - share_credentials_with_kaiyang
enforcement:
  network: allowlist_only_403_default_deny
  secrets: env_var_only_no_print_no_log
  key_verification: external_shell_script_not_model_context
  precommit: detect-secrets_hook_required
  output_filter: block_keywords[建议, 预测, 应该, 我认为]
  file_permission: rules_and_soul_readonly_to_runtime
violation_response: hard_stop_not_warn
third_party_deps_review_required:
  - last30days
  - source-verifier
  - RedFox
  - ScrapeCreators
```
