## Задание 
В продолжение прошлой темы необходимо реализовать микросервисное приложение, которые будет использовать данные из таблицы «spimex_trading_results» и отдавать их в формате JSON.

#### Функции для реализации: 
1. get_last_trading_dates – список дат последних торговых дней (фильтрация по кол-ву последних торговых дней).
2. get_dynamics – список торгов за заданный период (фильтрация по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date).
3. get_trading_results – список последних торгов (фильтрация по oil_id, delivery_type_id, delivery_basis_id)
#### Дополнительные параметры:
* Какие параметры должны быть обязательные, а какие нет, необходимо определить самостоятельно и обосновать.
* Необходимо организовать кэширование запросов (Redis) таким образом, чтобы они хранились до 14:11, а после происходил сброс всего кэша.

#### Основные используемые библиотеки:
- fastapi==0.111.1
- fastapi-cache2==0.2.1
- fastapi-filter==2.0.0
- fastapi_scheduler==0.0.15
- pydantic==2.8.2
- pydantic-settings==2.3.4
- aiofiles==24.1.0
- aiohttp==3.9.5
- asyncpg==0.29.0
- beautifulsoup4==4.12.3
- lxml==5.2.2
- pandas==2.2.2
- python-dotenv==1.0.1
- SQLAlchemy==2.0.31
- xlrd==2.0.1
- loguru==0.7.2
- alembic==1.13.2

#### Для создания базы данных:
1. Создаем таблицы с помощью alembic - alembic init migrations
2. Создаем ревизию-миграцию - alembic revision --autogenerate -m "Database create"
3. Применяем миграцию - alembic upgrade head
