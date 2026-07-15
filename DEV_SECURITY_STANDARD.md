---
title: 天玑 · 开发安全规范
version: v1.0
date: 2026-07-15
status: 强制执行 — 任何人（包括 Hermes 或其他 agent）向这个仓库提交代码，都必须遵守
---

# 天玑 · 开发安全规范

> 这份文档是给"写代码的人/agent"看的，回答的问题是：新写一个采集器、或者改一个现有采集器，
> 该怎么写才不会破坏天玑的安全边界。`RULES.md` 定义的是天玑能做什么/不能做什么，
> 这份文档是"怎么写代码才能让 RULES.md 里的红线真正生效"。
>
> 背景：本次改造前，13个采集器里发现了这些真实问题——密钥硬编码在源代码/明文JSON配置里、
> AnySearch搜索结果未经清洗直接入库、2个文件存在语法错误导致根本跑不起来、
> 子进程调用没传对PYTHONPATH导致改造后的安全模块导入失败。这份规范就是照着这些真实踩过的坑写的，
> 不是抽象原则。

---

## 1. 网络请求：只能走 `safe_requests.py`

```python
# ❌ 禁止
import requests
import urllib.request

# ✅ 必须
from scripts.security.safe_requests import get, get_json, get_text
```

- `get(url, reason="...")` — 拿 `requests.Response` 对象自己处理
- `get_json(url, reason="...")` — 直接返回解析后的 JSON
- `get_text(url, reason="...")` — 直接返回文本（RSS/HTML）

`reason` 参数不是可选的装饰——域名一旦被拒绝，会连同这个 `reason` 一起记录到待审核队列，人类审核时靠这个知道"这次请求是干什么用的"。写清楚，不要留空。

**新域名不在白名单里怎么办**：不要去改 `domain_whitelist.yaml`。让代码正常运行、正常报错，`safe_requests.py` 会自动把这个域名记到 `pending_domains.yaml`，走 `RULES.md` 里定义的人工审核流程。**任何采集器代码都不允许自己动手改白名单文件。**

## 2. 密钥：只能从环境变量读，只能存在 `.env` 里

```python
# ❌ 禁止：硬编码
api_key = "sk-abc123..."

# ❌ 禁止：明文JSON配置文件（这是本次审计中发现的实际问题）
config = json.load(open("~/.hermes/secrets/xxx.json"))

# ✅ 必须
from scripts.security.env_loader import load_env
load_env()
api_key = os.getenv("XXX_API_KEY")
```

- 真实的key写进项目根目录的 `.env`（已在 `.gitignore` 里），新增的 key 记得同步更新 `.env.example`（只写变量名，不写值）
- **验证key是否有效，用 `scripts/security/verify_key.sh`，不要在Python代码里 print/log 密钥变量**——上一次的安全事故就是从这里开始的
- 如果某个接口的 URL 本身必须包含密钥（比如 Telegram Bot API），异常处理里禁止把完整 URL 或异常原文输出，用 `env_loader.mask_secret()` 遮罩后再打印，参考 `telegram_collector.py` 的写法

## 3. 写操作：默认硬拒绝，例外必须单独审计

`safe_requests.py` 里 POST/PUT/DELETE/PATCH 一律抛异常。**天玑没有"临时需要写一次"这种情况**——如果你发现自己需要绕开这一条，说明这个功能不该放在 `collectors/` 目录下，应该是开阳的职责。

唯一的例外是 OAuth 认证握手（换令牌，不是业务写操作），走 `safe_requests.oauth_token_exchange()`，这个函数本身有硬编码的端点白名单和调用审计日志，**新增一个OAuth端点需要修改 `safe_requests.py` 源码本身，不是改配置**——这是故意设计成不好绕的。除此之外，不要再造第二个"例外"。

## 4. 聚合搜索工具（AnySearch等）的结果，必须过内容防注入层

