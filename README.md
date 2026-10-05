# changelog-gen-lite

零依赖的**变更日志生成器**：把一组变更条目（conventional commit 风格或纯文本）自动归类，生成符合 [Keep a Changelog](https://keepachangelog.com/) 规范的 Markdown 变更记录。无需任何 API。

## 功能简介

- 识别 `feat` / `fix` / `docs` / `refactor` / `perf` / `remove` / `security` 等类型前缀。
- 自动映射到标准分区：`Added` / `Changed` / `Deprecated` / `Removed` / `Fixed` / `Security`。
- 按固定顺序输出分区，自动去重，支持中文冒号 `：`。
- 普通文本条目用关键词兜底归类。

## 快速开始

```bash
python3 cli.py --version 1.2.0 --date 2026-10-06 \
  --entry "feat(auth): 新增手机号登录" \
  --entry "fix: 修复验证码倒计时错乱" \
  --entry "docs: 更新部署文档"
```

输出形如：

```markdown
# Changelog

本项目变更记录遵循 [Keep a Changelog](https://keepachangelog.com/) 规范。

## [1.2.0] - 2026-10-06

### Added

- 新增手机号登录

### Changed

- 更新部署文档

### Fixed

- 修复验证码倒计时错乱
```

也可以从文件读取（每行一条）：

```bash
python3 cli.py --file commits.txt --version 1.3.0
```

## 无 API key 如何运行

本项目**完全不需要 API key**，纯本地规则生成。

## 目录说明

```
changelog-gen-lite/
├── changelog_gen.py   # 分类 + Markdown 拼装
├── cli.py            # 命令行入口
├── tests/
│   └── test_changelog.py
├── README.md
├── LICENSE
└── .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests
```

## License

MIT License，Copyright (c) 2026 ljiang9。
