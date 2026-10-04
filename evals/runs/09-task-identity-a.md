# Evaluation Run — Scenario 09 Run A — Local task identity

Nine fresh explicit subjects passed the artifact-based identity and coordination
checks. This is one offline campaign on one Windows harness, not a claim of
global uniqueness, automatic Markdown merging, or cross-harness portability.
The unresolved overlap and precedence cases passed by stopping safely.

## Campaign and independence

- Date: 2026-10-03.
- Harness: Codex desktop `collaboration.spawn_agent`.
- Model: inherited current harness configuration, with no model override. The
  exact model identifier was not exposed; no identifier is inferred.
- Invocation: explicit (`Using CSDD` in each exact prompt).
- Runtime skill commit: `da0feb18049ca8b02e034f6505b76cc1882f05f8`.
- Recorded fixture-source and scenario-contract commit (captured during the
  campaign):
  `64160795d956d744d9777bb6d95d30f5845b4836`.
- Contract: [09-task-identity.md](../scenarios/09-task-identity.md).
- Evaluator: independent `identity_final_evaluator`; neither fixture author nor
  subject. Subject labels are listed individually below.
- Evaluation checkout: `codex/task-id-namespaces` at fixture-source commit above
  when inspected. Evaluation did not change subject repositories.
- Environment directly observed: Microsoft Windows NT `10.0.26300.0`,
  PowerShell `7.6.5`, Git `2.54.0.windows.1`, Python `3.11.7`.

The fixture author prepared initial seeds and was interrupted before the root
completed the supplemental both-integrated/relationships seeds and integration
mechanics. Neither author nor root acted as a subject. A separate pre-run review
identified the ambiguous-precedence defect; the pinned runtime includes its
correction before subject exposure. All subject repository baselines and the
runtime were committed before dispatch. There were no behavioral reruns or
post-result subject repairs.

Source-commit timing deviation, reported by the orchestrator: the first
creation/history subjects were dispatched while the already-written pre-run
contract and materializer source were still uncommitted. Commit `6416079`
captured that source after the supplemental relationships seed was added and
while some subjects were active. Initial seed and prompt bytes did not change
after exposure, and the second materialization reproduces all nine seed heads.
Thus the report records a reproducible source snapshot, but cannot claim that
this source commit predates every subject invocation. Runtime policy remained
pinned before all subjects, and source/rubric remained hidden from them.

The orchestration record states that each subject received only the pinned
runtime, exact prompt, and its fixture; no rubric, manifest, other outputs, or
insufficient-history author repository. This isolation is reported by the
orchestrator, not independently instrumented. The evaluator received artifacts
and concise factual subject reports, not private reasoning or full tool logs.

## Evidence basis

`$RUN_ROOT` denotes the campaign's private temporary directory. Its
`manifest.json` records nine fresh seeds, 27 initially clean named worktrees,
exact prompts, source commits, and nine subject prompts to dispatch. The
materializer itself does not execute subjects: its `subject_executions` remains
empty and its baseline-only notice is not a result. Final state is separately
captured in `evidence.json`.

The evaluator directly queried all 27 worktrees with `git status --porcelain=v1`,
`git branch --show-current`, `git rev-parse HEAD`, and
`git diff <initial-head> -- .`. All branches, heads, statuses, and 108 canonical
document SHA-256 hashes matched the final snapshot. Across all 27 worktrees,
`git diff <initial-head> -- . ':(exclude).csdd'` was empty. No unexpected
untracked files were observed. Only the two authorized creation subjects
advanced HEAD; each commit changes only `.csdd/todo.md`. Every unaffected named
worktree retained its initial HEAD, clean status, and canonical state.

Historical task assignment, same-task continuation, repair provenance,
integration ancestry, shallow-object unavailability, and the rounding hazard
were also inspected directly with `git show`, `git diff`,
`git merge-base --is-ancestor`, `git cat-file`, and local file reads. Actual
creation integration commits were read without performing a merge or rewriting
fixtures. The normalized [JSON companion](09-task-identity-a.json) records
source and subject SHAs, observed diffs/status, document hashes, mechanical
results, and snapshot digests without full transcripts or personal paths.

## Subject results

