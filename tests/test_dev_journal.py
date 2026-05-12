import json
from pathlib import Path

from app.dev_journal.cli import main


def test_new_creates_trace_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    exit_code = main(["new", "task-1", "--goal", "Build the MVP"])

    assert exit_code == 0
    trace_path = Path(".dev-journal/traces/task-1.json")
    assert trace_path.exists()

    trace = json.loads(trace_path.read_text(encoding="utf-8"))
    assert trace["task_id"] == "task-1"
    assert trace["goal"] == "Build the MVP"
    assert trace["tests"] == []
    assert trace["reviews"] == []
    assert trace["decisions"] == []
    assert trace["lessons"] == []


def test_add_commands_append_entries(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    main(["new", "task-1", "--goal", "Build the MVP"])

    assert (
        main(
            [
                "add-test",
                "task-1",
                "--command",
                "pytest",
                "--result",
                "passed",
                "--note",
                "baseline green",
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "add-review",
                "task-1",
                "--severity",
                "medium",
                "--note",
                "README needs example",
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "add-decision",
                "task-1",
                "--note",
                "Use JSON files",
                "--reason",
                "MVP forbids DB",
            ]
        )
        == 0
    )
    assert main(["add-lesson", "task-1", "--note", "Keep CLI small"]) == 0

    trace = json.loads(
        Path(".dev-journal/traces/task-1.json").read_text(encoding="utf-8")
    )
    assert trace["tests"] == [
        {
            "command": "pytest",
            "result": "passed",
            "note": "baseline green",
        }
    ]
    assert trace["reviews"] == [
        {
            "severity": "medium",
            "note": "README needs example",
        }
    ]
    assert trace["decisions"] == [
        {
            "note": "Use JSON files",
            "reason": "MVP forbids DB",
        }
    ]
    assert trace["lessons"] == [{"note": "Keep CLI small"}]


def test_export_writes_markdown_journal(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    main(["new", "task-1", "--goal", "Build the MVP"])
    main(
        [
            "add-test",
            "task-1",
            "--command",
            "pytest",
            "--result",
            "passed",
            "--note",
            "all tests pass",
        ]
    )
    main(
        [
            "add-review",
            "task-1",
            "--severity",
            "low",
            "--note",
            "Add usage docs",
        ]
    )
    main(
        [
            "add-decision",
            "task-1",
            "--note",
            "Use argparse",
            "--reason",
            "standard library is enough",
        ]
    )
    main(["add-lesson", "task-1", "--note", "Small files are easy to review"])

    assert main(["export", "task-1"]) == 0

    journal_path = Path(".dev-journal/journals/task-1.md")
    assert journal_path.exists()
    journal = journal_path.read_text(encoding="utf-8")
    assert "# Agent Development Journal: task-1" in journal
    assert "## Goal\nBuild the MVP" in journal
    assert "- `pytest` -> passed: all tests pass" in journal
    assert "- low: Add usage docs" in journal
    assert "- Use argparse\n  - Reason: standard library is enough" in journal
    assert "- Small files are easy to review" in journal
