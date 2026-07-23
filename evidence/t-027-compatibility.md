# T-027 — Compatibility evidence contract

Issue: [#24](https://github.com/ValenFelizia/csdd/issues/24)
Branch: `evidence/t-027-compatibility-matrix`
Task: T-027
Checkpoint: **documentary correction** — fixtures, prompts, and evaluation
rules corrected; new manual campaign still **not** executed.

Public matrix: [`docs/compatibility.md`](../docs/compatibility.md)

This file is the durable test contract and evidence register for T-027. It
freezes how tests must be run and how inherited evidence may be cited **before**
any new Cursor/Codex campaign for T-027.

## Status vocabulary (authoritative for T-027)

| Status | Use when |
| --- | --- |
| **verified** | The exact dimensional claim was observed under **complete required provenance**, with a durable evidence link. |
| **partial** | Positive observation exists, but the chain is incomplete, required provenance fields are missing (`not recorded`), the environment does not cover the full claim, or the skill/profile modes do not match the claimed end-to-end story. |
| **unsupported** | A **reproducible failure under valid preconditions**, or a **documented absence of support**. A transient error or incorrect setup is not enough. |
| **not tested** | No adequate evidence yet. Never treat as failure. Never treat as unsupported. |

A single successful prompt supports only the narrow claim actually observed. It
does not prove universal reliability.

### Provenance modes (record separately)

| Field | Allowed values |
| --- | --- |
| **Skill source mode** | `CLI-managed copy` \| `development checkout` \| `project-local` |
| **Profile mode** | `live user profile` \| `isolated profile` |

Do not collapse these into one “source mode” string. Do not write
`not user-visible` when the value was simply never captured — use
`not recorded`.

### Provenance completeness

- **verified:** every required provenance field for that dimension must be
  filled with a real value or an explicit `not user-visible` only when the
  harness genuinely does not expose it.
- **partial:** historical or incomplete evidence may remain, but every missing
  field must stay visible as `not recorded` (or an equivalent explicit gap)
  and must be part of why the cell is partial.

---

## Evidencia heredada

Inventory only. Do **not** reinterpret isolated install + development-checkout
discovery as clean managed-install discovery.

### H1 — T-025 CLI lifecycle (isolated profile)

| Field | Value |
| --- | --- |
| Record | [`evidence/t-025-installation.md`](t-025-installation.md) §A |
| Date | 2026-07-22 |
| OS | Windows 11 Pro (`NT 10.0.26200.0`), AMD64 |
| `skills` CLI | `1.5.20` |
| CSDD ref installed | `061ca5eab78c20207397b51bd5f360a6196073ac` (`main` at test time) |
| Skill source mode | `CLI-managed copy` (created inside isolated HOME) |
| Profile mode | `isolated profile` (temporary HOME; no real Codex/Cursor agent profiles) |
| Scope | global (`-g`), `--agent codex cursor` |

Observations (as recorded):

- `add` / reinstall / `update` / `remove` cycle passed;
- managed path under the isolated HOME received the full snapshot minus `.git`;
- project `.csdd/` sentinels preserved across install/remove;
- isolated listing reported agents not linked (no real Codex/Cursor profiles in
  that HOME).

**What H1 demonstrates:** the canonical Agent Skills CLI command can install,
reinstall, update, and remove a shared global `csdd` tree for the
`--agent codex cursor` target set inside an isolated profile, and can preserve
project `.csdd/` across those operations.

**What H1 does not demonstrate:** that a CLI-managed copy landed on the
path/link actually consumed by a live Codex or Cursor session; live-profile
linking; session discovery; protocol behavior. For Global install cells, H1
alone remains **partial**.

### H2 — T-025 Cursor new-session discovery (development checkout)

| Field | Value |
| --- | --- |
| Record | [`evidence/t-025-installation.md`](t-025-installation.md) §C.1 |
| Date | 2026-07-22 |
| OS | Windows 11 Pro (`NT 10.0.26200.0`), AMD64 (same machine as T-025 §A) |
| Harness / surface | Cursor |
| Client version | `3.12.30` (`63a2996a10d9e476b6c28e951dd7691d9c0cf480`, x64) |
| Installer / `skills` CLI | `not recorded` for this smoke (discovery-only) |
| CSDD ref | `7594550a2dbf83d3690b7b7e7de9c2c6682d6599` |
| Skill source mode | `development checkout` at `~/.agents/skills/csdd` |
| Profile mode | `live user profile` |
| Result | pass (skill discovered / loadable) |

**Does not show:** discovery from a CLI-managed copy on the same profile.

### H3 — T-025 Codex new-session discovery (development checkout)

| Field | Value |
| --- | --- |
| Record | [`evidence/t-025-installation.md`](t-025-installation.md) §C.2 |
| Date | 2026-07-22 |
| OS | Windows 11 Pro (`NT 10.0.26200.0`), AMD64 (same machine as T-025 §A) |
| Harness / surface | Codex Desktop |
| Client version | `not recorded` |
| Installer / `skills` CLI | `not recorded` for this smoke (discovery-only) |
| CSDD ref | `7594550a2dbf83d3690b7b7e7de9c2c6682d6599` |
| Skill source mode | `development checkout` at `~/.agents/skills/csdd` |
| Profile mode | `live user profile` |
| Result | pass (skill loaded); sandbox path observation noted |

**Does not show:** clean CLI-managed → discovery continuity.

### H4 — Scenario 08 Run A (Cursor, explicit `/csdd init`)

| Field | Value |
| --- | --- |
| Record | [`evals/runs/08-existing-repo-init-a.md`](../evals/runs/08-existing-repo-init-a.md) |
| Contract | [`evals/scenarios/08-existing-repo-init.md`](../evals/scenarios/08-existing-repo-init.md) |
| Date | 2026-07-21 |
| OS | `not recorded` |
| Harness | Cursor |
| Client version | `not recorded` |
| Installer / `skills` CLI | `not recorded` |
| Model | Grok 4.5 |
| Invocation | explicit `/csdd init` |
| Skill commit | `65b7ef68a8b7887a843ec535c490aa79b1e10f9e` |
| Skill source mode | `not recorded` |
| Profile mode | `not recorded` |
| Result | PASS |

Historical evaluation evidence only. **Not** a new T-027 run. Missing
provenance fields are why related matrix cells stay **partial**.

### H5 — Prior Git / branch / worktree-relevant scenarios (Cursor)

Primary supporting records:

| Record | Relevance | Missing provenance (explicit) |
| --- | --- | --- |
| [`evals/runs/06-git-divergence-a.md`](../evals/runs/06-git-divergence-a.md) | Explicit `/csdd` resume; Target refresh; branch/worktree collision stop; CSDD-aware fixture | OS `not recorded`; client version `not recorded`; installer `not recorded`; skill source mode `not recorded`; profile mode `not recorded` |
| [`evals/runs/04-stale-claim.md`](../evals/runs/04-stale-claim.md) | Git / worktree inspection as part of stale-claim reconciliation | same class of gaps as above unless a field is stated in that run |
| [`evals/runs/07-landing-todo-handoff-a.md`](../evals/runs/07-landing-todo-handoff-a.md) | Landing truthfulness vs branch reachability (supporting only) | same class of gaps |

Common recorded fields where present: harness Cursor (or Cursor-evaluated),
model Grok 4.5, date 2026-07-21 (scenario 06/07/08 family), older skill commit
`65b7ef68a8b7887a843ec535c490aa79b1e10f9e` for 06/08. Codex parity is **not**
implied.

### Honest chain gaps (do not close on paper)

| Desired chain | Inherited status |
| --- | --- |
| CLI-managed copy on live profile → path/link consumed by Cursor | **not demonstrated** |
| CLI-managed copy on live profile → path/link consumed by Codex | **not demonstrated** |
| Isolated-profile CLI install → harness discovery | **not demonstrated** (no real agent profiles in isolated HOME) |
| Implicit activation (either harness) | **not tested** |
| Codex explicit init / existing-project workflow / Git visibility | **not tested** |

---

## Procedimiento T-027

Repeatable procedure for **each** harness in the initial set (Codex, Cursor).
Execute only after this corrected checkpoint is reviewed. Separate **new
sessions** when prior conversational state could contaminate discovery or
activation results.

### Record template (required fields)

```text
Date:
OS / environment:
Harness / surface:
Harness version (real value, "not user-visible", or "not recorded"):
Model (only if visible and relevant):
skills CLI version:
CSDD ref (exact):
Scope (global / project):
Skill source mode: CLI-managed copy | development checkout | project-local
Profile mode: live user profile | isolated profile
Fixture id / version:
Fixture BASE commit / tree hash:
Exact invocation / prompt (must match a frozen variant below):
Expected status:
Observed behavior (factual, no chain-of-thought):
Result by dimension:
Limitations:
Modifications produced (paths only; no private project content):
Evidence path / attachment:
```

Do **not** collect private chain-of-thought or full transcripts. Do **not** store
private data or content from real user projects.

### Development-checkout safety (mandatory)

The live global path may be:

```text
C:\Users\Valen\.agents\skills\csdd
```

Before any `skills add` / `update` / `remove`:

1. Resolve the exact filesystem target that would be mutated.
2. If it is a Git checkout or contains user development work:
   - do **not** overwrite it;
   - do **not** delete it;
   - do **not** run installer mutations against that profile;
   - use a **truly isolated** profile that the harness can consume, **or**
     record honestly that CLI-managed → discovery continuity was **not
     tested**.
3. Do **not** automatically move, replace, or back up the development checkout
   as part of this checkpoint or campaign.

### Session separation rules

- Discovery: new session after the skill tree under test is in place.
- Explicit invocation: may follow discovery in a session that already loaded the
  skill, but record that the session was not discovery-fresh if relevant.
- Implicit activation: **only** in a new session using the frozen implicit
  prompt below (no naming CSDD / skill / `/csdd` / `$csdd`; no expected-outcome
  spoilers). If not run that way → leave **not tested**. Not a release blocker.

### Dimensions to score (same set and order for Codex and Cursor)

1. Global install via Agent Skills CLI
2. Discovery in a new session
3. Explicit invocation
4. Implicit activation
5. `/csdd init` or equivalent natural request
6. Representative workflow in an existing CSDD-aware project
7. Relevant Git / branch / worktree visibility

Score each dimension independently with the vocabulary above.

### Shared materialization rule (mandatory)

1. Materialize each fixture **once** from this contract (same machine/session is
   fine).
2. Record `BASE` commit and `git rev-parse HEAD^{tree}`.
3. Clone that exact repository (or worktree clones from the same `BASE`) for
   **Codex** and **Cursor** subjects.
4. Do **not** independently invent “an equivalent fixture” per harness.

---

## Fixtures and frozen prompts

Historical Scenario 08 / 06 runs are **not** T-027 executions. T-027 campaigns
must use the fixtures frozen below.

### Fixture A — `t027-a-catalog-init` / version `v1`

Derived from Scenario 08 properties, but fully specified here so both harnesses
share one materialization.

#### Identity

| Field | Value |
| --- | --- |
| Fixture id | `t027-a-catalog-init` |
| Version | `v1` |
| Purpose | Absent-only `/csdd init` (or Codex `$csdd` init variant) |
| Dimensions | `/csdd init`; may also inform explicit invocation |

#### Initial file manifest (exact)

```text
README.md
docs/architecture.md
src/__init__.py
src/catalog_cli.py
tests/test_catalog_cli.py
fixtures/catalog.json
```

No `.csdd/` path of any kind. No package manifest, CI, hooks, or project
instructions.

#### Deterministic file contents

`README.md`:

```text
# Catalog CLI

Offline catalog reader for local JSON data.

## Accepted requirements

1. The CLI MUST list catalog item names from a local JSON file.
2. The CLI MUST accept a `--path` argument pointing at the catalog JSON file.
3. The CLI MUST exit successfully when the catalog file is valid.
4. Catalog items MUST include `id`, `name`, and `category` fields.
5. The default catalog path MUST be `fixtures/catalog.json` when `--path` is omitted.

## Constraints

- The tool MUST work offline.
- The tool MUST NOT require network access.

## Non-authoritative notes

CSV export may be explored someday.
```

`docs/architecture.md`:

```text
# Architecture

## Accepted decision — whole-document load

The Catalog CLI loads the entire catalog JSON document into memory before
listing items.

### Rationale

The catalogs used by this tool are small local fixtures. Whole-document load
keeps the implementation simple and makes listing deterministic.

### Consequences

Very large catalogs are out of scope for the current tool.
```

`src/__init__.py`:

```text
# Catalog CLI package
```

`src/catalog_cli.py`:

```text
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_PATH = Path("fixtures/catalog.json")


def load_catalog(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("catalog must be a list")
    return data


def list_names(path: Path) -> list[str]:
    return [str(item["name"]) for item in load_catalog(path)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="catalog-cli")
    parser.add_argument("--path", type=Path, default=DEFAULT_PATH)
    args = parser.parse_args(argv)
    for name in list_names(args.path):
        print(name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

`tests/test_catalog_cli.py`:

```text
import unittest
from pathlib import Path

from src.catalog_cli import list_names

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "fixtures" / "catalog.json"


class CatalogCliTests(unittest.TestCase):
    def test_list_names(self) -> None:
        names = list_names(CATALOG)
        self.assertEqual(names, ["Alpha", "Beta"])


if __name__ == "__main__":
    unittest.main()
```

`fixtures/catalog.json`:

```text
[
  {"id": "a1", "name": "Alpha", "category": "tools"},
  {"id": "b2", "name": "Beta", "category": "books"}
]
```

#### Authoritative evidence vs uncertainty

| Kind | Content |
| --- | --- |
| Authoritative durable requirements | The five numbered README requirements |
| Authoritative constraints | Offline / no-network README constraints |
| Authoritative decision | Whole-document load in `docs/architecture.md` |
| Non-authoritative uncertainty | “CSV export may be explored someday.” |
| Non-durable code/test facts | Exact print formatting, internal function names, exit-code nuances beyond README |

#### Git / CSDD / topology (initial)

| Field | Value |
| --- | --- |
| Git | single commit on `main`; clean worktree |
| `origin` | local bare repository; `origin/main` == `main` == `BASE` |
| Worktrees | one subject worktree only |
| CSDD | Absent (no `.csdd` path) |
| Branches | `main` only |

#### Materialization recipe (deterministic)

Run in an empty parent directory. Use LF line endings and the exact file bodies
above (no BOM).

```text
mkdir t027-a-catalog-init-v1
cd t027-a-catalog-init-v1
git init -b main
# write the six files with the exact contents above
git add README.md docs/architecture.md src/__init__.py src/catalog_cli.py tests/test_catalog_cli.py fixtures/catalog.json
git -c user.name='t027' -c user.email='t027@example.invalid' commit -m "t027-a-catalog-init v1 baseline"
git rev-parse HEAD > ../t027-a-BASE.txt
git rev-parse HEAD^{tree} > ../t027-a-TREE.txt
git clone --bare . ../t027-a-catalog-init-v1.git
git remote add origin ../t027-a-catalog-init-v1.git
git fetch origin
```

Then clone once per harness subject from the same bare repo / same `BASE`:

```text
git clone ../t027-a-catalog-init-v1.git t027-a-subject-cursor
git clone ../t027-a-catalog-init-v1.git t027-a-subject-codex
```

Record `BASE` and tree hash in the run sheet. Re-materialization must yield the
same tree hash when contents and path set match.

#### Verification command (fixture integrity; evaluator or preflight)

```text
py -3.13 -m unittest discover -s tests -v
```

Expected: `Ran 1 test` … `OK`.

#### Paths that may be modified by the subject

Only:

```text
.csdd/specs.md
.csdd/todo.md
.csdd/decisions.md
.csdd/handoff.md
```

#### Expected conceptual diff

- tracked product files: unchanged vs `BASE`
- Git history / refs: unchanged
- untracked: `.csdd/` with exactly the four primaries
- `.csdd/archive/`: absent

#### Expected final TODO

Operationally empty: six canonical H2 headings in order, `Retention: 5`, zero
tasks. Handoff: no active entry.

#### Frozen prompts — Fixture A (mandatory)

Body (identical for both harnesses):

```text
Initialize CSDD for this existing repository using only evidence that the
project actually supports. Preserve uncertainty and leave gaps when durable
intent is not established. Do not modify product code, commit, push, or create
any additional workflow.
```

Allowed harness variants (choose exactly one; do not invent others after
seeing results):

**Cursor**

```text
/csdd init

Initialize CSDD for this existing repository using only evidence that the
project actually supports. Preserve uncertainty and leave gaps when durable
intent is not established. Do not modify product code, commit, push, or create
any additional workflow.
```

**Codex**

```text
$csdd init

Initialize CSDD for this existing repository using only evidence that the
project actually supports. Preserve uncertainty and leave gaps when durable
intent is not established. Do not modify product code, commit, push, or create
any additional workflow.
```

#### Observable rubric

| Check | Pass signal |
| --- | --- |
| Absent-only write set | Exactly the four primaries under `.csdd/` |
| Product / Git safety | No tracked file changes; no commit/push |
| Evidence discipline | Specs/decisions only from authoritative fixture evidence |
| Uncertainty preserved | CSV note not promoted |
| TODO / handoff | Canonical empty operational state |

---

### Fixture B — `t027-b-echo-loud` / version `v1`

Concrete ordinary existing-project workflow with one bounded task, a failing
test, and observable Git/worktree topology.

#### Identity

| Field | Value |
| --- | --- |
| Fixture id | `t027-b-echo-loud` |
| Version | `v1` |
| Purpose | Complete one pending task in a CSDD-aware repo |
| Dimensions | representative workflow; Git/branch/worktree visibility; may inform explicit invocation |

#### Initial file manifest (exact)

```text
README.md
src/echo_cli.py
tests/test_echo_cli.py
.csdd/specs.md
.csdd/todo.md
.csdd/decisions.md
.csdd/handoff.md
```

#### Deterministic product contents

`README.md`:

```text
# Echo CLI

Tiny offline echo utility used for CSDD compatibility fixture B.
```

`src/echo_cli.py` (incomplete — missing `--loud`):

```text
from __future__ import annotations

import argparse


def format_message(message: str, loud: bool = False) -> str:
    return message


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="echo-cli")
    parser.add_argument("message")
    parser.add_argument("--loud", action="store_true")
    args = parser.parse_args(argv)
    print(format_message(args.message, loud=args.loud))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

