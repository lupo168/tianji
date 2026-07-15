"""
report_filter.py — 天玑日报事实层过滤器

在 tianji_daily_report.py 生成日报的最后一步调用这个函数，
拦截任何"结论性/主观判断"语言，保证天玑的产出止步于事实，
不越界替开阳做解读。

用法：
    from scripts.security.report_filter import check_report

    report_text = generate_report(...)
    check_report(report_text)   # 命中就抛异常，不允许生成含判断性语言的日报
"""

import re

# 这些词一旦出现在天玑日报里，说明产出越过了"事实"进入了"解读/建议"
BLOCKED_KEYWORDS = [
    "建议", "应该", "我认为", "预测", "很可能", "这意味着",
    "商业价值", "差异化机会", "值得关注的是", "值得警惕",
    "推荐", "最佳选择", "风险在于",
]


class SubjectiveContentDetectedError(Exception):
    """日报里检测到了结论性/主观判断语言，天玑不允许产出这类内容"""


def check_report(text: str) -> None:
    hits = []
    for kw in BLOCKED_KEYWORDS:
        if kw in text:
            # 定位到具体哪一行，方便排查
            for lineno, line in enumerate(text.splitlines(), start=1):
                if kw in line:
                    hits.append((kw, lineno, line.strip()))

    if hits:
        msg_lines = ["[天玑安全层] 日报中检测到结论性/主观判断语言，天玑只允许输出事实层：\n"]
        for kw, lineno, line in hits:
            msg_lines.append(f'  第{lineno}行 命中"{kw}": {line}')
        msg_lines.append(
            "\n如果这些内容是有价值的分析判断，应该转交给开阳处理，"
            "并在日报里标注为「待开阳分析」，而不是天玑自己下结论。"
        )
        raise SubjectiveContentDetectedError("\n".join(msg_lines))
