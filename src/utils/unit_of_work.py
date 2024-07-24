from abc import ABC, abstractmethod

from src.database.db import async_session_maker
from src.repositories.str_repository import SpimexTradingResultsRepository


class AbstractUnitOfWork(ABC):

    spimex_trading_result: SpimexTradingResultsRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.spimex_trading_result = SpimexTradingResultsRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
