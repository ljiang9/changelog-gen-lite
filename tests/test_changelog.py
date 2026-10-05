import unittest

from changelog_gen import (SECTION_ORDER, build_changelog, classify_line,
                           parse_entries_from_text)


class TestClassify(unittest.TestCase):
    def test_feat_to_added(self):
        section, desc = classify_line("feat(auth): 新增手机号登录")
        self.assertEqual(section, "Added")
        self.assertEqual(desc, "新增手机号登录")

    def test_fix_to_fixed(self):
        section, desc = classify_line("fix: 修复验证码倒计时错乱")
        self.assertEqual(section, "Fixed")
        self.assertIn("验证码", desc)

    def test_docs_to_changed(self):
        section, _ = classify_line("docs: 更新部署文档")
        self.assertEqual(section, "Changed")

    def test_remove_to_removed(self):
        section, _ = classify_line("remove: 废弃旧版导出接口")
        self.assertEqual(section, "Removed")

    def test_plain_text_fallback(self):
        section, desc = classify_line("优化了首页加载速度")
        self.assertEqual(section, "Changed")
        self.assertEqual(desc, "优化了首页加载速度")

    def test_security(self):
        section, _ = classify_line("security: 修复越权访问漏洞")
        self.assertEqual(section, "Security")


class TestBuild(unittest.TestCase):
    def test_markdown_structure(self):
        md = build_changelog([
            "feat: 新增导出功能",
            "fix: 修复登录崩溃",
            "fix: 修复登录崩溃",
        ], version="1.2.0", date="2026-10-06")
        self.assertIn("# Changelog", md)
        self.assertIn("## [1.2.0] - 2026-10-06", md)
        self.assertIn("### Added", md)
        self.assertIn("- 新增导出功能", md)
        self.assertIn("### Fixed", md)
        self.assertEqual(md.count("- 修复登录崩溃"), 1)

    def test_section_order(self):
        md = build_changelog(["feat: a", "fix: b", "remove: c"])
        idx_added = md.index("### Added")
        idx_fixed = md.index("### Fixed")
        idx_removed = md.index("### Removed")
        self.assertLess(idx_added, idx_removed)
        self.assertLess(idx_removed, idx_fixed)

    def test_no_entries(self):
        md = build_changelog([])
        self.assertIn("无变更条目", md)

    def test_parse_entries(self):
        text = "feat: a\n\nfix: b\n   \n"
        self.assertEqual(parse_entries_from_text(text), ["feat: a", "fix: b"])


if __name__ == "__main__":
    unittest.main()
