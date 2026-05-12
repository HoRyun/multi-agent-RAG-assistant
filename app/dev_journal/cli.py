from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


JOURNAL_ROOT = Path(".dev-journal")
TRACES_DIR = JOURNAL_ROOT / "traces"
JOURNALS_DIR = JOURNAL_ROOT / "journals"


def _trace_path(task_id: str) -> Path:
    return TRACES_DIR / f"{task_id}.json"


def _journal_path(task_id: str) -> Path:
    return JOURNALS_DIR / f"{task_id}.md"


def _load_trace(task_id: str) -> dict[str, Any]:
    path = _trace_path(task_id)
    if not path.exists():
        raise FileNotFoundError(f"Trace not found for task_id: {task_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def _save_trace(trace: dict[str, Any]) -> Path:
    TRACES_DIR.mkdir(parents=True, exist_ok=True)
    path = _trace_path(str(trace["task_id"]))
    path.write_text(
        json.dumps(trace, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def _new_trace(task_id: str, goal: str) -> dict[str, Any]:
    return {
        "task_id": task_id,
        "goal": goal,
        "tests": [],
        "reviews": [],
        "decisions": [],
        "lessons": [],
    }


def _append_entry(task_id: str, section: str, entry: dict[str, str]) -> None:
    trace = _load_trace(task_id)
    trace[section].append(entry)
    _save_trace(trace)


def _render_journal(trace: dict[str, Any]) -> str:
    lines = [
        f"# Agent Development Journal: {trace['task_id']}",
        "",
        "## Goal",
        str(trace["goal"]),
        "",
        "## Tests",
    ]

    if trace["tests"]:
        for item in trace["tests"]:
            lines.append(f"- `{item['command']}` -> {item['result']}: {item['note']}")
    else:
        lines.append("- None")

    lines.extend(["", "## Reviews"])
    if trace["reviews"]:
        for item in trace["reviews"]:
            lines.append(f"- {item['severity']}: {item['note']}")
    else:
        lines.append("- None")

    lines.extend(["", "## Decisions"])
    if trace["decisions"]:
        for item in trace["decisions"]:
            lines.append(f"- {item['note']}")
            lines.append(f"  - Reason: {item['reason']}")
    else:
        lines.append("- None")

    lines.extend(["", "## Lessons"])
    if trace["lessons"]:
        for item in trace["lessons"]:
            lines.append(f"- {item['note']}")
    else:
        lines.append("- None")

    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dev-journal")
    subparsers = parser.add_subparsers(dest="action", required=True)

    new_parser = subparsers.add_parser("new")
    new_parser.add_argument("task_id")
    new_parser.add_argument("--goal", required=True)

    test_parser = subparsers.add_parser("add-test")
    test_parser.add_argument("task_id")
    test_parser.add_argument("--command", dest="test_command", required=True)
    test_parser.add_argument("--result", required=True)
    test_parser.add_argument("--note", required=True)

    review_parser = subparsers.add_parser("add-review")
    review_parser.add_argument("task_id")
    review_parser.add_argument("--severity", required=True)
    review_parser.add_argument("--note", required=True)

    decision_parser = subparsers.add_parser("add-decision")
    decision_parser.add_argument("task_id")
    decision_parser.add_argument("--note", required=True)
    decision_parser.add_argument("--reason", required=True)

    lesson_parser = subparsers.add_parser("add-lesson")
    lesson_parser.add_argument("task_id")
    lesson_parser.add_argument("--note", required=True)

    export_parser = subparsers.add_parser("export")
    export_parser.add_argument("task_id")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.action == "new":
            _save_trace(_new_trace(args.task_id, args.goal))
        elif args.action == "add-test":
            _append_entry(
                args.task_id,
                "tests",
                {
                    "command": args.test_command,
                    "result": args.result,
                    "note": args.note,
                },
            )
        elif args.action == "add-review":
            _append_entry(
                args.task_id,
                "reviews",
                {
                    "severity": args.severity,
                    "note": args.note,
                },
            )
        elif args.action == "add-decision":
            _append_entry(
                args.task_id,
                "decisions",
                {
                    "note": args.note,
                    "reason": args.reason,
                },
            )
        elif args.action == "add-lesson":
            _append_entry(args.task_id, "lessons", {"note": args.note})
        elif args.action == "export":
            trace = _load_trace(args.task_id)
            JOURNALS_DIR.mkdir(parents=True, exist_ok=True)
            _journal_path(args.task_id).write_text(
                _render_journal(trace),
                encoding="utf-8",
            )
    except FileNotFoundError as exc:
        parser.error(str(exc))

    return 0


def console() -> None:
    raise SystemExit(main())


if __name__ == "__main__":
    console()
