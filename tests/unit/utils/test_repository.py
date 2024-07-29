from typing import Sequence

import pytest

from src.filters.src_filter import STRFilter
from src.models import SpimexTradingResultsModel
from src.utils.repository import SqlAlchemyRepository
from tests.fakes import (
    TEST_SQLALCHEMY_REPOSITORY_GET_DYNAMICS,
    TEST_SQLALCHEMY_REPOSITORY_GET_LAST_TRADING_DATES_BY_QUERY_PARAMS,
)

str_filter = STRFilter()


class TestSqlAlchemyRepository:
    class _SqlAlchemyRepository(SqlAlchemyRepository):
        model = SpimexTradingResultsModel

    async def test_get_last_trading_dates_by_query(
        self, clean_data, results, add_results, async_session
    ):
        await clean_data()
        await add_results()
        sql_alchemy_repository = self._SqlAlchemyRepository(session=async_session)
        for res_schema in results:
            res_in_db: Sequence[SpimexTradingResultsModel] = (
                await sql_alchemy_repository.get_last_trading_dates_by_query(
                    **res_schema.model_dump()
                )
            )
            assert (
                set(res_in_db).issubset(
                    TEST_SQLALCHEMY_REPOSITORY_GET_LAST_TRADING_DATES_BY_QUERY_PARAMS
                )
                == True
            )
        await async_session.close()

    @pytest.mark.parametrize(
        "start_date, end_date, expected_result, expectation",
        TEST_SQLALCHEMY_REPOSITORY_GET_DYNAMICS,
    )
    async def test_get_dynamics_by_query(
        self,
        start_date,
        end_date,
        expected_result,
        expectation,
        clean_data,
        add_results,
        async_session,
    ):
        await clean_data()
        await add_results()
        sql_alchemy_repository = self._SqlAlchemyRepository(session=async_session)

        with expectation:
            res_in_db: Sequence[SpimexTradingResultsModel] = (
                await sql_alchemy_repository.get_dynamics_by_query(
                    start_date, end_date, str_filter
                )
            )
            result = (
                None
                if not res_in_db
                else [res.to_pydantic_schema() for res in res_in_db]
            )
            assert result == expected_result

        await async_session.close()

    async def test_get_trading_results_by_query(
        self, clean_data, results, add_results, async_session
    ):
        await clean_data()
        await add_results()
        sql_alchemy_repository = self._SqlAlchemyRepository(session=async_session)

        res_in_db: Sequence[SpimexTradingResultsModel] = (
            await sql_alchemy_repository.get_trading_results_by_query(str_filter)
        )
        result = (
            None if not res_in_db else [res.to_pydantic_schema() for res in res_in_db]
        )
        assert len(result) == 4

        await async_session.close()

    async def test_delete_data(
        self, clean_data, results, add_results, get_results, async_session
    ):

        await clean_data()
        await add_results()
        sql_alchemy_repository = self._SqlAlchemyRepository(session=async_session)
        await sql_alchemy_repository.delete_data()
        await async_session.commit()
        results: Sequence[SpimexTradingResultsModel] = await get_results()
        assert len(results) == 0

        await async_session.close()
