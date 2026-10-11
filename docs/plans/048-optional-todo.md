# Plan: Make `todo.md` optional (external task trackers)

Status: proposed (docs-only; no behavior change)
Issue: [#48](https://github.com/ValenFelizia/csdd/issues/48)
Date: 2026-10-09

## Summary

Today CSDD treats `.csdd/todo.md` as a required primary document. That works
for local/solo coordination, but duplicates GitHub Issues/PRs or Linear in
repos that already track work well elsewhere. This plan inventories every
contract that assumes `todo.md`, recommends how to declare an external-tracker
mode, and slices the follow-up implementation work. **No runtime or validator
behavior changes in this PR.**

## 1. Inventory

Inventory method (run from repository root; verified 2026-10-09 on `main` at
plan authoring time):

```bash
rg --glob '!.git/**' 'todo\.md' | wc -l
# → 304 hits in 38 files

rg --glob '!evals/runs/**' --glob '!.git/**' 'todo\.md' | wc -l
# → 185 hits in 21 files (excludes historical eval run artifacts)
```

Files that mention `todo.md` (excluding `evals/runs/**`):

| Path | Hits | Role today |
| --- | ---: | --- |
| `references/document-contracts.md` | 36 | Normative layout, init, `todo.md` contract, handoff relationship, reconciliation |
| `references/protocol.md` | 35 | Four-document model, hot context, lifecycle, concurrency, boundary rules |
| `SKILL.md` | 17 | Init creates four docs; hydration L1/L2; claim/update/close; doctor/status point at todo |
| `evals/fixtures/todo_integration.py` | 16 | Scenario 10 materializer writes `.csdd/todo.md` |
| `evals/fixtures/task_identity.py` | 13 | Scenario 09 materializer writes `.csdd/todo.md` |
| `evidence/t-027-compatibility.md` | 13 | Compatibility evidence assumes four primaries including todo |
| `references/read-only-workflows.md` | 11 | Doctor "Current" class requires todo + six H2s; status sources include todo |
| `tests/test_repository_validation.py` | 9 | Asserts on `assets/templates/todo.md` structure |
| `evals/scenarios/11-doctor-states.md` | 6 | Doctor fixtures require todo headings |
| `scripts/validate_repository.py` | 5 | `PRIMARY_TEMPLATES` includes `todo.md`; `validate_todo_template` |
| `README.md` | 3 | Layout diagram and document map |
| `evals/scenarios/06-git-divergence.md` | 3 | Divergence/blocker recording in todo |
| `evals/scenarios/07-landing-todo-handoff.md` | 3 | Landing/retention/handoff interaction with todo |
| `evals/scenarios/15-status-limits.md` | 3 | Status counts derived from todo |
| `evidence/t-030-release-readiness.md` | 3 | Release checklist lists `.csdd/todo.md` |
| `references/migration-v0.1-to-v0.2.md` | 2 | Migration of todo structure |
| `evidence/t-025-installation.md` | 2 | Install evidence lists `.csdd/todo.md` and template |
| `evals/scenarios/14-status-snapshot.md` | 2 | Status sources name `.csdd/todo.md` |
| `changelog.md` | 1 | Historical mention of v0.2 templates |
| `evals/scenarios/08-existing-repo-init.md` | 1 | Init must create `.csdd/todo.md` |
| `assets/templates/handoff.md` | 1 | "Do not duplicate todo.md" |

Additional artifacts that **assume** `todo.md` even when the string is absent
or secondary:

| Path | Assumption |
| --- | --- |
| `assets/templates/todo.md` | Canonical template; required by package validator (`PRIMARY_TEMPLATES`) |
| `.csdd/todo.md` | This repo's live project state (dogfood); not a package contract |
| `evals/scenarios/10-todo-integration.md` | Entire scenario is about shared TODO reconciliation (filename/topic) |
| `evals/scenarios/09-task-identity.md` | Task IDs live in todo entries |
| `docs/architecture.md` | "Four documents" boundary; optional integrations must not replace the task store silently |
| `CONTRIBUTING.md` / `.github/PULL_REQUEST_TEMPLATE.md` | Indirect: changes that touch document responsibilities need architecture review |

### Contract clusters (what would need defined behavior)

1. **Layout / "four primary documents"** — `protocol.md`, `document-contracts.md`, `README.md`, architecture language.
2. **Initialization** — `SKILL.md` step 6; `document-contracts.md` Generated structure; scenario 08.
3. **State classification (doctor/status/init)** — "Already initialized / Current" = all four files + todo heading contract (`read-only-workflows.md`, `document-contracts.md` State classification).
4. **Agent next-action / hydration / claim lifecycle** — `SKILL.md` levels 1–2, claim/update/close; protocol concurrency and landing tables.
5. **Handoff degradation** — handoff is defined as *additional* to todo; operational rule `coordination → todo.md` (`document-contracts.md` Relationship to todo.md).
6. **Package validation** — `scripts/validate_repository.py` always validates the skill's `assets/templates/todo.md` (package template, not adopted-project state).
7. **Evals / evidence** — scenarios 06–08, 10–11, 14–15; fixtures; compatibility/install/release evidence.

## 2. Design options

### Option A — File absence means external mode

Declare external-tracker mode solely by omitting `.csdd/todo.md`.

| Pros | Cons |
| --- | --- |
| No new file type | Collides with today's **Partial/malformed** class (missing primary) |
| Minimal authoring | Silent/accidental deletion looks like a deliberate mode switch |
| | No place to record tracker URL / next-action policy in-repo |

**Verdict:** Reject as the sole signal.

### Option B — Config flag (new `.csdd/config.md` / YAML)

Add an explicit config document with e.g. `tasks: external`.

| Pros | Cons |
| --- | --- |
| Unambiguous | New document type; init forbids "extra canonical documents" today |
| Extensible for future knobs | Architecture prefers not growing the core surface without evidence |
| | Config without a next-action pointer still leaves agents guessing |

**Verdict:** Possible later; heavier than needed for v0.

### Option C — Mutual exclusion: `.csdd/tracker.md` replaces `todo.md`

When `.csdd/tracker.md` exists and `todo.md` does not, mode is external.
When both exist → conflict/malformed. When neither → partial (unchanged).

`tracker.md` holds: tracker kind, URL(s), and a short next-action policy
(e.g. "open Issues with label `ready`", "Linear project X, cycle current").

| Pros | Cons |
| --- | --- |
| Explicit, greppable mode | New filename; touches "four primary documents" language |
| Clear next-action source | Doctor/init/status classification matrices all need a fifth name or a "task surface" abstraction |
| Absence of todo is intentional, not accidental | Migration must teach the mutual-exclusion rule |

**Verdict:** Strong, but more renaming churn across contracts.

### Option D — Alternate valid shape of `.csdd/todo.md` (external stub)

Keep the path `.csdd/todo.md`. Allow a second valid document shape:

```markdown
# TODO

Mode: external
Tracker: https://github.com/org/repo/issues
Next: Issues labeled `ready` (or: open Linear cycle / linked PR checklist)
```

No six canonical H2s required in this shape. Default init still creates the
full local todo. Opt-in via `/csdd init` with explicit external-tasks intent
(or a later conversion workflow).

| Pros | Cons |
| --- | --- |
| Preserves four-file layout and "Current" classification shape | File still named `todo.md` while not being a task board (mild naming debt) |
| Explicit mode + in-repo next-action pointer | Validators/doctor need a shape discriminator (`Mode: external` vs local headings) |
| Accidental delete still = partial, not silent opt-out | Does not literally "omit the file" (issue wording); functionally optional *board* |
| Smallest change to architecture "four documents" language | Stub can still drift if humans forget to update Tracker/Next |

**Verdict:** Best fit for v0.

### Option E — Do nothing structural; document "keep an empty todo"

Keep requiring the six-heading empty board; tell teams to put `Issue:` URLs
on tasks and maintain the real backlog elsewhere.

| Pros | Cons |
| --- | --- |
| Zero contract change | Does not solve duplicate source-of-truth / maintenance pain in #48 |
| | Agents still hydrate and claim through todo |

**Verdict:** Useful as a **lighter alternative** if #48 is deferred; not a fix.

### Recommendation

**Choose Option D** (external stub shape of `.csdd/todo.md`), with these rules:

1. **Default unchanged:** Absent → init creates local six-heading `todo.md` +
   `Retention: 5`.
2. **Opt-in only:** External mode requires an explicit human/init signal, never
   inferred from "issues exist on GitHub."
3. **Discriminator:** A single top-level `Mode: external` (or equivalent
   fenced/frontmatter form decided in implementation) selects the stub
   contract; otherwise the existing local contract applies.
4. **Mutual exclusion of shapes:** External stub MUST NOT also carry the six
   state H2s as a live board (malformed if mixed).
5. **No fifth primary document** in v0; revisit Option C only if naming
   confusion becomes a measured problem.
6. **Canonical authority:** The stub points agents at the external tracker for
   *task selection and status*. CSDD still owns specs, decisions, and
   boundary handoffs. This matches
   [architecture.md](../architecture.md) "Composable external context" while
   acknowledging that collision/scope claims are weaker without a local board
   (see §3).

## 3. What replaces `todo.md` as the agents' next-action source

In external mode, the ordered sources are:

1. **`.csdd/todo.md` stub** — `Tracker:` and `Next:` (required fields of the
   stub contract). Agents read this before calling out to tools.
2. **External tracker** — GitHub Issues/PRs, Linear, etc., via the stub's
   policy. The tracker is authoritative for backlog order and issue state.
3. **User message** — explicit task designation still wins for a single turn
   (same as today for trivial work).
4. **`.csdd/handoff.md`** — only for boundary + concrete resumption risk; never
   a substitute backlog.

### How other CSDD files degrade

| Surface | Local mode (today) | External mode (proposed) |
| --- | --- | --- |
| `specs.md` / `decisions.md` | Unchanged | Unchanged |
| `todo.md` | Full board + claims/scopes | Stub only; no In Progress board; no CSDD task IDs required |
| `handoff.md` | Additional to todo claims | Still valid for boundary risk; SHOULD link external issue/PR IDs instead of `T-…` when those are the work identity |
| Hydration L1 | Read active scopes in todo | Read stub; if overlap risk is plausible, inspect tracker / ask user — do **not** invent a local board |
| Claim / Scope / Agent fields | In todo entries | Not represented in CSDD; rely on PR assignment, issue assignees, or branch ownership. Document this as an honest capability loss |
| `/csdd status` | Counts from six states | Report `mode: external`, stub fields, handoff IDs; **no fake state counts** |
| `/csdd doctor` | Heading/Retention rules on local shape | Validate stub fields; do not demand six H2s; mixed shape = malformed |
| Landing / Ready to Land | Todo section + Verification | External: PR merge state + issue closure; CSDD does not mirror them into a board |
| Task-wise TODO reconciliation (#42) | Applies to local board | N/A for stub; divergence classes that assume todo text merges need an external-mode exception |
| Local task identity (#41) | `T-<ns>-<n>` in todo | Optional; external IDs may be referenced from handoff/PRs without minting CSDD IDs |

**Non-goal:** Automatic two-way sync between GitHub/Linear and CSDD. The stub
is a pointer and policy, not a mirror.

## 4. Backward compatibility and migration

| Existing repo state | Behavior after the change |
| --- | --- |
| Valid local `todo.md` (six H2s, Retention) | Unchanged; remains default |
| Missing `todo.md` among other primaries | Still **partial/malformed** (not auto-external) |
| Wants external mode | Explicit conversion: replace board with stub (or `init` with external intent on Absent roots only) |
| Mixed stub + board headings | Malformed; doctor reports; no silent preference |
| Package `assets/templates/todo.md` | Keep local template; add `assets/templates/todo.external.md` (or documented stub section) for init |
| This dogfood repo (`.csdd/todo.md`) | No forced migration; remains local unless maintainers opt in |

Migration notes for adopters:

1. Freeze or close in-flight CSDD claims, or land them, before converting.
2. Write the stub with real Tracker/Next URLs.
3. Delete or replace board content in one commit so observers do not see a
   half-board.
4. Update contributor docs so agents do not re-create a local board on init
   repair paths (repair must not "helpfully" restore local mode).

Versioning: this is a **compatible expansion** of allowed project state if
local mode remains default and existing valid boards stay valid. Call it out
in changelog; bump only if the project versioning policy treats new allowed
shapes as minor. No forced v0.1-style migration guide unless local→external
conversion proves error-prone.

## 5. Implementation breakdown (suggested PR slicing)

### PR-1 — Normative contracts (behavior authorization)

- Update `references/document-contracts.md`: layout wording ("task surface"),
  init branches, stub contract, state classification for external shape.
- Update `references/protocol.md`: four documents remain; todo responsibility
  splits into local-board vs external-pointer modes.
- Update `references/read-only-workflows.md`: doctor Current class; status
  external snapshot; finding IDs for stub validation.
- Add architecture note / DEC draft in `.csdd/decisions.md` only when the
  direction is accepted (not in the plan PR).
- Tests: still green; no validator behavior change yet if contracts are
  careful—or land stub validation in the same PR if preferred.

### PR-2 — Skill + templates + package validator

- `SKILL.md` init step 6: default local; external only on explicit intent.
- Hydration, claim, close, doctor, status fast paths: branch on mode.
- `assets/templates/todo.md` unchanged as local default; add external stub
  template.
- `scripts/validate_repository.py` + `tests/test_repository_validation.py`:
  validate both package templates; keep offline/deterministic.

### PR-3 — Evals and docs surfacing

- Scenario 08: default init still creates local todo; add variant or scenario
  for external init.
- New scenario: external-mode doctor/status; negative mixed-shape case.
- Scenarios 06/07/10/11/14/15: document applicability (local-only vs both).
- `README.md`, installation/compatibility as needed; changelog entry.

### Test changes (when behavior lands)

| Area | Change |
| --- | --- |
| Unit (`tests/test_repository_validation.py`) | Accept external stub template; reject mixed shape |
| Doctor/status scenarios | External current class; no six-H2 demand; status without fake counts |
| Init scenario | Default path unchanged; external path opt-in |
| Todo-integration / task-identity | Remain local-mode focused; mark N/A or skip under external |
| CI | Existing suite must stay green on every docs-only and incremental PR |

### Risks

| Risk | Mitigation |
| --- | --- |
| Agents treat missing todo as external | Keep absence = partial; require `Mode: external` |
| Collision/scope safety regresses | Document capability loss; recommend PR-scoped work or keep local mode for multi-agent repos |
| Handoff becomes a shadow todo | Keep handoff contract; doctor finding if handoff grows task-board-like |
| Stub drift vs real tracker | `Next:` policy should be durable (label/project), not a copied issue list |
| Architecture tension ("repo-local truth") | Stub + specs/decisions/handoff stay in-repo; tracker owns backlog only |
| Large doc churn / inconsistency | Slice PRs; one canonical stub contract section; skill remains a router |

## 6. Should we do it?

### Effort (technical, not calendar)

- **Contract surface:** High — `document-contracts.md` and `protocol.md` are
  the densest hit sites (~70 combined mentions); doctor/status classification
  is tightly coupled to "four files + six H2s."
- **Skill/router:** Medium — localized branches in init/hydration/claim/status.
- **Package validator:** Low–medium — second template shape + tests.
- **Evals:** Medium — new scenario plus applicability notes; several existing
  scenarios stay local-only.
- **Overall:** A multi-PR protocol change with honest coordination trade-offs,
  not a small docs tweak.

### Cost / benefit

**Benefit:** Removes duplicate backlog maintenance for teams whose SoT is
already GitHub/Linear; reduces todo drift and agent busywork updating a board
nobody uses.

**Cost:** Weakens in-repo claim/scope visibility (a core CSDD value for
multi-agent overlap). External mode is a poorer fit for parallel agents on
shared files unless the team accepts PR/branch discipline as the only
coordination. Doc and classification churn is real.

**Honest recommendation:** Worth doing **if** framed as an explicit opt-in for
tracker-centric repos, default local unchanged, and capability loss documented.
Not worth doing as "todo.md may simply be missing."

### Lighter alternative

Ship **guidance only** (Option E): keep requiring the empty six-heading
`todo.md`, encourage `Issue:` links, and tell tracker-centric teams to leave
the board empty. Cheaper, preserves contracts, partially addresses pain, does
**not** stop agents from claiming into todo or status from counting empty
states. Use this if maintainers want to defer contract risk after reviewing
this plan.

## Out of scope (this plan PR)

- Any skill, validator, template, or eval behavior change
- Automatic GitHub/Linear sync
- Merging this or follow-up PRs
- Changing this repository's own `.csdd/todo.md` mode
