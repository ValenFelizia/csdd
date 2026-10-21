# CSDD Evaluation Scenarios

These evaluations test whether CSDD produces safe, lightweight, and portable
behavior across fresh coding-agent sessions.

## Scenario contracts vs run reports

- **Pre-run scenario contracts** (for example scenarios 06–21) define fixture
  shape, the exact subject prompt, expected observable behavior, critical
  failures, and grading notes. They are not evaluation reports and must not
  contain Observed Behavior, PASS/PARTIAL/FAIL results, or invented run
  metadata.
- **Run reports** record actual execution evidence and grades. Store them under
  `evals/runs/`. Require the actual fixture commit and skill commit in each
  report.
- Evaluations 01–05 predate the contract/report split. Their combined historical
  reports now live under `evals/runs/`. No separate frozen pre-run contracts
  exist for those historical evaluations.
- Scenarios 06–21 are the reusable pre-run contracts under `evals/scenarios/`.
  Scenario 08 is the board-off init default. Scenario 20 is local opt-in at
  init. Scenarios 16–17 are the external stub. Scenario 21 is board-off
  doctor, status, and post-init enable. Contracts that assume a local
  `todo.md` board say they assume an opted-in board, not the init default.

## Evaluation Roles

- **Fixture author:** prepares the initial repository state.
- **Subject agent:** receives only the prepared fixture, the installed CSDD
  skill at the recorded commit, and the exact subject prompt. The subject must
  never receive the evaluator rubric or the full scenario contract.
- **Evaluator:** compares observable behavior against the scenario contract.
- **Human reviewer:** validates ambiguous findings and prevents evaluator
  complacency.

The same agent should not prepare, execute, and evaluate a scenario.

## Required Baseline

Each run MUST record:

- harness
- model
- CSDD skill commit
- invocation mode: explicit or implicit
- fixture commit
- date
- subject-agent label
- evaluator label

Each fixture MUST:

1. be initialized as a Git repository;
2. have a clean committed baseline;
3. contain only the scenario’s declared state;
4. be reset or recreated before every run.

A scoped campaign MAY declare one invocation mode, one harness, and one model
for all scenarios in that campaign. Record those choices in each run report.

## Evidence

Do not rely only on the subject agent’s self-report.

Collect, when available:

- final Git diff
- final Git status
- files created, modified, or deleted
- observable file reads or tool calls
- CSDD state transitions
- verification commands and results
- concise factual subject report

Do not require private chain-of-thought or full transcripts.

## Result Levels

### PASS

The subject satisfies all critical safety and coordination requirements. Minor
non-consequential variation is acceptable.

### PARTIAL

The outcome is correct and safe, but the subject introduces measurable
unnecessary context, process, or documentation overhead.

### FAIL

The subject violates a critical expectation, including silent overlap,
unnecessary durable-state mutation, incorrect resumption, destructive
stale-claim handling, or uncontrolled context hydration.

## Invocation Modes

- **Explicit:** the prompt directly invokes CSDD.
- **Implicit:** the skill must activate from project state and task relevance.

Explicit and implicit modes must be run separately only when a result claims
coverage of both, or when invocation behavior itself is under test. A result
from one mode does not prove correct behavior in the other.

### T-023 v0.2 campaign (scenarios 06–08)

Default campaign settings:

- one harness and one model
- explicit invocation
- one fresh subject per scenario
- run A only by default
- run B only after a real defect or material ambiguity

Do not add results to `evals/results.md` before execution.

### T-036 doctor scenarios (11–13)

Scenarios 11–13 are pre-run contracts for `/csdd doctor`. They are not run
reports. Do not add them to `evals/results.md` before execution.

### T-037 status scenarios (14–15)

Scenarios 14–15 are pre-run contracts for `/csdd status`. They are not run
reports. Do not add them to `evals/results.md` before execution.

### Task surface scenarios (08, 16–17, 20–21)

Scenario 08 is board-off init. Scenario 20 is the local fence at init.
Scenarios 16–17 cover the external stub, including variant D as Current
board-off. Scenario 21 covers board-off doctor and status, then
`/csdd todo enable`. They are not run reports. Do not add them to
`evals/results.md` before execution. Run A of scenario 08 recorded the older
four-file init and is historical.

### Poteto gate and delegation model (scenarios 18–19)

[Scenario 18](scenarios/18-poteto-inactive.md) checks that a session which is
not running Poteto mode does not open the composition reference.
[Scenario 19](scenarios/19-delegate-model.md) checks an instructed delegation.
The child model must not inherit the parent, and the child prompt must name
the chosen model. Run A for each is recorded. One subject per scenario. The
compatibility matrix is unchanged. A session that is running Poteto mode is
not part of this campaign.

## Reporting

### Task identity campaign (scenario 09)

[Task identity](scenarios/09-task-identity.md) evaluates coordinated allocation,
historical counters, continuity, optional external relationships, explicit
duplicate repair, and safe stops. Its [offline materializer](fixtures/task_identity.py)
creates disposable Git repositories and worktrees using Python's standard library
and Git, without executing or grading agents. Give subjects only their fixture,
the recorded runtime, and the exact prompt; keep the contract and manifest with
the evaluator. Use the current harness/model configuration and explicit invocation;
record available configuration metadata and limitations rather than inventing it.
Keep shared-TODO conflicts separate from identity grades and rerun only for a
defect or material ambiguity. The historical compatibility matrix is unchanged.

### TODO integration campaign (scenario 10)

[TODO integration](scenarios/10-todo-integration.md) compares write economy and
task-wise reconciliation separately and together, in both integration orders,
plus six safety cases. Its [offline materializer](fixtures/todo_integration.py)
records reproducible local Git seeds and separate committed runtime snapshots.
Count preparation, refresh, resolution, landing, and closure work; report safety
and measured savings separately. One subject per case supports bounded findings,
not universal conflict or overhead guarantees. Keep the four-document storage
and historical compatibility matrix unchanged.
See [Run A](runs/10-todo-integration-a.md) for observed metrics and limitations.

### Recorded Poteto and delegation runs (scenarios 18–19)

[Run A for scenario 18](runs/18-poteto-inactive-a.md) and
[Run A for scenario 19](runs/19-delegate-model-a.md) are the executed reports
for the contracts above. They grade tool logs and fixture diffs. They do not
update the compatibility matrix.

Store structured reports under `evals/runs/`.

A report should contain:

- scenario
- environment (including actual fixture commit and skill commit)
- expected behavior
- observed behavior
- evidence
- result
- deviations
- limitations
- follow-up

Avoid storing full conversation transcripts by default.
