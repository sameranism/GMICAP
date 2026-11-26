"""Regression fixtures for automated merge controls; all GitHub calls are mocked."""

import copy
from unittest.mock import Mock, call

import pytest

from tools import merge_guardian as guardian

REPO = "owner/repo"
A = "a" * 40
B = "b" * 40
ORDINARY = {"filename": "backend/modules/processing/classifier.py", "status": "modified"}
POLICY = {"filename": ".github/workflows/merge-guardian.yml", "status": "modified"}


def pr(sha=A, *, head_repo=REPO):
    return {
        "number": 3,
        "head": {"sha": sha, "repo": {"full_name": head_repo}},
        "base": {"ref": "main", "sha": "c" * 40, "repo": {"full_name": REPO}},
        "changed_files": 1,
        "state": "open",
        "draft": False,
        "merged_at": None,
        "merge_commit_sha": None,
    }


def rules():
    return [
        *({"type": name} for name in guardian.REQUIRED_RULES),
        {"type": "pull_request", "parameters": {"allowed_merge_methods": ["squash"]}},
        {"type": "required_status_checks", "parameters": {
            "strict_required_status_checks_policy": True,
            "required_status_checks": [{"context": name} for name in guardian.REQUIRED_CHECKS],
        }},
        {"type": "code_scanning", "parameters": {"code_scanning_tools": [{
            "tool": "CodeQL", "alerts_threshold": "all", "security_alerts_threshold": "all",
        }]}},
    ]


def test_protection_accepts_native_checks():
    guardian.verify_protection(rules())


@pytest.mark.parametrize("removed", [
    "deletion", "non_fast_forward", "required_signatures", "required_linear_history",
    "pull_request", "required_status_checks", "code_scanning",
])
def test_protection_rejects_missing_rule(removed):
    with pytest.raises(ValueError):
        guardian.verify_protection([rule for rule in rules() if rule["type"] != removed])


def test_protection_rejects_loose_checks():
    policy = rules()
    policy[-2]["parameters"]["strict_required_status_checks_policy"] = False
    with pytest.raises(ValueError, match="up-to-date"):
        guardian.verify_protection(policy)


def test_protection_rejects_weaker_codeql_threshold():
    policy = rules()
    policy[-1]["parameters"]["code_scanning_tools"][0]["security_alerts_threshold"] = "high"
    with pytest.raises(ValueError, match="CodeQL"):
        guardian.verify_protection(policy)


@pytest.mark.parametrize("files,head_repo", [([ORDINARY], "other/fork"), ([POLICY], REPO)])
def test_exact_head_has_pr_provenance(files, head_repo):
    guardian.evaluate(lambda: pr(head_repo=head_repo), lambda: files, A, REPO)


@pytest.mark.parametrize("files", [[], [ORDINARY, POLICY], [ORDINARY, ORDINARY]])
def test_incomplete_file_provenance_is_rejected(files):
    with pytest.raises(ValueError, match="file provenance"):
        guardian.evaluate(pr, lambda: files, A, REPO)


@pytest.mark.parametrize("file", [
    POLICY, ORDINARY | {"previous_filename": POLICY["filename"], "status": "renamed"},
])
def test_fork_cannot_change_control_paths(file):
    with pytest.raises(ValueError, match="must originate"):
        guardian.evaluate(lambda: pr(head_repo="other/fork"), lambda: [file], A, REPO)


def test_head_drift_before_evaluation():
    files = Mock()
    with pytest.raises(ValueError, match="revision"):
        guardian.evaluate(lambda: pr(B), files, A, REPO)
    files.assert_not_called()


def test_head_drift_during_evaluation():
    with pytest.raises(ValueError, match="changed"):
        guardian.evaluate(Mock(side_effect=[pr(), pr(B)]), lambda: [POLICY], A, REPO)


def test_base_drift_during_evaluation():
    changed = copy.deepcopy(pr())
    changed["base"]["sha"] = B
    with pytest.raises(ValueError, match="changed"):
        guardian.evaluate(Mock(side_effect=[pr(), changed]), lambda: [ORDINARY], A, REPO)


def test_draft_cannot_pass():
    with pytest.raises(ValueError, match="ready"):
        guardian.evaluate(lambda: pr() | {"draft": True}, lambda: [ORDINARY], A, REPO)


