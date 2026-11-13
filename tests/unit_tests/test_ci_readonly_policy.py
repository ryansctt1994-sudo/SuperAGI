"""Source guard: dormant fork CI must not grant write authority to tests.

This is configuration conformance only; it does not attest CI execution.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"


def test_ci_uses_readonly_token_and_unprivileged_checkout():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert re.search(r"(?m)^permissions:\s*\n  contents: read\s*$", source)
    assert not re.search(
        r"(?m)^\s*(?:contents|pull-requests|actions|checks|issues|packages|deployments):\s*write\s*$",
        source,
    )
    assert source.count("persist-credentials: false") == 2
    assert "github.event.pull_request.head.ref" not in source
    assert "github.event.pull_request.head.repo.full_name" not in source
    assert "pull_request_target:" not in source
    assert "workflow_dispatch:" not in source


def test_active_ci_triggers_are_explicit():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "\n  push:\n" in source
    assert "\n  pull_request:\n" in source
    assert 'branches: [ "main", "dev" ]' in source