`tests/test_echo_cli.py`:

```text
import unittest

from src.echo_cli import format_message


class EchoCliTests(unittest.TestCase):
    def test_default_echo(self) -> None:
        self.assertEqual(format_message("hi"), "hi")

    def test_loud_uppercases(self) -> None:
        self.assertEqual(format_message("hi", loud=True), "HI")


if __name__ == "__main__":
    unittest.main()
```

#### Deterministic CSDD contents

`.csdd/specs.md`:

```text
# Specifications

## Project Summary

Echo CLI is a tiny offline message printer.

## Requirements

- The CLI MUST print the provided message unchanged by default.
- The CLI MUST uppercase the message when `--loud` is passed.
```

`.csdd/todo.md`:

```text
# TODO

## In Progress

- [ ] T-901 — Add --loud uppercase support
  - Owner: valen
  - Agent: fixture-agent-t901
  - Scope: `src/echo_cli.py`, `tests/test_echo_cli.py`
  - Target: main
  - Base: REPLACE_WITH_BASE_SHA
  - Updated: 2026-07-22
  - Note: Default echo works. `--loud` must uppercase the message and satisfy tests.

## Ready to Land

## Blocked

## Pending

## Deferred

## Recently Completed

Retention: 5
```

`.csdd/decisions.md`:

