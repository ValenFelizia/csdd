# TODO

## In Progress

## Pending

- [ ] T-013 — Define branch and worktree baseline reconciliation
  - Owner: valen
  - Scope: `SKILL.md`, `references/protocol.md`, `references/document-contracts.md`
  - Note: Ensure agents verify that their branch or worktree contains the intended CSDD coordination baseline before claiming or resuming collaborative work.
## Blocked

## Recently Completed

- [x] T-005 — Complete the Phase 0 conceptual protocol
- [x] T-006 — Create the initial CSDD document templates
- [x] T-007 — Define the operational contract of the initial CSDD skill
  - Owner: valen
  - Agent: codex/skill-design
  - Scope: `.csdd/**`, `references/**`
  - Updated: 2026-07-10
  - Note: Operational contract and consistency audit accepted; `SKILL.md` remains undrafted.
- [x] T-008 — Draft the initial CSDD SKILL.md
  - Owner: valen
  - Agent: cursor/skill-draft
  - Scope: `SKILL.md`, `.csdd/todo.md`
  - Updated: 2026-07-10
  - Note: Initial draft validated on main after restoring canonical `.csdd/` state from `codex/t-007-operational-contract`.
- [x] T-009 — Review `SKILL.md` against the protocol and document contracts
  - Owner: valen
  - Updated: 2026-07-10
- [x] T-010 — Run the first manual dogfooding task using CSDD
  - Owner: valen
  - Updated: 2026-07-11
  - Note:
- [x] T-011 — Run the first manual dogfooding task using CSDD
- [x] T-012 — Prepare the five formal validation scenarios
  - Owner: valen
  - Scope: released
  - Note: Five manual scenarios completed. Two protocol defects were discovered, corrected and revalidated succesfully.
- [x] T-014 — Tighten closure and canonical-truth contracts
  - Owner: valen
  - Agent: cursor/csdd-contracts
  - Scope: released
  - Updated: 2026-07-12
  - Note: Added closure claim-release rules, protected historical Agent metadata, and clarified canonical specs/decisions boundaries.
