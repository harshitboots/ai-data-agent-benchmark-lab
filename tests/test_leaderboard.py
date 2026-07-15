import json
from datetime import datetime, timezone

from leaderboard import leaderboard_generator


def test_generate_includes_the_real_baseline_submission():
    leaderboard = leaderboard_generator.generate()

    assert "retail_sql_001" in leaderboard
    entries = leaderboard["retail_sql_001"]
    baseline_entries = [e for e in entries if e.agent_name == "baseline"]
    assert baseline_entries
    assert baseline_entries[0].final_score == 90.0


def _write_submission(directory, task_id, agent_name, submitted_by, final_score, timestamp=None):
    timestamp = timestamp or datetime.now(timezone.utc).isoformat(timespec="seconds")
    payload = {
        "task_id": task_id,
        "agent_name": agent_name,
        "category": "sql_analytics",
        "dimensions": {},
        "final_score": final_score,
        "elapsed_seconds": 0.1,
        "timestamp": timestamp,
        "error": None,
        "submitted_by": submitted_by,
    }
    path = directory / f"{task_id}__{agent_name}__{submitted_by}.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_generate_ranks_by_final_score_descending(tmp_path, monkeypatch):
    monkeypatch.setattr(leaderboard_generator, "SUBMISSIONS_DIR", tmp_path)
    _write_submission(tmp_path, "fake_task_001", "agent_a", "alice", final_score=50.0)
    _write_submission(tmp_path, "fake_task_001", "agent_b", "bob", final_score=80.0)

    leaderboard = leaderboard_generator.generate()

    entries = leaderboard["fake_task_001"]
    assert [e.agent_name for e in entries] == ["agent_b", "agent_a"]
    assert [e.rank for e in entries] == [1, 2]


def test_generate_keeps_only_the_newest_resubmission(tmp_path, monkeypatch):
    monkeypatch.setattr(leaderboard_generator, "SUBMISSIONS_DIR", tmp_path)
    _write_submission(
        tmp_path, "fake_task_001", "agent_a", "alice", final_score=50.0,
        timestamp="2026-01-01T00:00:00+00:00",
    )
    # Same (task, agent, submitter) resubmitted later with a different score —
    # writing to the same filename overwrites the file, exactly like a real resubmit.
    _write_submission(
        tmp_path, "fake_task_001", "agent_a", "alice", final_score=95.0,
        timestamp="2026-02-01T00:00:00+00:00",
    )

    leaderboard = leaderboard_generator.generate()

    entries = leaderboard["fake_task_001"]
    assert len(entries) == 1
    assert entries[0].final_score == 95.0


def test_generate_returns_empty_dict_when_no_submissions(tmp_path, monkeypatch):
    monkeypatch.setattr(leaderboard_generator, "SUBMISSIONS_DIR", tmp_path)

    assert leaderboard_generator.generate() == {}


def test_write_produces_results_json_and_markdown(tmp_path, monkeypatch):
    monkeypatch.setattr(leaderboard_generator, "SUBMISSIONS_DIR", tmp_path)
    monkeypatch.setattr(leaderboard_generator, "LEADERBOARD_DIR", tmp_path)
    monkeypatch.setattr(leaderboard_generator, "RESULTS_JSON", tmp_path / "results.json")
    monkeypatch.setattr(leaderboard_generator, "LEADERBOARD_MD", tmp_path / "leaderboard.md")
    _write_submission(tmp_path, "fake_task_001", "agent_a", "alice", final_score=50.0)

    leaderboard_generator.write(leaderboard_generator.generate())

    results = json.loads((tmp_path / "results.json").read_text(encoding="utf-8"))
    assert "fake_task_001" in results["tasks"]

    markdown = (tmp_path / "leaderboard.md").read_text(encoding="utf-8")
    assert "fake_task_001" in markdown
    assert "agent_a" in markdown
