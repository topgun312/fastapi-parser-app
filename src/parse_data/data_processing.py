import pathlib
import re
from datetime import datetime

import pandas as pd
from loguru import logger
from pandas import DataFrame


class ProcessingData:
    dir = pathlib.Path.cwd() / "excel_files"
    # path = r"/excel_files/"

    def create_dataframe_list(self) -> list[DataFrame]:
        """
        Метод для создания списка датафреймов
        """

        dataframe_list = []
        try:
            for file in self.dir.iterdir():
                if file.is_file():
                    correct_date = re.search(
                        "([0-9]{4}\-[0-9]{2}\-[0-9]{2})", file.name
                    ).group(1)
                    correct_date = datetime.strptime(correct_date, "%Y-%m-%d").date()
                    df_1 = self.data_and_dates_extraction_from_file(file)
                    df_2 = self.column_renaming_and_filtering_df(df_1)
                    df_3 = self.adding_new_columns(df_2, correct_date)
                    df_finish = self.replacing_nan_values_and_removing_unnecessary_rows(
                        df_3
                    )
                    dataframe_list.append(df_finish)
            logger.info("Данные в список датафреймов добавлены успешно!")
            return dataframe_list
        except Exception as ex:
            logger.error("Ошибка создания списка датафреймов: " + str(ex))

    def data_and_dates_extraction_from_file(self, file: pathlib.Path) -> DataFrame:
        """
        Метод для получения данных и даты из файла и создания датафрейма
        """

        df = pd.read_excel(io=file, engine="xlrd", index_col=None)
        index = (
            df[df["Форма СЭТ-БТ"] == "Единица измерения: Метрическая тонна"].index[0]
            + 1
        )
        df = df.iloc[index:, [1, 2, 3, 4, 5, 14]]
        return df

    def column_renaming_and_filtering_df(self, df: DataFrame) -> DataFrame:
        """
        Метод для переименования столбцов датафрейма и его фильтрации
        """

        df.rename(
            columns={
                "Форма СЭТ-БТ": "exchange_product_id",
                "Unnamed: 2": "exchange_product_name",
                "Unnamed: 3": "delivery_basis_name",
                "Unnamed: 4": "volume",
                "Unnamed: 5": "total",
                "Unnamed: 14": "count",
            },
            inplace=True,
        )
        df = df[df["count"] != "-"]
        return df

    def adding_new_columns(
        self, df: DataFrame, correct_date: datetime.date
    ) -> DataFrame:
        """
        Метод для добавления новых столбцов
        """

        df.insert(loc=2, column="oil_id", value=df["exchange_product_id"].str[:4])
        df.insert(
            loc=3,
            column="delivery_basis_id",
            value=df["exchange_product_id"].str[4:7],
        )
        df.insert(
            loc=5,
            column="delivery_type_id",
            value=df["exchange_product_id"].str[-1],
        )
        df.insert(loc=9, column="date", value=correct_date)
        return df

    def replacing_nan_values_and_removing_unnecessary_rows(
        self, df: DataFrame
    ) -> DataFrame:
        """
        Метод для замены Nan значений датафрейма и удаления не нужных столбцов
        """
        df = df.fillna("-")
        df = df.iloc[2:]
        df = df.iloc[:-2]
        return df
