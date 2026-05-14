import os
import asyncio
import aiormq
import aioredis
from abc import ABC, abstractmethod
from shared.logging_factory import get_structured_logger

class VoidCryptoAgent(ABC):
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = get_structured_logger(agent_name)
        self.rabbitmq_url = os.getenv("RABBITMQ_URL")
        self.redis_url = os.getenv("REDIS_URL")
        self.mq_connection = None
        self.mq_channel = None
        self.redis_client = None

    async def initialize_infrastructure(self):
        try:
            self.redis_client = await aioredis.from_url(self.redis_url, decode_responses=True)
            self.mq_connection = await aiormq.connect(self.rabbitmq_url)
            self.mq_channel = await self.mq_connection.channel()
            self.logger.info("INFRA_CONNECTION_ESTABLISHED", {"provider": "Azure"})
        except Exception as e:
            self.logger.critical("INFRA_CONNECTION_FAILED", {"error": str(e)})
            raise

    @abstractmethod
    async def process_cycle(self):
        pass

    async def shutdown(self):
        if self.mq_connection:
            await self.mq_connection.close()
        if self.redis_client:
            await self.redis_client.close()
        self.logger.info("AGENT_SHUTDOWN_COMPLETE")