```text
# Decisions

No accepted decisions yet.
```

`.csdd/handoff.md`:

```text
# Handoff

> No active handoff.
```

After the first commit creates `BASE`, rewrite `.csdd/todo.md` so
`Base: REPLACE_WITH_BASE_SHA` becomes `Base: <actual BASE sha>` in a second
commit on the feature branch only (see topology). Record both commits.

#### Accepted requirement under test

> The CLI MUST uppercase the message when `--loud` is passed.

#### Exact task and Scope

| Field | Value |
| --- | --- |
| Task | `T-901 — Add --loud uppercase support` |
| Scope | `src/echo_cli.py`, `tests/test_echo_cli.py` |
| Owner | `valen` (must be preserved) |

#### Git / worktree topology (material)

1. Create bare `origin`.
2. Commit product + CSDD skeleton on `main` at `BASE0` with placeholder Base
   line temporarily allowed only before feature commit; preferred sequence:
   - Commit 1 on `main`: product files + CSDD with `Base: pending` replaced
     immediately after computing sha via the recipe below.
3. Practical frozen sequence:

```text
mkdir t027-b-echo-loud-v1
cd t027-b-echo-loud-v1
git init -b main
# write README.md, src/echo_cli.py, tests/test_echo_cli.py, and the four .csdd files
# In todo.md set: Base: 0000000000000000000000000000000000000000
git add README.md src/echo_cli.py tests/test_echo_cli.py .csdd
git -c user.name='t027' -c user.email='t027@example.invalid' commit -m "t027-b-echo-loud v1 product baseline"
BASE0=$(git rev-parse HEAD)
# set Base: $BASE0 in .csdd/todo.md
git add .csdd/todo.md
git -c user.name='t027' -c user.email='t027@example.invalid' commit -m "t027-b-echo-loud v1 set Base"
BASE=$(git rev-parse HEAD)
git rev-parse HEAD > ../t027-b-BASE.txt
git rev-parse HEAD^{tree} > ../t027-b-TREE.txt
git clone --bare . ../t027-b-echo-loud-v1.git
git remote add origin ../t027-b-echo-loud-v1.git
git push -u origin main
git branch feature/t-901-loud-flag
git checkout feature/t-901-loud-flag
```

