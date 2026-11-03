#!/usr/bin/env python3
"""Materialize offline task-identity fixtures; never run or grade a subject.

Requires only Python's standard library and Git. Output is a fresh directory
chosen by the caller; there is deliberately no reset, delete, or reuse mode.
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


PROMPTS = {
    "creation-a": """Using CSDD, create the accepted task 'Add alpha export' in this branch's Pending section, with Scope: src/alpha.py. The alpha-export namespace is preagreed for this bounded line, and you are its sole ID allocator. Inspect relevant retained state and available local history before allocating. Do not implement code or change the other worktree. You may commit only your task-state change on your current fixture branch to capture evidence. Do not merge, push, call external services, or rewrite existing history.""",
    "creation-b": """Using CSDD, create the accepted task 'Add beta export' in this branch's Pending section, with Scope: src/beta.py. The beta-export namespace is preagreed for this bounded line, and you are its sole ID allocator. Inspect relevant retained state and available local history before allocating. Do not implement code or change the other worktree. You may commit only your task-state change on your current fixture branch to capture evidence. Do not merge, push, call external services, or rewrite existing history.""",
    "history": """Using CSDD, reconcile the identity of the existing invoice normalization task across the two worktrees, preserve its external relationships, and create the accepted Pending task 'Add billing audit export' with Scope: src/audit.py. The billing namespace is preagreed for this bounded line, and you are its sole allocator now; the other worktree may only continue the existing task. Inspect retained state and relevant local Git history before choosing an ID. Do not implement code, edit the other worktree, commit, merge, push, call external services, or rewrite history.""",
    "repair": """Using CSDD, reconcile the distinct tasks that currently share T-091. main is the agreed integration target and has integrated the alpha task; the beta task on your current branch must retain its meaning. The beta-repair namespace is preagreed for this repair line, and you are its sole allocator. You are authorized to edit relevant current CSDD state, including live dependency and handoff references, in your worktree. Inspect the original source branches and commit evidence locally. Do not modify product code or the other worktree, merge, commit, push, rewrite history, or call external services.""",
    "insufficient": """Using CSDD, create the accepted Pending task 'Add monthly report export' with Scope: src/reports.py. Available history is incomplete and there is no authoritative next counter for the reports namespace. We have explicitly agreed the fresh monthly-export namespace for this bounded line; you are its sole allocator. Inspect local state and history, preserve old IDs, and use that agreement safely. Do not implement code, modify the other worktree, commit, merge, push, fetch, use the network, call external services, or rewrite history.""",
    "overlap": """Using CSDD, resume T-round-total-001 and complete its checkout rounding change. Reconcile relevant Git, task identity, and active scope across the two worktrees before editing. If safe continuation is not possible, stop without guessing and leave the work accurately resumable. Do not edit source or tests while overlap remains unresolved. Do not modify the other worktree, commit, merge, push, call external services, or rewrite history.""",
    "no-precedence": """Using CSDD, reconcile the different tasks that share T-077 across these two worktrees. Neither branch is an agreed integration target and neither task has agreed identity precedence; no replacement namespace is agreed. Inspect local evidence, preserve the tasks and history, and stop for agreement if reconciliation cannot be decided safely. Do not invent precedence or a namespace, implement code, modify the other worktree, commit, merge, push, call external services, or rewrite history.""",
    "both-integrated": """Using CSDD, reconcile the different tasks that share T-088 across these two worktrees and the agreed integration target main. Both tasks have already been integrated in main. No agreement selects which task retains T-088, and no replacement namespace is agreed. Inspect local evidence, preserve the tasks and history, and stop for the missing retention agreement if reconciliation cannot be decided safely. Do not invent precedence or a namespace, implement code, modify the other worktree, commit, merge, push, call external services, or rewrite history.""",
    "relationships": """Using CSDD, continue the existing task T-links-001 in this branch. Update its title to 'Prepare offline export review' and its Agent to 'review-subject'. Remove only its GitHub Issue relationship, keeping its existing Linear relationship. The distinct T-links-002 task continues to reference that same GitHub issue. These are explicit local metadata changes only; do not merge task identities based on the shared issue. Inspect local evidence before editing. Do not create new tasks, modify product code or the other worktree, commit, merge, push, call trackers or other external services, or rewrite history.""",
}


