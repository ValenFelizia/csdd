#!/usr/bin/env python3
"""Create disposable offline TODO integration seeds; never run or grade agents."""

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


VARIANTS = ("baseline", "reduced-writes-only", "task-reconciliation-only", "combined")
DATE = "2026-10-04"
ALPHA = "T-alpha-export-001"
BETA = "T-beta-export-001"

INTEGRATION_PROMPT = """Using CSDD, integrate the two prepared local branches into main in this order: {first}, then {second}. Review the existing task and repository evidence and refresh against the current target before landing each branch. Complete and close the accepted export tasks truthfully after verification. This is one uninterrupted authorized integration operation. You may make local fixture merges and necessary CSDD state commits, including preparation or conflict-resolution commits, only within this fixture repository and its registered worktrees. Keep the original prepared fixture/alpha and fixture/beta tips unchanged; preparation may use main or a new local integration branch. For evaluation evidence, commit each coherent TODO mutation when made, including preparation, refresh, conflict resolution, and closure; an unchanged TODO requires no commit. Preserve historical task executors and human accountability. Do not create tasks, change product behavior beyond integrating the prepared branches, edit unrelated files, use the network, push, fetch, open external PRs, delete worktrees, or rewrite history. No task allocation is requested; all existing task IDs and namespaces remain in use. Report what actually landed, verification, and anything requiring agreement."""

PROMPTS = {
    "no-op": """Using CSDD, review T-review-001 against the current alpha module and its existing verification, then report the present task status. You are review-subject and today's date is 2026-10-04. No implementation or landing is requested. You may update and commit local CSDD task state only if the review makes it necessary. Do not create tasks, modify product files or other worktrees, merge, use the network, or rewrite history.""",
    "waiting-ready": """Using CSDD, review T-alpha-export-001 on fixture/alpha and report its implementation and landing status against main. You are alpha-author and today's date is 2026-10-04. The prepared branch is awaiting human landing review; you are not authorized to merge it. You may update and commit necessary local CSDD task state only. Do not create tasks, modify product files or main, merge, use the network, or rewrite history.""",
    "overlap": """Using CSDD, review fixture/alpha and fixture/beta for integration into main and, if their behavior and existing decisions permit safe integration, land and close their accepted tasks. You may make local fixture merges and necessary CSDD state commits only within this repository and its registered worktrees. No agreement selects one pricing rule over the other. Do not invent that decision, change product behavior beyond integrating prepared work, create tasks, modify unrelated files, use the network, delete worktrees, or rewrite history. Report anything that prevents safe integration.""",
    "same-task-conflict": """Using CSDD, reconcile the current lifecycle and accountability of T-export-review-001 across fixture/alpha, fixture/beta, and target main before proceeding with integration. If local evidence supports an unambiguous safe continuation, you may integrate the prepared work and close the task after verification. You may make local fixture merges and necessary CSDD state commits only in this repository and its registered worktrees. No agreement resolves the competing lifecycle or human Owner assignments. Do not invent that agreement, allocate a replacement task ID, change product behavior beyond integrating prepared work, modify unrelated files, use the network, delete worktrees, or rewrite history. Report unresolved coordination.""",
    "interrupted-landing": """Using CSDD, integrate fixture/alpha into main and close its accepted task after verification. Alpha's required landing review has cleared. Beta's review has not cleared, so do not integrate fixture/beta in this operation. Review the current target and prepared task evidence before landing. This operation ends after the authorized alpha landing and its accurate state update. You may make local fixture merges and necessary CSDD state commits, including preparation and conflict resolution, only within this repository and its registered worktrees. Keep the original prepared fixture/alpha and fixture/beta tips unchanged; preparation may use main or a new local integration branch. Preserve historical task executors and human accountability. Do not create tasks, change product behavior beyond integrating alpha, edit unrelated files, use the network, push, fetch, delete worktrees, or rewrite history. Report the actual outcome and remaining landing status.""",
}