def test_audit_requires_the_actual_merge_commit():
    merged = pr() | {"state": "closed", "merged_at": "2026-11-26", "merge_commit_sha": B}
    guardian.evaluate(lambda: merged, lambda: [ORDINARY], A, REPO, merged_sha=B)
    with pytest.raises(ValueError, match="does not prove provenance"):
        guardian.evaluate(lambda: merged, lambda: [ORDINARY], A, REPO, merged_sha=A)


def test_stale_event_cannot_publish_status(monkeypatch):
    monkeypatch.setattr(guardian, "api", lambda path: pr(B))
    publish = Mock()
    monkeypatch.setattr(guardian, "status", publish)
    with pytest.raises(ValueError):
        guardian.run_pr(REPO, {"pull_request": pr()})
    publish.assert_not_called()


def test_api_failure_marks_exact_head_failed(monkeypatch):
    monkeypatch.setattr(guardian, "api", Mock(side_effect=[pr(), RuntimeError("API")]))
    publish = Mock()
    monkeypatch.setattr(guardian, "status", publish)
    with pytest.raises(RuntimeError):
        guardian.run_pr(REPO, {"pull_request": pr()})
    assert [(call.args[1], call.args[2]) for call in publish.call_args_list] == [
        (A, "pending"), (A, "failure"),
    ]


def workflow_runs():
    return [
        {"id": i, "path": path, "head_sha": A, "event": "pull_request",
         "status": "completed", "conclusion": "success", "run_number": 1, "run_attempt": 1}
        for i, path in enumerate(guardian.WORKFLOW_JOBS, 1)
    ]


def test_audit_checks_actual_workflow_paths_and_jobs(monkeypatch):
    def pages(path, key):
        if key == "workflow_runs":
            return workflow_runs()
        assert key == "jobs"
        run_id = int(path.split("/")[-4])
        jobs = list(guardian.WORKFLOW_JOBS.values())[run_id - 1]
        return [{"name": name, "conclusion": "success"} for name in jobs]

    monkeypatch.setattr(guardian, "pages", pages)
    assert guardian.verify_pr_checks(REPO, A) == [1, 2, 3, 4]


@pytest.mark.parametrize("change", [
    {"head_sha": B}, {"path": ".github/workflows/other.yml"}, {"event": "push"},
])
def test_audit_rejects_wrong_head_event_or_workflow(monkeypatch, change):
    runs = workflow_runs()
    runs[0].update(change)
    monkeypatch.setattr(guardian, "pages", Mock(return_value=runs))
    with pytest.raises(ValueError, match="Missing PR workflow"):
        guardian.verify_pr_checks(REPO, A)


def test_audit_prefers_latest_failed_run(monkeypatch):
    runs = workflow_runs()
    failed = runs[0] | {"run_number": 2, "conclusion": "failure"}
    monkeypatch.setattr(guardian, "pages", Mock(return_value=[failed, *runs]))
    with pytest.raises(ValueError, match="Latest PR workflow did not pass"):
        guardian.verify_pr_checks(REPO, A)


def test_audit_requires_individual_successful_jobs(monkeypatch):
    monkeypatch.setattr(guardian, "pages", Mock(side_effect=[workflow_runs(), []]))
    with pytest.raises(ValueError, match="Missing successful required jobs"):
        guardian.verify_pr_checks(REPO, A)

def test_provenance_index_can_catch_up_after_merge(monkeypatch):
    merged = pr() | {"state": "closed", "merged_at": "2026-11-26", "merge_commit_sha": B}
    lookup = Mock(side_effect=[[], [merged]])
    wait = Mock()
    monkeypatch.setattr(guardian, "pages", lookup)
    monkeypatch.setattr(guardian, "sleep", wait)
    assert guardian.find_merged_pr(REPO, B) == merged
    assert lookup.call_args_list == [call(f"repos/{REPO}/commits/{B}/pulls")] * 2
    wait.assert_called_once_with(2)


def test_provenance_retries_fail_closed_for_unrelated_merge(monkeypatch):
    unrelated = pr() | {"state": "closed", "merged_at": "2026-11-26", "merge_commit_sha": A}
    lookup = Mock(return_value=[unrelated])
    wait = Mock()
    monkeypatch.setattr(guardian, "pages", lookup)
    monkeypatch.setattr(guardian, "sleep", wait)
    assert guardian.find_merged_pr(REPO, B) is None
    assert lookup.call_count == 6
    assert wait.call_args_list == [call(2), call(4), call(8), call(16), call(24)]
