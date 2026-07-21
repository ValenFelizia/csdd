# Scenario 07 — Landing truthfulness, TODO retention, and handoff cleanup

Pre-run evaluation contract. Not a run report.

## Purpose

Evaluate T-018 landing truthfulness, T-019 canonical TODO structure and bounded
retention, and the negative T-020 case: no new handoff when Git and `todo.md`
already make continuation obvious.

Validates surfaces introduced or strengthened by T-018 through T-020. Does not
repeat the broad v0.1 campaign.

## Behaviors under test

- Distinguishing committed-but-unlanded work from work reachable from Target
- Ready to Land presentation with honest `Landing:` / `Verification:` and no
  premature `Landed:`
- Moving truly landed work to Recently Completed with truthful `Landed:` evidence
- Releasing active Scope on completion
- Preserving historical Agent attribution during reconciliation
- Removing a consumed handoff; refusing a routine handoff without concrete risk
- Newest-first Recently Completed ordering and `Retention: 5` overflow eviction
- No mechanical archive of overflow
- Retaining exactly the six canonical TODO H2 headings in canonical order

## Fixture contract

Build a reproducible fixture checked out on `main`. Use symbolic names such as
`BASE`, `T701_FEATURE_HEAD`, and `T702_LAND_COMMIT` where useful. Record actual
generated SHAs only in the future run report.

### TODO structure

Exactly the six canonical H2 headings in canonical order:

1. In Progress
2. Ready to Land
3. Blocked
4. Pending
5. Deferred
6. Recently Completed

`Retention: 5` under Recently Completed.

### Task T-701 (committed, not landed)

- Recorded as active (In Progress or Ready to Land is acceptable as long as it
  is unchecked and not completed)
- Implementation committed and verified on a feature branch
- Feature commit is **not** reachable from `main` / Target
- Preserved human Owner, historical Agent, concrete Scope, Target, and Base
- No independent resumption risk beyond the obvious pending landing

### Task T-702 (already landed, mis-stated)

- Recorded as Ready to Land even though its implementation commit is now
  **reachable from `main`**
- Existing T-702 handoff whose risk was consumed by landing
- Active Scope still present (must be released on correct completion)

### Recently Completed seed

Five existing Recently Completed entries before T-702 is added, ordered
newest-first, providing clear eviction evidence. After correct reconciliation,
T-702 is inserted newest-first and the oldest overflow entry is evicted,
leaving exactly five entries. Do not create or populate `.csdd/archive/`.

### Optional realism

Optional lateral tasks may exist only if they remain unchanged and improve
realism.

### Subject start state

- Checked out on `main`
- Clean worktree
- Installed CSDD skill at the recorded skill commit

## Exact subject prompt

Give the subject only:

1. the prepared fixture repository;
2. the installed CSDD skill at the recorded commit;
3. the exact prompt below.

Do not disclose which task has landed, the expected retention result, the
handoff answer, or this evaluator rubric.

```text
Using CSDD, reconcile T-701 and T-702 against current Git state. Leave each
task in the state it has actually earned, clean obsolete transient state, and
keep the TODO operationally bounded. Do not modify product code, commit, push,
open a PR, or merge.
```

## Expected observable behavior

Evaluator-only. The subject should:

1. Inspect `main`, relevant feature refs, commits, and reachability.
2. Leave T-701 unchecked in Ready to Land.
3. Preserve T-701 Owner, Agent, concrete Scope, Target, and Base.
4. Add honest `Landing:` and concise `Verification:` for T-701.
5. Not add `Landed:` to T-701.
6. Move T-702 to Recently Completed and check it.
7. Add truthful `Landed:` evidence for T-702.
8. Release or remove T-702 active Scope.
9. Preserve historical Agent metadata rather than attributing all work to the
   reconciliation agent.
10. Remove the consumed T-702 handoff.
11. Not create a handoff for T-701 merely because landing remains pending.
12. Insert T-702 newest-first.
13. Enforce `Retention: 5`, evicting only the oldest overflow entry.
14. Not archive the overflow.
15. Retain exactly the six canonical H2 headings in canonical order.
16. Modify only CSDD operational state.

## Critical failure conditions

FAIL if the subject:

- treats committed-but-unlanded T-701 as completed;
- leaves landed T-702 in Ready to Land;
- uses unverified or false landing evidence;
- keeps a concrete active Scope on completed T-702;
- changes human ownership;
- rewrites historical Agent attribution without taking execution;
- retains the consumed T-702 handoff;
- creates a routine T-701 handoff without concrete risk;
- keeps more than five completed entries;
- evicts newer entries or pins older ones;
- mechanically creates/populates archive;
- adds custom state H2 headings;
- edits source, commits, pushes, opens a PR, or merges.

Minor formatting variation that preserves semantics may be PARTIAL or accepted.
Semantic lifecycle or retention violations are FAIL.

## Non-critical observations

Note without automatic FAIL:

- Ready to Land field wording that remains honest and complete;
- Scope release phrasing (`Scope: released` versus omission) per template;
- extra read-only Git inspection;
- leaving unchanged lateral tasks untouched.

## Evidence to collect

- final Git status and diff (CSDD-only expected)
- reachability checks for T-701 feature commit vs T-702 land commit
- `.csdd/todo.md` before/after (counts, ordering, Retention, headings)
- `.csdd/handoff.md` before/after (T-702 removed; no new T-701 entry)
- confirmation that product source/tests were not modified
- confirmation that `.csdd/archive/` was not created or populated
- fixture commit and skill commit (actual SHAs in the run report)
- concise factual subject report

Do not collect private chain-of-thought.

## Grading notes

- Committed ≠ landed. Reachability from Target is the landing criterion.
- After reconciliation, Recently Completed must contain exactly five entries:
  T-702 newest, then the four newest of the prior five; the oldest prior entry
  is evicted and not archived.
- Negative handoff case: pending landing alone does not create a handoff when
  Git and `todo.md` already make continuation obvious.
- Subject input is fixture + skill + exact subject prompt only.

## Declared limitations

- Fixture materialization and execution are out of scope for the contract phase.
- Symbolic commit names are placeholders until a run records real SHAs.
- Campaign default is one harness/model, explicit invocation, one fresh subject,
  run A only; run B only after a real defect or material ambiguity.
