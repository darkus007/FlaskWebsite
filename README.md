# FlaskWebsite v.1.0
Сайт по подбору квартир. Часть проекта Flats, в который также входит [FlatsScrapper](https://github.com/darkus007/FlatsScrapper) - сервис по сбору информации с сайтов застройщиков и наполнению базы данных.

Данный проект написан на Flask с применением SQLAlchemy и Alembic. Реализован просмотр квартир в виде таблиц, с сортировкой по жилым комплексам.

Написан `docker-compose.yml` который упаковывает и запускает приложение в контейнере используя [Nginx](https://nginx.org/ru/) + [Gunicorn](https://gunicorn.org/).

При разработке приложения использованы следующие основные пакеты, фреймворки и технологии: \
[Flask](https://flask.palletsprojects.com/); \
[SQLAlchemy](https://www.sqlalchemy.org); \
[Alembic](https://alembic.sqlalchemy.org/); \
[Bootstrap](https://bootstrap-4.ru/); \
[Docker](https://www.docker.com/).

Полный список в фале `requirements.txt`.

База данных [PostgreSQL](https://www.postgresql.org/).

### Описание Models
> Project - таблица с информацией о жилых комплексах.
>> project_id - уникальный идентификатор, совпадает с id застройщика.\
>> city - город.\
>> name - название ЖК.\
>> url - URL адрес ЖК на сайте застройщика.\
>> metro - ближайшее метро.\
>> time_to_metro - расстояние пешком до метро.\
>> latitude - координаты ЖК, широта.\
>> longitude - координаты ЖК, долгота.\
>> address - адрес ЖК.\
>> data_created - дата добавления ЖК в базу данных.\
>> data_closed - дата снятия ЖК с продажи.

> Flat - таблица с информацией о Квартирах.
>> flat_id - уникальный идентификатор, совпадает с id застройщика.\
>> address - адрес квартиры.\
>> floor - этаж.\
>> rooms - количество комнат.\
>> area - площадь.\
>> finishing - с отделкой?.\
>> settlement_date - дата заселения.\
>> url_suffix - продолжение URL к адресу ЖК.\
>> data_created - дата добавления квартиры в базу данных.\
>> data_closed - дата снятия квартиры с продажи.
>> project - проект к которому принадлежит квартира, связь один со многими.

> Price - таблица с информацией о ценах на Квартиру.
>> price_id - уникальный идентификатор, \
>> flat_id - проект к которому принадлежит квартира, связь один со многими,
>> benefit_name - ценовое предложение.\
>> benefit_description - описание ценового предложения.\
>> price - цена.\
>> meter_price - цена за метр.\
>> booking_status - статус бронирования.\
>> data_created - дата добавления записи в базу данных.


## Установка и запуск
Приложение написано на [Python v.3.11](https://www.python.org). \
Скачайте FlaskWebsite на Ваше устройство любым удобным способом (например Code -> Download ZIP, распакуйте архив 
или выполните `git clone https://github.com/darkus007/FlaskWebsite.git`). \
Установите [Docker](https://www.docker.com/), если он у Вас еще не установлен.

### Настройка приложения

Откройте файл `.env` и измените значения переменных окружения на свои: \
`DB_HOST` - адрес базы данных; \
`DB_PORT` - порт; \
`DB_NAME` - имя базы данных; \
`DB_USER` - пользователь базы данных; \
`DB_PASS` - пароль пользователя базы данных.

!!! Приложение запустится без корректировки и изменения указанных в данном разделе настроек, для теста можно их оставить без изменений !!!

#### Запуск в контейнере Docker
Откройте терминал, перейдите в каталог с приложением (`cd <путь к приложению>/FlaskWebsite`). \
Выполните команду `docker-compose up -d --build`. Дождитесь сборки и запуска контейнеров. \
Откройте любимый Веб-браузер и перейдите по адресу http://127.0.0.1/