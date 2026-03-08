from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class EvaluationResult:
    """Container for evaluation metrics."""

    accuracy: int
    research_quality: int
    speed: int
    usefulness: int
    overall: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _clamp(score: float, minimum: int = 1, maximum: int = 10_000) -> int:
    return int(max(minimum, min(maximum, round(score))))


def evaluate_response(
    question: str,
    answer: str,
    elapsed_seconds: float,
) -> EvaluationResult:
    """
    Simple heuristic scoring system for the agent's response.

    All scores are in the range [1, 10_000].

    Heuristics (very lightweight and beginner friendly):
        - accuracy: penalize explicit uncertainty like "I don't know".
        - research_quality: reward longer, more detailed responses.
        - speed: faster responses score higher.
        - usefulness: reward structured, step-by-step answers.
    """
    text = (answer or "").lower()

    # Accuracy heuristic
    if "i don't know" in text or "cannot answer" in text:
        accuracy = 1_500
    else:
        accuracy = 7_000

    # Research quality heuristic (based on length)
    length = len(answer or "")
    if length < 400:
        research_quality = 3_000
    elif length < 1_000:
        research_quality = 6_000
    else:
        research_quality = 8_000

    # Speed heuristic (faster is better)
    if elapsed_seconds <= 5:
        speed = 9_000
    elif elapsed_seconds <= 15:
        speed = 7_000
    elif elapsed_seconds <= 30:
        speed = 5_000
    else:
        speed = 3_000

    # Usefulness heuristic (look for steps and structure)
    has_steps = any(prefix in text for prefix in ["1.", "step 1", "- "])
    has_headings = any(h in text for h in ["context", "solution", "plan"])

    usefulness = 4_000
    if has_steps:
        usefulness += 2_000
    if has_headings:
        usefulness += 2_000

    usefulness = _clamp(usefulness)

    # Overall is a weighted combination
    overall = _clamp(
        0.3 * accuracy + 0.3 * research_quality + 0.2 * speed + 0.2 * usefulness
    )

    return EvaluationResult(
        accuracy=_clamp(accuracy),
        research_quality=_clamp(research_quality),
        speed=_clamp(speed),
        usefulness=usefulness,
        overall=overall,
    )

