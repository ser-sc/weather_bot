from telebot import TeleBot, types
from module import parsing_weather, get_favourite_list
from settings import get_token

# Основной модуль, инициализирует работу бота прогноза погоды


# Инициализация токена бота
bot = TeleBot(get_token())


def get_actual_main_keyboard(chat_id: int):
    keyboard = types.ReplyKeyboardMarkup()
    for item in dict.keys(get_favourite_list(chat_id)):
        # Названия городов в клавиатуре всегда в верхнем регистре
        keyboard.row(item.upper())
    return keyboard


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'В каком городе сообщить погоду?:',
                     reply_markup=get_actual_main_keyboard(message.chat.id))


@bot.message_handler(content_types=['text'])
def send_text(message):
    bot.send_message(message.chat.id, parsing_weather(message.text),
                     reply_markup=get_actual_main_keyboard(message.chat.id))


bot.polling()
