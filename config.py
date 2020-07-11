import re

def getConfig(value):
	file = open("config.txt","r")
	rawData = ""
	for line in file:
		rawData = rawData + line
	file.close
	capture = re.findall("\[" + value + "\s*=\s*([^\s\]]*)\s*\]", rawData)[0]
	return capture