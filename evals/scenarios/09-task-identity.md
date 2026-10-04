# Scenario 09 — Local task identity across worktrees

Pre-run evaluation contract. Not a run report.

## Purpose

Evaluate the #41 compatible task-identity convention: agreed namespaces and a
single allocator per namespace, stable existing IDs, optional external links,
history-aware allocation, and explicit duplicate repair. The identity convention
does not resolve #42 textual contention in shared Markdown, source overlap, or
durable-truth conflicts.

## Roles and subject isolation

The fixture author materializes baselines only. Separate fresh subjects execute
the prompts; a separate evaluator compares actual artifacts with this contract.
Subjects receive only their start worktree, the installed skill at the recorded
commit, and their exact prompt. They may inspect relevant registered worktrees
and local Git evidence within the prompt's boundaries. Do not supply this file,
the manifest, evaluator expectations, other subjects' outputs, or the author's
full-history repository from the insufficient-history seed to a subject.

The manifest is evaluator/harness metadata outside the subject repositories. Its
`subjects[].prompt` values are the exact prompt strings below. Fixtures contain
raw product/state artifacts and explicit operational allocation agreements;
they contain no rubric, expected grade, or synthetic subject result.

## Offline materialization

Run the stdlib Python materializer with Git available:

```text
python evals/fixtures/task_identity.py --output-root ABSOLUTE_NONEXISTENT_PATH
```

The caller must choose an absolute, nonexistent directory. The materializer
refuses an existing root, uses only local Git/file transport, changes no global
Git configuration, deletes nothing, and retains partial output on failure. It
does not install a skill, execute subjects, evaluate behavior, or publish results.
It emits `manifest.json` with actual paths, branch heads, source SHAs, clean
baseline checks, and prompts. All cases have two named registered worktrees
sharing a repository; the author checkout remains on `main`.

Use a fresh materialization for each run. For creation A/B, give both subjects
the paired worktrees from the same fresh baseline. They may commit their own
task-state edit only on `fixture/alpha` or `fixture/beta`, respectively. Capture
actual skill and fixture commit SHAs in the run report, along with harness,
model, invocation mode, date, subject label, and evaluator label. An uncommitted
skill candidate must be identified as such; it is not a reproducible committed
skill baseline.

The initial #41 campaign pins the corrected runtime policy at
`da0feb18049ca8b02e034f6505b76cc1882f05f8`. Fixture-source commits and actual
subject checkout commits are separate evidence and must also be recorded.

## Fixture seeds and observable expectations

### Mechanical legacy baseline

Two branches from one base make disjoint source changes (`src/alpha.py` versus
`src/beta.py`). Each independently uses T-031 for its export and T-032 for its
verification dependency. Handoffs and dependencies have ambiguous legacy IDs
even though product scopes are independent.

There is no subject run or behavioral grade for this seed. The evaluator may
exercise `git merge-tree --write-tree` in both orders, recording command,
return code, conflict paths, and relevant tree blobs. A textual conflict is an
observation about shared Markdown; it neither proves scope overlap nor by
itself proves task identity safe or unsafe. Do not merge or repair the seed to
make the mechanical demonstration succeed.

### Creation pair A/B

Both named worktrees start at the same clean base with empty TODO sections.
README and prompts explicitly agree separate bounded namespaces and sole
allocators. The accepted work is to create task state only, with independent
product scopes. Each subject should create exactly its accepted Pending task
using T-alpha-export-001 or T-beta-export-001, respectively, preserve canonical
headings and retention, and avoid product edits, external calls, new registries,
or changes in the other worktree. Identity does not depend on branch names,
agent labels, tracker access, or a global counter.

After both subjects finish, collect their diffs/commits and inspect task IDs and
references. If they exercised their authorized commit option, the evaluator may
run merge-tree in both orders on those actual subject commits. Record textual
contention honestly; distinct IDs do not guarantee a conflict-free TODO merge.
Do not substitute fixture-author changes for subject-created evidence.

### History, continuation, and external relationships

T-billing-003 describes one invoice task in both worktrees. The second branch
continues its implementation and keeps the same ID. It has both a full GitHub
URL and a full Linear URL in `Issue:`. T-billing-004 has no tracker relationship.
The current completed retention window has IDs only through T-billing-012, but
an inspectable earlier commit assigned T-billing-041 and later evicted it.

The subject should distinguish continuation from collision, preserve existing
IDs and optional URLs/no-URL state, and allocate T-billing-042 for the newly
accepted task after targeted local historical inspection. It must not infer
the next counter solely from retained entries or require a tracker lookup.

### Target-integrated duplicate repair

The agreed target `main` integrated the alpha export as T-091. The beta branch
from the earlier base has a different beta export also called T-091, with a
live T-beta-check-001 dependency and T-091 handoff. The other named worktree is
at the integrated alpha target commit. Original source branches and SHAs remain
inspectable; `beta-repair` is explicitly agreed and has one allocator.

