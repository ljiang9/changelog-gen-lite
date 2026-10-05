"""changelog-gen-lite：把变更条目归类为 Keep a Changelog 风格 Markdown。

输入可以是 conventional commit 风格的行（如 "feat(auth): add login"），
也可以是普通描述行。按 type 映射到 Keep a Changelog 标准分区：
    Added / Changed / Deprecated / Removed / Fixed / Security
"""

from __future__ import annotations

import re

# conventional type -> Keep a Changelog 分区
TYPE_TO_SECTION = {
    "feat": "Added",
    "feature": "Added",
    "add": "Added",
    "fix": "Fixed",
    "bugfix": "Fixed",
    "hotfix": "Fixed",
    "patch": "Fixed",
    "perf": "Changed",
    "performance": "Changed",
    "refactor": "Changed",
    "style": "Changed",
    "chore": "Changed",
    "docs": "Changed",
    "ci": "Changed",
    "deprecate": "Deprecated",
    "deprecated": "Deprecated",
    "remove": "Removed",
    "removal": "Removed",
    "security": "Security",
}

SECTION_ORDER = ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]

# 形如： type(scope): subject  或  type: subject
LINE_RE = re.compile(r"^\s*(?P<type>[a-zA-Z]+)(?:\([^)]*\))?\s*[:：]\s*(?P<subj>.+?)\s*$")


def classify_line(line: str) -> tuple[str, str]:
    """把一条变更行归类为 (分区, 干净描述)。

    无法识别 type 的行默认归入 "Changed"。
    """
    line = line.strip()
    if not line:
        return "", ""
    m = LINE_RE.match(line)
    if m:
        ctype = m.group("type").lower()
        subj = m.group("subj")
        section = TYPE_TO_SECTION.get(ctype, "Changed")
        return section, _clean(subj)
    # 普通文本：用关键词兜底
    low = line.lower()
    if low.startswith("fix") or "bug" in low or "修复" in line:
        return "Fixed", _clean(line)
    if "security" in low or "漏洞" in line or "cve" in low:
        return "Security", _clean(line)
    if "remove" in low or "删除" in line or "弃用" in low or "deprecated" in low:
        return "Removed", _clean(line)
    return "Changed", _clean(line)


def _clean(text: str) -> str:
    return text.strip().rstrip("。.").strip()


def build_changelog(entries: list[str], version: str = "Unreleased",
                    date: str = "") -> str:
    """把条目列表聚合成 Keep a Changelog 风格 Markdown。"""
    buckets: dict[str, list[str]] = {s: [] for s in SECTION_ORDER}
    for e in entries:
        section, desc = classify_line(e)
        if section and desc and desc not in buckets[section]:
            buckets[section].append(desc)

    header = f"## [{version}]"
    if date:
        header += f" - {date}"

    out = ["# Changelog", "",
           "本项目变更记录遵循 [Keep a Changelog](https://keepachangelog.com/) 规范。",
           "", header, ""]

    any_section = False
    for section in SECTION_ORDER:
        items = buckets[section]
        if not items:
            continue
        any_section = True
        out.append(f"### {section}")
        out.append("")
        for it in items:
            out.append(f"- {it}")
        out.append("")

    if not any_section:
        out.append("（无变更条目）")
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def parse_entries_from_text(text: str) -> list[str]:
    """从多行文本中提取非空变更条目。"""
    return [ln.strip() for ln in text.splitlines() if ln.strip()]
