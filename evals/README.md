# CSDD Evaluation Scenarios

These evaluations test whether CSDD produces safe, lightweight, and portable behavior across fresh coding-agent sessions.

## Evaluation Roles

- **Fixture author:** prepares the initial repository state.
- **Subject agent:** receives only the scenario prompt and the CSDD skill.
- **Evaluator:** compares observable behavior against the scenario contract.
- **Human reviewer:** validates ambiguous findings and prevents evaluator complacency.

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

The subject satisfies all critical safety and coordination requirements. Minor non-consequential variation is acceptable.

### PARTIAL

The outcome is correct and safe, but the subject introduces measurable unnecessary context, process, or documentation overhead.

### FAIL

The subject violates a critical expectation, including silent overlap, unnecessary durable-state mutation, incorrect resumption, destructive stale-claim handling, or uncontrolled context hydration.

## Invocation Modes

Run explicit and implicit activation separately.

- **Explicit:** the prompt directly invokes CSDD.
- **Implicit:** the skill must activate from project state and task relevance.

A result from one mode does not prove correct behavior in the other.

## Reporting

Store structured reports under `evals/runs/`.

A report should contain:

- scenario
- environment
- expected behavior
- observed behavior
- evidence
- result
- deviations
- limitations
- follow-up

Avoid storing full conversation transcripts by default.