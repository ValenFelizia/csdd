# T-027 — Compatibility evidence contract

Issue: [#24](https://github.com/ValenFelizia/csdd/issues/24)  
Branch: `evidence/t-027-compatibility-matrix`  
Task: T-027  
Checkpoint: **documentary** — procedure frozen; new manual campaign **not**
executed in this change.

Public matrix: [`docs/compatibility.md`](../docs/compatibility.md)

This file is the durable test contract and evidence register for T-027. It
freezes how tests must be run and how inherited evidence may be cited **before**
any new Cursor/Codex campaign for T-027.

## Status vocabulary (authoritative for T-027)

| Status | Use when |
| --- | --- |
| **verified** | The exact dimensional claim was observed under recorded provenance, with a durable evidence link. |
| **partial** | Positive observation exists, but the chain is incomplete (for example development-checkout discovery without clean-install continuity, or an older skill ref than current `main`). |
| **unsupported** | Negative evidence shows the dimension fails or is not supported. |
| **not tested** | No adequate evidence yet. Never treat as failure. |

A single successful prompt supports only the narrow claim actually observed. It
does not prove universal reliability.

---

## Evidencia heredada

Inventory only. Do **not** reinterpret isolated install + development-checkout
discovery as clean managed-install discovery.

### H1 — T-025 CLI lifecycle (isolated HOME)

| Field | Value |
| --- | --- |
| Record | [`evidence/t-025-installation.md`](t-025-installation.md) §A |
| Date | 2026-07-22 |
| OS | Windows 11 Pro (`NT 10.0.26200.0`), AMD64 |
| `skills` CLI | `1.5.20` |
| CSDD ref installed | `061ca5eab78c20207397b51bd5f360a6196073ac` (`main` at test time) |
| Source mode | **isolated HOME** clean CLI install (not the live user profile) |
| Scope | global (`-g`), `--agent codex cursor` |

Observations (as recorded):

- `add` / reinstall / `update` / `remove` cycle passed;
- managed path under the isolated HOME received the full snapshot minus `.git`;
- project `.csdd/` sentinels preserved across install/remove;
- isolated listing reported agents not linked (no real Codex/Cursor profiles in
  that HOME).

**Does not show:** clean install on the developer profile; session discovery
after clean install; protocol behavior.

### H2 — T-025 Cursor new-session discovery (development checkout)

| Field | Value |
| --- | --- |
| Record | [`evidence/t-025-installation.md`](t-025-installation.md) §C.1 |
| Date | 2026-07-22 |
| Harness / surface | Cursor |
| Client version | `3.12.30` (`63a2996a10d9e476b6c28e951dd7691d9c0cf480`, x64) |
| CSDD ref | `7594550a2dbf83d3690b7b7e7de9c2c6682d6599` |
| Source mode | **development checkout** at `~/.agents/skills/csdd` |
| Result | pass (skill discovered / loadable) |

**Does not show:** discovery from a clean CLI-managed install on the same
profile.

### H3 — T-025 Codex new-session discovery (development checkout)

| Field | Value |
| --- | --- |
| Record | [`evidence/t-025-installation.md`](t-025-installation.md) §C.2 |
| Date | 2026-07-22 |
| Harness / surface | Codex Desktop |
| Client version | not user-visible / not reported |
| CSDD ref | `7594550a2dbf83d3690b7b7e7de9c2c6682d6599` |
| Source mode | **development checkout** at `~/.agents/skills/csdd` |
| Result | pass (skill loaded); sandbox path observation noted |

**Does not show:** clean-install → discovery continuity.

### H4 — Scenario 08 Run A (Cursor, explicit `/csdd init`)

| Field | Value |
| --- | --- |
| Record | [`evals/runs/08-existing-repo-init-a.md`](../evals/runs/08-existing-repo-init-a.md) |
| Contract | [`evals/scenarios/08-existing-repo-init.md`](../evals/scenarios/08-existing-repo-init.md) |
| Date | 2026-07-21 |
| Harness | Cursor |
| Model | Grok 4.5 |
| Invocation | explicit `/csdd init` |
| Skill commit | `65b7ef68a8b7887a843ec535c490aa79b1e10f9e` |
| Result | PASS |

Historical evaluation evidence only. **Not** a new T-027 run. Does not upgrade
source mode to clean install.

### H5 — Prior Git / branch / worktree-relevant scenarios (Cursor)

| Record | Relevance |
| --- | --- |
| [`evals/runs/06-git-divergence-a.md`](../evals/runs/06-git-divergence-a.md) | Explicit `/csdd` resume; Target refresh; branch/worktree collision stop; CSDD-aware fixture |
| [`evals/runs/04-stale-claim.md`](../evals/runs/04-stale-claim.md) | Git / worktree inspection as part of stale-claim reconciliation |
| [`evals/runs/07-landing-todo-handoff-a.md`](../evals/runs/07-landing-todo-handoff-a.md) | Landing truthfulness vs branch reachability (supporting, not a substitute for H4/H5 primary claims) |

All are Cursor (or Cursor-evaluated) historical runs with older skill commits.
Codex parity is **not** implied.

### Honest chain gaps (do not close on paper)

| Desired chain | Inherited status |
| --- | --- |
| Clean CLI install on live profile → new-session discovery (Cursor) | **not demonstrated** (dev checkout occupies global path; CLI mutations skipped) |
| Clean CLI install on live profile → new-session discovery (Codex) | **not demonstrated** (same) |
| Isolated HOME install → harness discovery | **not demonstrated** (no real agent profiles in isolated HOME) |
| Implicit activation (either harness) | **not tested** |
| Codex explicit init / existing-project workflow / Git visibility | **not tested** |

---

## Procedimiento T-027

Repeatable procedure for **each** harness in the initial set (Codex, Cursor).
Execute only after this checkpoint is reviewed. Separate **new sessions** when
prior conversational state could contaminate discovery or activation results.

### Record template (required fields)

Copy one block per run (or per dimension group that shares one session only when
contamination is impossible):

```text
Date:
OS / environment:
Harness / surface:
Harness version (or "not user-visible"):
Model (only if visible and relevant):
skills CLI version:
CSDD ref (exact):
Scope (global / project):
Source mode: clean CLI install | development checkout | isolated profile | other:
Fixture commit / reproducible hash:
Exact invocation / prompt:
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
   - use a **truly isolated** profile/HOME that the harness can consume, **or**
     record honestly that clean-install → discovery continuity was **not
     tested**.
3. Do **not** automatically move, replace, or back up the development checkout
   as part of this checkpoint or campaign.

### Session separation rules

- Discovery: new session after the skill tree under test is in place.
- Explicit invocation: may follow discovery in a session that already loaded the
  skill, but record that the session was not discovery-fresh if relevant.
- Implicit activation: **only** in a new session whose prompt:
  - does not name CSDD;
  - does not name the skill;
  - does not use `/csdd` or `$csdd`;
  - does not reveal the expected outcome.
  If not run that way → leave **not tested**. Not a release blocker.

### Dimensions to score (same set for Codex and Cursor)

1. Global install via Agent Skills CLI  
2. Discovery in a new session  
3. Explicit invocation  
4. Implicit activation  
5. `/csdd init` or equivalent natural request  
6. Representative workflow in an existing CSDD-aware project  
7. Relevant Git / branch / worktree visibility  

Score each dimension independently with the vocabulary above.

---

## Fixtures and frozen prompts

Two reusable fixtures. Conceptual reuse of Scenario 08 is allowed for **A**; any
new T-027 run must record the harness, versions, and CSDD ref **actually**
tested. Do not present historical Cursor Run A as a new T-027 execution.

### Fixture A — Initialization

**Shape**

- small clean Git repository;
- unambiguous repository root;
- `.csdd` path Absent;
- some explicit durable evidence plus at least one clear uncertainty / non-authoritative idea;
- no unrelated dirty state.

**Invocation (explicit; identical wording across harnesses when practical)**

```text
/csdd init

Initialize CSDD for this existing repository using only evidence that the
project actually supports. Preserve uncertainty and leave gaps when durable
intent is not established. Do not modify product code, commit, push, or create
any additional workflow.
```

**Expected observable outcome**

- creates only the four primary documents under `.csdd/`;
- does not modify product files or Git history;
- does not invent tasks, decisions, or unsupported durable truth;
- TODO remains operationally empty with six canonical headings and `Retention: 5`;
- handoff has no active entry; no archive.

**Observable rubric (pass / partial / fail for this dimension)**

| Check | Pass signal |
| --- | --- |
| Absent-only write set | Exactly `specs.md`, `todo.md`, `decisions.md`, `handoff.md` |
| Product / Git safety | No tracked file changes; no commit/push |
| Evidence discipline | Specs/decisions only from authoritative fixture evidence |
| Uncertainty preserved | Non-authoritative ideas not promoted |
| TODO / handoff | Canonical empty operational state |

Maps primarily to dimension **`/csdd init`**. May also inform **explicit
invocation** when `/csdd init` is the invocation form.

### Fixture B — Existing-project workflow

**Shape**

- small reproducible CSDD-aware repository;
- one ordinary bounded task with a verifiable requirement;
- observable branch and worktree topology (local bare `origin` acceptable; no
  network or private data);
- prompt kept identical across harnesses when practical.

**Suggested explicit prompt (freeze at run time if adjusted; record exact text)**

```text
/csdd

Using CSDD, complete the pending bounded task recorded in .csdd/todo.md.
Reconcile against current Git and project state before editing. Stay inside
the claimed scope. Verify the result. Reconcile the TODO honestly. Do not
commit, push, merge, or rewrite existing branches.
```

**Must observe**

- discovery/application of CSDD (skill loaded; state read proportionally);
- proportional hydration;
- correct use of specs/todo (and decisions/handoff only as needed);
- bounded edit;
- verification;
- honest TODO reconciliation;
- shell/harness ability to identify relevant branch, repository root, and
  worktrees.

**Observable rubric**

| Check | Pass signal |
| --- | --- |
| CSDD applied | Relevant `.csdd/` read; claim respected or reconciled |
| Edit bound | Diff limited to claimed / justified paths |
| Verification | Command or check result recorded |
| TODO honesty | State matches repository reality |
| Git visibility | Branch, root, and relevant worktrees identified when material |

Maps to **representative workflow** and **Git / branch / worktree visibility**.
May also inform **explicit invocation**.

### Implicit activation (optional; not release blocker)

Only if a truly isolated new session is available. Example shape (do not reveal
CSDD in the prompt):

```text
This repository has project-state documents under .csdd/. Finish the single
pending task there, verify it, and leave the task list accurate. Do not
commit or push.
```

If the session cannot be isolated, or the prompt would have to name the skill →
leave the dimension **not tested**.

---

## Evaluation rule per dimension

| Dimension | verified | partial | unsupported | not tested |
| --- | --- | --- | --- | --- |
| Global install | Clean (or intentionally isolated) CLI install for the harness target with recorded CLI version and CSDD ref | CLI install proven but harness linking / live-profile continuity missing | Install fails for the claimed command/path | Not run |
| Discovery | New session loads skill from the **same source mode** claimed (prefer clean install when claiming clean install) | Discovery works only from development checkout or otherwise incomplete chain | Session cannot load skill when install is correct | Not run |
| Explicit invocation | Explicit `/csdd` / `$csdd` / equivalent succeeds for a recorded prompt | Succeeds historically or under incomplete provenance | Explicit invoke fails with durable negative evidence | Not run |
| Implicit activation | Isolated new-session prompt without naming CSDD/skill/`/csdd`/`$csdd` activates correctly | Ambiguous activation or contaminated session | Clear non-activation with correct install/discovery | Default until isolated test exists |
| `/csdd init` | Fixture A passes under recorded harness/ref | Positive init evidence with provenance gaps (older ref, non-clean source) | Init violates Absent-only / invents state / mutates product | Not run |
| Existing workflow | Fixture B passes under recorded harness/ref | Historical or incomplete-provenance positive run | Durable failure on ordinary workflow | Not run |
| Git / worktree visibility | Material branch/root/worktree facts observed when required | Partial inspection evidence or historical-only | Cannot obtain required Git facts when available | Not run |

Update [`docs/compatibility.md`](../docs/compatibility.md) in the same patch as
new run records. Never mark **verified** without provenance fields filled.

---

## Structural validation relationship

T-026 offline validation and CI success may be cited only as **repository
structural** health. They must not be used to mark any harness behavior cell
**verified**.

---

## Campaign log (T-027 new runs)

_No new manual Cursor or Codex runs in this documentary checkpoint._

| Run ID | Date | Harness | Source mode | Dimensions touched | Result summary | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | pending | — |
