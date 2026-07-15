from leaderboard.leaderboard_generator import LeaderboardEntry, generate_and_write


def build_leaderboard() -> dict[str, list[LeaderboardEntry]]:
    """Regenerate leaderboard/results.json + leaderboard.md and return the ranked data."""
    return generate_and_write()
