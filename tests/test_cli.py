"""Tests for the `aegize policy test` CLI."""

from __future__ import annotations

import textwrap

import pytest

from aegize.cli import main

POLICY = """
agents:
  research_bot:
    allow:
      - tool: web_search
        operations: ["search"]
        risk_level_max: medium
      - tool: file_reader
        operations: ["read"]
        paths: ["./safe_data/**"]
    require_approval:
      - tool: email
        operations: ["send"]
      - tool: shell
        operations: ["execute"]
    deny:
      - tool: payments
        operations: ["charge"]
      - tool: shell
        operations: ["rm", "delete"]
"""


@pytest.fixture
def policy_file(tmp_path):
    p = tmp_path / "policy.yaml"
    p.write_text(POLICY, encoding="utf-8")
    return p


def _write(tmp_path, body: str):
    f = tmp_path / "tests.yaml"
    f.write_text(textwrap.dedent(body), encoding="utf-8")
    return f


def run(policy_file, test_file):
    return main(["policy", "test", str(policy_file), str(test_file)])


def test_all_pass_returns_zero(policy_file, tmp_path, capsys):
    tf = _write(
        tmp_path,
        """
        tests:
          - name: search allowed
            agent: research_bot
            tool: web_search
            operation: search
            risk_level: low
            expect: allow
          - name: shell needs approval
            agent: research_bot
            tool: shell
            operation: execute
            risk_level: high
            expect: require_approval
          - name: payments denied
            agent: research_bot
            tool: payments
            operation: charge
            risk_level: critical
            expect: deny
        """,
    )
    code = run(policy_file, tf)
    out = capsys.readouterr().out
    assert code == 0
    assert "3 passed" in out
    assert "PASS" in out


def test_failing_case_returns_one(policy_file, tmp_path, capsys):
    tf = _write(
        tmp_path,
        """
        tests:
          - name: wrong expectation
            agent: research_bot
            tool: payments
            operation: charge
            risk_level: low
            expect: allow
        """,
    )
    code = run(policy_file, tf)
    out = capsys.readouterr().out
    assert code == 1
    assert "FAIL" in out


def test_risk_ceiling_enforced(policy_file, tmp_path, capsys):
    # web_search allows up to medium; high should be denied.
    tf = _write(
        tmp_path,
        """
        tests:
          - name: high-risk search denied
            agent: research_bot
            tool: web_search
            operation: search
            risk_level: high
            expect: deny
        """,
    )
    assert run(policy_file, tf) == 0


def test_metadata_path_allow_and_deny(policy_file, tmp_path, capsys):
    tf = _write(
        tmp_path,
        """
        tests:
          - name: read inside allowlist
            agent: research_bot
            tool: file_reader
            operation: read
            metadata: { path: "./safe_data/report.md" }
            expect: allow
          - name: read outside allowlist
            agent: research_bot
            tool: file_reader
            operation: read
            metadata: { path: "/etc/passwd" }
            expect: deny
        """,
    )
    code = run(policy_file, tf)
    assert code == 0
    assert "2 passed" in capsys.readouterr().out


def test_unknown_agent_denied(policy_file, tmp_path):
    tf = _write(
        tmp_path,
        """
        tests:
          - name: stranger denied
            agent: stranger
            tool: web_search
            operation: search
            expect: deny
        """,
    )
    assert run(policy_file, tf) == 0


def test_missing_policy_file_errors(tmp_path, capsys):
    tf = _write(
        tmp_path,
        """
        tests:
          - name: x
            agent: a
            tool: t
            operation: o
            expect: allow
        """,
    )
    code = main(["policy", "test", str(tmp_path / "nope.yaml"), str(tf)])
    assert code != 0
    assert "error" in capsys.readouterr().err.lower()


def test_missing_tests_key_errors(policy_file, tmp_path, capsys):
    tf = _write(tmp_path, "agents: []\n")
    code = run(policy_file, tf)
    assert code != 0
    assert "tests" in capsys.readouterr().err.lower()


def test_invalid_expect_errors(policy_file, tmp_path, capsys):
    tf = _write(
        tmp_path,
        """
        tests:
          - name: bad expect
            agent: research_bot
            tool: web_search
            operation: search
            expect: maybe
        """,
    )
    code = run(policy_file, tf)
    assert code != 0
    assert "expect" in capsys.readouterr().err.lower()


def test_invalid_risk_level_errors(policy_file, tmp_path, capsys):
    tf = _write(
        tmp_path,
        """
        tests:
          - name: bad risk
            agent: research_bot
            tool: web_search
            operation: search
            risk_level: spicy
            expect: allow
        """,
    )
    code = run(policy_file, tf)
    assert code != 0
    assert "risk" in capsys.readouterr().err.lower()


def test_missing_required_field_errors(policy_file, tmp_path, capsys):
    tf = _write(
        tmp_path,
        """
        tests:
          - name: no tool
            agent: research_bot
            operation: search
            expect: allow
        """,
    )
    code = run(policy_file, tf)
    assert code != 0
    assert "tool" in capsys.readouterr().err.lower()
