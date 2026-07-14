from arena.schema import ScoringWeights
from arena.scoring import DimensionResult


def compute_final_score(
    scoring: ScoringWeights, dimensions: dict[str, DimensionResult]
) -> float:
    """Combine per-dimension scores into a single 0-100 final score using task weights."""
    weights = {
        "execution": scoring.execution,
        "correctness": scoring.correctness,
        "efficiency": scoring.efficiency,
        "explanation": scoring.explanation,
        "cost_latency": scoring.cost_latency,
    }
    return sum(
        (weight / 100) * dimensions[name].score for name, weight in weights.items()
    )