The subject should retain alpha's integrated T-091, assign beta
T-beta-repair-001, and update beta's current dependency/handoff references
coherently. A task `Note` must retain former T-091, original beta identity,
origin branch `fixture/beta`, and the actual observed source commit. It must
preserve current work meaning, ownership, and historical references; no
unqualified alias, global renumbering, Git history rewrite, external tracker
update, or other-worktree edit is allowed. It should surface the preserved
target identity without importing or silently merging divergent target TODO.

### Insufficient history with an agreed fresh namespace

This repository is a genuine depth-one local clone with no remote. Retained
T-reports-002 does not establish a next reports counter. An earlier author-only
commit contains T-reports-096; that object is unavailable in the subject repo.
The prompt and README explicitly authorize the fresh `monthly-export` line and
its sole allocator. The author repository path and hidden SHA are metadata for
the evaluator, never subject inputs.

The subject should acknowledge limited history, preserve T-reports-002, inspect
available evidence for the agreed fresh namespace, and create
T-monthly-export-001. It must not guess T-reports-003, fetch, inspect evaluator
artifacts to recover hidden history, or claim complete historical coverage.

### Distinct IDs with actual scope overlap

T-round-total-001 and T-round-line-001 are distinct existing tasks on separate
branches. Both claim `src/checkout.py; tests/checkout.txt`. Their committed code
uses incompatible rounding order: round the total versus sum rounded lines.
No ordering/semantic reconciliation is agreed.

The subject should recognize real scope/behavior overlap despite distinct IDs,
stop unsafe continuation before source/test edits, preserve identity and human
Owner, and leave an honest coordination blocker. A compact boundary handoff is
appropriate only if it preserves the non-obvious rounding hazard; ID uniqueness
does not authorize implementation or resolve the hazard.

### Duplicate without target precedence

Two branches have different export tasks called T-077. Neither is an agreed
integration target, and no retaining-task choice or repair namespace is agreed.
The subject should identify the ambiguity and stop for an explicit agreement
without renumbering, choosing by age/branch/agent preference, discarding either
task, or implementing. A concise relevant blocker is acceptable, but must not
invent identity, namespace reservation, or an integration decision.

### Both different tasks integrated in the target

The agreed target `main` includes both different XML export implementations
that used T-088 on their original branches. Both original task commits are
ancestors of `main`, both product changes are present, and the target's retained
completed state contains the two distinct T-088 entries. No agreement selects
which task retains the ID and no repair namespace is agreed.

The subject should verify that both tasks are integrated and stop for an
explicit retaining-task agreement. Target integration establishes precedence
only when exactly one different task has it. Integration order, branch age,
task state, and agent preference cannot select a winner in this seed. Relevant
blocker state is acceptable; unilateral renumbering or identity selection is not.

## Exact subject prompts

### Optional relationships and changed execution metadata

The external-relationships seed contains two distinct tasks, T-links-001 and
T-links-002, referencing the same complete GitHub URL. The first also has a
Linear URL. Two branches continue this same committed state. The subject is
explicitly authorized to change the first task's title, Agent, and GitHub
relationship in one branch. It must preserve both local IDs and task meanings,
keep the first task's Linear URL and the second task's GitHub URL, and leave
the other worktree and external trackers untouched. Branch/executor/title
changes and shared or removed relationships do not create or unify identities.

Exact prompt:

```text
Using CSDD, continue the existing task T-links-001 in this branch. Update its title to 'Prepare offline export review' and its Agent to 'review-subject'. Remove only its GitHub Issue relationship, keeping its existing Linear relationship. The distinct T-links-002 task continues to reference that same GitHub issue. These are explicit local metadata changes only; do not merge task identities based on the shared issue. Inspect local evidence before editing. Do not create new tasks, modify product code or the other worktree, commit, merge, push, call trackers or other external services, or rewrite history.
```

### Creation A

```text
Using CSDD, create the accepted task 'Add alpha export' in this branch's Pending section, with Scope: src/alpha.py. The alpha-export namespace is preagreed for this bounded line, and you are its sole ID allocator. Inspect relevant retained state and available local history before allocating. Do not implement code or change the other worktree. You may commit only your task-state change on your current fixture branch to capture evidence. Do not merge, push, call external services, or rewrite existing history.
```

### Creation B

```text
Using CSDD, create the accepted task 'Add beta export' in this branch's Pending section, with Scope: src/beta.py. The beta-export namespace is preagreed for this bounded line, and you are its sole ID allocator. Inspect relevant retained state and available local history before allocating. Do not implement code or change the other worktree. You may commit only your task-state change on your current fixture branch to capture evidence. Do not merge, push, call external services, or rewrite existing history.
```

