#!/usr/bin/env python3
"""unittest suite for scripts/validate_repository.py."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "validate_repository.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_repository", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_validator()


VALID_SKILL = """\
---
name: csdd
description: Apply Collaborative Spec-Driven Development as a lightweight protocol.
---

# Collaborative Spec-Driven Development

Body text.
"""

VALID_TODO = """\
# TODO

## In Progress

## Ready to Land

## Blocked

## Pending

## Deferred

## Recently Completed

Retention: 5
"""

VALID_SPECS = "# Specifications\n\nSummary.\n"
VALID_DECISIONS = "# Decisions\n\nNone yet.\n"
VALID_HANDOFF = "# Handoff\n\nNone.\n"
VALID_PROTOCOL = "# Protocol\n\n## Adaptive context hydration\n\nDetails.\n"
VALID_CONTRACTS = "# Document contracts\n\n## Initialization\n\nDetails.\n"
VALID_MIGRATION = "# Migration\n\nDetails.\n"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_valid_repo(root: Path) -> None:
    write(root / "SKILL.md", VALID_SKILL)
    write(root / "references" / "protocol.md", VALID_PROTOCOL)
    write(root / "references" / "document-contracts.md", VALID_CONTRACTS)
    write(root / "references" / "migration-v0.1-to-v0.2.md", VALID_MIGRATION)
    write(root / "assets" / "templates" / "specs.md", VALID_SPECS)
    write(root / "assets" / "templates" / "todo.md", VALID_TODO)
    write(root / "assets" / "templates" / "decisions.md", VALID_DECISIONS)
    write(root / "assets" / "templates" / "handoff.md", VALID_HANDOFF)
    write(
        root / "README.md",
        "# CSDD\n\nSee [protocol](references/protocol.md#adaptive-context-hydration).\n",
    )


class RepositoryValidationTests(unittest.TestCase):
    def assert_has_rule(self, diagnostics, rule: str, file_substr: str | None = None):
        matched = [
            d
            for d in diagnostics
            if d.rule == rule and (file_substr is None or file_substr in d.file)
        ]
        self.assertTrue(
            matched,
            msg=f"expected rule {rule!r}; got {[d.format() for d in diagnostics]}",
        )
        for item in matched:
            self.assertTrue(item.file, msg="diagnostic missing file")
            self.assertTrue(item.rule, msg="diagnostic missing rule")
            self.assertTrue(item.expected, msg="diagnostic missing expected")

    def test_valid_fixture_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            diagnostics = VALIDATOR.validate_repository(root)
            self.assertEqual(diagnostics, [])

    def test_malformed_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            write(
                root / "SKILL.md",
                "name: csdd\ndescription: missing fences\n\n# Body\n",
            )
            diagnostics = VALIDATOR.validate_repository(root)
            self.assert_has_rule(diagnostics, "skill.frontmatter", "SKILL.md")
            self.assertNotEqual(diagnostics, [])

    def test_invalid_name_and_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            write(
                root / "SKILL.md",
                "---\n"
                "name: -Bad_Name--\n"
                "description:\n"
                "---\n\n# Body\n",
            )
            diagnostics = VALIDATOR.validate_repository(root)
            rules = {d.rule for d in diagnostics}
            self.assertIn("skill.name.value", rules)
            self.assertTrue(
                {"skill.name.charset", "skill.description.nonempty"} & rules
            )

    def test_todo_headings_missing_or_out_of_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            write(
                root / "assets" / "templates" / "todo.md",
                "# TODO\n\n"
                "## Ready to Land\n\n"
                "## In Progress\n\n"
                "## Blocked\n\n"
                "## Pending\n\n"
                "## Deferred\n\n"
                "## Recently Completed\n\n"
                "Retention: 5\n",
            )
            diagnostics = VALIDATOR.validate_repository(root)
            self.assert_has_rule(
                diagnostics, "todo_template.h2.order", "assets/templates/todo.md"
            )

            write(
                root / "assets" / "templates" / "todo.md",
                "# TODO\n\n"
                "## In Progress\n\n"
                "## Ready to Land\n\n"
                "## Blocked\n\n"
                "## Pending\n\n"
                "## Recently Completed\n\n"
                "Retention: 5\n",
            )
            diagnostics = VALIDATOR.validate_repository(root)
            self.assert_has_rule(
                diagnostics, "todo_template.h2.missing", "assets/templates/todo.md"
            )

    def test_icebox_or_archived_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            for state in ("Icebox", "Archived"):
                with self.subTest(state=state):
                    write(
                        root / "assets" / "templates" / "todo.md",
                        "# TODO\n\n"
                        "## In Progress\n\n"
                        "## Ready to Land\n\n"
                        "## Blocked\n\n"
                        "## Pending\n\n"
                        "## Deferred\n\n"
                        f"## {state}\n\n"
                        "## Recently Completed\n\n"
                        "Retention: 5\n",
                    )
                    diagnostics = VALIDATOR.validate_repository(root)
                    self.assert_has_rule(
                        diagnostics,
                        "todo_template.forbidden_state",
                        "assets/templates/todo.md",
                    )

    def test_retention_absent_duplicate_zero_or_non_integer(self):
        cases = [
            (
                "# TODO\n\n## In Progress\n\n## Ready to Land\n\n## Blocked\n\n"
                "## Pending\n\n## Deferred\n\n## Recently Completed\n",
                "todo_template.retention.missing",
            ),
            (
                "# TODO\n\n## In Progress\n\n## Ready to Land\n\n## Blocked\n\n"
                "## Pending\n\n## Deferred\n\n## Recently Completed\n\n"
                "Retention: 5\nRetention: 5\n",
                "todo_template.retention.duplicate",
            ),
            (
                "# TODO\n\n## In Progress\n\n## Ready to Land\n\n## Blocked\n\n"
                "## Pending\n\n## Deferred\n\n## Recently Completed\n\n"
                "Retention: 0\n",
                "todo_template.retention.value",
            ),
            (
                "# TODO\n\n## In Progress\n\n## Ready to Land\n\n## Blocked\n\n"
                "## Pending\n\n## Deferred\n\n## Recently Completed\n\n"
                "Retention: five\n",
                "todo_template.retention.value",
            ),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            for content, rule in cases:
                with self.subTest(rule=rule):
                    write(root / "assets" / "templates" / "todo.md", content)
                    diagnostics = VALIDATOR.validate_repository(root)
                    self.assert_has_rule(diagnostics, rule, "assets/templates/todo.md")

    def test_relative_link_to_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            write(root / "README.md", "# CSDD\n\nSee [missing](no-such-file.md).\n")
            diagnostics = VALIDATOR.validate_repository(root)
            self.assert_has_rule(diagnostics, "links.target", "README.md")

    def test_missing_fragment(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            write(
                root / "README.md",
                "# CSDD\n\nSee [bad](references/protocol.md#does-not-exist).\n",
            )
            diagnostics = VALIDATOR.validate_repository(root)
            self.assert_has_rule(diagnostics, "links.fragment", "README.md")

    def test_diagnostics_include_file_rule_and_expectation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            write(root / "README.md", "# CSDD\n\n[x](missing.md)\n")
            diagnostics = VALIDATOR.validate_repository(root)
            self.assertTrue(diagnostics)
            for item in diagnostics:
                rendered = item.format()
                self.assertIn("file=", rendered)
                self.assertIn("rule=", rendered)
                self.assertIn("expected=", rendered)
                self.assertTrue(item.file)
                self.assertTrue(item.rule)
                self.assertTrue(item.expected)

    def test_real_checkout_passes(self):
        diagnostics = VALIDATOR.validate_repository(REPO_ROOT)
        self.assertEqual(
            diagnostics,
            [],
            msg="\n".join(d.format() for d in diagnostics),
        )

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            ok = subprocess.run(
                [sys.executable, str(SCRIPT), str(root)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(ok.returncode, 0, msg=ok.stdout + ok.stderr)
            self.assertIn("Validation passed.", ok.stdout)

            write(root / "README.md", "# CSDD\n\n[bad](missing.md)\n")
            bad = subprocess.run(
                [sys.executable, str(SCRIPT), str(root)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn("file=README.md", bad.stdout)
            self.assertIn("rule=links.target", bad.stdout)
            self.assertIn("expected=", bad.stdout)

    def test_diagnostics_are_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            write(root / "README.md", "# A\n\n[a](missing-a.md)\n[b](missing-b.md)\n")
            write(
                root / "SKILL.md",
                "---\nname: no\ndescription:\n---\n\n# Body\n",
            )
            first = [d.format() for d in VALIDATOR.validate_repository(root)]
            second = [d.format() for d in VALIDATOR.validate_repository(root)]
            self.assertEqual(first, second)
            self.assertEqual(first, sorted(first))

    def test_extra_primary_template_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            write(root / "assets" / "templates" / "backlog.md", "# Backlog\n")
            diagnostics = VALIDATOR.validate_repository(root)
            self.assert_has_rule(
                diagnostics, "templates.primary.extra", "backlog.md"
            )

    def test_links_inside_fenced_code_are_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            write(
                root / "README.md",
                "# CSDD\n\n```markdown\n[broken](missing.md)\n```\n\n"
                "See [protocol](references/protocol.md).\n",
            )
            diagnostics = VALIDATOR.validate_repository(root)
            self.assertEqual(diagnostics, [])

    def test_broken_link_in_snapshot_dirs_is_detected(self):
        cases = (
            ("evals/broken.md", "evals"),
            ("evidence/broken.md", "evidence"),
            (".csdd/broken.md", ".csdd"),
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            for rel, label in cases:
                with self.subTest(dir=label):
                    path = root / rel
                    write(path, "# X\n\n[y](missing.md)\n")
                    diagnostics = VALIDATOR.validate_repository(root)
                    self.assert_has_rule(diagnostics, "links.target", rel)
                    path.unlink()

    def test_protocol_relative_url_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            write(
                root / "README.md",
                "# CSDD\n\n[CDN](//example.com/file.md)\n",
            )
            diagnostics = VALIDATOR.validate_repository(root)
            self.assertEqual(diagnostics, [])
            rules = {d.rule for d in diagnostics}
            self.assertNotIn("links.escape", rules)
            self.assertNotIn("links.target", rules)

    def test_valid_reference_definition(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            write(
                root / "README.md",
                "# CSDD\n\n"
                "See [protocol][proto].\n\n"
                "[proto]: references/protocol.md\n",
            )
            diagnostics = VALIDATOR.validate_repository(root)
            self.assertEqual(diagnostics, [])

    def test_missing_reference_definition_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            write(
                root / "README.md",
                "# CSDD\n\n"
                "See [missing][gone].\n\n"
                "[gone]: no-such-file.md\n",
            )
            diagnostics = VALIDATOR.validate_repository(root)
            self.assert_has_rule(diagnostics, "links.target", "README.md")

    def test_link_escaping_repository_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_valid_repo(root)
            write(
                root / "README.md",
                "# CSDD\n\n[escape](../../outside.md)\n",
            )
            diagnostics = VALIDATOR.validate_repository(root)
            self.assert_has_rule(diagnostics, "links.escape", "README.md")


if __name__ == "__main__":
    unittest.main()
