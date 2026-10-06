# Read-only inspection workflows

`/csdd doctor` is the canonical user-facing name for a portable, read-only
diagnosis of a repository's CSDD state. It is a workflow name, not a requirement
that a harness register a native slash command, and not a CLI executable.
Equivalent explicit skill or natural-language requests to diagnose CSDD state
are sufficient.

This document owns the doctor procedure, finding identifiers, and output
contract. Conceptual safety also lives in
[Read-only inspection](protocol.md#read-only-inspection). Document shape and
field meaning remain in [document-contracts.md](document-contracts.md). Doctor
applies those rules; it does not redefine them.

`/csdd status` is a separate workflow defined in
[the status section](#csdd-status). It may reuse the inspection below. Doctor
does not produce a status snapshot and does not store one.

## Non-goals

Doctor does not:

- repair, migrate, normalize, delete, stage, commit, push, or rewrite state;
- create or update `.csdd/` documents, including a status file or cache;
- infer abandonment from age alone;
- claim repository-wide safety when relevant branches, worktrees, or tools were
  inaccessible;
- launch initialization, repair, or migration, including by implication;
- require a daemon, watcher, lock service, or background process;
- guarantee that inaccessible external agent activity does not exist.

Any proposed fix requires a separate explicit user request and the normal CSDD
authority rules.

## Invocation

Run doctor only when the user explicitly requests diagnosis, or when project
instructions explicitly request `/csdd doctor`. Do not run it as part of
ordinary bootstrap, Level 0 work, or an unrelated task.

No CLI, script, hook, plugin, MCP, or harness-specific adapter is required.
When Git or worktree tools are missing, continue with file evidence and record
the limitation. Do not install tooling in order to diagnose.

## Shared inspection

Doctor and any later read-only workflow that reuses this section share these
steps. Perform them before assigning findings.

### Canonical root

Resolve one project root using the same rules as
[Canonical root](protocol.md#canonical-root). Read that root only.

- In a Git worktree, the worktree root is canonical. A subdirectory invocation
  does not create or prefer a nested `.csdd/`.
- A monorepo has one repository-root `.csdd/`.
- A nested Git repository or submodule is an independent root when inspection
  was invoked inside it.
- Outside Git, continue only when the human identified an unambiguous project
  directory.
- An unusable `.csdd` path, such as a regular file where the directory should
  be, is a destination conflict.

If more than one candidate root remains plausible, stop classification and
report `root.ambiguous`. If `.csdd` exists and is not a directory, report
`root.unusable`. Do not create a directory to remove the ambiguity.

### State classification

After the root is usable, classify with the same first-match precedence as
[State classification](document-contracts.md#state-classification):

| Order | Class | Doctor meaning |
| --- | --- | --- |
| 1 | Ambiguous or conflicting | Report `root.ambiguous` or `root.unusable`. Do not continue into document scoring. |
| 2 | Absent | `.csdd/` does not exist. This is a classification, not a structural defect. |
| 3 | Current | All four primary documents exist and the minimum current structure is recognizable: `todo.md` has the six canonical state H2 headings, each exactly once, in canonical order, with no forbidden state H2. Individual field defects do not demote this class. |
| 4 | Recognizable older | Not current, and a positive older-contract signal is present as defined below. |
| 5 | Partial or malformed | `.csdd/` exists but the state is neither current nor recognizable older. Missing primary documents are partial. Present documents that still fail recognition are malformed. |

Recognizable older v0.1 requires all of the following:

- the root is unambiguous and `.csdd/` is a directory;
- the state is not current;
- `specs.md`, `todo.md`, `decisions.md`, and `handoff.md` exist as files;
- `todo.md` contains none of the six canonical state H2 headings;
- at least one positive older signal is present: an `Icebox` H2, task-like
  content under a non-canonical H2, or an explicit v0.1 identification in one
  of the four documents.

A mix of canonical headings and older signals is malformed, not older. In that
case emit the structural findings, including `todo.h2.forbidden` when `Icebox`
or `Archived` is present. If the four files exist, the heading contract fails,
and no older signal meets the rule above, the class is malformed. If
recognition is still uncertain, emit `state.uncertain` (warning) and do not
choose current or older.

Doctor never writes, including when the class is Absent. Pointing at
[migration-v0.1-to-v0.2.md](migration-v0.1-to-v0.2.md) for recognizable older
state does not start migration.

### Evidence and severity

Every finding names a stable identifier, a severity, and an evidence path.
Include a heading, line, task ID, or Git ref when the repository exposes one.
A finding whose evidence does not support it must not be emitted.

| Severity | Use |
| --- | --- |
| error | The inspected artifact violates the current structural or field contract. |
| risk | Coordination evidence shows overlap, Git contradiction, or an unresolved contradiction. |
| warning | A reconciliation signal is real, but the safe action is to inspect rather than treat the state as proven broken. Uncertain consumption belongs here. |
| limitation | The check did not run because a tool, ref, branch, or worktree was inaccessible. A limitation is not a pass. |

Age of `Updated`, of a handoff, of a branch, or of a commit is never sufficient
evidence for any finding. Do not emit `claim.reconcile` or
`handoff.maybe-consumed` from age alone.

### Structural rules reused from repository validation

Where a check concerns TODO headings, forbidden state names, or `Retention`,
apply the same rules as `validate_todo_template` in
[`scripts/validate_repository.py`](../scripts/validate_repository.py), against
the project's `.csdd/todo.md` rather than `assets/templates/todo.md`:

- the only state H2 headings are `In Progress`, `Ready to Land`, `Blocked`,
  `Pending`, `Deferred`, and `Recently Completed`, each exactly once, in that
  order;
- `Icebox` and `Archived` are forbidden state H2 headings;
- any other H2 under `# TODO` is an extra state heading;
- `Retention` is a single declaration inside `## Recently Completed`;
- the retention value matches a positive decimal integer `N >= 1`. `0` is
  invalid.

Heading and fence handling follows that validator: ignore headings inside
fenced code blocks. Field checks that the template validator does not encode
come from the [`todo.md` contract](document-contracts.md#todomd) and the
[`handoff.md` contract](document-contracts.md#handoffmd). Do not invent a
second heading taxonomy.

Missing `Retention` on an otherwise current document is `todo.retention.missing`
with severity warning. The operational fallback remains five until a human or
explicit project policy sets `N`. Doctor does not insert the line.

Do not run `scripts/validate_repository.py` against a target project. That
script validates the CSDD skill package, not an adopted repository.

### Git and worktree observation

Observe only. Allowed observations, when the environment already exposes them,
include read-only Git status, local branch tips, and worktree lists. Do not
fetch, pull, stash, checkout, stage, commit, or update refs. A fetch would
mutate Git metadata and is outside this workflow.

The current worktree is the operational baseline, not proof of repository-wide
state. Follow [Branch and worktree
locality](document-contracts.md#branch-and-worktree-locality) for what absence
of a claim does and does not prove.

When `git` cannot be run, record `git.unavailable` and skip Git-dependent
checks. When a worktree list cannot be produced, record `worktree.unavailable`.
When a claim's truth depends on a remote tip that was not already present
locally, record `git.remote-unverified` instead of fetching it.

### Safety

Before returning, confirm the worktree has no changes from this workflow.
Preserve unrelated dirty state exactly. Do not format, normalize, or touch
files in order to make the next read easier.

## `/csdd doctor`

### Checks

Run the checks that the classification makes meaningful. Record skipped checks
and why.

**Structure**

- Four primary documents present as files. Each missing file is `docs.missing`.
  A primary path that exists and is not a file is `docs.not-file`.
- TODO headings, forbidden names, order, duplicates, and retention, using the
  shared structural rules. Identifiers: `todo.h2.missing`,
  `todo.h2.duplicate`, `todo.h2.order`, `todo.h2.extra`, `todo.h2.forbidden`,
  `todo.retention.missing`, `todo.retention.duplicate`,
  `todo.retention.placement`, `todo.retention.value`.
- More checked Recently Completed entries than `N` (or than the fallback five
  when the declaration is absent) is `todo.retention.overflow`, severity
  warning. Reporting it does not authorize compaction.
- Active and lateral tasks use unchecked items. Recently Completed uses checked
  items. A mismatch is `todo.task.checkbox`.
- A task that cannot be placed under exactly one canonical state H2 is
  `todo.task.unplaced`.
- Deferred entries require `Reason:` and an observable `Resume when:`, have no
  `Agent`, and omit active scope or use `Scope: released`. A violation is
  `todo.deferred.invalid`. Vague resume conditions such as "later" are invalid.
- Ready to Land entries include `Landing:` and do not include `Landed:`.
  Violations are `todo.ready.landing-missing` and `todo.ready.landed-present`.
- Pending entries do not carry an active `Agent` or active write scope.
  A violation is `todo.pending.claim`.
- Recently Completed entries do not retain a concrete active scope. A violation
  is `todo.completed.active-scope`.

**Task identity**

Apply [Local task identity](document-contracts.md#local-task-identity). Doctor
reports identity defects; it does not allocate, rename, or repair IDs.

- Legacy `T-NNN` IDs remain valid and MUST NOT emit `todo.task.id-invalid`.
- A namespaced ID that violates the documented grammar
  (`T-<namespace>-<number>` with namespace
  `[a-z][a-z0-9]*(?:-[a-z0-9]+)*` and a positive decimal counter padded to at
  least three digits), or that uses counter `000`, is
  `todo.task.id-invalid`.
- The same stable ID on more than one distinct task entry in the inspected
  `todo.md`, or the same ID naming observably different tasks across visible
  local baselines when both are in evidence, is `todo.task.id-duplicate`.
  Equality of title or external `Issue:` alone is not identity proof. Doctor
  does not choose which entry keeps the ID.

**Handoffs**

Apply the [handoff contract](document-contracts.md#handoffmd). Do not require
fixed labels such as `Risk:` or `Consumed:`.

- An entry with no identifiable concrete resumption risk is
  `handoff.risk-missing`.
- An entry that is only session narration, with no identifiable boundary, is
  `handoff.boundary-missing`. Do not invent a boundary to clear the finding.
- More than one current snapshot for the same task or workstream is
  `handoff.duplicate`.
- When the task is completed, or Git and `todo.md` show the stated risk already
  resolved, and a current handoff still presents that risk as open, emit
  `handoff.maybe-consumed`. Say that removal requires a separate explicit
  reconciliation. Age alone does not qualify.
- A handoff whose risk is still concrete and whose task is still active is a
  passed check, even when `Updated` or the surrounding commits are old.

**Coordination**

- Compare active scopes on In Progress, Ready to Land, and Blocked entries that
  still name a concrete scope. A path or glob intersection is `scope.overlap`.
  Semantic overlap qualifies only when cited repository evidence shows it.
  Vague scopes that cannot be compared produce `scope.uncomparable` and do not
  count as overlap.
- Emit `scope.git-contradiction` when observable Git status or reachability of
  the named scope paths contradicts the claim. Examples: an In Progress scope
  whose changes are already reachable from the declared Target, or a released
  scope whose paths are dirty with work the claim does not explain. A clean
  scope is not proof the claim is stale.
- Emit `claim.reconcile` when other inspected evidence signals that a claim
  needs human reconciliation, but that evidence is not a proven scope/Git
  contradiction of the named paths. Age alone never qualifies.
- Do not emit both `scope.git-contradiction` and `claim.reconcile` for the same
  evidence pair. Prefer `scope.git-contradiction` when the Git/scope
  contradiction is established.
- When `todo.md`, `handoff.md`, and observable Git disagree and the available
  evidence does not determine which is current, emit
  `contradiction.unresolved` and do not pick a winner.

Passed checks should be named briefly, for example `root.unambiguous`,
`docs.present`, `todo.structure`, `todo.retention`, `todo.identity`,
`handoff.shape`, and `scope.no-overlap-in-inspected-state`. Omit checks that
were skipped.

### Finding identifiers

Identifiers below are stable for evaluation and later automation. Severities
are part of the contract. Do not rename an identifier to rephrase a finding.
Free-text explanation may vary; the identifier, severity, and evidence path
may not be omitted.

| Identifier | Severity | Meaning |
| --- | --- | --- |
| `root.ambiguous` | error | More than one plausible canonical root remains. |
| `root.unusable` | error | `.csdd` exists and is not a usable directory. |
| `state.uncertain` | warning | Classification cannot choose current or older from the evidence. |
| `docs.missing` | error | A primary document file is absent. |
| `docs.not-file` | error | A primary path exists and is not a file. |
| `todo.h2.missing` | error | A required canonical state H2 is missing. |
| `todo.h2.duplicate` | error | A canonical state H2 appears more than once. |
| `todo.h2.order` | error | Canonical state H2 headings are out of order. |
| `todo.h2.extra` | error | An extra non-canonical state H2 is present. |
| `todo.h2.forbidden` | error | A forbidden state H2 such as `Icebox` or `Archived` is present. |
| `todo.retention.missing` | warning | `Retention` is absent on an otherwise current document. |
| `todo.retention.duplicate` | error | More than one `Retention` declaration is present. |
| `todo.retention.placement` | error | `Retention` is outside `## Recently Completed`. |
| `todo.retention.value` | error | `Retention` is not a positive decimal integer `N >= 1`. |
| `todo.retention.overflow` | warning | Checked Recently Completed entries exceed `N` or the fallback five. |
| `todo.task.checkbox` | error | Checkbox state does not match the containing section. |
| `todo.task.unplaced` | error | A task is not under exactly one canonical state H2. |
| `todo.task.id-invalid` | error | A namespaced task ID violates the identity grammar or uses `000`. |
| `todo.task.id-duplicate` | error | The same stable ID names more than one distinct task in evidence. |
| `todo.deferred.invalid` | error | A Deferred entry violates Deferred field rules. |
| `todo.ready.landing-missing` | error | A Ready to Land entry lacks `Landing:`. |
| `todo.ready.landed-present` | error | A Ready to Land entry includes `Landed:`. |
| `todo.pending.claim` | error | A Pending entry carries an active `Agent` or write scope. |
| `todo.completed.active-scope` | error | A Recently Completed entry retains a concrete active scope. |
| `handoff.risk-missing` | error | A handoff entry has no identifiable concrete resumption risk. |
| `handoff.boundary-missing` | warning | A handoff is only session narration with no identifiable boundary. |
| `handoff.duplicate` | error | More than one current handoff exists for the same task or workstream. |
| `handoff.maybe-consumed` | warning | Evidence shows the stated risk is resolved, but the handoff remains open. |
| `scope.overlap` | risk | Active concrete scopes intersect in the inspected state. |
| `scope.uncomparable` | warning | Vague scopes cannot be compared; not counted as overlap. |
| `scope.git-contradiction` | risk | Observable Git contradicts the claim for the named scope paths. |
| `claim.reconcile` | warning | Non-Git reconciliation evidence exists without a proven scope/Git contradiction. |
| `contradiction.unresolved` | risk | Documents and Git disagree and the evidence does not choose a winner. |
| `git.unavailable` | limitation | Git cannot be run; Git-dependent checks are skipped. |
| `worktree.unavailable` | limitation | Worktree listing cannot be produced. |
| `git.remote-unverified` | limitation | A needed remote tip was not already present locally. |

### Output

Produce a concise human-readable report. The exact wording may vary by
harness. Include:

- detected root;
- classification: absent, current, recognizable older v0.1, partial,
  malformed, ambiguous, or uncertain;
- detected version or state when evidence supports it, otherwise `unknown`;
- passed checks;
- findings grouped by severity, each with identifier and evidence path;
- checks skipped and why;
- one recommended next action;
- the explicit sentence `Nothing was modified.`

Do not include a machine schema, a persisted report, or a full copy of the
canonical documents.

### Recommended next action

Recommend one next step that this workflow does not itself perform.

- Absent: `/csdd init` only if the user separately wants adoption.
- Recognizable older: the migration guide, only with explicit migration intent.
- Partial or malformed: report the blocking defects. Repair stays a separate
  explicit request; doctor does not offer to perform it in the same turn.
- Current with risks: name the coordination item to reconcile before editing
  that scope.
- Current with no findings: state that the inspected artifacts passed the
  checks that ran, and repeat any visibility limitations. Do not call the
  repository safe beyond that evidence.

## `/csdd status`

`/csdd status` is the canonical user-facing name for a lightweight, read-only
operational snapshot. It answers what is active now. Doctor answers whether
the inspected state is valid and what is wrong. The workflows stay separable
even though status reuses [Shared inspection](#shared-inspection).

Status is a derived view. It MUST point back to `.csdd/todo.md`,
`.csdd/handoff.md`, and observable Git state. It MUST NOT become a second TODO,
a handoff surface, a cache, or a persisted status file.

### Invocation

Run status only for an explicit `/csdd status` request or an equivalent
natural-language request for the current CSDD snapshot. Do not run it during
ordinary bootstrap or unrelated work. No CLI, script, hook, plugin, or
harness adapter is required.

### When a snapshot is reliable

Follow shared inspection through classification.

| Classification | Status behavior |
| --- | --- |
| Absent | Report that `.csdd/` is absent. Do not print task counts of zero. `/csdd init` remains a separate request. |
| Current, and every task sits under exactly one canonical state H2 | Derive the snapshot below. |
| Current, but one or more tasks cannot be placed | Do not invent counts. Recommend `/csdd doctor`. |
| Partial, malformed, recognizable older, ambiguous, or uncertain | Do not invent counts. State the limitation and recommend `/csdd doctor`. |

Field defects that still leave every task placed, such as a Deferred entry
missing `Reason:`, do not block counts. Say that structural diagnosis belongs
to doctor, and do not copy doctor's finding list into the snapshot.

### Brief output

Default output is brief. The wording may vary. Include:

- root, classification, and detected version or `unknown`;
- the source paths used, at least `.csdd/todo.md` and `.csdd/handoff.md` when
  they were read;
- counts for In Progress, Ready to Land, Blocked, Pending, Deferred, and
  Recently Completed;
- retention as `used/N`, using the declared `N` or the fallback five when the
  declaration is absent;
- one line per active claim that names an `Agent` or a concrete `Scope`: task
  ID, state, agent, and scope;
- Ready to Land task IDs with the `Landing:` value only;
- blocked and deferred task IDs, without their full entries;
- the number of current handoff entries and the task or workstream IDs they
  name, without handoff bodies;
- either `No detected scope overlap in inspected state` or the overlapping
  task IDs;
- the sentence that no detected overlap is not proof about uninspected
  branches, worktrees, or external agents;
- Git or worktree limitations, including visible divergence that was not
  fetched;
- the sentence `Nothing was modified.`

Counts come from the current worktree baseline only. Do not add counts from
another branch or worktree into the same totals. If another local worktree or
branch is visible and its CSDD state differs, report that divergence in one
line and leave the totals on this baseline.

An illustrative shape, not a schema. Mandatory elements such as retention
`used/N`, the no-proof-on-uninspected sentence, and `Nothing was modified.`
MUST appear even when wording varies:

```text
CSDD v0.2
root: .
classification: current
sources: .csdd/todo.md, .csdd/handoff.md
2 in progress
1 ready to land
0 blocked
1 pending
1 deferred
2 recently completed
retention: 2/5
active claims: T-710 (In Progress, agent, src/a/**); T-711 (In Progress, agent, src/b/**)
ready to land: T-712 — Landing: open PR against main
blocked: none
deferred: T-714
handoffs: 1 (T-710)
No detected scope overlap in inspected state
No detected overlap is not proof about uninspected branches, worktrees, or external agents.
Nothing was modified.
```

### Detail

Add detail only when the user asks for it. Detail may include one-line titles
and the canonical file path for each counted task. It still MUST NOT reproduce
notes, verification writeups, specification sections, decision bodies, or
handoff narratives. Point at the file instead.

### Safety

Status uses the same read-only Git observation rules as doctor. It MUST NOT
claim, reassign, reconcile, repair, migrate, initialize, fetch, stage, or
edit. It MUST NOT write `.csdd/status.md` or any other generated status
artifact.

## Separable workflows

Doctor and status may share root resolution, classification, structural rules,
and Git observation. They remain different user contracts. Doctor output is
not a status board. Status output is not a diagnosis and does not authorize a
repair.
