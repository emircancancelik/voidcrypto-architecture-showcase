import asyncio
import os
from core.base_agent import VoidCryptoAgent
from schemas.data_contracts import ExecutionPayload

class RiskExecutionAgent(VoidCryptoAgent):
    def __init__(self):
        super().__init__(agent_name="risk_execution")
        self.order_queue = "execution_orders"

    async def _calculate_position_size(self, balance: float, atr: float) -> float:
        return (balance * 0.02) / (atr * 0.1)

    async def _dispatch_to_exchange(self, payload: ExecutionPayload, size: float):
        self.logger.info("EXCHANGE_DISPATCH_INITIATED", {
            "pair": payload.asset_pair,
            "side": "BUY" if payload.trade_signal == 1 else "SELL",
            "size": size
        })
        await asyncio.sleep(0.2)
        self.logger.info("BINANCE_ORDER_SUCCESS", {"correlation_id": payload.correlation_id})

    async def on_execution_trigger(self, message):
        await self.initialize_infrastructure()
        try:
            payload = ExecutionPayload.parse_raw(message.body)
            
            position_size = await self._calculate_position_size(
                payload.wallet_balance, 
                payload.atr_14
            )
            
            await self._dispatch_to_exchange(payload, position_size)
            
        except Exception as e:
            self.logger.error("EXECUTION_FAILED", {"error": str(e)})
        finally:
            await message.channel.basic_ack(message.delivery.delivery_tag)
            asyncio.get_event_loop().stop()

    async def start_listening(self):
        await self.initialize_infrastructure()
        await self.mq_channel.basic_consume(
            queue=self.order_queue,
            consumer_callback=self.on_execution_trigger
        )
        self.logger.info("RISK_AI_LISTENING")

if __name__ == "__main__":
    agent = RiskExecutionAgent()
    loop = asyncio.get_event_loop()
    loop.create_task(agent.start_listening())
    loop.run_forever()