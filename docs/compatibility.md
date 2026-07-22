# Agent compatibility matrix

This document is the **canonical public compatibility matrix** for the CSDD
skill. Compatibility is **dimensional**, not a single boolean for a harness.

A harness appearing in the Agent Skills installer does **not** prove CSDD
compatibility. CI success and structural validation do **not** prove discovery
or behavioral compatibility. Positive cells must stay narrow and evidence-backed.

## Status vocabulary

| Status | Meaning |
| --- | --- |
| **verified** | Reproducible evidence exists for the **exact** claim shown in that cell (harness, surface, versions/refs, date, source mode, evidence link). |
| **partial** | Positive evidence exists, but a relevant part of the claim is missing, the environment does not cover the full claim, or the end-to-end chain is incomplete. |
| **unsupported** | Evidence shows the dimension does not work or is not supported. Not a synonym for “unknown.” |
| **not tested** | Insufficient evidence. Not equivalent to failure or to unsupported. |

Do **not** read “verified” as a synonym of a vague “supported.” Do **not** treat
this matrix as proof that CSDD “works everywhere” or is “fully compatible.”

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

Cells below reflect **inherited evidence only** at the T-027 documentary
checkpoint. They are not a new manual campaign. Procedure and evaluation rules
live in [`evidence/t-027-compatibility.md`](../evidence/t-027-compatibility.md).

### Shared provenance keys

When a cell is **verified** or **partial**, follow the linked evidence for:

- harness and exact surface;
- visible harness version, or `not user-visible`;
- installer / `skills` CLI version when relevant;
- exact CSDD ref;
- date;
- OS / environment;
- source mode (`clean CLI install`, `development checkout`, `isolated HOME`, etc.);
- evidence record path.

### Codex

| Dimension | Status | Evidence / notes |
| --- | --- | --- |
| Global install via Agent Skills CLI | **partial** | Isolated-HOME CLI lifecycle with `--agent codex cursor` passed ([T-025 §A](../evidence/t-025-installation.md#a-evidence-executed-in-this-environment)). Shared managed path proven; real Codex profile linking on a clean user install was not exercised (isolated HOME reported agents not linked). |
| Discovery in a new session | **partial** | New Codex Desktop session discovered `csdd` from the **development checkout** on the global path ([T-025 §C.2](../evidence/t-025-installation.md#c-manual-smoke-tests-new-sessions)). Not clean-install → discovery. Client version: not user-visible. |
| Explicit invocation | **not tested** | No Codex record of an explicit `/csdd` / `$csdd` / equivalent workflow run under T-027 provenance. |
| Implicit activation | **not tested** | No isolated new-session prompt that avoids naming CSDD / the skill / `/csdd` / `$csdd`. Not a release blocker. |
| `/csdd init` or equivalent natural request | **not tested** | No Codex init run recorded. Scenario 08 Run A is Cursor-only. |
| Representative workflow in an existing CSDD-aware project | **not tested** | No Codex existing-project workflow run recorded under T-027 dimensions. |
| Relevant Git / branch / worktree visibility | **not tested** | No Codex-specific Git/worktree visibility evidence recorded for this matrix. |

### Cursor

| Dimension | Status | Evidence / notes |
| --- | --- | --- |
| Global install via Agent Skills CLI | **partial** | Same isolated-HOME CLI lifecycle as Codex ([T-025 §A](../evidence/t-025-installation.md#a-evidence-executed-in-this-environment)). Shared path proven; clean user-profile install → Cursor discovery chain not completed (dev checkout occupies the live global path). |
| Discovery in a new session | **partial** | New Cursor session discovered `csdd` from the **development checkout** on the global path ([T-025 §C.1](../evidence/t-025-installation.md#c-manual-smoke-tests-new-sessions)). Client `3.12.30`. Not clean-install → discovery. |
| Explicit invocation | **partial** | Explicit `/csdd` used successfully in Cursor evals (e.g. [Scenario 06 Run A](../evals/runs/06-git-divergence-a.md), skill `65b7ef6`). Narrow historical claim only; not re-run under current `main` / clean install for T-027. |
| Implicit activation | **not tested** | No isolated new-session implicit-activation prompt recorded. Not a release blocker. |
| `/csdd init` or equivalent natural request | **partial** | Explicit `/csdd init` PASS in Cursor ([Scenario 08 Run A](../evals/runs/08-existing-repo-init-a.md), skill `65b7ef6`, 2026-07-21). Historical eval evidence; not a new T-027 run and not clean-install end-to-end. |
| Representative workflow in an existing CSDD-aware project | **partial** | Cursor Scenario 06 Run A exercised Git-aware resume/stop on a CSDD-aware fixture ([run](../evals/runs/06-git-divergence-a.md)). Narrow historical claim; not revalidated for T-027 on current ref / clean install. |
| Relevant Git / branch / worktree visibility | **partial** | Cursor Scenario 06 Run A observed branch/worktree/Target refresh behavior ([run](../evals/runs/06-git-divergence-a.md); also earlier stale-claim Git inspection in [Scenario 04](../evals/runs/04-stale-claim.md)). Does not prove every Git surface or Codex parity. |

## How to read the matrix

- One cell = one dimension for one harness. Do not collapse install, discovery,
  and behavior into a single badge.
- **verified** always means “this exact claim has a durable record,” not
  “always works for all users.”
- **partial** is still useful: it shows positive signal and names the gap
  (usually clean-install continuity, current CSDD ref, or harness version).
- **not tested** must stay visible. It is neither red nor green.
- **unsupported** requires negative evidence; absence of tests is **not tested**.

## Limitations

- The live developer path `~/.agents/skills/csdd` may be a Git development
  checkout. CLI mutations against that path were intentionally skipped in
  T-025; see the safety rules in the evidence contract.
- Isolated HOME proves CLI install/remove mechanics; it does not by itself prove
  Codex/Cursor session discovery after a clean managed install on the same
  profile.
- Structural validation / CI ([T-026](https://github.com/ValenFelizia/csdd/issues/21))
  checks repository contracts offline. Green CI is not harness compatibility.
- Historical eval runs use older skill commits and explicit invocation. They
  must not be presented as a fresh T-027 campaign.
- Implicit activation is optional evidence for v0.2.1 and is not a release
  blocker when left **not tested**.

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
