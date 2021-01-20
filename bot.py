import requests, bs4, telebot

def parce_weather(city):
        if city == 'мшинская':
                site = requests.get("https://meteo7.ru/forecast/59828")
        elif city == 'приморск':
                site = requests.get("https://meteo7.ru/forecast/76628")
        parse = bs4.BeautifulSoup(site.text, "html.parser")
        weather = parse.select('.textForecast')
        pogoda3 = weather[1].getText()
        return pogoda3

bot = telebot.TeleBot("505752923:AAFkeLE4JlmWTOWDhLaYQY79YqrVoSG-vM0")

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Мшинская', 'Приморск')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
#	bot.reply_to(message, "Howdy, how are you doing?")
	bot.send_message(message.chat.id, 'Привет',reply_markup=keyboard1)

#@bot.message_handler(func=lambda message: True)
#def echo_all(message):
#	bot.reply_to(message, message.text)

@bot.message_handler(content_types=['text'])
def send_text(message):
	if message.text.lower() == 'мшинская':
        	bot.send_message(message.chat.id, parce_weather('мшинская'))
	elif message.text.lower() == 'приморск':
		bot.send_message(message.chat.id, parce_weather('приморск'))



bot.polling()