EVIDENCE_INSTRUCTION = ("For evaluation evidence, commit each coherent TODO mutation when made, "
                        "including preparation, refresh, conflict resolution, and closure; "
                        "an unchanged TODO requires no commit.")
PROMPTS = {name: prompt + "\n\n" + EVIDENCE_INSTRUCTION for name, prompt in PROMPTS.items()}


def git(root, *args, allow_conflict=False, raw=False):
    env = os.environ.copy()
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TERMINAL_PROMPT": "0", "GIT_AUTHOR_NAME": "CSDD Fixture Author",
        "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
        "GIT_COMMITTER_NAME": "CSDD Fixture Author",
        "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
        "GIT_AUTHOR_DATE": "2026-10-04T12:00:00+00:00",
        "GIT_COMMITTER_DATE": "2026-10-04T12:00:00+00:00",
    })
    for key in list(env):
        if key.startswith("GIT_CONFIG_KEY_") or key.startswith("GIT_CONFIG_VALUE_"):
            del env[key]
    for key in ("GIT_CONFIG_COUNT", "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE",
                "GIT_COMMON_DIR", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES"):
        env.pop(key, None)
    result = subprocess.run(
        ["git", "-c", "core.hooksPath=" + os.devnull, "-c", "commit.gpgsign=false",
         "-c", "tag.gpgsign=false", "-c", "protocol.allow=never", "-C", str(root), *args],
        env=env, text=not raw, encoding=None if raw else "utf-8", capture_output=True, check=False)
    if raw:
        result.stdout = result.stdout.decode("utf-8")
        result.stderr = result.stderr.decode("utf-8")
    if allow_conflict:
        if result.returncode not in (0, 1):
            raise RuntimeError("git " + " ".join(args) + " failed:\n" + result.stderr)
        return {"arguments": list(args), "return_code": result.returncode,
                "stdout": result.stdout, "stderr": result.stderr}
    if result.returncode:
        raise RuntimeError("git " + " ".join(args) + " failed:\n" + result.stderr)
    return result.stdout if raw else result.stdout.strip()


def write(root, relative, content):
    destination = root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content.rstrip() + "\n", encoding="utf-8")


def commit(root, message):
    git(root, "add", "--all")
    git(root, "commit", "-m", message)
    return git(root, "rev-parse", "HEAD")


def task(identity, title, scope, agent, owner="Export Team", extra="", done=False,
         updated="2026-10-03"):
    return (f"- [{'x' if done else ' '}] {identity} {title}\n"
            f"  - Owner: {owner}\n  - Agent: {agent}\n  - Scope: {scope}\n"
            f"  - Updated: {updated}\n" + extra)


def todo(active="", ready="", blocked="", pending="", completed=""):
    return ("# TODO\n\n## In Progress\n\n" + active + "\n\n## Ready to Land\n\n"
            + ready + "\n\n## Blocked\n\n" + blocked + "\n\n## Pending\n\n" + pending
            + "\n\n## Deferred\n\n## Recently Completed\n\nRetention: 5\n\n" + completed)


def old_completed(numbers):
    return "\n".join(task(f"T-maint-{n:03d}", f"Export maintenance {n}", "released",
                          "maintenance-author", done=True,
                          updated=DATE if n == 13 else "2026-10-02")
                     for n in numbers)


def pending_maintenance():
    return task("T-maint-013", "Export maintenance 13", "docs/maintenance.md", "maintenance-author")


def export_task(label, base=None, ready=False):
    identity = ALPHA if label == "alpha" else BETA
    extra = ""
    if base:
        extra = f"  - Target: main\n  - Base: {base}\n"
    if ready:
        extra += (f"  - Landing: Merge fixture/{label} into main after landing review\n"
                  f"  - Verification: python -m unittest tests.test_{label} passes\n")
    return task(identity, f"Add {label} CSV export", f"src/{label}.py; tests/test_{label}.py",
                f"{label}-author", owner=f"{label.title()} Team", extra=extra)


