import asyncpg
from loguru import logger

from services.str_service import SpimexTradingResultsService
from src.config import settings
from src.parse_data.data_processing import ProcessingData
from src.utils.unit_of_work import UnitOfWork


class AddDataToDataBase:

    async def clear_database(self):
        uow = UnitOfWork()
        await SpimexTradingResultsService.delete_data(uow=uow)

    async def add_processing_data_to_db(self) -> None:
        """
        Метод класса для загрузки обработанных данных в таблицу "spimex_trading" базы данных
        """
        dataframe_list = ProcessingData().create_dataframe_list()
        await self.clear_database()
        conn = await asyncpg.connect(database=f"{settings.DB_NAME}")

        try:
            for df_item in dataframe_list:
                tuples = [tuple(x) for x in df_item.values]
                await conn.copy_records_to_table(
                    "spimex_trading_results",
                    records=tuples,
                    columns=list(df_item.columns),
                    timeout=10,
                )
            logger.info("Данные в таблицу spimex_trading_results загружены успешно!")
        except Exception as ex:
            logger.error("Ошибка добавления данных БД: " + str(ex))
