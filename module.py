pfrom typing import Dict, Any

import bs4
import requests
from dbconnect import Database
from settings import get_weather_source

# Модуль содержит методы, которые возвращают данные для бота, после обращения к БД
# Все обращения к БД выполняются в рамках методов этого модуля и не выносятся наружу

# Создаем конекшен к БД, далее в рамках него будем выполнять запросы
db = Database()


# Метод получения прогноза погоды и преобразования его в читаемому формату
def parsing_weather(city_name: str):
    dictionary_of_city = db.get_dict_of_city_db()
    # Словарь и имя переводим в верхний регистр, чтобы он не учитывался
    dictionary_of_city = dict((name.upper(), city_id) for name, city_id in dictionary_of_city.items())
    if city_name.upper() in dictionary_of_city:
        city_link = get_city_link(city_name, dictionary_of_city)
        site = requests.get(city_link)
        parse = bs4.BeautifulSoup(site.text, "html.parser")
        weather = parse.select('.textForecast')
        weather_list = weather[-1].getText()
        result = '\n'.join(weather_list.split('. '))
    else:
        result = 'Ошибка! введите город из списка: '
        result = result + str(list(dictionary_of_city.keys()))
    return result


# Метод получения справочника городов, справочник содержи записи ‘ключ’: ’значение’ вида:
# ‘Имя города’: ‘ИД города на сайте погоды’
def get_dictionary_of_city():
    result = db.get_dict_of_city_db()
    return result


# Метод получения ссылки на прогноз погоды города city_name из справочника городов dictionary_of_city
# Поиск осуществляется без учета регистра
def get_city_link(city_name: str, dictionary_of_city: dict):
    dictionary_of_city = dict((name.lower(), city_id) for name, city_id in dictionary_of_city.items())
    result = get_weather_source() + str(dictionary_of_city.get(city_name.lower()))
    return result