4. Create a second worktree on `main` for visibility (shared by materialization,
   then cloned per harness as needed):

```text
git worktree add ../t027-b-main-worktree main
```

5. Per harness, clone the bare repo and recreate the same refs/worktree shape
   from the recorded `BASE` / branch tips — or clone the materialization
   directory after `git worktree list` shows:

```text
<repo>  <FEATURE_HEAD or BASE on feature branch> [feature/t-901-loud-flag]
<repo-main-worktree>  <BASE> [main]
```

Subject start state for each harness:

| Field | Value |
| --- | --- |
| Branch | `feature/t-901-loud-flag` @ same commit as `main` / `BASE` (no unique feature commits required before the run) |
| `origin/main` | `BASE` |
| Second worktree | `main` @ `BASE` (observable via `git worktree list`) |
| Dirty state | clean |
| Tests before fix | `test_loud_uppercases` FAIL; `test_default_echo` OK |

#### Verification command

```text
py -3.13 -m unittest discover -s tests -v
```

| When | Expected |
| --- | --- |
| Pre-run | 1 failure (`test_loud_uppercases`), 1 success |
| Post-run success | `Ran 2 tests` … `OK` |

#### Paths that may be modified by the subject

Allowed:

```text
src/echo_cli.py
tests/test_echo_cli.py
.csdd/todo.md
```

