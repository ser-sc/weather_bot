# Тестирование бота

## Содержание
1. [Введение](#Introduction)
2. [Создание тестовой БД с Docker-compose](#Docker-compose)
3. [Настройка параметров окружения в IDE](#IDE_environment)

## Введение <a name="Introduction"></a>
Тестирования бота удобно выполнять, запуская бота непосредственно в среде разработки IDE.  При этом необходимо создать тестовую базу данных (см. [Создание тестовой БД] (#Docker-compose)) и настроить параметры окружения (см. [Настройка параметров окружения в IDE](#IDE_environment))

Для того чтобы тестирование бота не мешало работе со стабильной версией необходимо зарегистрировать нового тестового бота и *токен тестового бота*. Инструкция по регистрации бота: https://botcreators.ru/blog/botfather-instrukciya/

## Создание тестовой БД с Docker-compose <a name="Docker-compose"></a>

Для запуска docker container с тестовой БД необходимо в терминале в папке *./Test* выполнить команду:

`docker-compose up --build -d`

Инициализация тестовой БД произойдет автоматически. К тестовой БД можно подключится с помощью pgAdmin с параметрами:
  * Host name/address: localhost
  * Port: 5435
  * Maintenance database: test_weather_bot
  * Username: test_weather_bot
  * Password: <the same like username>

## Настройка параметров окружения в IDE <a name=" IDE_environment "></a>
Настройка будет описана на примере IDE Intellij Idea Community Edition 2021.1.2
1. Необходимо открыть проект в IDE. Idea сама предложить скачать все необходимые зависимости. Необходимо скачать их и не забыть добавить в свой *.gitignore*
2. Необходимо настроить Run/Debug Configuration:
	* Выбрать Python
* Script pasth: <путь к папке проекта>\bot.py
	* Python interpreter: Use SDK of module: weather_bot
3. Необходимо в Run/Debug Configuration добавить переменные окружения Environment variables:
    * BOT_TOKEN : <токен тестового бота>
    * DB_NAME : test_weather_bot
    * DB_USER : test_weather_bot
    * DB_PASS : test_weather_bot
    * DB_HOST : localhost
    * DB_PORT : 5435
    * WEATHER_SOURCE : https://meteo7.ru/forecast
4. После этого применить настройки. Бот готов к запуску и отладке из IDE. Взаимодействие при этом осуществляется с тестовым ботом
