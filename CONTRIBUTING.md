# Contributing to CSDD

CSDD changes can affect several linked descriptions of the same behavior. Keep
one canonical source for each claim, review the affected surfaces together, and
scale verification to the change. Start with the
[architecture and product boundaries](docs/architecture.md) for feature or
integration proposals; small maintenance changes do not need the full design
gate.

## Know the source boundaries

| Path | Responsibility |
| --- | --- |
| `references/protocol.md` | Conceptual protocol behavior and lifecycle rules |
| `references/document-contracts.md` | Exact document structure, fields, read/write boundaries, and cleanup |
| `SKILL.md` | Operational router and fast paths; detailed rules stay in references |
| `assets/templates/` | Distributed starting documents for adoption |
| `references/migration-v0.1-to-v0.2.md` | Existing migration contract; future breaking changes need appropriate migration guidance |
| `docs/architecture.md` | Canonical contributor product-scope and integration review policy |
| `docs/installation.md`, `docs/compatibility.md` | Distribution guidance and evidence-backed dimensional compatibility claims |
| `evals/scenarios/`, `evals/runs/`, `evals/results.md` | Frozen scenario contracts, actual run evidence, and the results index |
| `scripts/`, `tests/`, `.github/workflows/` | Optional offline repository validation and its CI execution |
| `evidence/`, `dogfooding/`, `field-reports/` | Observations and supporting evidence, not additional normative sources |
| `.csdd/` | This repository's own project state; it is not a template for adopters |
| `README.md`, `changelog.md`, `adapters/` | Public entrypoint, release history, and harness-specific guidance |

Protocol references and this repository's own `.csdd/` specifications and
decisions have different purposes. Do not turn a local task note, example,
evaluation expectation, issue, or unmerged PR into a new protocol rule.

## Classify the change and review its impact

Classify by effect, not file extension: changing a Markdown instruction can
change required agent behavior. A change may fit more than one row.

| Change | Review at minimum |
| --- | --- |
| Protocol or task/document semantics | Protocol, document contracts, skill routing, affected templates, migration impact, and relevant evals |
| Workflow or operational fast path | Skill, protocol, applicable document contract, and workflow scenarios |
| Canonical structure or initialization | Templates, init rules in skill/protocol/contracts, migration guidance, README, structural validator/tests, and initialization evals |
| Template | Governing contract, initialization, related examples/evals, and structural validation |
| Packaging, frontmatter, or distribution | Skill runtime boundary, installation docs, compatibility evidence, validator/tests, and CI |
| Evaluation or evidence | Governing behavior, scenario/run separation, results links, and any public compatibility claim relying on that evidence |
| Documentation or maintenance | Canonical source of the edited claim, related links, and affected tooling; expand review if wording changes behavior |

Review does not mean editing every listed file. Update surfaces whose meaning
changes and explain material omissions. Prefer links to repeating complete
rules. Examples, when added, teach the accepted contract; they do not own it.

For a new feature or integration, use the
[feature review gate](docs/architecture.md#review-a-feature-proposal). Present
evidence and alternatives before treating a candidate as accepted. Architectural
defaults may evolve through an explicit reviewed decision; a prototype alone
does not change them.

## Breaking changes and migration

Assess effects on valid existing `.csdd/` state, required agent behavior,
document responsibility, paths, fields, and installation/runtime boundaries.
If previously valid state becomes invalid or requires reinterpretation, document
the breaking impact and a migration path. Do not silently rewrite existing
projects or retrofit new requirements into old run evidence.

Use the [versioning policy](README.md#versioning): patch releases clarify or fix
non-breaking defects; minor releases add compatible rules, fields, or workflows;
major releases may change canonical contracts or required behavior. Before 1.0,
contracts can evolve, but the impact still needs explicit review. Documentation
and contributor-policy changes do not by themselves require project migration.

## Validate proportionally

Run the same offline checks as
[CI](.github/workflows/validate.yml), using Python's standard library:

```bash
python -m unittest discover -s tests -v
python scripts/validate_repository.py
git diff --check
```

The validator checks package structure, templates, and relative Markdown links;
it does not prove semantic correctness, agent behavior, or harness compatibility.
For documentation-only changes, review consistency with the canonical source
and record that behavioral evaluations were not needed when behavior is
unchanged. Do not add tests that merely mirror wording.

Add or update an evaluation scenario when a change introduces or alters an
observable workflow, safety condition, coordination outcome, or behavior that
existing scenarios do not adequately cover. State the expected behavior and
critical failures before running it. For a behavior fix, reproduce the defect
and evaluate the correction and relevant regression risks.

Follow [the evaluation guide](evals/README.md): keep scenario contracts separate
from run reports, separate fixture author/subject/evaluator roles, record actual
fixture and skill commits, and publish only observed results. State skipped or
unavailable coverage. CI success alone does not authorize upgrading a public
compatibility claim; use the evidence requirements in the
[compatibility matrix](docs/compatibility.md).

Installation experiments should use an isolated destination. Do not run skill
install/update/remove over a development checkout, including one located at
`~/.agents/skills/csdd`.

## Prepare a reviewable pull request

Keep each PR focused on a concrete problem and resulting behavior. Include:

- related issues and the intended change;
- whether normative behavior changes, and the canonical sources affected;
- breaking, migration, template, and evaluation impact when applicable;
- validation actually performed, with limitations or pending checks.

Use the [PR template](.github/PULL_REQUEST_TEMPLATE.md). For a small documentation
or maintenance change, a short summary, `none` for contract/migration impact,
and relevant checks are enough. Do not manufacture decisions, task claims, or
handoffs to fill a template.

There is no CI-enforced branch naming or conventional-commit format. Follow
applicable project instructions, use descriptive branch names, and include the
task ID in task-focused commits when relevant under the
[Git contract](references/protocol.md#minimal-git-contract).

When coordination is needed, follow existing scope and branch/worktree rules
before editing shared state. Leave verified but unmerged work Ready to Land;
completion requires reachability from the target. A PR does not authorize
merge, release, or deployment. Keep unrelated changes and private project data
out of the contribution.
