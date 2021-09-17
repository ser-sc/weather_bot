import bs4
import requests
from dbconnect import Database

# Модуль содержит методы, которые возвращают данные для бота, после обращения к БД
# Все обращения к БД выполняются в рамках методов этого модуля и не выносятся наружу

# Создаем конекшен к БД, далее в рамках него будем выполнять запросы
db = Database()


# Метод получения прогноза погоды и преобразования его в читаемому формату
def parsing_weather(city_name):
    dictionary_of_city = db.get_dict_of_city_db()
    if city_name in dictionary_of_city:
        city_link = db.get_city_link_db(city_name)
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
