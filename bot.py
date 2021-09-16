import module
import os
import telebot

token = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(token)

keyboard1 = telebot.types.ReplyKeyboardMarkup()
for item in dict.keys(module.get_dictionary_of_city()):
    keyboard1.row(item)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'В каком городе сообщить погоду?:', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    bot.send_message(message.chat.id, module.parsing_weather(message.text.upper()), reply_markup=keyboard1)


bot.polling()
