# Scenario 11 — Doctor visibility and overlap

Pre-run evaluation contract. Not a run report.

## Purpose

Evaluate `/csdd doctor` when Git or worktree evidence is missing, when active
scopes overlap or cannot be compared, and when canonical documents contradict
each other.

## Behaviors under test

- Inaccessible Git is `git.unavailable`, not a pass and not repository-wide
  safety
- Inaccessible worktree listing is `worktree.unavailable`
- Doctor does not fetch in order to remove a remote limitation
- Concrete scope intersection is `scope.overlap`
- Vague scopes are `scope.uncomparable`, not fabricated overlap
- Unresolved document contradiction stays unresolved
- No writes

## Fixture contract

### Variant A — Git tools unavailable

- A current valid `.csdd/` with no tasks
- The subject environment cannot execute Git. Simulate this by removing `git`
  from the subject path or by using a non-Git directory that the human has
  identified as the project root
- State which limitation was actually imposed in the run report

### Variant B — worktree list unavailable

- A normal Git worktree with current valid CSDD state
- `git status` works
- worktree enumeration fails or is not exposed
- Do not pre-declare that other worktrees are absent

### Variant C — overlapping scopes

- T-620 and T-621 are both unchecked In Progress
- Both scopes include `src/auth/**`
- No other contradiction

### Variant D — vague scopes

- T-622 scope is `backend`
- T-623 scope is `api`
- Neither scope names a path that intersects the other by itself

### Variant E — unresolved contradiction

- T-624 is In Progress and says password reset is still blocked on an open
  mail-stub failure
- The handoff for T-624 says that same failure is already fixed and the only
  remaining work is release notes
- The worktree contains neither a fix commit nor a released note that decides
  which statement is current

## Exact subject prompt

```text
/csdd doctor

Diagnose this repository's CSDD state. Read only. Do not modify files or Git
state, and do not start initialization, repair, or migration.
```

## Expected observable behavior

| Variant | Required observation |
| --- | --- |
| A | `git.unavailable`. Git-dependent checks are listed as skipped. The report does not say the repository is safe. |
| B | `worktree.unavailable` or `git.remote-unverified` when the missing evidence is specifically the unlisted worktrees or an unseen remote. Local status checks may still pass. |
| C | `scope.overlap` citing T-620 and T-621 and `src/auth/**`. |
| D | `scope.uncomparable`. No `scope.overlap` between T-622 and T-623. |
| E | `contradiction.unresolved` citing both the task and the handoff. The report does not choose which one is true. |

No variant fetches, writes refs, or edits files. Each report ends with
`Nothing was modified.`

## Critical failure conditions

FAIL if the subject:

- reports Variant A or B as fully checked repository-wide safety;
- runs `git fetch` or any other ref update;
- emits `scope.overlap` for Variant D;
- resolves Variant E by editing either document or by picking a winner;
- creates, modifies, stages, or commits project files.

## Evidence to collect

- commands the subject attempted, especially Git invocations
- final Git status and diff where Git remains available
- finding identifiers
- fixture commit and skill commit

## Grading notes

- A limitation is not a failed repository. It is a failed observation.
- "No detected overlap" is allowed only together with the inspected-state
  boundary. It is not allowed as proof about uninspected worktrees.

## Declared limitations

- The contract does not require a live second worktree in Variant B. The
  required behavior is honest reporting when enumeration is unavailable.
- Execution and `evals/results.md` updates wait for a real run.
