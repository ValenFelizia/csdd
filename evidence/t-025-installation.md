# T-025 — Global installation evidence

Issue: [#14](https://github.com/ValenFelizia/csdd/issues/14)  
Branch: `distribution/t-025-global-installation`  
Task: T-025

## Environment

| Field | Value |
| --- | --- |
| Date | 2026-07-22 |
| OS | Microsoft Windows 11 Pro (`NT 10.0.26200.0`), `AMD64` |
| Shell | PowerShell |
| Node.js | `v24.15.0` |
| npm / npx | `11.13.0` |
| `skills` CLI | `1.5.20` (via `npx skills`) |
| Repository remote | `https://github.com/ValenFelizia/csdd.git` |
| `origin/main` at test time | `061ca5eab78c20207397b51bd5f360a6196073ac` |
| Development checkout | `C:\Users\Valen\.agents\skills\csdd` (Git worktree on branch `distribution/t-025-global-installation`) |

### Path preflight (mandatory before CLI mutation)

On the current user profile, global `-g` operations would target:

```text
C:\Users\Valen\.agents\skills\csdd
```

That path **is** the live CSDD development checkout (`Source: local` in
`npx skills list -g`). Therefore **no** `skills add`, `skills update`, or
`skills remove` was executed against the current user profile.

Destructive / clean-install CLI verification used an **isolated temporary
HOME** so the managed path became:

```text
%TEMP%\csdd-t025-iso-<id>\.agents\skills\csdd
```

The development checkout HEAD remained `061ca5e` before and after those runs.

## Canonical command under test

```bash
npx skills add ValenFelizia/csdd --skill csdd --agent codex cursor -g -y
```

Install source for automated runs: GitHub `main` at `061ca5e` (published
tree). This is **not** an install of unpublished branch contents. Pre-publish
branch content was authored in the development checkout and documented
separately from the GitHub install evidence below.

## A. Evidence executed in this environment

### A.1 Read-only discovery on the development profile

Commands:

```bash
npx skills --version
npx skills list -g
```

Results:

- CLI version: `1.5.20`
- `csdd` listed at `~\.agents\skills\csdd`
- Listed source: **`local`** (development checkout), not a clean CLI install
- Agents shown by the CLI for this entry included Codex, Cursor, and other
  detected agents on this machine

Interpretation: this smoke observation discovers a **development checkout
located on the global skills path**, not a clean installation created by the
CLI. It is useful for global discovery during CSDD development, and must not
be reported as a clean-install result.

### A.2 Package listing without install (isolated HOME)

Isolated HOME root example:

```text
C:\Users\Valen\AppData\Local\Temp\csdd-t025-iso-e4260113
```

Command:

```bash
npx --yes skills add ValenFelizia/csdd --skill csdd --list
```

Result: exit `0`. CLI reported source
`https://github.com/ValenFelizia/csdd.git`, found **1** skill named `csdd`.

### A.3 Clean install (isolated HOME)

Preflight managed path (did not exist before install):

```text
C:\Users\Valen\AppData\Local\Temp\csdd-t025-iso-e4260113\.agents\skills\csdd
```

Command:

```bash
npx --yes skills add ValenFelizia/csdd --skill csdd --agent codex cursor -g -y
```

Result: exit `0`.

CLI summary (abridged):

- Installation target: `~\.agents\skills\csdd`
- Mode: `copy → Codex, Cursor`
- Installed: `csdd (copied)` → `~\.agents\skills\csdd`
- `.git` absent from the installed tree

### A.4 Installed file set vs versioned snapshot

Installed file count: **32** files.

Exact relative paths observed after install (and again after reinstall):

```text
.gitignore
changelog.md
LICENSE
README.md
SKILL.md
.csdd/decisions.md
.csdd/handoff.md
.csdd/specs.md
.csdd/todo.md
adapters/codex/AGENTS.snippet.md
assets/templates/decisions.md
assets/templates/handoff.md
assets/templates/specs.md
assets/templates/todo.md
dogfooding/001-trivial-fast-path-cursor-grok.md
evals/README.md
evals/results.md
evals/runs/01-trivial-edit.md
evals/runs/02-session-resume.md
evals/runs/03-overlapping-scopes.md
evals/runs/04-stale-claim.md
evals/runs/05-phase-archive.md
evals/runs/06-git-divergence-a.md
evals/runs/07-landing-todo-handoff-a.md
evals/runs/08-existing-repo-init-a.md
evals/scenarios/06-git-divergence.md
evals/scenarios/07-landing-todo-handoff.md
evals/scenarios/08-existing-repo-init.md
field-reports/001-v0.1-real-world-usage.md
references/document-contracts.md
references/migration-v0.1-to-v0.2.md
references/protocol.md
```

Comparison to `git ls-files` on `061ca5e`: same 32 paths; installed tree has
no `.git`. Conclusion: the CLI distributes the full versioned snapshot minus
`.git`. No filter excludes evals/dogfooding/etc.

**Runtime required by CSDD** (present):

- `SKILL.md`
- `references/**`
- `assets/templates/**`

### A.5 Global list after clean install (isolated HOME)

```bash
npx --yes skills list -g
```

Result: exit `0`. Listed `csdd` at `~\.agents\skills\csdd` with
`Source: ValenFelizia/csdd`. In the isolated HOME (no real Codex/Cursor
profiles), the CLI reported `Agents: not linked`. The install summary still
recorded `copy → Codex, Cursor` into the universal `~/.agents/skills` location.

Limitation: isolated-HOME listing does not prove agent-profile linking on a
fully provisioned developer machine; it does prove the canonical global path
and source registration.

### A.6 Reinstall (isolated HOME)

Repeated:

```bash
npx --yes skills add ValenFelizia/csdd --skill csdd --agent codex cursor -g -y
```

Result: exit `0`. Still a single directory at
`~/.agents/skills/csdd`; file count remained **32**; no duplicate sibling
directories observed.

### A.7 Update (isolated HOME)

```bash
npx --yes skills update csdd -g -y
```

Result: exit `0`. CLI output: checking `ValenFelizia/csdd`, then
`All global skills are up to date` (expected: installed copy already matched
`main` at `061ca5e`).

### A.8 Uninstall (isolated HOME)

```bash
npx --yes skills remove csdd --agent codex cursor -g -y
```

Result: exit `0`. Managed path
`...\.agents\skills\csdd` no longer existed afterward.

### A.9 Project `.csdd/` preservation (isolated HOME)

Created a sample project with sentinel `.csdd/{specs,todo,decisions,handoff}.md`
contents, set isolated HOME, ran global install then remove while cwd was the
sample project.

Result: all four sentinel files unchanged after install and after remove
(`PRESERVED=True`). Skill install/remove did not modify project `.csdd/`.

### A.10 Development checkout integrity

| Checkpoint | HEAD | Notes |
| --- | --- | --- |
| Before isolated CLI runs | `061ca5e` | Branch `distribution/t-025-global-installation` |
| After isolated CLI runs | `061ca5e` | Unchanged; no `skills` mutation against current user profile |

## B. Official documentary backing

Consulted during T-025 (not a substitute for the runs above):

- [vercel-labs/skills README](https://github.com/vercel-labs/skills) — `npx skills add`, `-g`, `--agent`, `--skill`, `-y`, list/update/remove.
- [Installation Methods](https://vercel-labs-skills.mintlify.app/guides/installation-methods) — canonical global copy under `~/.agents/skills/<skill>`; Codex and Cursor listed among agents that use `.agents/skills` natively; symlink vs copy behavior.
- CLI `--help` for `skills` `1.5.20` — option surface matches the documented commands.

Documentary points used in the installation guide:

- Global install writes a user-level skills tree; Codex/Cursor consume
  `~/.agents/skills` as a universal location.
- Prefer explicit `--agent codex cursor` over broad autodetection when only
  those targets are claimed.
- No `.skillignore` / install-time filter is offered by the current CLI.

## C. Manual smoke tests (new sessions)

These smoke tests verify **discovery in a new client session** against the
**development checkout** already present at the global skills path
(`~/.agents/skills/csdd`). They are **not** clean CLI
add/reinstall/update/remove evidence; that lifecycle was exercised separately
in an isolated HOME (section A).

Both runs used CSDD ref `7594550a2dbf83d3690b7b7e7de9c2c6682d6599`, global
scope, source mode: development checkout.

### C.1 Cursor — new session discovery

| Field | Value |
| --- | --- |
| Client version | `3.12.30` (`63a2996a10d9e476b6c28e951dd7691d9c0cf480`, x64) |
| Date | 2026-07-22 |
| CSDD ref | `7594550a2dbf83d3690b7b7e7de9c2c6682d6599` |
| Scope | global |
| Source mode | development checkout at `~/.agents/skills/csdd` |
| Result | **pass** |

Observations:

- Skill discovered at `C:\Users\Valen\.agents\skills\csdd\SKILL.md`.
- Name: `csdd`.
- Main heading: “Collaborative Spec-Driven Development”.
- Checkout HEAD matched the tested CSDD ref.
- Loaded from the user global skills scope, not from the workspace.
- The Study Tracker project was not CSDD-aware (no `.csdd/`).
- Harness listing truncated the description to
  “Apply Collaborative Spec-Driven De...”.
- No load errors or unexpected behavior.

### C.2 Codex — new session discovery

| Field | Value |
| --- | --- |
| Client / surface | Codex Desktop |
| Client version | Not reported by harness |
| Date | 2026-07-22 |
| CSDD ref | `7594550a2dbf83d3690b7b7e7de9c2c6682d6599` |
| Scope | global |
| Source mode | development checkout at `~/.agents/skills/csdd` |
| Result | **pass** |

Observations:

- Skill `csdd` loaded correctly.
- Main heading: “Collaborative Spec-Driven Development”.
- Workspace was not CSDD-aware (`.csdd/` absent).
- The harness shell exposed a sandbox path instead of the configured workspace
  path. Recorded as an environment observation, not a CSDD discovery failure.

## D. Not executed / out of scope here

| Item | Status |
| --- | --- |
| `skills add/update/remove` on current user profile | **Skipped** — would replace or delete the development checkout at `C:\Users\Valen\.agents\skills\csdd` |
| Windows Sandbox / separate Windows user clean profile | Not available in this session (`WindowsSandbox.exe` not found; feature query required elevation) |
| Install of unpublished branch tip from GitHub | Not applicable — T-025 docs not yet on `main` |
| Claiming harnesses beyond Codex and Cursor | Out of scope for T-025 |

## E. Verdict

| Check | Result |
| --- | --- |
| One-command global install (Codex + Cursor) | Pass (isolated HOME, section A) |
| Managed path `~/.agents/skills/csdd` | Pass (isolated HOME) |
| Runtime files present | Pass (isolated HOME) |
| Full snapshot minus `.git` distributed | Pass (isolated HOME) |
| Reinstall without duplicates | Pass (isolated HOME) |
| Update when already current | Pass (isolated HOME) |
| Uninstall removes managed copy | Pass (isolated HOME) |
| Project `.csdd/` preserved | Pass (isolated HOME) |
| Dev checkout not mutated by CLI tests | Pass |
| New Cursor session discovery | Pass (section C.1; development checkout on global path) |
| New Codex session discovery | Pass (section C.2; development checkout on global path) |

Overall: CLI lifecycle evidence (isolated HOME) and new-session discovery
smoke tests (development checkout at the global path, ref `7594550`) are both
recorded as satisfactory. Session discovery here is **not** evidence of a
clean CLI install on the current user profile.
