import bs4
import requests
from dbconnect import Database

# Модуль содержит методы, которые возвращают данные для бота, после обращения к БД
# Все обращения к БД выполняются в рамках методов этого модуля и не выносятся наружу

# Создаем конекшен к БД, далее в рамках него будем выполнять запросы
db = Database()


# Метод получения прогноза погоды и преобразования его в читаемому формату
def parsing_weather(city_name: str):
    city_link = db.get_city_link_db(city_name)
    if city_link:
        site = requests.get(city_link)
        parse = bs4.BeautifulSoup(site.text, "html.parser")
        weather = parse.select('.textForecast')
        weather_list = weather[-1].getText()
        result = '\n'.join(weather_list.split('. '))
    else:
        # result = 'Ошибка! введите город из списка: '
        # result = result + str(list(dictionary_of_city.keys()))
        result = 'Ошибка! Указанного города нет в справочнике.'
    return result


# Метод получения справочника городов, справочник содержи записи ‘ключ’: ’значение’ вида:
# ‘Имя города’: ‘ИД города на сайте погоды’
def get_dictionary_of_city():
    result = db.get_dict_of_city_db()
    return result


def get_favourite_list(chat_id: int):
    if db.check_chat_id_db(chat_id):
        result = db.get_favourite_list_db(chat_id)
    else:
        db.set_default_favourite_list_db(chat_id)
        result = db.get_favourite_list_db(chat_id)
    return result