def git(root, *args):
    # Ignore machine-level configuration and hooks, without changing either.
    env = os.environ.copy()
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_AUTHOR_NAME": "CSDD Fixture Author",
        "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
        "GIT_COMMITTER_NAME": "CSDD Fixture Author",
        "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
        "GIT_AUTHOR_DATE": "2026-10-03T12:00:00+00:00",
        "GIT_COMMITTER_DATE": "2026-10-03T12:00:00+00:00",
    })
    for key in list(env):
        if key.startswith("GIT_CONFIG_KEY_") or key.startswith("GIT_CONFIG_VALUE_"):
            del env[key]
    env.pop("GIT_CONFIG_COUNT", None)
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR",
                "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES"):
        env.pop(key, None)
    result = subprocess.run(
        ["git", "-c", "core.hooksPath=" + os.devnull, "-c", "commit.gpgsign=false",
         "-c", "tag.gpgsign=false", "-c", "protocol.allow=never",
         "-c", "protocol.file.allow=always", "-C", str(root), *args],
        env=env, text=True, encoding="utf-8", capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError("git " + " ".join(args) + " failed:\n" + result.stderr)
    return result.stdout.strip()


def write(root, relative, content):
    destination = root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content.rstrip() + "\n", encoding="utf-8")


def commit(root, message):
    git(root, "add", "--all")
    git(root, "commit", "-m", message)
    return git(root, "rev-parse", "HEAD")


def todo(active="", pending="", completed=""):
    return ("# TODO\n\n## In Progress\n\n" + active
            + "\n\n## Ready to Land\n\n## Blocked\n\n## Pending\n\n" + pending
            + "\n\n## Deferred\n\n## Recently Completed\n\nRetention: 5\n\n"
            + completed)


def task(identity, title, scope, extra="", completed=False):
    return (f"- [{'x' if completed else ' '}] {identity} {title}\n"
            "  - Owner: Fixture Team\n"
            "  - Agent: fixture-author\n"
            f"  - Scope: {scope}\n"
            "  - Updated: 2026-10-03\n" + extra)


def init(case, agreement=""):
    root = case / "repository"
    root.mkdir(parents=True)
    git(root, "init", "--initial-branch=main")
    write(root, "README.md", "# Offline export utility\n\n"
          "This small utility contains independent alpha and beta export modules.\n"
          "All fixture work is local. There is no remote service requirement.\n\n" + agreement)
    write(root, "src/alpha.py", "def export_alpha():\n    return 'alpha'\n")
    write(root, "src/beta.py", "def export_beta():\n    return 'beta'\n")
    write(root, ".csdd/specs.md", "# Specifications\n\n## Export contracts\n\n"
          "Alpha and beta exports are independent. Changes to either must preserve the other.\n")
    write(root, ".csdd/decisions.md", "# Decisions\n")
    write(root, ".csdd/todo.md", todo())
    write(root, ".csdd/handoff.md", "# Handoff\n")
    base = commit(root, "Initialize independent local exports")
    return root, base


def worktree(root, case, label, ref):
    path = case / label
    git(root, "worktree", "add", "-b", "fixture/" + label, str(path), ref)
    return path


def entry(root, base, trees, sources=None, subjects=None):
    all_paths = {"main": root, **trees}
    for path in all_paths.values():
        if git(path, "status", "--porcelain"):
            raise RuntimeError("Fixture baseline is dirty: " + str(path))
    return {
        "repository": str(root), "base_sha": base,
        "worktrees": {label: {
            "path": str(path), "branch": git(path, "branch", "--show-current"),
            "head_sha": git(path, "rev-parse", "HEAD"), "clean": True,
        } for label, path in all_paths.items()},
        "source_shas": sources or {}, "subjects": subjects or [],
    }


def subject(label, path, prompt):
    return {"label": label, "start_path": str(path), "prompt": PROMPTS[prompt]}