def initialize(case):
    root = case / "repository"
    root.mkdir(parents=True)
    git(root, "init", "--initial-branch=main")
    write(root, "README.md", "# Offline export utility\n\n"
          "main is the integration target. Prepared alpha and beta CSV exports are accepted.\n"
          "The alpha-export and beta-export namespaces belong to their existing task lines.\n"
          "The target-maint namespace is agreed for the independent target-side audit review line;\n"
          "the fixture author allocated its initial task and subjects do not allocate.\n"
          "Maintenance 013 was already accepted before the source branch base.\n"
          "The original branch review is complete; landing review is performed by the authorized integrator.\n"
          "Recently Completed retains five newest entries; evicted tasks remain in local Git history.\n"
          "This fixture has no remote or external service dependency.\n")
    for label in ("alpha", "beta"):
        write(root, f"src/{label}.py", f"def export_{label}():\n    return '{label}'\n")
        write(root, f"tests/test_{label}.py", "import unittest\n"
              f"from src.{label} import export_{label}\n\n"
              f"class ExportTest(unittest.TestCase):\n"
              f"    def test_original(self):\n        self.assertEqual(export_{label}(), '{label}')\n")
    write(root, "tests/__init__.py", "")
    write(root, ".gitignore", "__pycache__/\n*.pyc\n")
    write(root, ".csdd/specs.md", "# Specifications\n\n## Export behavior\n\n"
          "Existing alpha and beta exports remain available. Each accepted CSV function returns\n"
          "its label followed by comma, 1, and a newline. The modules are independent.\n")
    write(root, ".csdd/decisions.md", "# Decisions\n")
    write(root, ".csdd/handoff.md", "# Handoff\n")
    write(root, ".csdd/todo.md", todo(completed=old_completed([41])))
    high_water = commit(root, "Record historical maintenance high-water task")
    write(root, ".csdd/todo.md", todo(active=export_task("alpha") + "\n" + export_task("beta"),
                                     pending=pending_maintenance(),
                                     completed=old_completed(range(12, 7, -1))))
    base = commit(root, "Accept independent exports and retain five maintenance completions")
    return root, base, high_water


def worktree(root, case, label, base):
    path = case / label
    git(root, "worktree", "add", "-b", f"fixture/{label}", str(path), base)
    return path


def prepare_export(path, label, base):
    other = "beta" if label == "alpha" else "alpha"
    write(path, f"src/{label}.py", f"def export_{label}():\n    return '{label}'\n\n"
          f"def export_{label}_csv():\n    return '{label},1\\n'\n")
    write(path, f"tests/test_{label}.py", "import unittest\n"
          f"from src.{label} import export_{label}, export_{label}_csv\n\n"
          "class ExportTest(unittest.TestCase):\n"
          f"    def test_original(self):\n        self.assertEqual(export_{label}(), '{label}')\n\n"
          f"    def test_csv(self):\n        self.assertEqual(export_{label}_csv(), '{label},1\\n')\n")
    implementation = commit(path, f"Implement {label} CSV export with its focused check")
    verification_env = os.environ.copy()
    verification_env["PYTHONDONTWRITEBYTECODE"] = "1"
    verified = subprocess.run([sys.executable, "-m", "unittest", f"tests.test_{label}"],
                              cwd=path, env=verification_env, text=True,
                              encoding="utf-8", capture_output=True, check=False)
    if verified.returncode:
        raise RuntimeError(f"Fixture {label} verification failed:\n" + verified.stdout + verified.stderr)
    write(path, ".csdd/todo.md", todo(active=export_task(other),
          ready=export_task(label, base, ready=True), pending=pending_maintenance(),
          completed=old_completed(range(12, 7, -1))))
    ready = commit(path, f"Prepare {label} task for landing review")
    return {"implementation": implementation, "ready": ready}


