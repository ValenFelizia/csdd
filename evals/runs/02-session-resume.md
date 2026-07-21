# Evaluation Run 002 — Session Resume

## Environment

- Harness: Cursor
- Model: Grok 4.5
- CSDD invocation: explicit
- Git Repository: yes
- Date: 2026-07-11

## Scenario

A fresh agent must resume partially completed password-reset token work without access to the previous session.

## Expected Behavior

- Classify the task as operational continuation work.
- Read relevant TODO, handoff, specifications, and decisions.
- Validate the handoff against repository reality.
- Preserve completed token-generation work.
- Implement token consumption and corresponding tests.
- Update operational state truthfully.
- Remove obsolete handoff state.
- Avoid archive and unrelated protocol hydration.

## Observed Behavior

The subject classified the task as Level 2 — Operational.

It read:

- `.csdd/todo.md`
- `.csdd/handoff.md`
- `.csdd/specs.md`
- `.csdd/decisions.md`

It inspected the existing token store, token generation, incomplete consumption implementation, tests, and project configuration.

The handoff matched repository reality. Existing generation and hashed-storage work was preserved.

The subject implemented:

- successful token consumption
- unknown-token rejection
- expired-token rejection
- second-use rejection

It reused the accepted SHA-256 token-storage decision and existing store APIs.

All five tests passed.

T-201 was moved from In Progress to Recently Completed, active scope was released, and the obsolete handoff entry was removed.

## Result

PASS

The fresh agent reconstructed sufficient project context, preserved prior work, respected durable decisions, completed the task, and left CSDD state consistent without unnecessary deep hydration.

## Deviations and Limitations

- `node_modules/.vite/` appeared in the Git diff because dependencies were included in the fixture baseline. Future fixtures must ignore `node_modules/`.
- Some CSDD metadata used `YYYY-MM-DD` placeholders rather than real dates.
- This run tested explicit skill invocation only.
- The fixture did not test contradictory handoff state.

## Follow-up

- Add a fixture `.gitignore`.
- Use real dates in future baselines.
- Repeat the scenario with implicit skill activation.
- Preserve this scenario for future cross-harness comparisons.