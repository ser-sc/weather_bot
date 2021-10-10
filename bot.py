from telebot import TeleBot
from module import parsing_weather, set_city_to_favourite, del_city_from_favourite, get_favourite_list_keyboard, \
    get_command_list, get_all_cites_list_keyboard, get_city_link, get_action_with_city_keyboard
from settings import get_token

# Основной модуль, инициализирует работу бота прогноза погоды


# Инициализация токена бота
bot = TeleBot(get_token())

# Инициализация списка комманд бота
bot.set_my_commands(get_command_list())


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     'Я умею предсказывать погоду.\n'
                     'Для того чтобы получить предсказание, введите название интересующего города. '
                     'Или выберете город из списка избранных городов ниже.\n'
                     'Доступные команды приведены в меню.\n'
                     'Также города можно добавлять или удалять из списка избранных. '
                     'Для этого необходимо ввести команду /save или /delete и сразу после нее имя города, например: '
                     '/save ШУЯ. '
                     'Или воспользоваться кнопками после получения предсказания.\n\n'
                     'В каком городе сообщить погоду?\nСписок избранных городов:',
                     reply_markup=get_favourite_list_keyboard(message.chat.id)
                     )


@bot.message_handler(commands=['all'])
def send_all_cites(message):
    bot.send_message(message.chat.id,
                     'В каком городе сообщить погоду?\nСписок всех доступных городов:',
                     reply_markup=get_all_cites_list_keyboard()
                     )


@bot.message_handler(commands=['favourite'])
def send_favourite_cites(message):
    bot.send_message(message.chat.id,
                     'В каком городе сообщить погоду?\nСписок избранных городов:',
                     reply_markup=get_favourite_list_keyboard(message.chat.id)
                     )


@bot.message_handler(commands=['save'])
def send_set_to_favourite_text(message):
    bot.send_message(message.chat.id,
                     set_city_to_favourite(message.chat.id, message.text),
                     reply_markup=get_favourite_list_keyboard(message.chat.id)
                     )


@bot.message_handler(commands=['delete'])
def send_del_from_favourite_text(message):
    bot.send_message(message.chat.id,
                     del_city_from_favourite(message.chat.id, message.text),
                     reply_markup=get_favourite_list_keyboard(message.chat.id)
                     )


@bot.message_handler(content_types=['text'])
def send_weather_forecast(message):
    city_link = get_city_link(message.text)
    if city_link:
        bot.send_message(message.chat.id,
                         parsing_weather(city_link),
                         reply_markup=get_action_with_city_keyboard(message.chat.id, city_link, message.text)
                         )
    else:
        bot.send_message(message.chat.id,
                         'Ошибка! Города {city_name} НЕТ в справочнике'.format(city_name=message.text.upper())
                         )
    bot.send_message(message.chat.id,
                     'В каком городе сообщить погоду?\nСписок избранных городов:',
                     reply_markup=get_favourite_list_keyboard(message.chat.id)
                     )


@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    if '/save' in call.data:
        bot.send_message(call.message.chat.id,
                         set_city_to_favourite(call.message.chat.id, call.data),
                         reply_markup=get_favourite_list_keyboard(call.message.chat.id)
                         )
    if '/delete' in call.data:
        bot.send_message(call.message.chat.id,
                         del_city_from_favourite(call.message.chat.id, call.data),
                         reply_markup=get_favourite_list_keyboard(call.message.chat.id)
                         )


bot.polling()
