import asyncio
import pathlib
from datetime import datetime

import aiofiles
from aiohttp import ClientSession
from bs4 import BeautifulSoup as bs
from loguru import logger

from src.config import SITE_DOMAIN, SITE_URL


class ParseDataFromSite:

    def __init__(self):
        self.create_dir = self.create_files_dir()

    def create_files_dir(self) -> None:
        """
        Метод класса для создания директории excel_files
        """

        dir = pathlib.Path.cwd() / "excel_files"
        if not dir.exists() and not dir.is_dir():
            dir.mkdir(exist_ok=True)
            logger.info("Директория excel_files создана!")
        else:
            logger.info("Директория excel_files инициализирована!")

    async def get_page_count(self) -> None:
        """
        Метод для получения количества страниц в пагинаторе
        """

        tasks = []
        async with ClientSession() as session:
            response = await session.get(url=SITE_URL)
            soup = bs(await response.text(), "lxml")
            page_count = int(
                soup.find("div", class_="bx-pagination-container")
                .find_all("span")[5]
                .get_text()
            )
            for page in range(1, page_count):
                task = await self.get_links_and_date_files(session, page)
                if not task:
                    break
                tasks.append(task)
                await asyncio.gather(*tasks)

    async def get_links_and_date_files(self, session: ClientSession, page: int) -> None:
        """
        Метод для получения сслылок и дат загрузки файлов
        """

        dates = []
        links = []
        page_url = SITE_URL + f"?page=page-{page}"
        async with session.get(url=page_url) as response:
            soup = bs(await response.text(), "lxml")
            docs_on_page = soup.find_all("div", class_="accordeon-inner__wrap-item")
            for item in docs_on_page[:10]:
                doc_date = (
                    item.find("div", class_="accordeon-inner__item-inner__title")
                    .find("span")
                    .get_text()
                )
                doc_date = (
                    datetime.strptime(doc_date, "%d.%m.%Y").date().strftime("%Y-%m-%d")
                )
                current_date = datetime.strptime(doc_date, "%Y-%m-%d").date()
                end_date = datetime.strptime("2024-07-17", "%Y-%m-%d").date()
                if current_date < end_date:
                    break
                else:
                    dates.append(doc_date)
                    link = item.find(
                        "a", class_="accordeon-inner__item-title link xls"
                    ).get("href")
                    file_link = SITE_DOMAIN + link
                    links.append(file_link)
        dict_result = dict(zip(dates, links))
        if len(dict_result) > 0:
            await self.download_files_on_repository(dict_result, session)

    async def download_files_on_repository(
        self, dict_result: dict, session: ClientSession
    ) -> None:
        """
        Метод для создания файлов
        """

        for date, link in dict_result.items():
            filename = f"excel_files/{date}.xls"
            async with session.get(url=link) as response:
                data = await response.read()
                async with aiofiles.open(filename, "wb") as file:
                    await file.write(data)
