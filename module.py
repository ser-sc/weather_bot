import bs4
import requests
from settings import get_weather_source
from dbconnect import Database

# Модуль содержит методы, которые возвращают данные для бота, после обращения к БД
# Все обращения к БД выполняются в рамках методов этого модуля и не выносятся наружу

# Создаем конекшен к БД, далее в рамках него будем выполнять запросы
db = Database()


# Метод получения прогноза погоды и преобразования его в читаемому формату
def parsing_weather(city_name: str):
    city_link = db.get_city_id_db(city_name)
    if city_link:
        city_link = get_weather_source() + city_link
        site = requests.get(city_link)
        parse = bs4.BeautifulSoup(site.text, "html.parser")
        weather = parse.select('.textForecast')
        weather_list = weather[-1].getText()
        result = '\n'.join(weather_list.split('. '))
    else:
        # result = 'Ошибка! введите город из списка: '
        # result = result + str(list(dictionary_of_city.keys()))
        result = 'Ошибка! Города [' + city_name.upper() + '] НЕТ в справочнике'
    return result


# Метод получения справочника городов, справочник содержи записи ‘ключ’: ’значение’ вида:
# ‘Имя города’: ‘ИД города на сайте погоды’
def get_dictionary_of_city():
    result = db.get_dict_of_city_db()
    return result


# Метод получения справочника избранных городов для чата <chat_id>, справочник содержи записи ‘ключ’: ’значение’ вида:
# ‘Имя города’: ‘ИД города на сайте погоды’
# Если для чата еще нет городов в избранном, то осуществляется первичная инициализация и добавляются города по умолчанию
def get_favourite_list(chat_id: int):
    if db.check_chat_id_db(chat_id):
        result = db.get_favourite_list_db(chat_id)
    else:
        db.set_default_favourite_list_db(chat_id)
        result = db.get_favourite_list_db(chat_id)
    return result


# Метод добавляет город <city_name> в справочник избранных городов для чата <chat_id>
# и возвращает сообщение о результате добавления
def set_city_to_favourite(chat_id: int, city_name: str):
    city_id = db.get_city_id_db(city_name)
    if city_id:
        if db.check_city_in_favourite_db(chat_id, city_id):
            result = 'Предупреждение! Город [' + city_name.upper() + '] УЖЕ добавлен в избранное'
        else:
            db.set_city_to_favourite_db(chat_id, city_id)
            result = 'Город [' + city_name.upper() + '] добавлен в избранное'
    else:
        result = 'Ошибка сохранения! Города [' + city_name.upper() + '] НЕТ в справочнике'
    return result


# Метод удаляет город <city_name> из справочника избранных городов для чата <chat_id>
# и возвращает сообщение о результате удаления
def del_city_from_favourite(chat_id: int, city_name: str):
    city_id = db.get_city_id_db(city_name)
    if city_id:
        if db.check_city_in_favourite_db(chat_id, city_id):
            db.del_city_from_favourite_db(chat_id, city_id)
            result = 'Город [' + city_name.upper() + '] уделен из избранного'
        else:
            result = 'Ошибка удаления! Город [' + city_name.upper() + '] еще НЕ добавлен в избранное'
    else:
        result = 'Ошибка удаления! Города [' + city_name.upper() + '] НЕТ в справочнике'
    return result