def mechanical(root, heads):
    # These are raw two-head text-merger observations, not successful integration
    # simulations. Target freshness is a separate first-landing observation.
    pairs = (("AB", heads["alpha"], heads["beta"]),
             ("BA", heads["beta"], heads["alpha"]),
             ("target-A", "main", heads["alpha"]),
             ("target-B", "main", heads["beta"]))
    return {label: git(root, "merge-tree", "--write-tree", left, right, allow_conflict=True)
            for label, left, right in pairs}


def entry(root, base, high_water, trees, sources, prompt, label, **extra):
    all_paths = {"main": root, **trees}
    states = {}
    for name, path in all_paths.items():
        if git(path, "status", "--porcelain"):
            raise RuntimeError("Dirty fixture baseline: " + str(path))
        states[name] = {"path": str(path), "branch": git(path, "branch", "--show-current"),
                        "head_sha": git(path, "rev-parse", "HEAD"), "clean": True}
    heads = {name: states[name]["head_sha"] for name in trees}
    data = {"repository": str(root), "base_sha": base, "historical_high_water_sha": high_water,
            "worktrees": states, "source_shas": sources,
            "runtime_variant": "combined",
            "subjects": [{"label": label, "start_path": str(root), "prompt": prompt}],
            "seed_todo_commit_changes": git(root, "log", "--all", "--format=commit %H %s",
                                              "--numstat", "--", ".csdd/todo.md")}
    if "alpha" in heads and "beta" in heads:
        data["raw_merge_tree"] = mechanical(root, heads)
    data.update(extra)
    return data


def integration(output, variant, order):
    case = output / f"integration-{variant}-{order}"
    root, base, high_water = initialize(case)
    trees = {label: worktree(root, case, label, base) for label in ("alpha", "beta")}
    sources = {label: prepare_export(path, label, base) for label, path in trees.items()}
    newer = task("T-target-maint-001", "Review offline audit export", "docs/audit.md", "audit-author")
    write(root, ".csdd/todo.md", todo(active=export_task("alpha") + "\n" + export_task("beta"),
          pending=newer, completed=old_completed(range(13, 8, -1))))
    target = commit(root, "Record newer target maintenance completion and accepted audit review")
    first, second = ("alpha", "beta") if order == "AB" else ("beta", "alpha")
    prompt = INTEGRATION_PROMPT.format(first="fixture/" + first, second="fixture/" + second)
    return entry(root, base, high_water, trees, sources, prompt, f"{variant}-{order}",
                 runtime_variant=variant, integration_order=[first, second], target_sha=target)


def no_op(output):
    root, base, high_water = initialize(output / "no-op")
    review = task("T-review-001", "Review existing alpha export", "src/alpha.py", "review-subject",
                  extra="  - Verification: python -m unittest tests.test_alpha passes; alpha unchanged\n",
                  updated=DATE)
    write(root, ".csdd/todo.md", todo(active=review, completed=old_completed(range(12, 7, -1))))
    seed = commit(root, "Record current alpha review checkpoint")
    return entry(root, base, high_water, {}, {"review_checkpoint": seed}, PROMPTS["no-op"], "no-op")


def waiting(output):
    case = output / "waiting-ready"
    root, base, high_water = initialize(case)
    alpha = worktree(root, case, "alpha", base)
    sources = prepare_export(alpha, "alpha", base)
    current = export_task("alpha", base, ready=True).replace("Updated: 2026-10-03", f"Updated: {DATE}")
    write(alpha, ".csdd/todo.md", todo(active=export_task("beta"), ready=current,
                                      pending=pending_maintenance(),
                                      completed=old_completed(range(12, 7, -1))))
    sources["current_checkpoint"] = commit(alpha, "Keep waiting alpha landing review visible")
    data = entry(root, base, high_water, {"alpha": alpha}, sources,
                 PROMPTS["waiting-ready"], "waiting-ready")
    data["subjects"][0]["start_path"] = str(alpha)
    return data


