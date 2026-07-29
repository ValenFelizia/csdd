# T-032 Antigravity installation evidence

- Date: 2026-07-29
- Issue: [#34](https://github.com/ValenFelizia/csdd/issues/34)
- Scope: Antigravity skill distribution only
- Protocol semantics changed: no

## Result

The Agent Skills CLI can install CSDD from `ValenFelizia/csdd` into
`.agents/skills/csdd` for an Antigravity workspace with one command. That path
matches Antigravity's current official workspace skill location.

This record does **not** prove Antigravity discovery or CSDD behavior. No
Antigravity session was run.

## Sources inspected

- [Google Antigravity Skills documentation](https://antigravity.google/docs/skills):
  workspace skills live at `.agents/skills/<skill-folder>/`; global skills live
  at `~/.gemini/config/skills/<skill-folder>/`; a skill uses `SKILL.md` with
  YAML frontmatter.
- Agent Skills CLI `1.5.20` installed from the npm package `skills`.
- The installed CLI's agent registry and packaged README identify
  `antigravity` as a target, use `.agents/skills` for project scope, and encode
  `~/.gemini/antigravity/skills` for global scope.

## Environment

| Field | Value |
| --- | --- |
| OS | Linux `6.12.13`, x86_64 |
| Node | `v24.14.0` |
| npm | `11.9.0` |
| Agent Skills CLI | `1.5.20` |
| Source | `ValenFelizia/csdd` from GitHub `main` |
| Exact CSDD commit | `not recorded` by the install output or `skills-lock.json` |
| Skill source mode | project-local CLI-managed copy |
| Profile mode | isolated workspace |
| Antigravity version | `not recorded` |
| Model | `not recorded` |

## Project-local install run

Precondition: an empty Git repository used as the target workspace.

Command:

```bash
npx skills@1.5.20 add ValenFelizia/csdd \
  --skill csdd \
  --agent antigravity \
  -y
```

Observed installer summary:

```text
./.agents/skills/csdd
  copy → Antigravity
```

Postconditions:

- `.agents/skills/csdd/SKILL.md` existed;
- `.agents/skills/csdd/references/protocol.md` existed;
- `.agents/skills/csdd/assets/templates/` existed;
- `skills-lock.json` recorded source `ValenFelizia/csdd`, source type `github`,
  skill path `SKILL.md`, and computed hash
  `54eed7515979d73d7c9ecce8837d3f15098c561078713b2b38706faac1f75886`;
- the complete versioned repository snapshot was copied, consistent with the
  T-025 distribution behavior.

The CLI also printed `codex Agent detected` before the explicit Antigravity
installation summary. The requested destination and final summary were still
Antigravity, but the unrelated detection line is retained here as an observed
CLI quirk.

Status: **partial** distribution evidence. The exact source commit was not
retained and an Antigravity session did not consume the installed copy.

## Update run

Command:

```bash
npx skills@1.5.20 update csdd -p -y
```

Result: exit code `0`; the CLI reported `Updated csdd` and `Updated 1 skill(s)`.
It also emitted a non-fatal `Failed to check for deleted skills from
ValenFelizia/csdd` message.

## Remove run

Command:

```bash
npx skills@1.5.20 remove csdd --agent antigravity -y
```

Result: exit code `0`; the CLI removed the `csdd` entry from
`skills-lock.json`, but `.agents/skills/csdd` remained on disk and was still
listed by path discovery. The current uninstall instructions therefore require
deleting that exact workspace skill directory if it remains. Project `.csdd/`
state was absent and unaffected.

## Global path mismatch

The current contracts disagree:

| Source | Antigravity global skill path |
| --- | --- |
| Google Antigravity documentation | `~/.gemini/config/skills/<skill-folder>/` |
| Agent Skills CLI `1.5.20` | `~/.gemini/antigravity/skills/<skill-folder>/` |

The Agent Skills CLI global Antigravity flow was not executed. A target listed
by an installer is not evidence that the harness consumes the installed path.
Until the paths align or an end-to-end run proves compatibility:

- the canonical one-command path is project-local and omits `-g`;
- global CLI installation is **not tested** and not recommended;
- a manual checkout or copy under Antigravity's documented global path may be
  used as an explicit fallback.

## Behavioral dimensions

| Dimension | Status |
| --- | --- |
| Project install via Agent Skills CLI | partial |
| Global install via Agent Skills CLI | not tested |
| Discovery in a new session | not tested |
| Explicit invocation | not tested |
| Implicit activation | not tested |
| `/csdd init` or equivalent | not tested |
| Existing CSDD-aware workflow | not tested |
| Git / branch / worktree visibility | not tested |

## Reverification triggers

Re-run this evidence when:

- Antigravity changes its documented workspace or global skill paths;
- the Agent Skills CLI changes its Antigravity destinations or removal
  behavior;
- an actual Antigravity session can test discovery and CSDD workflows;
- a release candidate changes CSDD runtime files or installation structure.