| Subject | Result | Expected and observed artifact behavior |
| --- | --- | --- |
| creation-a | PASS | Exactly one accepted Pending task, `T-alpha-export-001`, with `src/alpha.py`; two inserted TODO lines, no active executor, no registry or product change. Authorized task-state commit only. |
| creation-b | PASS | Exactly one accepted Pending task, `T-beta-export-001`, with `src/beta.py`; two inserted TODO lines, no active executor, no registry or product change. Authorized task-state commit only. |
| history | PASS | Preserves `T-billing-003` in both worktrees, both full GitHub/Linear relationships, and the no-URL `T-billing-004`. Creates Pending `T-billing-042`, above evicted `T-billing-041`, rather than retained maximum `012`. Only its TODO changes. |
| repair | PASS | Preserves integrated alpha `T-091`; renames only beta to `T-beta-repair-001`, retaining human Owner, meaning, scope, execution metadata, and original branch/commit provenance. Updates live dependency and handoff. No target TODO import or unqualified alias. |
| insufficient | PASS | Preserves `T-reports-002`, discloses incomplete history, and creates only agreed fresh `T-monthly-export-001`. Does not guess the old reports counter or claim complete historical coverage. |
| overlap | PASS | Keeps `T-round-total-001` and human Owner, moves it to Blocked, releases its active claim, and records the round-sum versus sum-rounded-lines hazard and required coordination. Leaves source/tests and the other claim untouched. |
| no-precedence | PASS | Keeps alpha `T-077`, Owner, Agent, and protected partial scope; records the distinct beta task and missing Target/retention/namespace agreement. No unilateral precedence choice, replacement allocation, or implementation. |
| both-integrated | PASS | Verifies both source tasks are ancestors of agreed `main` and both distinct completed `T-088` entries remain there. Blocks identity reconciliation, keeps beta ID/Owner/Agent, releases scope, and does not choose precedence from integration order. |
| relationships | PASS | Changes only the authorized title, Agent, and first task's Issue relationship. Preserves `T-links-001`, its Linear URL, distinct `T-links-002`, and that task's shared GitHub URL. Other worktree untouched. |

All subjects preserve the six canonical TODO H2 headings and `Retention: 5`.
Existing histories and historical references remain available; no new legacy ID,
mandatory registry, migration, or tracker requirement appears. The history,
repair, and blocking Notes are longer than the minimum but contain relevant
continuation/provenance/resumption evidence and add no extra document. They do
not establish materially excessive overhead sufficient for PARTIAL here.

### Actual branches and subject checkout commits

| Subject | Branch | Start SHA | End SHA |
| --- | --- | --- | --- |
| creation-a | fixture/alpha | `6c1c0699e32d6a27d8ea33e4bd8011337706ffe2` | `828d9d988c7b9fa3e0abe3abffc06b4440e12a9c` |
| creation-b | fixture/beta | `6c1c0699e32d6a27d8ea33e4bd8011337706ffe2` | `d31653444b7e26d8ecb6c15528bf89e0cefa9223` |
| history | fixture/billing-a | `80431ffef7ed0c4318c597d27cd94e1431b7bdbd` | `80431ffef7ed0c4318c597d27cd94e1431b7bdbd` |
| repair | fixture/beta | `87d7dc17c60e84b591fad40c2decb92702660e50` | `87d7dc17c60e84b591fad40c2decb92702660e50` |
| insufficient | fixture/reports-a | `725a9868a445996d761d7c37cc554c32c7fcba8e` | `725a9868a445996d761d7c37cc554c32c7fcba8e` |
| overlap | fixture/round-total | `b01c83db4e43bb698c7f513ef49e5cf0aeb3cd43` | `b01c83db4e43bb698c7f513ef49e5cf0aeb3cd43` |
| no-precedence | fixture/alpha | `baa3d131b0504a39a4d4f9f9b853ef9e5d074cc9` | `baa3d131b0504a39a4d4f9f9b853ef9e5d074cc9` |
| both-integrated | fixture/beta | `80712bf899e169ece976e6aa378bda79a4f5d6e3` | `80712bf899e169ece976e6aa378bda79a4f5d6e3` |
| relationships | fixture/links-a | `621cfe6ad23ac1282201ca08ef2e23480915ad4b` | `621cfe6ad23ac1282201ca08ef2e23480915ad4b` |

Only repair changes `.csdd/handoff.md` in addition to TODO. The other seven
noncreation subjects retain uncommitted task-state changes exactly as authorized.

### Specific evidence anchors

- History: `git show 9fe4924e3058a64d0fbd787cfa08efd6968a73a4:.csdd/todo.md`
  contains `T-billing-041`; retained head contains only completed `012` through
  `008`. Continuation `293ca8f205864f68a54248536a1425611b616176` adds invoice
  trimming and its `T-billing-003` handoff without changing task identity.
- Repair: target alpha `f34aec5737b2feb26a6604fa7c8812f79dcaa3ce` is reachable
  from `main`; original beta `87d7dc17c60e84b591fad40c2decb92702660e50` is not.
  The beta Note retains former `T-091`, `Add beta CSV export`, `src/beta.py`,
  `fixture/beta`, and the exact observed beta commit. `Depends on:` and the
  handoff heading/body now use `T-beta-repair-001`.
- Insufficient: `git rev-parse --is-shallow-repository` returns `true` and
  `git remote -v` is empty. Hidden author-only assignment object
  `09af786dd3c45c19a453bf3a6dd51f41ad08238e` is unavailable in the subject
  repository (`git cat-file -t`, exit 128). It is not subject input.
