import bs4
import requests


def parsing_weather(city):
    city_link = get_city_link(city)
    city_id = []
    for item in dict.keys(get_dictionary_of_city()):
        city_id.append(item)

    if city_link:
        site = requests.get(city_link)
        parse = bs4.BeautifulSoup(site.text, "html.parser")
        weather = parse.select('.textForecast')
        weather_list = weather[1].getText()
        result = '\n'.join(weather_list.split('. '))
    else:
        result = 'Ошибка! введите город из списка: '
        result = result + str(city_id)
    return result


def get_dictionary_of_city():
    file = open('city.txt', encoding="utf-8")
    file.read(1)
    list_of_city = file.read().split("\n")
    list_of_city = list_of_city[:-1]
    # print(list_of_city)
    file.close()
    result = dict()

    for item in list_of_city:
        key = item.split(" ")[0]
        value = item.split(" ")[1]
        result[key] = value
    # print(result)
    return result


def get_city_link(city):
    dictionary_of_city = get_dictionary_of_city()
    if city in dictionary_of_city:
        result = dictionary_of_city[city]
    else:
        result = None
    return result

# if __name__ == "__main__":
#	print(getdict())
#    dict = get_dict()
#	city = 'приморск'
#	print(getlink(city))
#	keycity = []
#	for item in dict.keys(getdict()):
#		keycity.append(item)
#	print(keycity)
#    print(dict)
#	#list = []
#	#print(len(dict.items()))
#	#list.append(dict.items())
#	#print(list)
