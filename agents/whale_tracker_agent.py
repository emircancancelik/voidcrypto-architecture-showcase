import asyncio
from datetime import datetime
from core.base_agent import VoidCryptoAgent
from schemas.data_contracts import AgentSignal

class WhaleTrackerAgent(VoidCryptoAgent):
    def __init__(self):
        super().__init__(agent_name="whale_tracker")
        self.volume_threshold = 1000000.0

    async def fetch_onchain_data(self):
        return [{"asset": "BTC", "amount": 1500.0, "type": "exchange_outflow"}]

    async def process_cycle(self):
        await self.initialize_infrastructure()
        flows = await self.fetch_onchain_data()
        
        for flow in flows:
            if flow["amount"] > self.volume_threshold:
                signal = AgentSignal(
                    agent_id=self.agent_name,
                    asset_pair=f"{flow['asset']}USDT",
                    trade_signal=1 if flow["type"] == "exchange_outflow" else -1,
                    confidence=0.94,
                    observation_epoch=datetime.now().timestamp()
                )
                
                await self.redis_client.set(
                    f"void:signal:{self.agent_name}", 
                    signal.json(), 
                    ex=300
                )
                self.logger.info("WHALE_SIGNAL_PUBLISHED", {"asset": signal.asset_pair})
        
        await self.shutdown()

if __name__ == "__main__":
    asyncio.run(WhaleTrackerAgent().process_cycle())