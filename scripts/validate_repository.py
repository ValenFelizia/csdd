#!/usr/bin/env python3
"""Structural repository validation for the CSDD skill package.

Offline, deterministic checks using only the Python standard library.
This is repository tooling, not a CSDD skill runtime dependency.

Frontmatter parsing covers the simple ``key: value`` subset used by CSDD's
``SKILL.md``. It is not a general YAML parser.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlparse

REQUIRED_RUNTIME_PATHS = (
    "SKILL.md",
    "references/protocol.md",
    "references/document-contracts.md",
    "references/migration-v0.1-to-v0.2.md",
    "assets/templates",
)

PRIMARY_TEMPLATES = (
    "specs.md",
    "todo.md",
    "decisions.md",
    "handoff.md",
)

CANONICAL_TODO_H2 = (
    "In Progress",
    "Ready to Land",
    "Blocked",
    "Pending",
    "Deferred",
    "Recently Completed",
)

FORBIDDEN_TODO_H2 = ("Icebox", "Archived")

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
H2_RE = re.compile(r"^##[ \t]+(.+?)\s*$")
RETENTION_RE = re.compile(r"^Retention:\s*(.*?)\s*$")
INLINE_LINK_RE = re.compile(
    r"(?<!!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)"
)
IMAGE_LINK_RE = re.compile(
    r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)"
)
REF_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\[([^\]]*)\]")
REF_DEF_RE = re.compile(
    r"^\[([^\]]+)\]:\s*(\S+)(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*$",
    re.MULTILINE,
)
FENCE_RE = re.compile(r"^(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)\s*$")

# Link scan covers shipped docs/runtime only (not project ops / eval evidence).
LINK_SKIP_TOP_LEVEL = frozenset({".csdd", "evals", "evidence"})


@dataclass(frozen=True)
class Diagnostic:
    file: str
    rule: str
    expected: str
    detail: str = ""

    def format(self) -> str:
        parts = [
            f"file={self.file}",
            f"rule={self.rule}",
            f"expected={self.expected}",
        ]
        if self.detail:
            parts.append(f"detail={self.detail}")
        return "; ".join(parts)


def repo_rel(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def strip_fenced_code_blocks(text: str) -> str:
    """Replace fenced code block interiors with blank lines (keep line count)."""
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in lines:
        stripped = line.lstrip()
        if not in_fence:
            match = FENCE_RE.match(stripped)
            if match:
                in_fence = True
                fence_marker = match.group(1)
                out.append(line)
            else:
                out.append(line)
        else:
            if stripped.startswith(fence_marker):
                in_fence = False
                fence_marker = ""
                out.append(line)
            else:
                # Preserve newlines only so later line-based scans stay aligned.
                out.append("\n" if line.endswith("\n") else "")
    return "".join(out)


def iter_markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        if not path.is_file():
            continue
        parts = path.resolve().relative_to(root.resolve()).parts
        if ".git" in parts:
            continue
        if parts and parts[0] in LINK_SKIP_TOP_LEVEL:
            continue
        files.append(path)
    return files


def parse_skill_frontmatter(text: str) -> tuple[dict[str, str], str, list[Diagnostic]]:
    """Parse the simple CSDD SKILL.md frontmatter subset.

    Accepts opening/closing ``---`` fences and single-line ``key: value``
    entries. Does not implement general YAML.
    """
    diagnostics: list[Diagnostic] = []
    file_label = "SKILL.md"

    if not (text.startswith("---\n") or text.startswith("---\r\n")):
        diagnostics.append(
            Diagnostic(
                file_label,
                "skill.frontmatter",
                "SKILL.md begins with opening --- frontmatter fence",
                "opening fence missing",
            )
        )
        return {}, text, diagnostics

    lines = text.splitlines(keepends=True)
    # First line is opening fence.
    closing_index = None
    for idx in range(1, len(lines)):
        if lines[idx].rstrip("\r\n") == "---":
            closing_index = idx
            break

    if closing_index is None:
        diagnostics.append(
            Diagnostic(
                file_label,
                "skill.frontmatter",
                "SKILL.md has a closing --- frontmatter fence",
                "closing fence missing",
            )
        )
        return {}, text, diagnostics

    meta_lines = lines[1:closing_index]
    body = "".join(lines[closing_index + 1 :])
    fields: dict[str, str] = {}
    seen: dict[str, int] = {}

    for raw in meta_lines:
        line = raw.rstrip("\r\n")
        if not line.strip():
            continue
        if ":" not in line:
            diagnostics.append(
                Diagnostic(
                    file_label,
                    "skill.frontmatter",
                    "frontmatter entries use 'key: value' form",
                    f"unparseable line: {line!r}",
                )
            )
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            diagnostics.append(
                Diagnostic(
                    file_label,
                    "skill.frontmatter",
                    "frontmatter keys are non-empty",
                    f"empty key in line: {line!r}",
                )
            )
            continue
        seen[key] = seen.get(key, 0) + 1
        fields[key] = value

    for key, count in sorted(seen.items()):
        if key in ("name", "description") and count > 1:
            diagnostics.append(
                Diagnostic(
                    file_label,
                    "skill.frontmatter.unique",
                    f"{key} appears exactly once",
                    f"appeared {count} times",
                )
            )

    return fields, body, diagnostics


def validate_skill_md(root: Path) -> list[Diagnostic]:
    path = root / "SKILL.md"
    file_label = "SKILL.md"
    if not path.is_file():
        return [
            Diagnostic(
                file_label,
                "skill.exists",
                "SKILL.md exists at repository root",
                "file missing",
            )
        ]

    text = path.read_text(encoding="utf-8")
    fields, body, diagnostics = parse_skill_frontmatter(text)

    if "name" not in fields:
        diagnostics.append(
            Diagnostic(
                file_label,
                "skill.name",
                "frontmatter contains name",
                "name missing",
            )
        )
    else:
        name = fields["name"]
        if name != "csdd":
            diagnostics.append(
                Diagnostic(
                    file_label,
                    "skill.name.value",
                    "name equals csdd",
                    f"observed {name!r}",
                )
            )
        if not (1 <= len(name) <= 64):
            diagnostics.append(
                Diagnostic(
                    file_label,
                    "skill.name.length",
                    "name length is between 1 and 64 characters",
                    f"length={len(name)}",
                )
            )
        if not NAME_RE.fullmatch(name):
            diagnostics.append(
                Diagnostic(
                    file_label,
                    "skill.name.charset",
                    "name uses only lowercase ASCII letters, digits, and "
                    "single hyphens between segments (no leading/trailing/"
                    "consecutive hyphens)",
                    f"observed {name!r}",
                )
            )

    if "description" not in fields:
        diagnostics.append(
            Diagnostic(
                file_label,
                "skill.description",
                "frontmatter contains description",
                "description missing",
            )
        )
    else:
        description = fields["description"]
        if description == "":
            diagnostics.append(
                Diagnostic(
                    file_label,
                    "skill.description.nonempty",
                    "description is non-empty",
                    "description is empty",
                )
            )
        if len(description) > 1024:
            diagnostics.append(
                Diagnostic(
                    file_label,
                    "skill.description.length",
                    "description length is at most 1024 characters",
                    f"length={len(description)}",
                )
            )

    if not body.strip():
        diagnostics.append(
            Diagnostic(
                file_label,
                "skill.body",
                "Markdown body after frontmatter is non-empty",
                "body empty",
            )
        )

    return diagnostics


def validate_runtime_boundary(root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for rel in REQUIRED_RUNTIME_PATHS:
        path = root / rel
        if rel.endswith(".md"):
            ok = path.is_file()
            expected = f"{rel} exists as a file"
        else:
            ok = path.is_dir()
            expected = f"{rel}/ exists as a directory"
        if not ok:
            diagnostics.append(
                Diagnostic(
                    rel,
                    "runtime.required",
                    expected,
                    "missing from repository",
                )
            )
    return diagnostics


def validate_primary_templates(root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    templates_dir = root / "assets" / "templates"
    label = "assets/templates"

    if not templates_dir.is_dir():
        diagnostics.append(
            Diagnostic(
                label,
                "templates.dir",
                "assets/templates/ directory exists",
                "directory missing",
            )
        )
        return diagnostics

    present = sorted(p.name for p in templates_dir.iterdir() if p.is_file())
    markdown = [name for name in present if name.endswith(".md")]
    expected = set(PRIMARY_TEMPLATES)
    observed = set(markdown)

    missing = sorted(expected - observed)
    extra = sorted(observed - expected)

    for name in missing:
        diagnostics.append(
            Diagnostic(
                f"{label}/{name}",
                "templates.primary.missing",
                f"primary template {name} exists",
                "file missing",
            )
        )

    for name in extra:
        diagnostics.append(
            Diagnostic(
                f"{label}/{name}",
                "templates.primary.extra",
                "only specs.md, todo.md, decisions.md, and handoff.md "
                "are primary templates",
                f"unexpected primary template {name}",
            )
        )

    return diagnostics


def heading_text(raw: str) -> str:
    text = raw.strip()
    # Strip simple wrapping emphasis/code markers for anchor text.
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*+([^*]+)\*+", r"\1", text)
    text = re.sub(r"_+([^_]+)_+", r"\1", text)
    return text.strip()


def collect_h2_headings(text: str) -> list[tuple[int, str]]:
    cleaned = strip_fenced_code_blocks(text)
    headings: list[tuple[int, str]] = []
    for lineno, line in enumerate(cleaned.splitlines(), start=1):
        match = H2_RE.match(line)
        if match:
            headings.append((lineno, heading_text(match.group(1))))
    return headings


def validate_todo_template(root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    path = root / "assets" / "templates" / "todo.md"
    label = "assets/templates/todo.md"

    if not path.is_file():
        diagnostics.append(
            Diagnostic(
                label,
                "todo_template.exists",
                "assets/templates/todo.md exists",
                "file missing",
            )
        )
        return diagnostics

    text = path.read_text(encoding="utf-8")
    headings = collect_h2_headings(text)
    names = [name for _, name in headings]

    allowed = set(CANONICAL_TODO_H2)
    forbidden = set(FORBIDDEN_TODO_H2)
    for name in names:
        if name in forbidden:
            diagnostics.append(
                Diagnostic(
                    label,
                    "todo_template.forbidden_state",
                    f"H2 '{name}' must not appear in the shipped template",
                    f"found ## {name}",
                )
            )
        elif name not in allowed:
            diagnostics.append(
                Diagnostic(
                    label,
                    "todo_template.h2.extra",
                    "only the six canonical TODO H2 headings are present",
                    f"unexpected H2 {name!r}",
                )
            )

    canonical_observed = [name for name in names if name in allowed]
    expected_list = list(CANONICAL_TODO_H2)

    for name in expected_list:
        count = canonical_observed.count(name)
        if count == 0:
            diagnostics.append(
                Diagnostic(
                    label,
                    "todo_template.h2.missing",
                    f"H2 '{name}' appears exactly once",
                    "missing",
                )
            )
        elif count > 1:
            diagnostics.append(
                Diagnostic(
                    label,
                    "todo_template.h2.duplicate",
                    f"H2 '{name}' appears exactly once",
                    f"appeared {count} times",
                )
            )

    # Order among canonical headings that are present (unique sequence).
    unique_canonical: list[str] = []
    for name in canonical_observed:
        if name not in unique_canonical:
            unique_canonical.append(name)

    expected_present = [name for name in expected_list if name in unique_canonical]
    if unique_canonical != expected_present:
        diagnostics.append(
            Diagnostic(
                label,
                "todo_template.h2.order",
                "canonical H2 headings appear in order: "
                + ", ".join(expected_list),
                f"observed order: {', '.join(unique_canonical) or '(none)'}",
            )
        )

    # Retention: scan outside fences.
    cleaned = strip_fenced_code_blocks(text)
    lines = cleaned.splitlines()
    retention_hits: list[tuple[int, str]] = []
    for lineno, line in enumerate(lines, start=1):
        match = RETENTION_RE.match(line)
        if match:
            retention_hits.append((lineno, match.group(1)))

    if len(retention_hits) == 0:
        diagnostics.append(
            Diagnostic(
                label,
                "todo_template.retention.missing",
                "exactly one Retention declaration exists",
                "none found",
            )
        )
    elif len(retention_hits) > 1:
        diagnostics.append(
            Diagnostic(
                label,
                "todo_template.retention.duplicate",
                "exactly one Retention declaration exists",
                f"found {len(retention_hits)} declarations",
            )
        )

    # Recently Completed section line range.
    rc_start = None
    rc_end = len(lines)
    for lineno, name in headings:
        if name == "Recently Completed":
            rc_start = lineno
            break
    if rc_start is not None:
        for lineno, name in headings:
            if lineno > rc_start:
                rc_end = lineno - 1
                break

    for lineno, raw_value in retention_hits:
        in_rc = rc_start is not None and rc_start <= lineno <= rc_end
        if not in_rc:
            diagnostics.append(
                Diagnostic(
                    label,
                    "todo_template.retention.placement",
                    "Retention declaration is inside ## Recently Completed",
                    f"line {lineno} is outside Recently Completed",
                )
            )
        if not re.fullmatch(r"[1-9][0-9]*", raw_value):
            detail = f"observed {raw_value!r}"
            if raw_value == "0":
                detail = "observed 0 (N must be >= 1)"
            diagnostics.append(
                Diagnostic(
                    label,
                    "todo_template.retention.value",
                    "Retention value is a positive decimal integer N >= 1",
                    detail,
                )
            )

    return diagnostics


def github_slug(text: str) -> str:
    """Deterministic GitHub-like heading slug."""
    value = unicodedata.normalize("NFKD", text)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = value.replace(" ", "-")
    value = re.sub(r"[^a-z0-9\-]", "", value)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-")


def collect_heading_slugs(text: str) -> set[str]:
    cleaned = strip_fenced_code_blocks(text)
    counts: dict[str, int] = {}
    slugs: set[str] = set()
    for line in cleaned.splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue
        base = github_slug(heading_text(match.group(2)))
        if not base:
            continue
        n = counts.get(base, 0)
        counts[base] = n + 1
        slug = base if n == 0 else f"{base}-{n}"
        slugs.add(slug)
    return slugs


def is_external_or_ignored_url(url: str) -> bool:
    if url.startswith("#"):
        return False
    parsed = urlparse(url)
    if parsed.scheme in ("http", "https", "mailto", "ftp", "ftps", "data"):
        return True
    if parsed.scheme and parsed.scheme not in ("", "file"):
        # Unknown / non-relative schemes are ignored (not checked as repo paths).
        return True
    return False


def extract_markdown_targets(text: str) -> list[str]:
    cleaned = strip_fenced_code_blocks(text)
    targets: list[str] = []

    for match in INLINE_LINK_RE.finditer(cleaned):
        targets.append(match.group(2))
    for match in IMAGE_LINK_RE.finditer(cleaned):
        targets.append(match.group(2))

    definitions: dict[str, str] = {}
    for match in REF_DEF_RE.finditer(cleaned):
        definitions[match.group(1).lower()] = match.group(2)

    for match in REF_LINK_RE.finditer(cleaned):
        label = match.group(1)
        ref = match.group(2) or label
        url = definitions.get(ref.lower())
        if url is not None:
            targets.append(url)

    # Standalone reference definitions are also destinations.
    for url in definitions.values():
        targets.append(url)

    return targets


def validate_relative_markdown_links(root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    root_resolved = root.resolve()

    for path in iter_markdown_files(root):
        label = repo_rel(root, path)
        text = path.read_text(encoding="utf-8")
        targets = extract_markdown_targets(text)
        # Deterministic unique order.
        ordered: list[str] = []
        seen: set[str] = set()
        for target in targets:
            if target not in seen:
                seen.add(target)
                ordered.append(target)

        for raw_target in ordered:
            target = raw_target.strip()
            if not target or is_external_or_ignored_url(target):
                continue

            parsed = urlparse(target)
            raw_path = unquote(parsed.path or "")
            fragment = unquote(parsed.fragment or "")

            if target.startswith("#") or (raw_path == "" and fragment):
                dest_file = path
                fragment_only = True
            else:
                fragment_only = False
                # Reject absolute filesystem paths pretending to be links.
                candidate = (path.parent / raw_path).resolve()
                try:
                    candidate.relative_to(root_resolved)
                except ValueError:
                    diagnostics.append(
                        Diagnostic(
                            label,
                            "links.escape",
                            "relative Markdown links stay inside the repository root",
                            f"target escapes root: {raw_target}",
                        )
                    )
                    continue
                dest_file = candidate

            if not fragment_only:
                if not (dest_file.exists()):
                    diagnostics.append(
                        Diagnostic(
                            label,
                            "links.target",
                            "relative link target exists as a file or directory",
                            f"missing target: {raw_target}",
                        )
                    )
                    continue

            if fragment:
                if dest_file.is_dir():
                    diagnostics.append(
                        Diagnostic(
                            label,
                            "links.fragment",
                            "fragment targets a Markdown file with a matching heading",
                            f"fragment on directory: {raw_target}",
                        )
                    )
                    continue
                if dest_file.suffix.lower() != ".md":
                    # Non-markdown fragment targets are not validated further.
                    continue
                try:
                    dest_text = dest_file.read_text(encoding="utf-8")
                except OSError as exc:
                    diagnostics.append(
                        Diagnostic(
                            label,
                            "links.fragment",
                            "fragment target file is readable",
                            f"could not read {repo_rel(root, dest_file)}: {exc}",
                        )
                    )
                    continue
                slugs = collect_heading_slugs(dest_text)
                if fragment not in slugs:
                    diagnostics.append(
                        Diagnostic(
                            label,
                            "links.fragment",
                            f"heading fragment #{fragment} exists in "
                            f"{repo_rel(root, dest_file)}",
                            f"fragment not found for {raw_target}",
                        )
                    )

    return diagnostics


def validate_repository(root: Path) -> list[Diagnostic]:
    root = root.resolve()
    diagnostics: list[Diagnostic] = []
    diagnostics.extend(validate_skill_md(root))
    diagnostics.extend(validate_runtime_boundary(root))
    diagnostics.extend(validate_primary_templates(root))
    diagnostics.extend(validate_todo_template(root))
    diagnostics.extend(validate_relative_markdown_links(root))
    return sort_diagnostics(diagnostics)


def sort_diagnostics(diagnostics: Iterable[Diagnostic]) -> list[Diagnostic]:
    return sorted(
        diagnostics,
        key=lambda d: (d.file, d.rule, d.expected, d.detail),
    )


def default_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate CSDD repository structural contracts."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=None,
        help="Repository root (default: parent of scripts/)",
    )
    args = parser.parse_args(argv)
    root = Path(args.root).resolve() if args.root else default_root()

    diagnostics = validate_repository(root)
    for item in diagnostics:
        print(item.format())

    if diagnostics:
        print(
            f"Validation failed with {len(diagnostics)} diagnostic(s).",
            file=sys.stderr,
        )
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
