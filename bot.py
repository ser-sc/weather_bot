import requests, bs4, telebot
import module

def parce_weather(city):
	link = module.getlink(city)
	keycity = []
	for item in dict.keys(module.getdict()):
	        keycity.append(item)

	if link:
		site = requests.get(link)
		parse = bs4.BeautifulSoup(site.text, "html.parser")
		weather = parse.select('.textForecast')
		pogoda = weather[1].getText()
		pogodalist = pogoda.split('. ')
		result = '\n'.join(pogodalist)
	else:
		result = 'Ошибка! введите город из списка: '
		result = result + str(keycity)
	return result

f = open('bot.token')
token = f.read()
f.close()
token = token[:-1]
#print(token)
bot = telebot.TeleBot(token)


keyboard1 = telebot.types.ReplyKeyboardMarkup()
#keyboard1.row('Погода')
keyboard1.row('Мшинская', 'Победа', 'Приморск')
#keycity = []
#for item in dict.keys(module.getdict()):
#	
 #       keycity.append(item)
#keyboard1.row(keycity)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, 'Привет',reply_markup=keyboard1)
 #       bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(content_types=['text'])
def send_text(message):
	bot.send_message(message.chat.id, parce_weather(message.text.lower()))



#@bot.message_handler(content_types=['Погода'])
#def send_message(message):
#	markup = telebot.types.InlineKeyboardMarkup()
#	markup.add(telebot.types.InlineKeyboardButton(text='Три', callback_data=3))
#	markup.add(telebot.types.InlineKeyboardButton(text='Четыре', callback_data=4))
#	markup.add(telebot.types.InlineKeyboardButton(text='Пять', callback_data=5))
#	bot.send_message(message.chat.id, text="Какая средняя оценка была у Вас в школе?",reply_markup=markup)


bot.polling()