def overlap(output):
    case = output / "overlap"
    root, _, high_water = initialize(case)
    write(root, "src/pricing.py", "def total(items):\n    return sum(items)\n")
    identities = {"alpha": "T-round-total-001", "beta": "T-round-line-001"}
    def pricing_task(label, base=None, ready=False):
        extra = f"  - Target: main\n  - Base: {base}\n" if base else ""
        if ready:
            extra += f"  - Landing: Merge fixture/{label} after pricing rule agreement\n"
            extra += "  - Verification: implementation checked locally; pricing acceptance unresolved\n"
        return task(identities[label], f"Apply {label} pricing rule", "src/pricing.py",
                    f"{label}-author", extra=extra)
    write(root, ".csdd/todo.md", todo(active=pricing_task("alpha") + "\n" + pricing_task("beta"),
                                     completed=old_completed(range(12, 7, -1))))
    base = commit(root, "Record two pricing proposals requiring one rounding decision")
    trees = {label: worktree(root, case, label, base) for label in ("alpha", "beta")}
    heads = {}
    for label, path in trees.items():
        rule = "round(sum(items), 2)" if label == "alpha" else "sum(round(item, 2) for item in items)"
        write(path, "src/pricing.py", f"def total(items):\n    return {rule}\n")
        write(path, ".csdd/decisions.md", f"# Decisions\n\n## D-pricing — Rounding placement\n\n"
              f"Accepted direction on fixture/{label}: {rule}.\n"
              "Rationale: preserve the rounding unit selected by this branch's pricing proposal.\n"
              "No cross-branch agreement selects the integration rule.\n")
        other = "beta" if label == "alpha" else "alpha"
        write(path, ".csdd/todo.md", todo(active=pricing_task(other),
              ready=pricing_task(label, base, True), completed=old_completed(range(12, 7, -1))))
        heads[label] = commit(path, f"Prepare incompatible {label} pricing proposal")
    return entry(root, base, high_water, trees, heads, PROMPTS["overlap"], "overlap")


def same_task(output, cancellation=False):
    case_label = "cancellation-ready" if cancellation else "same-task-conflict"
    case = output / case_label
    root, _, high_water = initialize(case)
    identity = "T-export-review-001"
    original = task(identity, "Prepare CSV export review", "src/alpha.py; src/beta.py", "review-author",
                    owner="Export Team")
    write(root, ".csdd/todo.md", todo(active=original, completed=old_completed(range(12, 7, -1))))
    base = commit(root, "Accept one CSV review task under Export Team accountability")
    trees = {label: worktree(root, case, label, base) for label in ("alpha", "beta")}
    heads = {}
    for label, path in trees.items():
        write(path, f"src/{label}.py", f"def export_{label}():\n    return '{label}-review'\n")
        extra = f"  - Target: main\n  - Base: {base}\n"
        if label == "alpha":
            extra += "  - Landing: Merge fixture/alpha after export review\n  - Verification: alpha review checked locally\n"
            current = task(identity, "Prepare CSV export review", "src/alpha.py; src/beta.py",
                           "alpha-author", owner="Export Team", extra=extra)
            state = todo(ready=current, completed=old_completed(range(12, 7, -1)))
        else:
            extra += "  - Blocker: Export review approval and human accountability are unresolved\n"
            current = task(identity, "Prepare CSV export review", "src/alpha.py; src/beta.py",
                           "beta-author", owner="Operations Team", extra=extra)
            state = todo(blocked=current, completed=old_completed(range(12, 7, -1)))
        write(path, ".csdd/todo.md", state)
        heads[label] = commit(path, f"Record competing {label} review lifecycle and accountability")
    cancelled = None
    if cancellation:
        write(root, "README.md", "# Offline export utility\n\nmain is the integration target.\n\n"
              "Export Team cancelled T-export-review-001 on main after the branch base,\n"
              "because its review objective was withdrawn. No agreement resolves this\n"
              "cancellation versus the branch readiness/blocker or competing Owner changes.\n")
        write(root, ".csdd/todo.md", todo(completed=old_completed(range(12, 7, -1))))
        cancelled = commit(root, "Record explicit target cancellation of export review task")
    return entry(root, base, high_water, trees, heads, PROMPTS["same-task-conflict"],
                 case_label, target_cancellation_sha=cancelled)


