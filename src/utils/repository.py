from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from filters.src_filter import STRFilter


class AbstractRepository(ABC):

    @abstractmethod
    async def get_last_trading_dates_by_query(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_dynamics_by_query(self, *args, **kwargs):
        raise NotImplementedError

    async def get_trading_results_by_query(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_data(self, *args, **kwargs):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_last_trading_dates_by_query(
        self, *args, **kwargs
    ) -> Sequence[type(model)]:
        query = select(self.model.date).distinct()
        result: Result = await self.session.execute(query)
        return result.scalars().all()

    async def get_dynamics_by_query(
        self, start_date, end_date, str_filter: STRFilter, *args, **kwargs
    ) -> Sequence[type(model)]:
        query = str_filter.filter(
            select(self.model).where(self.model.date.between(start_date, end_date))
        )
        result: Result = await self.session.execute(query.order_by(self.model.date))
        return result.scalars().all()

    async def get_trading_results_by_query(
        self, str_filter: STRFilter, *args, **kwargs
    ) -> Sequence[type(model)]:
        query = str_filter.filter(select(self.model))
        result: Result = await self.session.execute(query.order_by(self.model.date))
        return result.scalars().all()

    async def delete_data(self, *args, **kwargs) -> None:
        query = delete(self.model)
        await self.session.execute(query)
