import pytest
from core.data_contracts import AgentSignal

def test_pydantic_signal_validation():
    invalid_data = {
        "agent_id": "whale_tracker",
        "trade_signal": 5,
        "confidence": 1.2  
    }
    with pytest.raises(ValueError):
        AgentSignal(**invalid_data)