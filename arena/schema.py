from pydantic import BaseModel, Field


class ScoringWeights(BaseModel):
    execution: int
    correctness: int
    efficiency: int
    explanation: int
    cost_latency: int


class TaskSpec(BaseModel):
    id: str
    title: str
    category: str
    difficulty: str
    domain: str
    tools_allowed: list[str] = Field(default_factory=list)
    input_files: list[str] = Field(default_factory=list)
    expected_output: str | None = None
    time_limit_seconds: int
    max_cost_usd: float
    description: str
    success_criteria: list[str] = Field(default_factory=list)
    scoring: ScoringWeights