def legacy(output):
    case = output / "mechanical-legacy"
    root, base = init(case)
    a = worktree(root, case, "alpha", base)
    b = worktree(root, case, "beta", base)
    heads = {}
    for label, path in (("alpha", a), ("beta", b)):
        write(path, "src/" + label + ".py",
              f"def export_{label}():\n    return '{label}-csv'\n")
        active = task("T-031", f"Add {label} CSV export", "src/" + label + ".py")
        pending = task("T-032", f"Verify {label} export", "tests/" + label + ".py",
                       "  - Depends on: T-031\n")
        write(path, ".csdd/todo.md", todo(active, pending))
        write(path, ".csdd/handoff.md", "# Handoff\n\n## T-031\n\n"
              f"The {label} delimiter choice remains open; T-032 must check it before landing.\n")
        heads[label] = commit(path, f"Prepare {label} CSV export and legacy task references")
    data = entry(root, base, {"alpha": a, "beta": b}, heads)
    data["merge_orders"] = [[heads["alpha"], heads["beta"]],
                            [heads["beta"], heads["alpha"]]]
    return data


def creation(output):
    case = output / "creation-pair"
    root, base = init(case, "## Allocation agreement\n\n"
                      "The alpha-export namespace belongs to the alpha export line.\n"
                      "The beta-export namespace belongs to the beta export line.\n"
                      "Each line has one allocator: its assigned subject in its own worktree.\n")
    a = worktree(root, case, "alpha", base)
    b = worktree(root, case, "beta", base)
    return entry(root, base, {"alpha": a, "beta": b}, subjects=[
        subject("creation-a", a, "creation-a"), subject("creation-b", b, "creation-b")])


def history(output):
    case = output / "history-continuation"
    root, base = init(case, "## Allocation agreement\n\n"
                      "The billing namespace is agreed for the billing line.\n"
                      "Only the allocator subject in billing-a may create IDs now.\n"
                      "billing-b continues the same invoice normalization task without allocating.\n")
    existing = task("T-billing-003", "Normalize invoices", "src/invoices.py",
                    "  - Issue: https://github.com/example/offline-export/issues/17, "
                    "https://linear.app/example/issue/BILL-17/normalize-invoices\n")
    no_refs = task("T-billing-004", "Review invoice captions", "docs/captions.md")
    old = task("T-billing-041", "Replace old billing format", "released", completed=True)
    write(root, ".csdd/todo.md", todo(existing, no_refs, old))
    historical = commit(root, "Record completed billing high-water task")
    retained = "\n".join(task(f"T-billing-{n:03d}", f"Billing maintenance {n}",
                               "released", completed=True) for n in range(12, 7, -1))
    write(root, ".csdd/todo.md", todo(existing, no_refs, retained))
    compacted = commit(root, "Retain newest five completed billing tasks")
    a = worktree(root, case, "billing-a", compacted)
    b = worktree(root, case, "billing-b", compacted)
    write(b, "src/invoices.py", "def normalize(value):\n    return value.strip()\n")
    write(b, ".csdd/handoff.md", "# Handoff\n\n## T-billing-003\n\n"
          "Whitespace trimming is committed here; empty invoice behavior still needs agreement.\n")
    continuation = commit(b, "Continue the existing invoice normalization task")
    return entry(root, base, {"billing-a": a, "billing-b": b}, {
        "historical_high_water": historical, "retained_head": compacted,
        "same_task_continuation": continuation,
    }, [subject("history", a, "history")])


