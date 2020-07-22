import sys
import os
import time
from config import getConfig

def initLogging():
	global mmLogFileObject
	mmLogFileObject = open(os.getcwd() + "/calculateRecipeOrder.log", "w+")

initLogging()

def log(level, process, subProcess, activity, entry):
	if(int(getConfig("logLevel")) >= level):
		if(activity != ""):
			formattedEntry = "[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + "][" + process + "][" + subProcess + "][" + activity + "] " + entry + "\n"
		elif(subProcess != ""):
			formattedEntry = "[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + "][" + process + "][" + subProcess + "] " + entry + "\n"
		else:
		   formattedEntry = "[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + "][" + process + "] " + entry + "\n"
		mmLogFileObject.write(formattedEntry)
		mmLogFileObject.flush()
		print(formattedEntry, end="")
		sys.stdout.flush()