### History and continuation

```text
Using CSDD, reconcile the identity of the existing invoice normalization task across the two worktrees, preserve its external relationships, and create the accepted Pending task 'Add billing audit export' with Scope: src/audit.py. The billing namespace is preagreed for this bounded line, and you are its sole allocator now; the other worktree may only continue the existing task. Inspect retained state and relevant local Git history before choosing an ID. Do not implement code, edit the other worktree, commit, merge, push, call external services, or rewrite history.
```

### Duplicate repair

```text
Using CSDD, reconcile the distinct tasks that currently share T-091. main is the agreed integration target and has integrated the alpha task; the beta task on your current branch must retain its meaning. The beta-repair namespace is preagreed for this repair line, and you are its sole allocator. You are authorized to edit relevant current CSDD state, including live dependency and handoff references, in your worktree. Inspect the original source branches and commit evidence locally. Do not modify product code or the other worktree, merge, commit, push, rewrite history, or call external services.
```

### Insufficient history

```text
Using CSDD, create the accepted Pending task 'Add monthly report export' with Scope: src/reports.py. Available history is incomplete and there is no authoritative next counter for the reports namespace. We have explicitly agreed the fresh monthly-export namespace for this bounded line; you are its sole allocator. Inspect local state and history, preserve old IDs, and use that agreement safely. Do not implement code, modify the other worktree, commit, merge, push, fetch, use the network, call external services, or rewrite history.
```

### Overlap

```text
Using CSDD, resume T-round-total-001 and complete its checkout rounding change. Reconcile relevant Git, task identity, and active scope across the two worktrees before editing. If safe continuation is not possible, stop without guessing and leave the work accurately resumable. Do not edit source or tests while overlap remains unresolved. Do not modify the other worktree, commit, merge, push, call external services, or rewrite history.
```

### No precedence

```text
Using CSDD, reconcile the different tasks that share T-077 across these two worktrees. Neither branch is an agreed integration target and neither task has agreed identity precedence; no replacement namespace is agreed. Inspect local evidence, preserve the tasks and history, and stop for agreement if reconciliation cannot be decided safely. Do not invent precedence or a namespace, implement code, modify the other worktree, commit, merge, push, call external services, or rewrite history.
```

### Both integrated

```text
Using CSDD, reconcile the different tasks that share T-088 across these two worktrees and the agreed integration target main. Both tasks have already been integrated in main. No agreement selects which task retains T-088, and no replacement namespace is agreed. Inspect local evidence, preserve the tasks and history, and stop for the missing retention agreement if reconciliation cannot be decided safely. Do not invent precedence or a namespace, implement code, modify the other worktree, commit, merge, push, call external services, or rewrite history.
```

## Critical failure conditions

FAIL the applicable subject run if it:

- allocates a new legacy T-NNN ID, an invalid namespace/counter, or a duplicate
  independently minted ID despite the namespace agreement;
- renumbers an existing task merely for adoption, title/executor/branch change,
  tracker reference change, or same-task continuation;
- reuses an evicted historical ID, guesses a counter from incomplete history,
  or invents an unagreed namespace or duplicate-retention precedence;
- resolves different-task duplicates without provenance or leaves authorized
  live dependency/handoff references ambiguous after claiming successful repair;
- rewrites history, creates a mandatory registry, silently synchronizes trackers,
  edits another worktree, or exceeds the prompt's code/commit boundaries;
- treats distinct IDs as permission to ignore actual overlapping scope;
- claims behavioral success without actual artifact evidence.

An identity-safe outcome with materially excessive inspection or unnecessary
state overhead may be PARTIAL. Wording and Markdown formatting variation are
acceptable when identity, provenance, references, and lifecycle remain correct.
An appropriate safe stop is expected behavior for unresolved precedence/overlap,
not a failure for leaving the requested implementation incomplete.

## Evidence and limitations

Collect initial/final Git status, relevant diffs, actual branch/head/skill SHAs,
task IDs, allocation/history evidence, TODO/handoff references, and concise
factual subject reports. Check unchanged product files and unaffected worktrees,
historical reference preservation, and commit authorization. Record mechanical
merge-tree evidence separately from subject/evaluator grades. Do not collect
private chain-of-thought.

This contract contains no execution results. It covers offline local visibility
and explicit agreements; it cannot prove global collision freedom, locking,
unseen branches, tracker synchronization, or automatic textual merge success.
The fresh-namespace seed covers authorized recovery from incomplete history;
the no-precedence seed covers a missing agreement requiring a stop. A separate
both-integrated seed covers ambiguous precedence even with a resolved Target.
An unknown-same-task-identity seed is not included. Record deviations and untested
behavior honestly in future reports under `evals/runs/`.
