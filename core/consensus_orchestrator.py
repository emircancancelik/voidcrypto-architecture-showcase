from typing import List
from .data_contracts import AgentSignal, ExecutionPayload

class ConsensusOrchestrator:
    def __init__(self, threshold: float = 0.75):
        self.threshold = threshold

    async def aggregate_signals(self, signals: List[AgentSignal]) -> float:
        total_confidence = sum([s.confidence for s in signals]) / len(signals)
        return total_confidence

    def generate_execution_intent(self, final_score: float) -> bool:
        return final_score >= self.threshold