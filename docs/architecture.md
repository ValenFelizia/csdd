# Architecture and product boundaries

CSDD preserves explicit project state and coordinates coding work through small,
inspectable Markdown documents versioned with the repository. Its core value is
safe orientation, resumption, and Git-aware coordination with context and process
proportional to the task.

This is the canonical contributor design policy for reviewing product scope and
optional integrations. It consolidates existing intent; it does not change the
v0.2 runtime contract, add a project-state document, or require agents to load
this file during ordinary work. Runtime behavior remains defined by the
[protocol](../references/protocol.md) and
[document contracts](../references/document-contracts.md).

## Design principles

1. **Explicit accepted state.** Repository evidence and recovered context can
   inform proposals. Inferred memory alone cannot authorize requirements,
   decisions, task claims, or canonical writes. Investigate contradictions;
   neither code nor documentation automatically wins.
2. **Repository-local truth.** Canonical state travels with the repository and
   can be inspected through files, diffs, commits, branches, and worktrees.
   Integrations must not silently move that authority into a service. The current
   four documents retain their
   [distinct responsibilities](../references/protocol.md#core-project-state-documents).
3. **Usable without optional infrastructure.** The core needs no daemon,
   database, hosted backend, model proxy, continuous model calls, control panel,
   authenticated agent identity, or central coordination server. Optional tools
   may assist, but plain repository state must remain sufficient to inspect,
   edit, migrate, and use CSDD when those tools are absent.
4. **Minimum sufficient context.** Preserve consequential knowledge rather than
   activity exhaust. Keep ordinary hydration free of full conversation logs,
   large indexes, accumulated histories, and unbounded backlogs. Protect the
   [trivial fast path](../SKILL.md#take-the-trivial-fast-path).
5. **Operational purpose.** Specifications, decisions, task lifecycle, write
   scopes, landing, and boundary-driven handoffs are core concerns. General
   memory storage, retrieval, and knowledge management belong to complementary
   systems. Partial overlap in continuity does not make either layer a complete
   replacement for the other.
6. **Advisory coordination with honest limits.** Claims are visible evidence for
   observers of that branch, not distributed locks or authenticated identities.
   Preserve explicit conflict detection and reconciliation; do not imply
   consensus, global visibility, automatic synchronization, or guaranteed
   conflict-free merges.
7. **Portable semantics.** Protocol behavior must remain usable across
   harnesses. Installation and discovery adapters may differ, but one proprietary
   API, IDE, agent framework, or model provider must not define canonical state.
8. **Composable external context.** Memory systems, issue trackers, RAG indexes,
   and code graphs may provide context or tooling. Reconcile their output with
   current repository evidence and accepted state before using it as project
   truth. An external reference does not by itself transfer canonical authority.

## Default exclusions from the core

Unless evidence and an explicit architecture decision justify a change, keep
these capabilities in specialized external systems:

- Conversation capture, chat-history warehouses, automatic user/persona memory
  extraction, and canonical mutation based solely on inferred memory.
- Embeddings, vector retrieval, RAG infrastructure, whole-repository semantic
  indexing, code graphs, and impact-analysis engines.
- Automatic skill extraction, skill registries, and general knowledge platforms.
- Background watchers, daemons, continuous synchronization, hosted dashboards,
  control planes, LLM proxies, and model-processing services.
- Team/user ACL systems, central task databases, coordination servers,
  distributed locks, and consensus.

These are product defaults, not claims that the capabilities are useless.
Changing a default requires a reviewed, explicit scope decision and assessment
of protocol, compatibility, and migration impact. An issue, prototype, or
unmerged PR is not an accepted change to the runtime contract.

## Review a feature proposal

Use this gate for a feature, integration, or architectural change. Answer only
the relevant questions in the proposal or PR; routine wording fixes and small
maintenance changes do not need a separate design document or full checklist.

1. What concrete CSDD operational failure is observed, and what dogfooding,
   evaluation, or user evidence supports it? Separate observations from
   hypotheses and untested benefits.
2. Why are the existing four documents and workflows insufficient? Compare the
   smallest credible alternatives, including using an external specialized tool.
3. Where does canonical truth live, and can ordinary repository files still
   express it? Identify any changed document responsibilities or derived views.
4. What required runtime, external service, model dependency, data export, or
   synchronization does the proposal introduce? State what happens without it.
5. What context, coordination, and maintenance cost does it add to trivial,
   local, and collaborative work? Does it improve explicit coordination or add
   general memory/retrieval capability?
6. If optional, does it preserve the same canonical semantics with and without
   the integration, rather than creating incompatible CSDD modes?
7. Which current non-guarantees, contracts, versions, and migrations are
   affected? Do not introduce stronger guarantees or structural changes by
   implication; use the [versioning policy](../README.md#versioning).
8. What observable evaluation would demonstrate the benefit while preserving
   conflict detection, task state, and safe resumption? Define acceptance before
   reporting a successful result.

## Optional integration contract

An integration proposal should state:

- which system owns each canonical fact and which outputs are derived;
- how CSDD remains usable and how failures are reported when the integration is
  absent, unavailable, or stale;
- what data leaves the repository, for what purpose, and under whose authority;
- how contradictions are surfaced and reconciled before dependent execution;
- which guarantees remain outside CSDD and which claims have actually been
  evaluated.

Read-only exports or diagnostics, external indexing of CSDD documents,
installation/discovery adapters, and optional structural validation can fit
these boundaries. A derived status view should point back to repository truth;
it should not become a separately maintained task store. A memory system may
retrieve CSDD state, but stale retrieved state does not authorize overwriting
the current repository.

The accepted direction for [#41](https://github.com/ValenFelizia/csdd/issues/41)
is defined by the [local task identity contract](../references/document-contracts.md#local-task-identity):
bounded namespaces with optional external relationships. The accepted direction
for [#42](https://github.com/ValenFelizia/csdd/issues/42) combines
[write economy](../references/document-contracts.md#write-economy) with
[task-wise landing reconciliation](../references/document-contracts.md#task-wise-landing-reconciliation).
Its measured scope belongs in evaluation reports; neither direction introduces
stronger coordination guarantees or changes the four-document runtime boundary.