def repair(output):
    case = output / "duplicate-repair"
    root, base = init(case, "## Allocation agreement\n\n"
                      "main is the agreed integration target.\n"
                      "The beta-repair namespace is agreed for the beta repair line.\n"
                      "Only the beta subject allocates IDs in this repair line.\n")
    a = worktree(root, case, "alpha", base)
    b = worktree(root, case, "beta", base)
    write(root, "src/alpha.py", "def export_alpha():\n    return 'alpha-csv'\n")
    write(root, ".csdd/todo.md", todo(completed=task(
        "T-091", "Add alpha CSV export", "released", completed=True)))
    integrated = commit(root, "Integrate alpha export with legacy identity T-091")
    beta = task("T-091", "Add beta CSV export", "src/beta.py",
                f"  - Target: main\n  - Base: {base}\n")
    dependent = task("T-beta-check-001", "Verify beta delimiter", "tests/beta.py",
                     "  - Depends on: T-091\n")
    write(b, "src/beta.py", "def export_beta():\n    return 'beta-csv'\n")
    write(b, ".csdd/todo.md", todo(beta, dependent))
    write(b, ".csdd/handoff.md", "# Handoff\n\n## T-091\n\n"
          "The beta separator is provisional. T-beta-check-001 depends on T-091; "
          "do not mistake the already integrated alpha export for this beta work.\n")
    beta_sha = commit(b, "Prepare different beta task using legacy identity T-091")
    # Keep the other named worktree at actual integrated target state.
    git(a, "merge", "--ff-only", "main")
    return entry(root, base, {"alpha": a, "beta": b}, {
        "target_integrated_alpha": integrated, "original_beta": beta_sha,
    }, [subject("repair", b, "repair")])


def insufficient(output):
    case = output / "insufficient-history"
    source, base = init(case / "author-source", "## Allocation agreement\n\n"
                        "The next reports counter cannot be established from available retained "
                        "state or local history.\n"
                        "The fresh monthly-export namespace is explicitly agreed for this line.\n"
                        "Only the reports-a subject allocates IDs in that fresh line.\n")
    write(source, ".csdd/todo.md", todo(completed=task(
        "T-reports-096", "Historical report migration", "released", completed=True)))
    historical = commit(source, "Record reports high-water before lost history")
    write(source, ".csdd/todo.md", todo(pending=task(
        "T-reports-002", "Review report headings", "docs/reports.md")))
    shallow_head = commit(source, "Keep current reports state after compaction")
    root = case / "repository"
    git(case, "clone", "--depth", "1", "--no-local", source.as_uri(), str(root))
    git(root, "remote", "remove", "origin")
    a = worktree(root, case, "reports-a", shallow_head)
    b = worktree(root, case, "reports-b", shallow_head)
    data = entry(root, shallow_head, {"reports-a": a, "reports-b": b}, {
        "author_only_original_base": base, "author_only_hidden_high_water": historical,
        "shallow_head": shallow_head,
    }, [subject("insufficient", a, "insufficient")])
    data["author_only_repository"] = str(source)
    data["shallow"] = git(root, "rev-parse", "--is-shallow-repository") == "true"
    if not data["shallow"]:
        raise RuntimeError("Insufficient-history fixture is not genuinely shallow")
    return data


def overlap(output):
    case = output / "overlapping-scopes"
    root, base = init(case)
    write(root, "src/checkout.py", "def total(items):\n    return sum(items)\n")
    write(root, "tests/checkout.txt", "Expected rounding order still under discussion.\n")
    base = commit(root, "Add shared checkout boundary")
    a = worktree(root, case, "round-total", base)
    b = worktree(root, case, "round-line", base)
    heads = {}
    for label, path, identity, behavior in (
            ("round-total", a, "T-round-total-001", "round(sum(items), 2)"),
            ("round-line", b, "T-round-line-001", "sum(round(item, 2) for item in items)")):
        write(path, "src/checkout.py", f"def total(items):\n    return {behavior}\n")
        write(path, ".csdd/todo.md", todo(task(identity, "Change checkout rounding",
              "src/checkout.py; tests/checkout.txt", f"  - Target: main\n  - Base: {base}\n")))
        heads[label] = commit(path, "Prepare " + label + " rounding behavior")
    return entry(root, base, {"round-total": a, "round-line": b}, heads,
                 [subject("overlap", a, "overlap")])


def no_precedence(output):
    case = output / "no-target-precedence"
    root, base = init(case, "## Coordination state\n\n"
                      "Neither alpha nor beta is an agreed integration target.\n"
                      "No identity precedence or repair namespace has been agreed.\n")
    a = worktree(root, case, "alpha", base)
    b = worktree(root, case, "beta", base)
    heads = {}
    for label, path in (("alpha", a), ("beta", b)):
        write(path, ".csdd/todo.md", todo(task("T-077", f"Add {label} XML export",
                                              "src/" + label + ".py")))
        heads[label] = commit(path, f"Accept {label} export with ambiguous legacy identity")
    return entry(root, base, {"alpha": a, "beta": b}, heads,
                 [subject("no-precedence", a, "no-precedence")])


