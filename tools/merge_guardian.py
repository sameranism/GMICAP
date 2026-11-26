"""Validate branch controls and PR provenance using only the trusted base."""
from __future__ import annotations

import json
import os
import re
import subprocess
from time import sleep

CONTEXT = "etemad/trusted-guardian"
WORKFLOW_JOBS = {
    ".github/workflows/backend-ci.yml": {"backend"},
    ".github/workflows/contract-check.yml": {
        "backend unit tests", "contract layer (S00-017 / S00-018)",
    },
    ".github/workflows/bootstrap-check.yml": {"verify-bootstrap"},
    ".github/workflows/codeql.yml": {
        "Analyze (actions)", "Analyze (javascript-typescript)", "Analyze (python)",
    },
}
REQUIRED_CHECKS = set().union(*(
    jobs for path, jobs in WORKFLOW_JOBS.items() if not path.endswith("/codeql.yml")
))
POLICY_FILES = {"tools/merge_guardian.py", "tools/check_gate00.py"}
REQUIRED_RULES = {"deletion", "non_fast_forward", "required_linear_history", "required_signatures"}


def verify_protection(rules):
    by_type = {}
    for rule in rules:
        by_type.setdefault(rule["type"], []).append(rule.get("parameters", {}))
    if missing := REQUIRED_RULES - by_type.keys():
        raise ValueError(f"Required branch controls missing: {', '.join(sorted(missing))}")
    if not any(pr.get("allowed_merge_methods") == ["squash"] for pr in by_type.get("pull_request", [])):
        raise ValueError("Protected main must require squash merges through a PR")
    strict_checks = {
        check["context"]
        for rule in by_type.get("required_status_checks", [])
        if rule.get("strict_required_status_checks_policy") and not rule.get("do_not_enforce_on_create")
        for check in rule["required_status_checks"]
    }
    if missing := REQUIRED_CHECKS - strict_checks:
        raise ValueError(f"Required up-to-date checks missing: {', '.join(sorted(missing))}")
    if not any(
        tool.get("tool") == "CodeQL"
        and tool.get("alerts_threshold") == tool.get("security_alerts_threshold") == "all"
        for rule in by_type.get("code_scanning", [])
        for tool in rule["code_scanning_tools"]
    ):
        raise ValueError("Required CodeQL scanning or its alert thresholds are missing")


def snapshot(pr, expected, repo, *, merged_sha=None):
    if (not re.fullmatch(r"[0-9a-f]{40}", expected)
            or pr["head"]["sha"] != expected or pr["base"]["ref"] != "main"
            or pr["base"]["repo"]["full_name"].casefold() != repo.casefold()):
        raise ValueError("PR revision or base changed")
    if merged_sha is None:
        if pr["state"] != "open" or pr["draft"]:
            raise ValueError("PR must be open and ready")
    elif not pr["merged_at"] or pr["merge_commit_sha"] != merged_sha:
        raise ValueError("PR does not prove provenance for the main commit")
    head_repo = (pr["head"].get("repo") or {}).get("full_name")
    return (pr["head"]["sha"], head_repo, pr["base"]["sha"], pr["changed_files"],
            pr["state"], pr["draft"], pr["merge_commit_sha"] if merged_sha else None)


def evaluate(get_pr, get_files, expected, repo, *, merged_sha=None):
    before = snapshot(get_pr(), expected, repo, merged_sha=merged_sha)
    files = get_files()
    filenames = {item["filename"] for item in files}
    if not filenames or len(files) != before[3] or len(filenames) != len(files):
        raise ValueError("Incomplete PR file provenance")
    if merged_sha is None:
        paths = filenames | {item["previous_filename"] for item in files if item.get("previous_filename")}
        head_repo = before[1]
        if any(path.startswith(".github/") or path in POLICY_FILES for path in paths) and (
            not head_repo or head_repo.casefold() != repo.casefold()
        ):
            raise ValueError("Repository control changes must originate on a repository branch")
    if snapshot(get_pr(), expected, repo, merged_sha=merged_sha) != before:
        raise ValueError("PR changed during provenance evaluation")


def command(*args):
    return subprocess.check_output(args, text=True)


def api(path):
    return json.loads(command("gh", "api", path))


def pages(path, key=None):
    data = json.loads(command("gh", "api", "--paginate", "--slurp", path))
    return [item for page in data for item in (page if key is None else page[key])]


def inspect(repo, number, expected, *, merged_sha=None):
    root = f"repos/{repo}/pulls/{number}"
    evaluate(lambda: api(root), lambda: pages(root + "/files"), expected, repo, merged_sha=merged_sha)


