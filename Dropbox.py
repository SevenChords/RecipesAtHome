# Note: You must pip install dropbox for this to work

import sys
import dropbox

from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

# Access token
TOKEN = 'RFWQOkXXGFAAAAAAAAAADnW-qFTyj7DsDYko2FT-vqFkxRRCusFVvVA95PKXOb-C'

# Uploads contents of LOCALFILE to Dropbox
def backup(LOCALFILE, dbx):
	with open(LOCALFILE, 'rb') as f:
		# We use WriteMode=overwrite to make sure that the settings in the file
		# are changed on upload
		BACKUPPATH = '/' + LOCALFILE.strip("results/") + "t"
		print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
		try:
			dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
		except ApiError as err:
			# This checks for the specific error where a user doesn't have enough Dropbox space quota to upload this file
			if (err.error.is_path() and
					err.error.get_path().error.is_insufficient_space()):
				sys.exit("ERROR: Cannot back up; insufficient space.")
			elif err.user_message_text:
				print(err.user_message_text)
				sys.exit()
			else:
				print(err)
				sys.exit()


# Adding few functions to check file details
def getFastestRecordOnDropBox():
	fileTimes = []
	dbx = dropbox.Dropbox(TOKEN)
	for entry in dbx.files_list_folder('').entries:
		fileTimes.append(entry.name[1:-5])
	fileTimes.sort()
	return int(fileTimes[0])


# Run this script independently
def upload_file(LOCALPATH, dbx):
	BACKUPPATH = '/' + LOCALPATH # Keep the forward slash before destination filename
	
	# Check for an access token
	if (len(TOKEN) == 0):
		sys.exit("ERROR: Looks like you didn't add your access token. Open up backup-and-restore-example.py in a text editor and paste in your token in line 14.")

	print("Creating backup...")
	# Create a backup of the current settings file
	backup(LOCALPATH, dbx)

	print("Done!")
	
# See if a passed-in solution  is faster than the record on Dropbox
def test_record(record): # Passed in as framecount integer
	# Create an instance of a Dropbox class, which can make requests to the API.
	dbx = dropbox.Dropbox(TOKEN)

	# Check that the access token is valid
	try:
		dbx.users_get_current_account()
	except AuthError as err:
		sys.exit(
			"ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

	try:
		dropboxRecord = getFastestRecordOnDropBox()
	except Error as err:
		sys.exit("Error while checking file details")
	
	if record < int(dropboxRecord):
		upload_file('results/[' + str(record) + '].txt', dbx)