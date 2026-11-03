# Migrating CSDD v0.2 to v0.3

Status: non-normative operational guide. The [protocol](protocol.md) and
[document contracts](document-contracts.md) remain authoritative.

## What changed

- v0.2 kept `.csdd/handoff.md` as a tracked, branch-local document.
- v0.3 makes the handoff workspace-local and untracked. A committed
  `.csdd/.gitignore` excludes it.
- `.csdd/specs.md`, `.csdd/todo.md`, and `.csdd/decisions.md` stay committed.
- `/csdd init` creates the three committed documents and `.csdd/.gitignore`. It
  does not create `handoff.md`.
- A missing `.csdd/handoff.md` is valid current state, not partial state.

A tracked handoff is legacy state. An agent MUST offer this migration explicitly
and MUST NOT untrack, delete, or rewrite the file on its own.

## Who needs this

Run this migration when any of the following is true:

- `git ls-files .csdd/handoff.md` prints a path.
- The project was initialized with v0.2 templates and has no
  `.csdd/.gitignore`.
- The project has the three committed documents but no ignore policy for the
  local handoff.

Do not migrate a project with no `.csdd/`. Use `/csdd init` instead.

## Detect the current state

```bash
git ls-files .csdd/handoff.md
git check-ignore -v .csdd/handoff.md
test -f .csdd/.gitignore && cat .csdd/.gitignore
```

- A non-empty first command identifies a tracked legacy handoff.
- `git check-ignore` exits 0 with a matching rule when the local handoff is
  already ignored.
- An uncommented `handoff.md` line in `.csdd/.gitignore` is the required ignore
  policy.

## Migrate

1. Read `.csdd/handoff.md`. Promote durable requirements to `specs.md`, accepted
   directions to `decisions.md`, and active work state to `todo.md`. The local
   handoff must not stay the only home for anything another person or machine
   needs.
2. Untrack the file without deleting the local copy:

   ```bash
   git rm --cached .csdd/handoff.md
   ```

3. Create `.csdd/.gitignore` with an uncommented handoff rule:

   ```gitignore
   # CSDD workspace-local handoff. Never commit handoff.md.
   handoff.md
   ```

4. Keep or delete the local file. Keep it only when a concrete resumption risk
   remains that committed state cannot recover. Otherwise delete it; the file is
   optional.
5. Stage the ignore policy and commit both changes together:

   ```bash
   git add .csdd/.gitignore
   git commit -m "chore(csdd): make handoff workspace-local"
   ```

   `git rm --cached` stages a deletion. Committing the deletion without the
   ignore rule lets a later `git add -A` re-add the file. Keep both in one
   commit.

6. Verify:

   ```bash
   git ls-files .csdd/handoff.md
   git check-ignore -v .csdd/handoff.md
   git status --short
   ```

   The first command prints nothing. The second prints the matching
   `.csdd/.gitignore` rule. The third does not list `.csdd/handoff.md`.

## What does not change

- The canonical `.csdd/` location.
- The paths and fields of `specs.md`, `todo.md`, and `decisions.md`.
- The six canonical TODO headings and `Retention`.
- The boundary-plus-risk rule for creating a handoff.
- Branch and worktree reconciliation for committed documents.

## Compatibility

- A v0.3 skill reads v0.2 state. It recognizes a tracked handoff as legacy and
  does not migrate it automatically.
- A v0.2 skill may treat a missing handoff as partial state and may create or
  commit one. Upgrade the skill before relying on v0.3 behavior in a shared
  repository.
- Older agents ignore the unknown `.csdd/.gitignore` file. The committed
  documents remain readable.
- Do not rewrite v0.2 evaluation runs or historical evidence.

## Rollback

```bash
git add -f .csdd/handoff.md
git commit -m "chore(csdd): restore tracked handoff"
```

Remove the `handoff.md` line from `.csdd/.gitignore`. Rollback restores Git
tracking only. It does not restore handoff content that was deleted.
