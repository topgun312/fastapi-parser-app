from typing import Sequence

import pytest

from src.filters.src_filter import STRFilter
from src.models import SpimexTradingResultsModel
from tests.fakes import (
    TEST_BASE_SERVICE_GET_DYNAMICS,
    TEST_BASE_SERVICE_GET_LAST_TRADING_DATES_BY_QUERY_PARAMS,
)
from utils.service import BaseService
from utils.unit_of_work import UnitOfWork

str_filter = STRFilter()


class TestBaseService:
    class _BaseService(BaseService):
        base_repository: str = "spimex_trading_result"

    async def test_get_last_trading_dates_by_query(
        self, clean_data, results, add_results
    ):
        await clean_data()
        for res_schema in results:
            res_in_db: Sequence[SpimexTradingResultsModel] = (
                await self._BaseService.get_last_trading_dates_by_query(
                    uow=UnitOfWork(), **res_schema.model_dump()
                )
            )
            assert (
                set(res_in_db).issubset(
                    TEST_BASE_SERVICE_GET_LAST_TRADING_DATES_BY_QUERY_PARAMS
                )
                == True
            )

    @pytest.mark.parametrize(
        "start_date, end_date, expected_result, expectation",
        TEST_BASE_SERVICE_GET_DYNAMICS,
    )
    async def test_get_dynamics_by_query(
        self,
        start_date,
        end_date,
        expected_result,
        expectation,
        clean_data,
        add_results,
    ):
        await clean_data()
        await add_results()

        with expectation:
            res_in_db: Sequence[SpimexTradingResultsModel] = (
                await self._BaseService.get_dynamics_by_query(
                    start_date, end_date, str_filter=str_filter, uow=UnitOfWork()
                )
            )
            result = (
                None
                if not res_in_db
                else [res.to_pydantic_schema() for res in res_in_db]
            )
            assert result == expected_result

    async def test_get_trading_results_by_query(self, clean_data, results, add_results):
        await clean_data()
        await add_results()

        res_in_db: Sequence[SpimexTradingResultsModel] = (
            await self._BaseService.get_trading_results_by_query(
                str_filter=str_filter, uow=UnitOfWork()
            )
        )
        result = (
            None if not res_in_db else [res.to_pydantic_schema() for res in res_in_db]
        )
        assert len(result) == 4

    async def test_delete_data(self, clean_data, results, add_results, get_results):
        await clean_data()
        await add_results()
        await self._BaseService.delete_data(uow=UnitOfWork())
        results: Sequence[SpimexTradingResultsModel] = await get_results()
        assert len(results) == 0
