# Agent compatibility matrix

This document is the **canonical public compatibility matrix** for the CSDD
skill. Compatibility is **dimensional**, not a single boolean for a harness.

A harness appearing in the Agent Skills installer does **not** prove CSDD
compatibility. CI success and structural validation do **not** prove discovery
or behavioral compatibility. Positive cells must stay narrow and evidence-backed.

## Status vocabulary

| Status | Meaning |
| --- | --- |
| **verified** | Reproducible evidence exists for the **exact** claim shown in that cell, with **complete required provenance** (harness, surface, versions/refs, date, skill source mode, profile mode, evidence link). |
| **partial** | Positive evidence exists, but a relevant part of the claim is missing, required provenance fields are `not recorded`, the environment does not cover the full claim, or the end-to-end chain is incomplete. Missing fields must stay visible. |
| **unsupported** | A **reproducible failure under valid preconditions**, or a **documented absence of support**. Transient errors and incorrect setup are not enough. Not a synonym for “unknown” or for **not tested**. |
| **not tested** | Insufficient evidence. Not equivalent to failure or to unsupported. |

Do **not** read “verified” as a synonym of a vague “supported.” Do **not** treat
this matrix as proof that CSDD “works everywhere” or is “fully compatible.”

Use `not recorded` when a provenance field was never captured. Use
`not user-visible` only when the harness genuinely does not expose the value.

## What the matrix measures

Keep these layers distinct:

| Layer | What it answers |
| --- | --- |
| **Distribution** | Can the skill be installed to a path the harness can consume? |
| **Discovery** | Does a **new** session see / load the skill? |
| **Behavior** | Does explicit (or, if tested, implicit) use follow CSDD workflows? |

Installer availability ≠ discovery. Discovery ≠ correct protocol behavior.

## Initial matrix (Codex and Cursor)

Initial support set for v0.2.1 readiness: **Codex** and **Cursor** only. Other
harnesses are out of scope here unless listed as **not tested** with no
positive claim.

Cells below reflect the **T-027 manual campaign** (4/4 PASS) plus retained
inherited **partial** install/discovery evidence. Procedure, frozen fixtures,
and evaluation rules live in
[`evidence/t-027-compatibility.md`](../evidence/t-027-compatibility.md).

Shared campaign provenance (behavioral cells): CSDD ref
`d2640af0641addb656cc8110fb445cae1b4694d3`; skills CLI `1.5.20`; skill source
mode `development checkout`; profile mode `live user profile`; OS Windows 11;
model `not recorded`; Cursor `3.12.30`; Codex harness version
`not user-visible`.

### Shared provenance keys

Record separately:

- **Skill source mode:** `CLI-managed copy` | `development checkout` |
  `project-local`
- **Profile mode:** `live user profile` | `isolated profile`

For every **verified** or **partial** cell, follow the linked evidence for:

- harness and exact surface;
- harness version (`not user-visible` only if truly unavailable; otherwise a
  real value or `not recorded`);
- installer / `skills` CLI version when relevant (or `not recorded`);
- exact CSDD ref when available (or `not recorded`);
- date;
- OS / environment (or `not recorded`);
- skill source mode and profile mode (or `not recorded`);
- evidence record path.

**verified** requires that set to be complete for the claim. **partial** may
cite historical evidence with gaps, but those gaps must remain explicit and are
part of the reason for partial.

### Codex

