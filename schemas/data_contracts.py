from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class AgentSignal(BaseModel):
    agent_id: str
    asset_pair: str = Field(..., pattern=r"^[A-Z0-9]{5,12}$")
    trade_signal: int = Field(..., description="1: LONG, -1: SHORT, 0: NOMINAL")
    confidence: float = Field(..., ge=0.0, le=1.0)
    observation_epoch: float # Unix timestamp
    metadata: Optional[dict] = None

class ExecutionPayload(BaseModel):
    correlation_id: str
    trade_signal: int
    asset_pair: str
    current_price: float
    atr_14: float
    wallet_balance: float