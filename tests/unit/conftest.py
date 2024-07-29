from copy import deepcopy
from typing import Callable, Sequence

import pytest
from sqlalchemy import Result, delete, insert, select

from src.models import SpimexTradingResultsModel
from src.schemas.str_schema import SpimexTradingResultsSchema
from tests.fakes import FAKE_RESULTS


@pytest.fixture(scope="function")
def results() -> list[SpimexTradingResultsSchema]:
    return deepcopy(FAKE_RESULTS)


@pytest.fixture(scope="session")
def clean_data(async_session_maker) -> Callable:
    async def _clear_data():
        async with async_session_maker() as session:
            query = delete(SpimexTradingResultsModel)
            await session.execute(query)
            await session.commit()

    return _clear_data


@pytest.fixture(scope="function")
def add_results(async_session_maker, results) -> Callable:
    async def _add_results():
        async with async_session_maker() as session:
            for res_schema in results:
                await session.execute(
                    insert(SpimexTradingResultsModel).values(**res_schema.model_dump())
                )
            await session.commit()

    return _add_results


@pytest.fixture(scope="session")
def get_results(async_session_maker) -> Callable:
    async def _get_results() -> Sequence[SpimexTradingResultsModel]:
        async with async_session_maker() as session:
            result: Result = await session.execute(select(SpimexTradingResultsModel))
            return result.scalars().all()

    return _get_results
