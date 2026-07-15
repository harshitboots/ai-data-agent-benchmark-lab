"""Aggregates leaderboard/submissions/*.json into results.json + leaderboard.md.

Runnable standalone (`python -m leaderboard.leaderboard_generator`) so CI can
regenerate the leaderboard without going through the `arena` CLI.
"""

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from arena.config import LEADERBOARD_DIR, SUBMISSIONS_DIR

RESULTS_JSON = LEADERBOARD_DIR / "results.json"
LEADERBOARD_MD = LEADERBOARD_DIR / "leaderboard.md"


@dataclass
class LeaderboardEntry:
    rank: int
    agent_name: str
    submitted_by: str
    final_score: float
    category: str
    timestamp: str


def load_submissions() -> list[dict]:
    """Read every submission file, keeping the newest per (task, agent, submitter)."""
    if not SUBMISSIONS_DIR.exists():
        return []

    latest: dict[tuple[str, str, str], dict] = {}
    for path in sorted(SUBMISSIONS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        submitted_by = data.get("submitted_by", "anonymous")
        key = (data["task_id"], data["agent_name"], submitted_by)
        existing = latest.get(key)
        if existing is None or data["timestamp"] > existing["timestamp"]:
            latest[key] = data

    return list(latest.values())


def generate() -> dict[str, list[LeaderboardEntry]]:
    """Group submissions by task_id and rank each task's entries by final_score."""
    by_task: dict[str, list[dict]] = {}
    for submission in load_submissions():
        by_task.setdefault(submission["task_id"], []).append(submission)

    leaderboard: dict[str, list[LeaderboardEntry]] = {}
    for task_id, submissions in by_task.items():
        ranked = sorted(submissions, key=lambda s: s["final_score"], reverse=True)
        leaderboard[task_id] = [
            LeaderboardEntry(
                rank=i,
                agent_name=s["agent_name"],
                submitted_by=s.get("submitted_by", "anonymous"),
                final_score=s["final_score"],
                category=s["category"],
                timestamp=s["timestamp"],
            )
            for i, s in enumerate(ranked, start=1)
        ]
    return leaderboard


def _render_markdown(leaderboard: dict[str, list[LeaderboardEntry]]) -> str:
    lines = ["# Leaderboard", ""]
    if not leaderboard:
        lines.append("No submissions yet — see `leaderboard/submissions/README.md`.")
        return "\n".join(lines) + "\n"

    for task_id in sorted(leaderboard):
        lines.append(f"## {task_id}")
        lines.append("")
        lines.append("| Rank | Agent | Score | Submitted by | Timestamp |")
        lines.append("|---|---|---|---|---|")
        for entry in leaderboard[task_id]:
            lines.append(
                f"| {entry.rank} | {entry.agent_name} | {entry.final_score:.1f} "
                f"| {entry.submitted_by} | {entry.timestamp} |"
            )
        lines.append("")
    return "\n".join(lines)


def write(leaderboard: dict[str, list[LeaderboardEntry]]) -> None:
    """Write results.json and leaderboard.md to leaderboard/."""
    LEADERBOARD_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tasks": {
            task_id: [asdict(entry) for entry in entries]
            for task_id, entries in leaderboard.items()
        },
    }
    RESULTS_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    LEADERBOARD_MD.write_text(_render_markdown(leaderboard), encoding="utf-8")


def generate_and_write() -> dict[str, list[LeaderboardEntry]]:
    leaderboard = generate()
    write(leaderboard)
    return leaderboard


if __name__ == "__main__":
    result = generate_and_write()
    total = sum(len(entries) for entries in result.values())
    print(f"Wrote {RESULTS_JSON} and {LEADERBOARD_MD} ({total} entries across {len(result)} task(s)).")