```python
# ❌ 禁止：直接把AnySearch/网页抓取的原始内容拼进后续流程
raw = subprocess.run([...]).stdout
save_to_report(raw)

# ✅ 必须
from scripts.security.safe_search import search_anysearch
safe_text, flagged = search_anysearch(query, max_results=3)
save_to_report(safe_text)
```

原因：域名白名单管的是"天玑能直连哪些域名"，管不到通过白名单内的聚合服务间接返回的、来自任意网页的内容——网页里可能藏着专门写给 AI 看的指令。`search_anysearch()` 已经把 `content_sanitizer.sanitize()` 包在里面了，不需要额外再调用一次。

## 5. 日报/报告：只写事实，不写判断

```python
# 生成完日报文本后，写入文件之前，必须过一遍：
from scripts.security.report_filter import check_report
check_report(report_text)  # 命中"建议""预测""商业价值"等词会抛异常
```

`tianji_daily_report.py` 已经接入了这一步。如果你新写一个会生成日报/报告类文本的采集器，也要接上这一步——不是可选项。

## 6. 提交前必须做的检查

```bash
# 1. 语法检查（py_compile 只检查语法，检查不出模块不存在的问题）
python3 -m py_compile scripts/collectors/你改的文件.py

# 2. 真实import测试（这一步能抓到 py_compile 抓不到的问题——
#    本次审计里 reddit_collector.py 曾经因为一个多余的错误import而无法运行，
#    py_compile 完全没报错，只有真实import才能发现）
python3 -c "
import sys; sys.path.insert(0, '.')
from scripts.collectors import 你改的模块名
"

# 3. pre-commit 全套检查
pre-commit run --all-files
```

**跑分支/新采集器之前，必须实际执行一次 import 测试，不能只依赖语法检查通过就当作没问题。**

## 7. 子进程调用：注意 PYTHONPATH

如果你写的代码要用 `subprocess.run([sys.executable, some_script.py])` 的方式调用另一个 Python 文件（比如 `tianji_runner.py` 调用各个采集器），而那个文件内部用了 `from scripts.security.xxx import yyy` 这种包路径导入，**必须**在 subprocess 里传 `cwd=仓库根目录` 并且设置 `env["PYTHONPATH"] = 仓库根目录`，否则会报 `ModuleNotFoundError: No module named 'scripts'`——这是本次改造中真实踩过的坑，`tianji_runner.py` 已经按这个方式修好，新增类似的调用逻辑要照抄这个模式。

## 8. 常见代码质量问题（本次审计中发现的真实案例，别再犯）

- **f-string里嵌套同类型引号**：`f"...{brand_name}"..."` 这种写法会直接语法错误（`marketing_intel_collector.py` 曾经因此完全跑不起来）。字符串内部要用不同类型的引号，或者用 `\"` 转义
- **重复import**：`from datetime import datetime, timedelta, timedelta`（`wiki_trends_collector.py` 曾经这样写）——不影响运行但说明代码没有被认真检查过
- **提交前跑一次 `python3 -m py_compile`**：这个成本几乎为零，能挡掉大部分低级语法错误

## 9. Pull Request / 提交清单

在提交代码前确认：

- [ ] 网络请求全部走 `safe_requests.py`，没有裸 `import requests`/`urllib`
- [ ] 没有硬编码的密钥，新增的环境变量写进了 `.env.example`
- [ ] 没有新的写操作尝试（POST/PUT/DELETE），OAuth例外走的是 `oauth_token_exchange()`
- [ ] 用到聚合搜索/网页抓取的地方，结果过了 `content_sanitizer` 或 `safe_search`
- [ ] 生成报告/日报的地方接入了 `report_filter.check_report()`
- [ ] 跑过 `python3 -m py_compile` 和真实 import 测试
- [ ] 跑过 `pre-commit run --all-files`
- [ ] 涉及新的子进程调用，确认 `cwd`/`PYTHONPATH` 设置正确

这份清单本身也应该被当作强制项——不是"建议做"，是不满足就不该合并。
