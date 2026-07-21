# Migrating CSDD v0.1 → v0.2

This guide applies only to recognizable CSDD v0.1 state. It is not `/csdd init`,
not a generic repair workflow, and does not define a `/csdd migrate` command.
It does not run automatically.

[`protocol.md`](protocol.md) and [`document-contracts.md`](document-contracts.md)
remain authoritative. This guide is operational and non-normative.

## Migration principle

Do not replace an existing `.csdd/` with the v0.2 templates. Preserve valid
project truth and coordination state while bringing the existing documents into
conformance with v0.2.

## Suggested workflow

### 1. Preflight

Resolve the canonical root, Target, Base, Git/worktree state, active claims,
and unrelated dirty state. Stop on unresolved overlap or ambiguous CSDD state.

### 2. Inventory

Inspect the existing four documents and any optional archive. Identify valid
durable truth, operational state, transient state, untouched placeholders,
contradictions, and ambiguous content. Do not modify yet.

### 3. Transform in place

Preserve valid existing content. Add required v0.2 structure. Move or remove
content only when its classification is supported. Surface ambiguity instead of
guessing.

### 4. Verify

Confirm v0.2 structure and semantics. Confirm no valid truth or live
coordination state was lost. Inspect the resulting diff and unrelated
working-tree state.

## Document-by-document transformation

### `specs.md`

Preserve supported durable requirements, constraints, invariants, and
contracts. Do not infer durable intent from code. Do not rewrite valid content
merely to resemble the template. Relocate operational content only when its
correct destination is clear.

### `todo.md`

Add and order the six canonical state headings: In Progress, Ready to Land,
Blocked, Pending, Deferred, Recently Completed. Keep each task under exactly
one state. Preserve current task meaning and human Owner. Do not invent Agent,
Scope, readiness, deferral, dependencies, or completion.

Add `Retention: 5` unless an explicit valid project policy already defines a
different positive retention value. Validate Ready to Land against Git-aware
landing evidence. Validate Deferred against authoritative intent, Reason, and
Resume when. Compact Recently Completed only after confirming overflow is not
carrying active coordination or durable truth. Do not create or populate
archive mechanically.

### `decisions.md`

Preserve real decisions regardless of their ID. Remove `DEC-001` only when it
is clearly the untouched fictional v0.1 placeholder. Never delete a populated
real `DEC-001` merely because the template used that identifier. Do not
reconstruct rationale from implementation.

### `handoff.md`

Retain an entry only when a real boundary and concrete resumption risk still
exist. Validate entries against Git and current `todo.md`. Reduce surviving
entries to one current replaceable snapshot. Remove consumed or false entries.
Do not remove ambiguous entries based only on age—surface the uncertainty.

### Optional `archive/`

Preserve it if it already exists. Do not create it during migration. Do not
move overflow or history into it automatically. Keep it outside default
hydration.

## Incremental adoption

Using the v0.2 skill in a v0.1 repository does not authorize an autonomous
repository-wide migration.

During otherwise authorized CSDD work, an agent may reconcile the specific
document it must update when the missing v0.2 change is mechanical,
non-destructive, and inside current Scope—for example adding missing empty
state headings or `Retention`. Semantic reclassification, deletion,
cross-document movement, or ambiguous cleanup must be surfaced rather than
performed silently.

Incremental conformance of one document must not be reported as completion of
the full migration.

Do not introduce `backlog.md` or any other new canonical document.

## Authority boundary

This guide does not authorize agents to:

- overwrite state;
- repair malformed or ambiguous CSDD;
- migrate unrelated documents;
- modify source or project instructions;
- stage, commit, push, open a PR, or merge.
