from typing import Any, Sequence

from filters.src_filter import STRFilter
from src.utils.unit_of_work import UnitOfWork


class BaseService:

    base_repository: str = None

    @classmethod
    async def get_last_trading_dates_by_query(
        cls, uow: UnitOfWork, **kwargs
    ) -> Sequence[Any]:
        async with uow:
            result = await uow.__dict__[
                cls.base_repository
            ].get_last_trading_dates_by_query(**kwargs)
            return result

    @classmethod
    async def get_dynamics_by_query(
        cls, start_date, end_date, uow: UnitOfWork, str_filter: STRFilter, **kwargs
    ) -> Sequence[Any]:
        async with uow:
            result = await uow.__dict__[cls.base_repository].get_dynamics_by_query(
                start_date, end_date, str_filter, **kwargs
            )
            return result

    @classmethod
    async def get_trading_results_by_query(
        cls, uow: UnitOfWork, str_filter: STRFilter, **kwargs
    ) -> Sequence[Any]:
        async with uow:
            result = await uow.__dict__[
                cls.base_repository
            ].get_trading_results_by_query(str_filter, **kwargs)
            return result

    @classmethod
    async def delete_data(cls, uow: UnitOfWork, **kwargs) -> None:
        async with uow:
            await uow.__dict__[cls.base_repository].delete_data(**kwargs)
