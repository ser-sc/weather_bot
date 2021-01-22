import requests, bs4, telebot
import module

def parce_weather(city):
	city = 'приморск'
	link = module.getlink(city)
	print(link)
	site = requests.get(link)
	print(site)
	parse = bs4.BeautifulSoup(site.text, "html.parser")
	weather = parse.select('.textForecast')
	pogoda = weather[1].getText()
	pogodalist = pogoda.split('. ')
	result = '\n'.join(pogodalist)
	print(result)
	return result

#f = open('bot.token')
#token = f.read()
#f.close()
#token = token[:-1]
#print(token)


#print(parce_weather('приморск'))
print(module.getlink('приморск'))
