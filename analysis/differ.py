import difflib
from pydantic import BaseModel, ConfigDict


class DiffResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    is_interesting: bool
    similarity_score: float
    time_ratio: float
    reason: str


class Differ:
    def __init__(self, baseline: str, baseline_time: float = 0.3, similarity_threshold: float = 0.8, time_multiplier: float = 3.0):
        self.baseline = baseline
        self.baseline_time = max(baseline_time, 0.001)
        self.similarity_threshold = similarity_threshold
        self.time_multiplier = time_multiplier

    def compare(self, body: str, elapsed: float) -> DiffResult:
        matcher = difflib.SequenceMatcher(None, self.baseline, body)
        similarity = matcher.ratio()

        time_ratio = elapsed / self.baseline_time
        reasons = []

        if similarity < self.similarity_threshold:
            reasons.append(f"Body similarity drop ({similarity:.2f} < {self.similarity_threshold:.2f})")

        if time_ratio >= self.time_multiplier:
            reasons.append(f"Response timing spike ({elapsed:.2f}s vs baseline {self.baseline_time:.2f}s)")

        is_interesting = len(reasons) > 0
        reason_str = " | ".join(reasons) if reasons else "No significant deviation"

        return DiffResult(
            is_interesting=is_interesting,
            similarity_score=similarity,
            time_ratio=time_ratio,
            reason=reason_str,
        )