def cancellation_ready(output):
    return same_task(output, cancellation=True)


def interrupted(output):
    # Same raw integration seed, plus a concrete review boundary and narrowed authority.
    data = integration(output, "boundary", "AB")
    root = Path(data["repository"])
    current = todo(active=export_task("alpha"), ready=export_task("beta", data["base_sha"], True),
                   pending=task("T-target-maint-001", "Review offline audit export", "docs/audit.md", "audit-author"),
                   completed=old_completed(range(13, 8, -1)))
    write(root, ".csdd/todo.md", current)
    review = commit(root, "Record beta waiting review claim in current target state")
    data["worktrees"]["main"]["head_sha"] = review
    data["target_sha"] = review
    data["runtime_variant"] = "combined"
    data["subjects"] = [{"label": "interrupted-landing", "start_path": str(root),
                          "prompt": PROMPTS["interrupted-landing"]}]
    data["raw_merge_tree"] = mechanical(root, {label: data["worktrees"][label]["head_sha"]
                                               for label in ("alpha", "beta")})
    data["seed_todo_commit_changes"] = git(root, "log", "--all", "--format=commit %H %s",
                                            "--numstat", "--", ".csdd/todo.md")
    return data


def section(text, title):
    match = re.search(r"^### " + re.escape(title) + r"\n", text, re.MULTILINE)
    if not match:
        raise RuntimeError("Missing pinned policy section: " + title)
    following = re.search(r"^#{1,3} ", text[match.end():], re.MULTILINE)
    end = match.end() + following.start() if following else len(text)
    return text[match.start():end]


def snapshot(root, ref):
    sha = git(root, "rev-parse", "--verify", ref + "^{commit}")
    paths = git(root, "ls-tree", "-r", "--name-only", sha, "--", "SKILL.md", "references", "assets").splitlines()
    if "SKILL.md" not in paths:
        raise RuntimeError("Runtime ref has no tracked SKILL.md")
    return sha, {path: git(root, "show", sha + ":" + path, raw=True) for path in paths}