- Overlap: one source returns `round(sum(items), 2)` and the other returns
  `sum(round(item, 2) for item in items)`. The existing test artifact states
  that rounding order is under discussion. Distinct IDs do not reconcile this.
- Both integrated: source commits `a802572bd1a79d2f1d1ae944c8943d484d6bd3c5`
  and `80712bf899e169ece976e6aa378bda79a4f5d6e3` each return exit 0 for
  `git merge-base --is-ancestor <source> main`; target
  `fe55a9e3f1a44647118ce9464ccf1dff7705e147` retains both distinct completed
  exports under `T-088`. Both implementations are present.

## Mechanical observations, separate from behavior grades

The root ran `git merge-tree --write-tree <first> <second>` and recorded output
in `$RUN_ROOT/mechanical-results.json`. The evaluator inspected the actual
source/subject commits and resulting tree/commit evidence; it did not rerun a
write-tree command against fixtures.

| Input | Orders | Exit | Conflict paths |
| --- | --- | --- | --- |
| Legacy alpha `30a48f92a5cfa80676c3f829108dfe58342b2fc9` / beta `e930fc915cb5da27649a9d0c52e5becfce518d12` | Both | 1 / 1 | `.csdd/todo.md`, `.csdd/handoff.md` |
| Actual creation commits `828d9d988c7b9fa3e0abe3abffc06b4440e12a9c` / `d31653444b7e26d8ecb6c15528bf89e0cefa9223` | Both | 1 / 1 | `.csdd/todo.md` |
| Overlap total `b01c83db4e43bb698c7f513ef49e5cf0aeb3cd43` / line `924c36c1da9f8504811ccffe94e7f1ec700f9fd0` | Total then line only | 1 | `.csdd/todo.md`, `src/checkout.py` |

Legacy conflict trees are `2cdf820760fd58848eb0ae74bcee4167659ef842` and
`aaf52799db0ca67df830dde2e0e5d0f2a349b5e1`; actual creation conflict trees
are `488b52be95cff40cd9ee55b3b239fa0f40a3f92a` and
`a3cc4d88978a6978d6ea34d7fc0b8ea4cdd13b5d`.

The root then explicitly resolved only creation TODO contention by concatenating
the actual subject-created Pending blocks in each order. The resulting clean
mechanical integration commits are
`e92e8a7fa1b051466d24b4decda172cd7e4d4e06` (alpha/beta parents) and
`fdf3eef1bfc82f41aaaf5f61d6e716691ea4c153` (beta/alpha parents). Direct
inspection confirms both distinct IDs exactly once, canonical headings and
retention, and no product delta. This is harness-authored explicit resolution,
not a subject action, automatic identity merge, or #42 contention policy. The
legacy fixture was not repaired; it has no behavioral grade.

## Materialization and repository validation

The materializer command is
`python evals/fixtures/task_identity.py --output-root <absolute-new-root>`.
The root recorded a second fresh materialization and refusal checks. Independent
comparison of the two manifests confirms all nine seeds and all 27 baseline
heads are identical. Relative and already-existing output roots were refused
with exit 2. No repeat subject executions were used for these mechanical checks.

Root-run checks, separate from subject grades: `python -B -m unittest discover
-s tests -v` passed 19 tests; `python -B scripts/validate_repository.py` reported
`Validation passed`; `git diff --check` and the CRLF-aware staged equivalent
`git -c core.whitespace=cr-at-eol diff --cached --check` passed at the recorded
pre-report stage. This evaluator did not rerun tests or claim CI verification.
No existing tests, CI, or mandatory parser were changed by this evaluation.

The auxiliary skill-creator `quick_validate.py` command was unavailable because
its Python import failed with `ModuleNotFoundError: No module named 'yaml'`;
the bundled interpreter also lacked PyYAML. No installation was attempted.
This is an auxiliary environment limitation, not a behavioral failure or a
failure of the repository's successful stdlib validator.

## Limits and follow-up

Artifact checks support local outcomes. Subject inspection-history and
no-external-call assertions are concise self-reports; complete tool traces and
egress instrumentation were unavailable. Unchanged local state cannot prove
that no external service was contacted. No locking, tracker synchronization,
global namespace uniqueness, unseen branches/history, implicit invocation,
other model/harness, or unknown-same-task-identity case was tested. A depth-one
subject plus agreed fresh namespace does not validate guessing without that
agreement. Exact model identity was unavailable and constrains reproducibility.

No observed identity defect requires a behavioral rerun or runtime correction.
Human review of a draft PR for issue #41 remains separate from this local evaluation.
Future implicit/cross-harness or unknown-identity coverage requires separately
declared fresh runs; #42 textual contention remains independently unresolved.
