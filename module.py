import bs4
import requests
from telebot import types
from settings import get_weather_source
from dbconnect import Database

# Модуль содержит методы, которые возвращают данные для бота, после обращения к БД
# Все обращения к БД выполняются в рамках методов этого модуля и не выносятся наружу

# Создаем конекшен к БД, далее в рамках него будем выполнять запросы
db = Database()


# Метод получения прогноза погоды и преобразования его в читаемому формату
def parsing_weather(city_link: str):
    city_link = get_weather_source() + city_link
    site = requests.get(city_link)
    parse = bs4.BeautifulSoup(site.text, "html.parser")
    weather = parse.select('.textForecast')
    weather_list = weather[-1].getText()
    result = '\n'.join(weather_list.split('. '))
    return result


# Метод получения справочника городов, справочник содержи записи ‘ключ’: ’значение’ вида:
# ‘Имя города’: ‘ИД города на сайте погоды’
def get_dictionary_of_cites():
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


# Метод возвращает ссылку на город или false
def get_city_link(city_name: str):
    result = db.get_city_id_db(city_name)
    return result


# Метод добавляет город <city_name> в справочник избранных городов для чата <chat_id>
# и возвращает сообщение о результате добавления
def set_city_to_favourite(chat_id: int, message: str):
    city_name = message.split(maxsplit=1)
    if len(city_name) == 2:
        city_id = db.get_city_id_db(city_name[1])
        if city_id:
            if db.check_city_in_favourite_db(chat_id, city_id):
                result = 'Предупреждение! Город {city_name} УЖЕ добавлен в избранное' \
                    .format(city_name=city_name[1].upper())
            else:
                db.set_city_to_favourite_db(chat_id, city_id)
                result = 'Город {city_name} добавлен в избранное'.format(city_name=city_name[1].upper())
        else:
            result = 'Ошибка добавления в избранное! Города {city_name} НЕТ в справочнике'\
                .format(city_name=city_name[1].upper())
    else:
        result = 'Ошибка добавления в избранное! Не указан город'
    return result


# Метод удаляет город <city_name> из справочника избранных городов для чата <chat_id>
# и возвращает сообщение о результате удаления
def del_city_from_favourite(chat_id: int, message: str):
    city_name = message.split(maxsplit=1)
    if len(city_name) == 2:
        city_id = db.get_city_id_db(city_name[1])
        if city_id:
            if db.check_city_in_favourite_db(chat_id, city_id):
                db.del_city_from_favourite_db(chat_id, city_id)
                result = 'Город {city_name} уделен из избранного'.format(city_name=city_name[1].upper())
            else:
                result = 'Ошибка удаления из избранного! Город {city_name} еще НЕ добавлен в избранное' \
                    .format(city_name=city_name[1].upper())
        else:
            result = 'Ошибка удаления из избранного! Города {city_name} НЕТ в справочнике'\
                .format(city_name=city_name[1].upper())
    else:
        result = 'Ошибка удаления из избранного! Не указан город'
    return result


# Метод возвращает клавиатуру со списком избранных городов
def get_favourite_list_keyboard(chat_id: int):
    result = types.ReplyKeyboardMarkup()
    for item in dict.keys(get_favourite_list(chat_id)):
        # Названия городов в клавиатуре всегда в верхнем регистре
        result.row(item.upper())
    return result


# Метод возвращает клавиатуру со списком всех городов
def get_all_cites_list_keyboard():
    result = types.ReplyKeyboardMarkup()
    for item in dict.keys(get_dictionary_of_cites()):
        # Названия городов в клавиатуре всегда в верхнем регистре
        result.row(item.upper())
    return result


# Метод возвращает клавиатуру добавления/удаления города из избранного
def get_action_with_city_keyboard(chat_id: int, city_id: int, message: str):
    result = types.InlineKeyboardMarkup()
    if db.check_city_in_favourite_db(chat_id, city_id):
        button_text = 'Удалить город {city_name} из избранного'.format(city_name=message.upper())
        callback_data = '/delete {city_name}'.format(city_name=message.upper())
    else:
        button_text = 'Сохранить город {city_name} в избранное'.format(city_name=message.upper())
        callback_data = '/save {city_name}'.format(city_name=message.upper())
    callback_button = types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
    result.add(callback_button)
    return result


# Метод возвращает список доступных комманд
def get_command_list():
    result = list()
    result.append(types.BotCommand('/help', 'Возможности бота'))
    result.append(types.BotCommand('/favourite', 'Список избранных городов'))
    result.append(types.BotCommand('/all', 'Список всех доступных городов'))
    result.append(types.BotCommand('/save', 'Сохранить город в избранное'))
    result.append(types.BotCommand('/delete', 'Удалить город из избранного'))
    return result