Optionally `.csdd/handoff.md` only if a real boundary + concrete resumption risk
exists (ordinary successful completion should not need it).

Forbidden without justification: `README.md`, `.csdd/specs.md`,
`.csdd/decisions.md`, Git refs rewrite, commit/push/merge.

#### Expected conceptual diff

- `src/echo_cli.py`: `format_message` returns `message.upper()` when `loud` is
  true; otherwise unchanged.
- `tests/test_echo_cli.py`: may stay unchanged if already correct; edits allowed
  only inside Scope.
- `.csdd/todo.md`: T-901 completed, Scope released or omitted per template
  norms, moved under Recently Completed (or equivalent truthful completion).
- No commit/push by the subject.

#### Expected final TODO

- T-901 no longer In Progress.
- Completion reflected under Recently Completed (or project-truthful equivalent)
  with `Scope: released` or claim metadata removed.
- Owner `valen` not silently replaced.
- No invented extra tasks.

#### Frozen prompts — Fixture B (mandatory)

Body (identical):

```text
Using CSDD, complete the pending bounded task recorded in .csdd/todo.md.
Reconcile against current Git and project state before editing. Stay inside
the claimed scope. Verify the result. Reconcile the TODO honestly. Do not
commit, push, merge, or rewrite existing branches.
```

