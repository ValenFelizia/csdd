"""Lock the task-surface phrase fence and the retired init wording.

The skill is the runtime. These checks fail when the lines an agent copies
drift, or when the old default comes back in a live document.
"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FENCE_LINES = (
    "/csdd todo enable local board",
    "csdd todo enable local board",
    "/csdd todo enable external stub",
    "csdd todo enable external stub",
)

FENCE_OWNERS = (
    "references/document-contracts.md",
    "SKILL.md",
    "README.md",
)

# Released notes at 0.2.1 and earlier keep the old sentences on purpose.
CHANGELOG_CUT = "## [0.2.1]"

LIVE_TEXTS = (
    "SKILL.md",
    "README.md",
    "changelog.md",
    "docs/installation.md",
    "docs/architecture.md",
    "references/document-contracts.md",
    "references/protocol.md",
    "references/read-only-workflows.md",
    "references/poteto-composition.md",
    "references/migration-v0.1-to-v0.2.md",
    "evals/README.md",
)

RETIRED = (
    "missing `todo.md` is partial",
    "missing `todo.md` remains partial",
    "Missing `.csdd/todo.md` is **partial**",
    "local board by default",
    "By default `todo.md` is the six-heading",
    "Omitting `todo.md` is not a mode",
    "Omitting the `todo.md` file is",
    "never a mode declaration",
    "never a mode switch",
    "Default projects keep the local board",
    "Creates four primary documents",
    "Created four primary documents",
    "default init and local six-heading",
    "four docs plus valid",
)


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def _text_blocks(source: str) -> list[str]:
    blocks: list[str] = []
    marker = "```text\n"
    start = 0
    while True:
        opened = source.find(marker, start)
        if opened < 0:
            return blocks
        body_at = opened + len(marker)
        closed = source.find("```", body_at)
        if closed < 0:
            return blocks
        body = source[body_at:closed]
        if body.endswith("\n"):
            body = body[:-1]
        blocks.append(body)
        start = closed + 3


def _fence_bodies(source: str) -> list[str]:
    expected = "\n".join(FENCE_LINES)
    return [body for body in _text_blocks(source) if body == expected]


def _live_text(relative: str) -> str:
    text = _read(relative)
    if relative == "changelog.md":
        cut = text.find(CHANGELOG_CUT)
        if cut >= 0:
            text = text[:cut]
    return text


class TaskSurfaceContractTest(unittest.TestCase):
    def test_phrase_fence_is_the_same_block(self) -> None:
        bodies = {name: _fence_bodies(_read(name)) for name in FENCE_OWNERS}
        for name, found in bodies.items():
            self.assertEqual(
                found,
                ["\n".join(FENCE_LINES)],
                f"{name} must contain the fence once, as its own text block",
            )
        self.assertEqual(
            len({tuple(found) for found in bodies.values()}),
            1,
        )

    def test_retired_sentences_stay_out_of_live_docs(self) -> None:
        scenario_dir = ROOT / "evals" / "scenarios"
        relatives = list(LIVE_TEXTS)
        relatives.extend(
            f"evals/scenarios/{path.name}" for path in sorted(scenario_dir.glob("*.md"))
        )
        hits: list[str] = []
        for relative in relatives:
            text = _live_text(relative)
            for sentence in RETIRED:
                if sentence in text:
                    hits.append(f"{relative}: {sentence}")
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()
