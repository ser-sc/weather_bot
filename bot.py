import requests, bs4, telebot, module

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
bot = telebot.TeleBot(token)


keyboard1 = telebot.types.ReplyKeyboardMarkup()
for item in dict.keys(module.getdict()):
	keyboard1.row(item)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, 'В каком городе сообщить погоду?:',reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
	bot.send_message(message.chat.id, parce_weather(message.text.upper()), reply_markup=keyboard1)



bot.polling()
