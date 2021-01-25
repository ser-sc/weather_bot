def getdict():
	file = open('city.txt', encoding="utf-8")
	file.read(1)
	onstring = file.read().split("\n")
	onstring = onstring[:-1]
#	print(onstring)
	file.close()
	dictcity = dict()

	for item in onstring:
		key = item.split(" ")[0]
		value = item.split(" ")[1]
		dictcity[key] = value
#		print(dictcity)
	return dictcity

def getlink(city):
	dictcity = getdict()
	if city in dictcity:
		link = dictcity[city]
	else:
		link = None
	return link

if __name__ == "__main__":
#	print(getdict())
	dict = getdict()
#	city = 'приморск'
#	print(getlink(city))
#	keycity = []
#	for item in dict.keys(getdict()):
#		keycity.append(item)
#	print(keycity)
	print(dict)
#	list = []
#	print(len(dict.items()))
#	list.append(dict.items())
#	print(list)
