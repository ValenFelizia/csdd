# CSDD Evaluation Scenarios

These evaluations test whether CSDD produces safe, lightweight, and portable
behavior across fresh coding-agent sessions.

## Scenario contracts vs run reports

- **Pre-run scenario contracts** (for example scenarios 06–08) define fixture
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
- Scenarios 06–08 are the reusable pre-run contracts under `evals/scenarios/`.

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

## Reporting

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