def status(repo, sha, state, description):
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("Invalid commit SHA")
    url = f"{os.environ['GITHUB_SERVER_URL']}/{repo}/actions/runs/{os.environ['GITHUB_RUN_ID']}"
    command("gh", "api", "--method", "POST", f"repos/{repo}/statuses/{sha}",
            "-f", f"state={state}", "-f", f"context={CONTEXT}",
            "-f", f"description={description}", "-f", f"target_url={url}")


def run_pr(repo, payload):
    pr = payload["pull_request"]
    number, sha = int(pr["number"]), pr["head"]["sha"]
    # A stale event must never write a result against a different PR revision.
    snapshot(api(f"repos/{repo}/pulls/{number}"), sha, repo)
    status(repo, sha, "pending", "Checking PR provenance and native branch controls")
    try:
        verify_protection(api(f"repos/{repo}/rules/branches/main"))
        inspect(repo, number, sha)
    except Exception:
        status(repo, sha, "failure", "PR provenance or native branch controls could not be verified")
        raise
    status(repo, sha, "success", "Exact PR provenance and native branch controls verified")


def verify_pr_checks(repo, sha):
    root = f"repos/{repo}"
    runs = pages(f"{root}/actions/runs?head_sha={sha}&event=pull_request", "workflow_runs")
    verified = []
    for path, names in WORKFLOW_JOBS.items():
        candidates = [
            run for run in runs
            if run["path"] == path and run["head_sha"] == sha and run["event"] == "pull_request"
        ]
        if not candidates:
            raise ValueError(f"Missing PR workflow evidence: {path}")
        latest = max(candidates, key=lambda run: (run["run_number"], run["run_attempt"]))
        if latest["status"] != "completed" or latest["conclusion"] != "success":
            raise ValueError(f"Latest PR workflow did not pass: {path}")
        jobs = pages(f"{root}/actions/runs/{latest['id']}/attempts/{latest['run_attempt']}/jobs", "jobs")
        if not names <= {job["name"] for job in jobs if job["conclusion"] == "success"}:
            raise ValueError(f"Missing successful required jobs: {path}")
        verified.append(latest["id"])
    return verified


def find_merged_pr(repo, sha):
    """Allow GitHub's commit-to-PR index to catch up after the main push."""
    for delay in (0, 2, 4, 8, 16, 24):
        if delay:
            sleep(delay)
        candidates = pages(f"repos/{repo}/commits/{sha}/pulls")
        for pr in candidates:
            if (pr["merged_at"] and pr["merge_commit_sha"] == sha
                    and pr["base"]["ref"] == "main"
                    and pr["base"]["repo"]["full_name"].casefold() == repo.casefold()):
                return pr
    return None


def audit_push(repo, before, after):
    subprocess.run(["git", "merge-base", "--is-ancestor", before, after], check=True)
    verify_protection(api(f"repos/{repo}/rules/branches/main"))
    commits = command("git", "rev-list", "--first-parent", f"{before}..{after}").split()
    failures = []
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary:
        print("| Main commit | Pull request | Provenance and CI |", file=summary)
        print("| --- | --- | --- |", file=summary)
        for sha in commits:
            merged = find_merged_pr(repo, sha)
            if merged is None:
                print(f"Main commit {sha}: no matching merged PR after bounded retries")
                print(f"| `{sha}` | — | MISSING_PR |", file=summary)
                failures.append(sha)
                continue
            number, head = merged["number"], merged["head"]["sha"]
            try:
                inspect(repo, number, head, merged_sha=sha)
                run_ids = verify_pr_checks(repo, head)
            except (ValueError, KeyError, subprocess.CalledProcessError) as exc:
                print(f"Main commit {sha}, PR #{number}: {exc}")
                print(f"| `{sha}` | #{number} | FAILED |", file=summary)
                failures.append(sha)
            else:
                links = ", ".join(
                    f"[{run_id}]({os.environ['GITHUB_SERVER_URL']}/{repo}/actions/runs/{run_id})"
                    for run_id in run_ids
                )
                print(f"| `{sha}` | #{number} | PASS, head `{head}`, {links} |", file=summary)
    if failures:
        raise SystemExit(f"Missing PR provenance or CI evidence for {len(failures)} main commit(s)")


if __name__ == "__main__":
    repo = os.environ["GITHUB_REPOSITORY"]
    event = os.environ["GITHUB_EVENT_NAME"]
    with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as handle:
        payload = json.load(handle)
    if event == "push":
        audit_push(repo, payload["before"], payload["after"])
    elif event == "pull_request_target":
        run_pr(repo, payload)
    else:
        raise SystemExit("Unsupported workflow event")