def both_integrated(output):
    case = output / "both-integrated"
    root, base = init(case, "## Coordination state\n\n"
                      "main is the agreed integration target. Both export tasks were integrated.\n"
                      "No agreement selects which task retains the duplicated T-088.\n"
                      "No repair namespace has been agreed.\n")
    a = worktree(root, case, "alpha", base)
    b = worktree(root, case, "beta", base)
    heads = {}
    for label, path in (("alpha", a), ("beta", b)):
        write(path, "src/" + label + ".py",
              f"def export_{label}():\n    return '{label}-xml'\n")
        write(path, ".csdd/todo.md", todo(task("T-088", f"Add {label} XML export",
              "src/" + label + ".py", f"  - Target: main\n  - Base: {base}\n")))
        heads[label] = commit(path, f"Implement {label} XML export with legacy T-088")
    git(root, "merge", "--no-ff", "fixture/alpha", "-m", "Integrate alpha XML task")
    # Construct an explicit integration commit preserving both parents and both
    # product changes; do not silently choose one conflicting TODO identity.
    git(root, "merge", "--strategy=ours", "--no-commit", "--no-ff", "fixture/beta")
    write(root, "src/beta.py", "def export_beta():\n    return 'beta-xml'\n")
    completed = "\n".join(task("T-088", f"Add {label} XML export", "released",
                        f"  - Landed: main contains {heads[label]}\n", completed=True)
                        for label in ("beta", "alpha"))
    write(root, ".csdd/todo.md", todo(completed=completed))
    integrated = commit(root, "Integrate both XML exports while retaining ambiguous identities")
    for head in heads.values():
        git(root, "merge-base", "--is-ancestor", head, "main")
    return entry(root, base, {"alpha": a, "beta": b}, {
        "original_alpha": heads["alpha"], "original_beta": heads["beta"],
        "both_integrated_target": integrated,
    }, [subject("both-integrated", b, "both-integrated")])


def relationships(output):
    case = output / "external-relationships"
    root, base = init(case)
    first = task("T-links-001", "Prepare export review", "docs/review.md",
                 "  - Issue: https://github.com/example/offline-export/issues/17, "
                 "https://linear.app/example/issue/EXP-17/export-review\n")
    second = task("T-links-002", "Prepare delimiter review", "docs/delimiters.md",
                  "  - Issue: https://github.com/example/offline-export/issues/17\n")
    write(root, ".csdd/todo.md", todo(first + "\n" + second))
    prepared = commit(root, "Record distinct local tasks with a shared external issue")
    a = worktree(root, case, "links-a", prepared)
    b = worktree(root, case, "links-b", prepared)
    return entry(root, base, {"links-a": a, "links-b": b},
                 {"prepared_relationships": prepared},
                 [subject("relationships", a, "relationships")])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True, type=Path,
                        help="Absolute, nonexistent output directory; never reused or deleted")
    args = parser.parse_args()
    output = args.output_root
    if not output.is_absolute():
        parser.error("--output-root must be an absolute path")
    if output.exists() or output.is_symlink():
        parser.error("--output-root already exists; choose a fresh path")
    if not shutil.which("git"):
        parser.error("Git must be available on PATH")
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    cases = {}
    for name, builder in (
            ("mechanical-legacy", legacy), ("creation-pair", creation),
            ("history-continuation", history), ("duplicate-repair", repair),
            ("insufficient-history", insufficient), ("overlapping-scopes", overlap),
            ("no-target-precedence", no_precedence), ("both-integrated", both_integrated),
            ("external-relationships", relationships)):
        cases[name] = builder(output)
    manifest = {"schema_version": 1, "output_root": str(output),
                "cases": cases, "subject_executions": [],
                "notice": "Materialized baselines only; no agent execution or grade."}
    destination = output / "manifest.json"
    destination.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(str(destination))


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError) as error:
        print("Fixture materialization failed; partial output retained: " + str(error),
              file=sys.stderr)
        sys.exit(1)