**Cursor**

```text
/csdd

Using CSDD, complete the pending bounded task recorded in .csdd/todo.md.
Reconcile against current Git and project state before editing. Stay inside
the claimed scope. Verify the result. Reconcile the TODO honestly. Do not
commit, push, merge, or rewrite existing branches.
```

**Codex**

```text
$csdd

Using CSDD, complete the pending bounded task recorded in .csdd/todo.md.
Reconcile against current Git and project state before editing. Stay inside
the claimed scope. Verify the result. Reconcile the TODO honestly. Do not
commit, push, merge, or rewrite existing branches.
```

Do not adjust these prompts after observing results.

#### Observable rubric

| Check | Pass signal |
| --- | --- |
| CSDD applied | Relevant `.csdd/` read; T-901 claim respected or reconciled |
| Edit bound | Diff limited to allowed paths |
| Verification | `py -3.13 -m unittest discover -s tests -v` → OK |
| TODO honesty | T-901 completed/released; matches repo reality |
| Git visibility | Subject identifies current branch, repo root, and the extra `main` worktree when material |

---

### Implicit activation (optional; not release blocker)

Use Fixture B subject start state. New isolated session only. Exact prompt
(same for Codex and Cursor; no harness prefix):

```text
This repository has project-state documents under .csdd/. Finish the single
pending task there, verify it, and leave the task list accurate. Do not
commit or push.
```