| Dimension | Status | Evidence / notes |
| --- | --- | --- |
| Global install via Agent Skills CLI | **partial** | H1 shows the CLI `add`/`update`/`remove` lifecycle for `--agent codex cursor` into a shared managed path inside an **isolated profile** ([T-025 §A](../evidence/t-025-installation.md#a-evidence-executed-in-this-environment)). Agents were not linked there. T-027 campaign did **not** prove CLI-managed copy → live Codex consumption → remains partial. |
| Discovery in a new session | **partial** | New Codex Desktop session discovered `csdd` from a **development checkout** on the live global path ([T-025 §C.2](../evidence/t-025-installation.md#c-manual-smoke-tests-new-sessions)). Skill source mode: development checkout; profile mode: live user profile. Client version: `not recorded`. Not CLI-managed → discovery. |
| Explicit invocation | **verified** | Frozen `$csdd` / `$csdd init` succeeded under T-027 provenance: [Fixture A](../evals/runs/t027-02-codex-fixture-a.md), [Fixture B](../evals/runs/t027-04-codex-fixture-b.md). |
| Implicit activation | **not tested** | Frozen implicit prompt not executed. Not a release blocker. |
| `/csdd init` or equivalent natural request | **verified** | Fixture A Absent-only `$csdd init` PASS ([t027-02](../evals/runs/t027-02-codex-fixture-a.md)). |
| Representative workflow in an existing CSDD-aware project | **verified** | Fixture B T-901 workflow PASS ([t027-04](../evals/runs/t027-04-codex-fixture-b.md)). |
| Relevant Git / branch / worktree visibility | **verified** | Fixture A Git root/status and Fixture B feature branch + parallel `main` worktree observed ([t027-02](../evals/runs/t027-02-codex-fixture-a.md), [t027-04](../evals/runs/t027-04-codex-fixture-b.md)). |

### Cursor

| Dimension | Status | Evidence / notes |
| --- | --- | --- |
| Global install via Agent Skills CLI | **partial** | Same H1 isolated-profile CLI lifecycle as Codex ([T-025 §A](../evidence/t-025-installation.md#a-evidence-executed-in-this-environment)). Shared path mechanics proven; live Cursor path/link consumption of a CLI-managed copy not shown (dev checkout occupies the live global path). T-027 campaign did not close that gap → partial. |
| Discovery in a new session | **partial** | New Cursor session discovered `csdd` from a **development checkout** on the live global path ([T-025 §C.1](../evidence/t-025-installation.md#c-manual-smoke-tests-new-sessions)). Client `3.12.30`. Skill source mode: development checkout; profile mode: live user profile. Not CLI-managed → discovery. |
| Explicit invocation | **verified** | Frozen `/csdd` / `/csdd init` succeeded under T-027 provenance: [Fixture A](../evals/runs/t027-01-cursor-fixture-a.md), [Fixture B](../evals/runs/t027-03-cursor-fixture-b.md). |
| Implicit activation | **not tested** | Frozen implicit prompt not executed. Not a release blocker. |
| `/csdd init` or equivalent natural request | **verified** | Fixture A Absent-only `/csdd init` PASS ([t027-01](../evals/runs/t027-01-cursor-fixture-a.md)). |
| Representative workflow in an existing CSDD-aware project | **verified** | Fixture B T-901 workflow PASS ([t027-03](../evals/runs/t027-03-cursor-fixture-b.md)). |
| Relevant Git / branch / worktree visibility | **verified** | Fixture A Git root/status and Fixture B feature branch + parallel `main` worktree observed ([t027-01](../evals/runs/t027-01-cursor-fixture-a.md), [t027-03](../evals/runs/t027-03-cursor-fixture-b.md)). |

## How to read the matrix

- One cell = one dimension for one harness. Do not collapse install, discovery,
  and behavior into a single badge.
- **verified** always means “this exact claim has a durable record with complete
  required provenance,” not “always works for all users.”
- **partial** is still useful: it shows positive signal and names the gap
  (usually CLI-managed continuity, live path/link consumption, current CSDD
  ref, or missing recorded fields).
- **not tested** must stay visible. It is neither red nor green.
- **unsupported** requires reproducible failure under valid preconditions or
  documented absence of support; absence of tests is **not tested**.

## Limitations

- The live developer path `~/.agents/skills/csdd` may be a Git development
  checkout. CLI mutations against that path were intentionally skipped in
  T-025; see the safety rules in the evidence contract.
- Isolated-profile CLI success proves installer mechanics. It does not prove
  that Codex or Cursor consumed that managed copy.
- Structural validation / CI ([T-026](https://github.com/ValenFelizia/csdd/issues/21))
  checks repository contracts offline. Green CI is not harness compatibility.
- Historical eval runs (pre-campaign) use older skill commits and incomplete
  provenance; the T-027 campaign records supersede them for behavioral cells
  marked **verified** above.
- Implicit activation is optional evidence for v0.2.1 and is not a release
  blocker when left **not tested**.
- Model strings were `not recorded` for campaign subject sessions; Codex
  harness version was `not user-visible`.

## Reverification triggers

Re-run or narrow the affected cells when any of the following occur:

- material change to `SKILL.md`, `references/`, or `assets/templates/`;
- change to the installation mechanism or managed install path;
- material Agent Skills CLI / installer update;
- material harness update or change to how it loads skills;
- a new release candidate after the tests that back current cells;
- a reproducible report that contradicts a current **verified** or **partial**
  claim.

Record new runs in [`evidence/t-027-compatibility.md`](../evidence/t-027-compatibility.md)
(or linked run sheets) and update this matrix in the same coherent change.

## Related documents

- Installation guide: [`docs/installation.md`](installation.md)
- Installation evidence: [`evidence/t-025-installation.md`](../evidence/t-025-installation.md)
- Compatibility test contract: [`evidence/t-027-compatibility.md`](../evidence/t-027-compatibility.md)
- Structural validation note: repository `.csdd/specs.md` (Structural validation)
  and CI workflows — mechanical only
