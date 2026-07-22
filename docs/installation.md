# Installing the CSDD skill

This guide covers global installation of the **CSDD Agent Skill** so Codex
and Cursor can discover it. It does **not** create project `.csdd/` state.

Installing the skill and adopting CSDD in a repository are separate steps:

1. Install the skill globally (this document).
2. In a repository, run [`/csdd init`](../SKILL.md#csdd-init-fast-path) (or an
   equivalent explicit request) to create that project's `.csdd/` documents.

Skill install, update, and remove operate on the managed skill copy under
`~/.agents/skills/csdd`. They do **not** delete or modify any project's
`.csdd/` directory.

## Prerequisites

- Node.js with `npx` available (evidence recorded with Node `v24.15.0` and
  npm/`npx` `11.13.0`).
- Network access so `npx` can fetch the `skills` CLI and clone
  `ValenFelizia/csdd` from GitHub.
- Codex and/or Cursor as the agent targets you intend to use.

Supported claims in this guide are limited to **Codex** and **Cursor** on the
Agent Skills path verified in T-025 evidence. Other harnesses are outside the
current contract even if the CLI can target them.

## Canonical global install

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

## Verify installation

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

## Install the skill vs `/csdd init`

| Step | What it does | Where |
| --- | --- | --- |
| `npx skills add ... -g` | Makes the CSDD skill available to agents | `~/.agents/skills/csdd` |
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

## Update

```bash
npx skills update csdd -g -y
```

Updates the global `csdd` skill from its recorded source when a newer revision
is available. If the installed copy already matches the source, the CLI reports
that global skills are up to date.

## Uninstall

```bash
npx skills remove csdd --agent codex cursor -g -y
```

Removes the global skill registration and the managed copy under
`~/.agents/skills/csdd` for the targeted agents. Project `.csdd/` directories
are left untouched.

## Discovery in a new session

After install:

1. Start a **new** Cursor session and a **new** Codex session (or restart the
   clients so they reload skills).
2. Confirm the skill is offered or attachable as `csdd`.
3. Optionally invoke CSDD on a repository that already has `.csdd/`, or run
   `/csdd init` on a repository that does not.

Session discovery is client-side. Passing `skills list -g` is necessary but not
sufficient proof that a given client session has loaded the skill.

## Troubleshooting

- **`npx` / network errors:** Ensure Node.js is on `PATH` and GitHub is
  reachable. Retry after connectivity is restored.
- **Skill missing from `skills list -g`:** Re-run the canonical install
  command, then list again. Confirm you used `-g`.
- **Files missing under `~/.agents/skills/csdd`:** Reinstall. Do not manually
  patch an incomplete tree as a substitute for the CLI.
- **Agent session does not see `csdd`:** Verify the files on disk, then open a
  new session. Confirm you targeted `codex` and/or `cursor` in the install
  command.
- **Wrong directory edited:** Before any `skills add` / `update` / `remove`,
  resolve the exact path that would be modified. On a machine used for CSDD
  development, `~/.agents/skills/csdd` may already be a Git checkout. Do not
  run those CLI operations against a live development checkout unless you
  intend to replace it.

## Do not edit the installed copy by hand

Treat `~/.agents/skills/csdd` as managed by the Agent Skills CLI. Manual edits
are overwritten by reinstall or update and are easy to confuse with a
development checkout.

Contribute changes in a Git clone of `ValenFelizia/csdd`, then install or
update from the published source (or an explicitly documented local path used
only for pre-publish verification).

## Project `.csdd/` safety

Global skill install, reinstall, update, and remove affect only the managed
skill location (and agent skill registration). They do **not** create, delete,
or rewrite `.csdd/` inside user projects.

## Evidence and limitations

Reproducible CLI evidence for T-025 lives in
[`evidence/t-025-installation.md`](../evidence/t-025-installation.md). Claims
in this guide should not exceed that evidence and the official Agent Skills
documentation it cites.