If the session cannot be isolated, or a different prompt would be required →
leave **not tested**. Do not edit this text after observing results.

---

## Evaluation rule per dimension

| Dimension | verified | partial | unsupported | not tested |
| --- | --- | --- | --- | --- |
| Global install | CLI-managed install lands on the **path/link actually consumed** by the exact harness under test, with CLI version, CSDD ref, skill source mode `CLI-managed copy`, and profile mode recorded | Positive CLI lifecycle evidence without harness path/link consumption (for example H1 isolated profile with agents not linked), or other incomplete chain | Reproducible install failure under valid preconditions for the claimed command/path, or documented absence of support | Not run |
| Discovery | New session loads skill from the **same skill source mode and profile mode** claimed | Discovery works only from development checkout, or provenance incomplete | Reproducible non-discovery under valid install/discovery preconditions | Not run |
| Explicit invocation | Frozen explicit variant succeeds under complete provenance | Historical/incomplete-provenance positive run | Reproducible explicit-invoke failure under valid preconditions | Not run |
| Implicit activation | Frozen implicit prompt in an isolated new session activates correctly | Ambiguous activation or contaminated session | Reproducible non-activation under valid install/discovery preconditions | Default until isolated test exists |
| `/csdd init` | Fixture A passes under recorded harness/ref/provenance | Positive init evidence with provenance gaps | Reproducible Absent-only / safety failure under valid preconditions | Not run |
| Existing workflow | Fixture B passes under recorded harness/ref/provenance | Historical or incomplete-provenance positive run | Reproducible ordinary-workflow failure under valid preconditions | Not run |
| Git / worktree visibility | Material branch/root/worktree facts observed when required | Partial or historical-only inspection evidence | Reproducible inability to obtain required Git facts when available under valid preconditions | Not run |

Update [`docs/compatibility.md`](../docs/compatibility.md) in the same patch as
new run records. Never mark **verified** without complete required provenance.

---

## Structural validation relationship

T-026 offline validation and CI success may be cited only as **repository
structural** health. They must not be used to mark any harness behavior cell
**verified**.

---

## Campaign log (T-027 new runs)

_No new manual Cursor or Codex runs in this documentary correction._

| Run ID | Date | Harness | Skill source mode | Profile mode | Dimensions touched | Result summary | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | — | pending | — |
