# T-033 Claude Code distribution evidence

- Date: 2026-10-11
- Scope: Claude Code skill distribution and frontmatter/layout checks only
- Protocol semantics changed: no (optional `license: MIT` frontmatter field only)

## Result

The Agent Skills CLI can install CSDD from `ValenFelizia/csdd` into Claude
Code's documented personal and project skill locations with one command each.
A separate offline layout check confirms that copy and symlink installs at
those paths expose parseable `SKILL.md` frontmatter and the T-025 runtime
files.

This record does **not** prove Claude Code discovery or CSDD behavior. No
Claude Code session was run.

## Sources inspected

- [Claude Code skills documentation](https://code.claude.com/docs/en/skills):
  personal skills at `~/.claude/skills/<skill>/SKILL.md`; project skills at
  `.claude/skills/<skill>/SKILL.md`; symlinked skill folders are supported;
  frontmatter `name` and `description` are the primary discovery fields
  (`name` optional in Claude Code, defaults to directory name; recommended
  `description`).
- [Agent Skills overview (Anthropic)](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview):
  required `name` and `description` for the Agent Skills format.
- [Agent Skills specification](https://agentskills.io/specification):
  `name` / `description` required; optional `license`, `compatibility`,
  `metadata`, `allowed-tools`.
- Agent Skills CLI `1.5.18` from the npm package `skills`.

## Environment

| Field | Value |
| --- | --- |
| OS | Linux `6.12.94+`, x86_64 |
| Node | `v22.14.0` |
| npm | `10.9.9` |
| Agent Skills CLI | `1.5.18` |
| Source | `ValenFelizia/csdd` from GitHub (CLI clone) and local checkout for layout |
| Exact CSDD commit (CLI clone) | `not recorded` by the install output |
| Local checkout commit (layout check) | `30c4d8f6123c6120ce51f2a59135908912ca1764` |
| Skill source mode | CLI-managed copy; separate manual copy / symlink |
| Profile mode | isolated `HOME` / workspace |
| Claude Code version | `not recorded` (CLI not invoked) |
| Model | `not recorded` |

## Frontmatter check

Observed `SKILL.md` frontmatter (after the optional `license` addition in this
change):

```yaml
name: csdd
description: Apply Collaborative Spec-Driven Development as a lightweight coordination and durable project-state protocol. Use when a repository contains canonical `.csdd/` project-state documents, making it CSDD-aware, when the user or project instructions explicitly require CSDD, or when the user explicitly requests `/csdd doctor` or `/csdd status`.
license: MIT
```

Checks:

- `name` is `csdd` (lowercase, ≤64 chars, charset OK);
- `description` length `340` (non-empty, ≤1024; states what and when);
- `license` is `MIT`, matching the repository [`LICENSE`](../LICENSE) file
  title (`MIT License`);
- directory name `csdd` matches `name` when installed under
  `…/skills/csdd/`.

## Bare package add

Command:

```bash
npx --yes skills add ValenFelizia/csdd -y
```

Observed (ANSI stripped; isolated project directory):

```text
Source: https://github.com/ValenFelizia/csdd.git
Repository cloned
Found 1 skill
Skill: csdd
Installation Summary
  ./.agents/skills/csdd
    copy → Cursor, Amp, Antigravity, Antigravity CLI, Cline +12 more
Installed 1 skill
  ✓ csdd (copied)
    → ./.agents/skills/csdd
EXIT: 0
skills version: 1.5.18
```

Status: package install **works**. Prefer explicit `--agent` targeting so the
destination harness is intentional.

## Personal CLI install

Precondition: empty isolated `HOME`.

Command:

```bash
npx --yes skills add ValenFelizia/csdd --skill csdd --agent claude-code -g -y
```

Observed summary:

```text
Installation Summary
  ~/.agents/skills/csdd
    copy → Claude Code
Installed 1 skill
  ✓ csdd (copied)
    → ~/.claude/skills/csdd
EXIT: 0
```

Postconditions under the isolated `HOME`:

- `~/.claude/skills/csdd/SKILL.md` existed;
- `npx skills list -g --agent claude-code` listed
  `csdd ~/.claude/skills/csdd Agents: Claude Code`.

Status: **partial** distribution evidence (no Claude Code session).

## Project CLI install

Precondition: empty isolated workspace directory.

Command:

```bash
npx --yes skills add ValenFelizia/csdd --skill csdd --agent claude-code -y
```

Observed summary:

```text
Installation Summary
  ./.agents/skills/csdd
    copy → Claude Code
Installed 1 skill
  ✓ csdd (copied)
    → ./.claude/skills/csdd
EXIT: 0
```

Postcondition: `./.claude/skills/csdd/SKILL.md` existed.

Status: **partial** distribution evidence (no Claude Code session).

## Manual layout check

Offline check (no Claude Code binary):

1. Copied the local repository into
   `<tmpdir>/project/.claude/skills/csdd`.
2. Symlinked the local repository to
   `<tmpdir>/user/.claude/skills/csdd`.
3. Parsed each `SKILL.md` frontmatter with the same fence/`key: value` rules
   used by `scripts/validate_repository.py`.

Observed:

```text
## project
skill_md_exists: True
references_exists: True
templates_exists: True
name: csdd
name_ok: True
description_len: 340
description_ok: True
body_nonempty: True
dir_name_matches_name: True
is_symlink: False

## user-symlink
skill_md_exists: True
references_exists: True
templates_exists: True
name: csdd
name_ok: True
description_len: 340
description_ok: True
body_nonempty: True
dir_name_matches_name: True
is_symlink: True
```

Status: **partial** layout evidence. Proves files-in-place and frontmatter
parse for Claude Code-style paths; not session discovery.

## What this does not claim

- Claude Code loaded or offered `/csdd` in a real session;
- implicit activation, `/csdd init`, or any behavioral fixture in Claude Code;
- Cowork / cloud / claude.ai sync surfaces (out of scope for this record);
- that a project `CLAUDE.md` is required (it is not, per Claude Code docs).

## Related documents

- [`docs/installation.md`](../docs/installation.md)
- [`docs/compatibility.md`](../docs/compatibility.md)
- [`SKILL.md`](../SKILL.md)
- [`LICENSE`](../LICENSE)
