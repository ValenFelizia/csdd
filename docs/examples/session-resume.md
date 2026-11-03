# Example: session resume with adaptive hydration

Concrete walkthrough of the same resumable task with and without CSDD.
Readable summary also lives in the [README](../../README.md#before-after-session-resume).

## Sources

| Kind | Path | Role |
| --- | --- | --- |
| Run report | [`evals/runs/02-session-resume.md`](../../evals/runs/02-session-resume.md) | PASS run: fresh agent resumes password-reset work |
| Run report | [`evals/runs/01-trivial-edit.md`](../../evals/runs/01-trivial-edit.md) | PASS (minor observation): Level 0 skips CSDD contents |
| Results matrix | [`evals/results.md`](../../evals/results.md) | Final grades for scenarios 01–02 |
| Protocol intent | [`references/protocol.md`](../../references/protocol.md#planned-validation-scenarios) | Planned scenarios 1–2: no hydration vs fresh resume |
| Field observation | [`field-reports/001-v0.1-real-world-usage.md`](../../field-reports/001-v0.1-real-world-usage.md) | Qualitative: less repeated explanation between sessions |

Scenarios 01–05 predate the contract/report split; their historical reports live
under `evals/runs/` (see [`evals/README.md`](../../evals/README.md)). There is
no separate frozen pre-run contract file for scenario 02, and no recorded
counterfactual run that executed the same fixture without CSDD installed.

## The task

A prior session left password-reset work half done: token generation and hashed
persistence were complete; token consumption was not. A **fresh** agent — no
prior conversation — must finish consumption and tests without redoing finished
work or inventing a new storage approach.

That matches planned validation scenario 2 in the protocol: one agent starts a
feature and a fresh agent resumes it later.

## Without CSDD

Without durable project state, the next session has only the repository and a
new chat. Typical failure modes the protocol targets:

- **Lost continuity** — nothing records that generation is done and consumption
  remains, so the agent re-explains or re-implements finished work.
- **Unconditional loading** — hoping for context, the agent reads broad history,
  docs, or unrelated modules instead of a bounded operational set.
- **Decision drift** — an accepted choice (here, SHA-256 hashed token storage)
  lives only in a dead conversation and is easy to contradict.

These are design targets and field observations, not measurements from a
without-CSDD eval run on this fixture.

## With CSDD (recorded run 02)

From [`evals/runs/02-session-resume.md`](../../evals/runs/02-session-resume.md)
(Cursor, Grok 4.5, explicit invocation, 2026-07-11), result **PASS**:

1. **Classify** — Level 2 — Operational (multi-file, resumable work).
2. **Hydrate only what the level needs** — read:
   - `.csdd/todo.md`
   - `.csdd/handoff.md`
   - `.csdd/specs.md`
   - `.csdd/decisions.md`
3. **Skip cold / unrelated context** — expected and observed: avoid archive and
   unrelated protocol hydration.
4. **Validate against the repo** — handoff matched reality; existing generation
   and hashed-storage work was preserved.
5. **Continue** — implement successful consumption plus unknown-token,
   expired-token, and second-use rejection; reuse the accepted SHA-256 storage
   decision and existing store APIs.
6. **Verify and close** — all five tests passed; T-201 moved to Recently
   Completed; active scope released; obsolete handoff removed.

No token-count or “files in the whole repo” metrics appear in that run report.
What is recorded is the document set read, the restraint against deep
hydration, and the outcome (PASS, five tests green).

## Contrast: trivial work stays cheap (run 01)

Adaptive hydration is not “always load the four documents.”

From [`evals/runs/01-trivial-edit.md`](../../evals/runs/01-trivial-edit.md):
change a button label `Enviar` → `Guardar`. The subject classified **Level 0 —
Direct**, read `src/button.tsx` only for the edit, confirmed `.csdd/` exists
via a glob, and **did not read any `.csdd/` document contents**. Result: PASS
with a minor observation about that existence glob.

Together, runs 01 and 02 show the same rule applied twice: load the minimum
sufficient context — none of the CSDD documents for a trivial label change;
exactly the operational four for a session resume.

## What this does not claim

- It does not claim a measured token or dollar delta versus a without-CSDD
  control on the same fixture.
- It does not claim implicit skill activation; both cited runs used explicit
  invocation.
- It does not replace the full evaluation matrix in
  [`evals/results.md`](../../evals/results.md).