def runtimes(output, source, baseline_ref, candidate_ref):
    baseline_sha, baseline = snapshot(source, baseline_ref)
    candidate_sha, candidate = snapshot(source, candidate_ref)
    allowed = {"SKILL.md", "references/document-contracts.md", "references/protocol.md",
               "assets/templates/todo.md", "references/migration-v0.1-to-v0.2.md"}
    changed = {path for path in set(baseline) | set(candidate) if baseline.get(path) != candidate.get(path)}
    if changed - allowed:
        raise RuntimeError("Runtime comparison includes unrelated tracked changes: " + repr(sorted(changed - allowed)))
    contracts = "references/document-contracts.md"
    selected = {"reduced-writes-only": ("Write economy", "write-economy"),
                "task-reconciliation-only": ("Task-wise landing reconciliation", "task-wise-landing-reconciliation")}
    result = {}
    for variant in VARIANTS:
        root = output / "runtimes" / variant
        root.mkdir(parents=True, exist_ok=False)
        git(root, "init", "--initial-branch=main")
        for path, content in baseline.items():
            destination = root / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content.encode("utf-8"))
        original = commit(root, "Snapshot committed baseline CSDD runtime")
        files = dict(baseline)
        if variant == "combined":
            files = candidate
        elif variant in selected:
            title, anchor = selected[variant]
            policy = section(candidate[contracts], title)
            marker = "## Document map\n"
            if files[contracts].count(marker) != 1:
                raise RuntimeError("Ambiguous baseline insertion marker")
            files[contracts] = files[contracts].replace(marker, policy + marker, 1)
            router = f"For {title.lower()}, consult [{title}](references/document-contracts.md#{anchor}).\n\n"
            marker = "### `todo.md` fast path\n"
            if files["SKILL.md"].count(marker) != 1:
                raise RuntimeError("Ambiguous baseline skill insertion marker")
            files["SKILL.md"] = files["SKILL.md"].replace(marker, router + marker, 1)
        for path, content in files.items():
            (root / path).write_bytes(content.encode("utf-8"))
        sha = original if variant == "baseline" else commit(root, f"Compose {variant} evaluation runtime")
        result[variant] = {"path": str(root), "commit_sha": sha, "baseline_snapshot_commit": original,
                           "source_repository": str(source), "baseline_source_sha": baseline_sha,
                           "candidate_source_sha": candidate_sha, "changed_source_paths": sorted(changed),
                           "policy_section": selected[variant][0] if variant in selected else variant,
                           "clean": not bool(git(root, "status", "--porcelain"))}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True, type=Path,
                        help="Absolute nonexistent directory; no reuse, reset, or deletion")
    parser.add_argument("--runtime-repo", type=Path, help="Absolute local repository containing both committed runtime refs")
    parser.add_argument("--baseline-ref", help="Committed baseline runtime ref; requires --runtime-repo and --candidate-ref")
    parser.add_argument("--candidate-ref", help="Committed combined runtime ref; requires --runtime-repo and --baseline-ref")
    args = parser.parse_args()
    output = args.output_root
    if not output.is_absolute():
        parser.error("--output-root must be absolute")
    if output.exists() or output.is_symlink():
        parser.error("--output-root already exists; choose a fresh path")
    if not shutil.which("git"):
        parser.error("Git must be available on PATH")
    runtime_args = (args.runtime_repo, args.baseline_ref, args.candidate_ref)
    if any(runtime_args) and not all(runtime_args):
        parser.error("Provide all three runtime arguments or none")
    if args.runtime_repo and not args.runtime_repo.is_absolute():
        parser.error("--runtime-repo must be absolute")
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    cases = {}
    for variant in VARIANTS:
        for order in ("AB", "BA"):
            label = f"integration-{variant}-{order}"
            cases[label] = integration(output, variant, order)
    # A paired campaign must start from the same Git objects, not merely similar text.
    signatures = {json.dumps({"base": item["base_sha"], "history": item["historical_high_water_sha"],
                              "target": item["target_sha"], "sources": item["source_shas"],
                              "heads": {name: state["head_sha"] for name, state in item["worktrees"].items()}},
                             sort_keys=True) for item in cases.values()}
    if len(signatures) != 1:
        raise RuntimeError("Integration campaign seeds have different initial Git SHAs")
    for label, builder in (("no-op", no_op), ("waiting-ready", waiting),
                           ("overlap", overlap), ("same-task-conflict", same_task),
                           ("cancellation-ready", cancellation_ready),
                           ("interrupted-landing", interrupted)):
        cases[label] = builder(output)
    runtime_entries = runtimes(output, args.runtime_repo, args.baseline_ref, args.candidate_ref) if all(runtime_args) else {}
    manifest = {"schema_version": 1, "output_root": str(output), "fixture_date": DATE,
                "cases": cases, "runtime_variants": list(VARIANTS), "runtime_snapshots": runtime_entries,
                "subject_executions": [],
                "notice": "Raw committed seeds and mechanical merge-tree observations only; no subject execution or grade."}
    destination = output / "manifest.json"
    destination.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(str(destination))


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError) as error:
        print("Fixture materialization failed; partial output retained: " + str(error), file=sys.stderr)
        sys.exit(1)
