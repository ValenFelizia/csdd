# Installing the CSDD skill

This guide covers installation of the **CSDD Agent Skill** for Codex, Cursor,
and Google Antigravity. It does **not** create project `.csdd/` state.

Installing the skill and adopting CSDD in a repository are separate steps:

1. Install the skill globally or into one workspace (this document).
2. In a repository, run [`/csdd init`](../SKILL.md#csdd-init-fast-path) (or an
   equivalent explicit request) to create that project's `.csdd/` documents.

Skill install, update, and remove operate on a skill copy. They do **not**
delete or modify any project's `.csdd/` directory.

## Prerequisites

- Node.js with `npx` available (evidence recorded with Node `v24.15.0` and
  npm/`npx` `11.13.0`).
- Network access so `npx` can fetch the `skills` CLI and clone
  `ValenFelizia/csdd` from GitHub.
- Codex, Cursor, and/or Antigravity as the agent targets you intend to use.

Codex and Cursor global claims are backed by T-025. Antigravity claims are
limited to the project-local distribution evidence recorded in T-032; actual
Antigravity discovery and behavior remain not tested.

## Codex and Cursor: global install

```bash
npx skills add ValenFelizia/csdd --skill csdd --agent codex cursor -g -y
```

This command:

- installs skill `csdd` from the GitHub repository `ValenFelizia/csdd`;
- targets Codex and Cursor explicitly (avoids installing to additional agents
  that `skills` might otherwise detect);
- writes a shared global copy under `~/.agents/skills/csdd`;
- skips interactive confirmation (`-y`).

On Windows, `~` is the current user profile (for example
`C:\Users\<you>\.agents\skills\csdd`).

Codex and Cursor both use `~/.agents/skills` as a universal skills location.
The CLI places one shared copy there; you do not need a separate clone for each
agent.

## Antigravity: workspace install

From the target workspace root, run:

```bash
npx skills add ValenFelizia/csdd --skill csdd --agent antigravity -y
```

This installs a project-local copy under:

```text
<workspace-root>/.agents/skills/csdd/
```

Antigravity documents `.agents/skills/<skill-folder>/` as its workspace skill
location. Agent Skills CLI `1.5.20` was also verified to install the CSDD
repository snapshot at that exact path. This proves the distribution step; it
does not prove that a new Antigravity session discovered or followed the skill.

### Global Antigravity caveat

Antigravity currently documents its global skill location as:

```text
~/.gemini/config/skills/csdd/
```

Agent Skills CLI `1.5.20` encodes a different Antigravity global destination
(`~/.gemini/antigravity/skills`). Do **not** add `-g` to the Antigravity command
above while that mismatch remains.

If you need a global manual fallback, place a CSDD repository checkout or copy
at the documented Antigravity path:

```bash
git clone https://github.com/ValenFelizia/csdd.git ~/.gemini/config/skills/csdd
```

This fallback is not managed by the Agent Skills CLI. Update it with Git and
remove it manually. Do not confuse the global skill directory with a project's
`.csdd/` state.

### What gets installed

The CLI clones the repository and copies the versioned snapshot recursively,
excluding `.git`. There is currently no `.skillignore` (or equivalent filter)
applied by the CLI.

**Runtime required by CSDD:**

- `SKILL.md`
- `references/**`
- `assets/templates/**`

Additional repository files (evals, field reports, dogfooding notes, adapters,
project `.csdd/` from the skill repo itself, and so on) may also be present in
the installed copy. They are **distributed** but not required for skill
execution. Do not restructure the repository or invent a custom installer solely
to shrink that copy.

## Verify Codex or Cursor installation

```bash
npx skills list -g
```

Confirm that `csdd` appears with path `~/.agents/skills/csdd` (shown by the CLI
as `~\.agents\skills\csdd` on Windows).

Also confirm required files exist on disk:

```text
~/.agents/skills/csdd/SKILL.md
~/.agents/skills/csdd/references/
~/.agents/skills/csdd/assets/templates/
```

`skills list` proves the CLI registered the skill. Discovery inside a **new**
Codex or Cursor session is a separate smoke check (restart or open a new
session after install).

## Verify Antigravity workspace installation

From the same workspace root:

```bash
npx skills list --agent antigravity
```

Also confirm the required runtime files exist:

```text
.agents/skills/csdd/SKILL.md
.agents/skills/csdd/references/
.agents/skills/csdd/assets/templates/
```

Then start a new Antigravity session for the workspace and confirm that `csdd`
is discoverable. The file and CLI checks verify installation only; session
discovery remains a separate smoke test.

