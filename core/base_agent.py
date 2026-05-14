from abc import ABC, abstractmethod
import logging

class VoidCryptoAgent(ABC):
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = logging.getLogger(agent_name)

    @abstractmethod
    async def connect_infrastructure(self):
        pass

    @abstractmethod
    async def process_cycle(self):
        pass