import re
import sys
import requests
import json
from logger import log
from config import getConfig

def getFastestRecordOnFTP():
	url_with_fastest = "https://hundorecipes.blob.core.windows.net/foundpaths/fastestFrames.txt"
	req = requests.get(url_with_fastest)
	if(req.ok):
		return int(req.text)
	else:
		log(0, "Network", "Check", "", "There was an error getting the fastest record. Proceeding with a fastest record of 9999.")
		return 9999

def testRecord(value):
	remoteRecord = getFastestRecordOnFTP()
	localRecord = value
	if(localRecord <= remoteRecord):
		url_to_submit = "https://hundorecipes.azurewebsites.net/api/uploadAndVerify"
		with open("results/[" + str(localRecord) + "].txt", "rb") as localFile:
			dataToSend = {
				'frames': localRecord,
				'userName': getConfig("Username"),
				'routeContent': localFile.read().decode("utf-8")
			}
			r = requests.post(url_to_submit, data = json.dumps(dataToSend))
			if (r.ok):
				log(1, "Submit", "File", "Upload", "File [" + str(localRecord) + "].txt has been uploaded.")
			else:
				log(1, "Submit", "File", "Upload", "There was a problem uploading file [" + str(localRecord) + "].txt. Message returned by the server was: " + r.text)
		localFile.close()

def checkForUpdates():
	url_for_update_check = "https://api.github.com/repos/SevenChords/RecipesAtHome/releases/latest"
	req = requests.get(url_for_update_check)
	jsonBlob = req.json()
	remoteVersion = jsonBlob.get('tag_name')
	if(remoteVersion):
		localVersion = getConfig("Version")
		if(localVersion[0] != 'v'):
			localVersion = 'v' + localVersion
		if(remoteVersion == localVersion):
			log(0, "Update", "Check", "", "You are running the newest release of this script.\nHappy calculation time!")
			return True
		else:
			log(0, "Update", "Check", "", "You are running the wrong version of this script, please get the newest release from github.")
			input()
			sys.exit()
	else:
		log(0, "Update", "Check", "", "There was an error checking for updates. Please ensure you're running the latest release.")