## Install the skill vs `/csdd init`

| Step | What it does | Where |
| --- | --- | --- |
| `npx skills add ... --agent codex cursor -g` | Makes CSDD globally available to Codex and Cursor | `~/.agents/skills/csdd` |
| `npx skills add ... --agent antigravity` | Makes CSDD available to Antigravity in one workspace | `<workspace>/.agents/skills/csdd` |
| `/csdd init` | Creates four primary documents for one repository | `<project>/.csdd/` |

`/csdd init` never installs the skill. Skill install never initializes a
project. After the skill is installed, open any repository and ask the agent to
initialize CSDD when that repository has no `.csdd/` yet.

## Reinstall

Repeat the canonical install command:

```bash
npx skills add ValenFelizia/csdd --skill csdd --agent codex cursor -g -y
```

Expected behavior: the managed path remains a single `~/.agents/skills/csdd`
directory (no duplicate sibling installs). The copy is replaced from the
current GitHub source.

For an Antigravity workspace, repeat its project-local install command from the
workspace root. CLI `1.5.20` replaces the project copy from the current source.

## Update

```bash
npx skills update csdd -g -y
```

Updates the global `csdd` skill from its recorded source when a newer revision
is available. If the installed copy already matches the source, the CLI reports
that global skills are up to date.

For an Antigravity workspace:

```bash
npx skills update csdd -p -y
```

In T-032 evidence, CLI `1.5.20` updated the project copy successfully, although
it also emitted a non-fatal warning while checking deleted skills.

## Uninstall

```bash
npx skills remove csdd --agent codex cursor -g -y
```

Removes the global skill registration and the managed copy under
`~/.agents/skills/csdd` for the targeted agents. Project `.csdd/` directories
are left untouched.

For an Antigravity workspace:

```bash
npx skills remove csdd --agent antigravity -y
```

CLI `1.5.20` cleared the project's `skills-lock.json` entry but left the
universal `.agents/skills/csdd` copy on disk in the T-032 run. If it remains,
delete that exact directory manually. Never delete the separate project
`.csdd/` directory when uninstalling the skill.

## Discovery in a new session

After install:

1. Start a **new** session in each installed target (Codex, Cursor, or
   Antigravity) so it reloads skills.
2. Confirm the skill is offered or attachable as `csdd`.
3. Optionally invoke CSDD on a repository that already has `.csdd/`, or run
   `/csdd init` on a repository that does not.

Session discovery is client-side. Passing `skills list` is necessary but not
sufficient proof that a given client session has loaded the skill.

## Troubleshooting

- **`npx` / network errors:** Ensure Node.js is on `PATH` and GitHub is
  reachable. Retry after connectivity is restored.
- **Skill missing from `skills list -g`:** Re-run the canonical install
  command, then list again. Confirm you used `-g`.
- **Antigravity workspace skill missing:** Run the Antigravity install from the
  workspace root without `-g`, then confirm `.agents/skills/csdd/SKILL.md`.
- **Files missing under `~/.agents/skills/csdd`:** Reinstall. Do not manually
  patch an incomplete tree as a substitute for the CLI.
- **Agent session does not see `csdd`:** Verify the files on disk, then open a
  new session. Confirm the intended `--agent` target and scope.
- **Wrong directory edited:** Before any `skills add` / `update` / `remove`,
  resolve the exact path that would be modified. On a machine used for CSDD
  development, `~/.agents/skills/csdd` may already be a Git checkout. Do not
  run those CLI operations against a live development checkout unless you
  intend to replace it.

## Do not edit the installed copy by hand

Treat CLI-installed skill copies as managed. Manual edits are overwritten by
reinstall or update and are easy to confuse with a development checkout. The
manual Antigravity global fallback is the exception: it must be maintained as a
normal Git checkout or copied directory.

Contribute changes in a Git clone of `ValenFelizia/csdd`, then install or
update from the published source (or an explicitly documented local path used
only for pre-publish verification).

## Project `.csdd/` safety

Skill install, reinstall, update, and remove affect only skill locations and
installer metadata. They do **not** create, delete, or rewrite `.csdd/` inside
user projects.

## Evidence and limitations

Reproducible CLI evidence for T-025 lives in
[`evidence/t-025-installation.md`](../evidence/t-025-installation.md). Claims
for Antigravity live in
[`evidence/t-032-antigravity.md`](../evidence/t-032-antigravity.md). Claims in
this guide should not exceed those records and the official documentation they
cite.
