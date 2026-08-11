# T-030 — CSDD v0.2.1 release readiness

Issue: [#29](https://github.com/ValenFelizia/csdd/issues/29)  
PR: [#38](https://github.com/ValenFelizia/csdd/pull/38)  
Branch: `release/t-030-v0.2.1`  
Task: T-030  
Role: release-preparation evidence and draft release notes  
Date: 2026-08-11

This document prepares publication of **CSDD v0.2.1**. It does **not** publish
the tag or GitHub Release. Tagging, release publication, post-merge lifecycle
checks, and issue closure remain intentionally pending.

## 1. Objective and scope

Prepare an auditable patch release that:

- packages distribution, structural validation, compatibility evidence, and
  onboarding improvements landed after v0.2.0;
- preserves the v0.2 protocol contract without normative expansion;
- records the accepted T-029 release-gate exception (DEC-006);
- leaves publication, remote verification, and T-030 closure for after review.

In-scope preparation files for this branch:

- `.csdd/todo.md`
- `changelog.md`
- `evidence/t-030-release-readiness.md`

Out of scope for this preparation PR: merge, tag `v0.2.1`, GitHub Release,
administrative Recently Completed compaction, closing #29 or #28, and
destructive install-lifecycle mutations against the live development checkout.

## 2. Base SHA for preparation

| Field | Value |
| --- | --- |
| Preparation base (`origin/main`) | `caf43dba97087afeac8e597401cff232fb8430a8` |
| Base subject | `chore: disposition T-029 onboarding gate` |
| Prior published release | `v0.2.0` @ `9bf960967e6a1e81fd0c0b84068a69601a788668` |
| Working tree at branch creation | clean; local `main` fast-forwarded to `origin/main` |

## 3. Inventory of changes since v0.2.0

Git inventory (`git diff --stat v0.2.0..caf43db` / `git log --oneline v0.2.0..caf43db`):

| Area | Evidence |
| --- | --- |
| T-025 / #14 | Global Agent Skills install docs + `evidence/t-025-installation.md`; landed PR #31 @ `8ed582b` |
| T-026 / #21 | `scripts/validate_repository.py`, `tests/`, `.github/workflows/validate.yml`; landed PR #32 @ `d016d23` |
| T-027 / #24 | `docs/compatibility.md`, campaign runs, `evidence/t-027-compatibility.md`; landed PR #33 @ `5af4746` |
| T-028 / #19 | README public-beta onboarding polish (`5104fac`); issue closed 2026-07-24 |
| T-032 / #34 | Partial Antigravity project-local install path + `evidence/t-032-antigravity.md`; landed PR #35 @ `80d26a8` |
| T-029 disposition | DEC-006 + Deferred T-029 + issue comments; commit `caf43db` |
| README description tweak | `b59ad98` |

Files touched since `v0.2.0` (20 paths, +4328 / −167 before this preparation):
`.csdd/{decisions,specs,todo}.md`, `.github/workflows/validate.yml`,
`README.md`, `docs/{compatibility,installation}.md`, T-027 eval run sheets,
`evidence/t-025-installation.md`, `evidence/t-027-compatibility.md`,
`evidence/t-032-antigravity.md`, `scripts/validate_repository.py`,
`tests/test_repository_validation.py`.

## 4. Runtime / protocol change confirmation

**No normative runtime or protocol change since v0.2.0.**

Observed:

```text
git diff --name-only v0.2.0..caf43db -- SKILL.md references/ assets/templates/
# (empty)
```

`SKILL.md`, `references/**`, and `assets/templates/**` are unchanged relative to
tag `v0.2.0`. Distribution, validation, compatibility docs/evidence, and
onboarding wording changed; protocol semantics did not.

## 5. Migration justification

No migration from v0.2.0 to v0.2.1 is required because:

- the v0.2 document contracts and templates are unchanged;
- `/csdd init` remains Absent-only and creates the same four primary documents;
- existing v0.2 project state remains valid without rewrite;
- the only migration guide in-tree remains v0.1 → v0.2.

## 6. Relevant task / requirement status

| Item | Status | Notes |
| --- | --- | --- |
| T-025 / #14 | Completed | Closed; install path documented and evidenced |
| T-026 / #21 | Completed | Closed; offline validator + CI |
| T-027 / #24 | Completed | Closed; dimensional Codex/Cursor matrix |
| T-028 / #19 | Completed | Closed; README public-beta onboarding |
| T-029 / #28 | Deferred (open) | DEC-006 accepted 2026-08-05; zero external sessions; keep open |
| T-030 / #29 | Active release prep | This branch prepares publication only |
| T-032 / #34 | Completed | Closed; Antigravity partial project-local distribution only |

DEC-006 is consistent with `todo.md`, issue #28/#29 comments, and this release
positioning. No DEC-006 edit was required.

## 7. Pre-publication audit

### Executed in this preparation

| Surface | Result |
| --- | --- |
| README status wording | Experimental public beta; latest published version via release badge (still `v0.2.0` until publication); no hardcoded “externally validated onboarding” claim found |
| Install commands | README and `docs/installation.md` agree on Codex/Cursor global `npx skills add ... --agent codex cursor -g -y` and Antigravity project-local `... --agent antigravity -y` (no `-g`) |
| Internal relative links | 119 relative links under root/docs/evidence/references resolved; 0 missing |
| Badges | Release, validation workflow, MIT license, public-beta status badges present and point at expected targets |
| Changelog | v0.2.1 entry added in this branch; distinguishes distribution/docs/infra from protocol |
| Compatibility docs | `docs/compatibility.md` remains dimensional; partial / not tested cells retained |
| License | `LICENSE` present (MIT, Copyright 2026 Valentín Felizia) |
| Validation workflow | `.github/workflows/validate.yml` runs unittest + `scripts/validate_repository.py` on PR/push/`main` |
| Claims vs evidence | Public claims do not exceed T-025 / T-027 / T-032 evidence; Antigravity discovery/behavior remain not tested |

### Historical evidence reused (not re-executed here)

| Claim area | Reused record |
| --- | --- |
| Install lifecycle (isolated profile) | `evidence/t-025-installation.md` |
| Codex/Cursor behavioral matrix | `evidence/t-027-compatibility.md` + `evals/runs/t027-*.md` |
| Antigravity project-local install | `evidence/t-032-antigravity.md` |
| v0.2 protocol eval scenarios 06–08 | `evals/results.md` / Run A reports from v0.2.0 |

### Intentionally not executed on this machine during preparation

Destructive or profile-mutating lifecycle operations against the live
`~/.agents/skills/csdd` development checkout (this workspace). Those checks
remain on the post-merge checklist using an isolated temporary profile.

## 8. Validations executed on this branch

Interpreter: `C:\Users\Valen\AppData\Local\Programs\Python\Python313\python.exe`
(`Python 3.13.2`). Canonical `python` on PATH was a Windows Store stub and was
not used.

| Check | Command | Result |
| --- | --- | --- |
| Unit tests | `python -m unittest discover -s tests -v` | **PASS** — Ran 19 tests in ~1.131s, OK |
| Structural validator | `python scripts/validate_repository.py` | **PASS** — `Validation passed.` |
| Whitespace | `git diff --check` / `git diff --check origin/main` | **PASS** — no output |
| Relative link resolution | offline path existence check over `*.md`, `docs/`, `evidence/`, `references/` | **PASS** — 119 links, 0 missing |
| Protocol drift | `git diff --name-only v0.2.0..caf43db -- SKILL.md references/ assets/templates/` | **PASS** — empty |

PR-head CI for `6c88adc` completed successfully in CSDD validation run
[#16](https://github.com/ValenFelizia/csdd/actions/runs/31535573679).
CI on the eventual merge SHA remains pending.

## 9. Risks and limitations

- Independent onboarding risk is **unknown**: zero external sessions completed.
- Do not claim “externally validated onboarding.”
- Codex/Cursor Global install and Discovery remain **partial**; Implicit
  activation remains **not tested**.
- Antigravity remains **partial** for project-local install only; global CLI
  path mismatch, discovery, and behavior are **not tested**.
- Structural validation does not prove harness compatibility or protocol
  semantics.
- CSDD remains experimental public-beta software without shared runtime memory,
  distributed locking, or automatic synchronization.
- Post-merge publication steps are not covered by this PR.

## 10. Proposed release notes — CSDD v0.2.1

### Highlights

CSDD v0.2.1 is a public-beta patch release focused on distribution, structural
validation, compatibility evidence, and onboarding clarity. It does **not**
change the v0.2 protocol contract.

### What's new since v0.2.0

- Clearer one-command install for Codex and Cursor, plus install lifecycle docs.
- Offline structural validator and CI workflow.
- Dimensional Codex/Cursor compatibility matrix with durable evidence.
- README onboarding polish for first use and `/csdd init`.
- Partial Antigravity project-local installation path (discovery/behavior not
  tested).

### Upgrade from v0.2.0

No migration is required. Update the installed skill from the published source
when ready; existing v0.2 project `.csdd/` state remains valid.

### Honest limitations

- Experimental public beta.
- Independent human onboarding pilot still pending (deferred; not completed).
- Compatibility is dimensional, not binary.
- Install/discovery evidence remains partial for some cells; implicit activation
  is not tested.
- No shared runtime memory, distributed locking, or automatic synchronization.

## 11. Post-merge checklist (pending)

Do **not** treat these as done by this preparation PR:

- [ ] CI green on the merge SHA
- [ ] Re-run unittest + structural validator from a clean checkout of the merge SHA
- [ ] Isolated-profile install lifecycle (not the live development checkout):
  - [ ] install
  - [ ] reinstall
  - [ ] update
  - [ ] list / inspect installed files
  - [ ] uninstall
  - [ ] confirm project `.csdd/` preservation
- [ ] New Cursor session discovery / init smoke
- [ ] New Codex session discovery / init smoke
- [ ] Create tag `v0.2.1` on the exact reviewed release commit
- [ ] Publish GitHub Release `CSDD v0.2.1` (non-draft, non-prerelease, Latest)
- [ ] Verify remote tag and release
- [ ] Administrative commit: move T-030 to Recently Completed / release scope
- [ ] Close issue #29 only after publication and reconciliation are true
- [ ] Leave issue #28 open in Deferred until real external evidence exists

## Evidence classification legend

- **Executed here:** observed during T-030 preparation on this branch.
- **Historical reused:** prior durable evidence accepted without re-running.
- **Pending post-merge:** required before calling the release complete.
