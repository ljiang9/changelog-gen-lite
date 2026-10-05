"""changelog-gen-lite 命令行入口。

用法示例：
    python3 cli.py --version 1.2.0 --date 2026-10-06 \
        --entry "feat(auth): 新增手机号登录" \
        --entry "fix: 修复验证码倒计时错乱" \
        --entry "docs: 更新部署文档"
    python3 cli.py --file commits.txt --version 1.3.0
"""

from __future__ import annotations

import argparse
import sys

from changelog_gen import build_changelog, parse_entries_from_text


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="changelog-gen-lite",
        description="把变更条目归类为 Keep a Changelog 风格 Markdown",
    )
    p.add_argument("--entry", action="append", default=[], help="变更条目，可重复传入")
    p.add_argument("--file", help="从文本文件读取变更条目（每行一条）")
    p.add_argument("--version", default="Unreleased", help="版本号，默认 Unreleased")
    p.add_argument("--date", default="", help="发布日期，如 2026-10-06")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    entries = list(args.entry)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            entries.extend(parse_entries_from_text(f.read()))

    if not entries:
        print("错误：请用 --entry 或 --file 提供变更条目", file=sys.stderr)
        return 2

    print(build_changelog(entries, version=args.version, date=args.date))
    return 0


if __name__ == "__main__":
    sys.exit(main())
