import re
import sys
from ftplib import FTP
from logger import log
from config import getConfig

ftp = FTP("ftp.byethost7.com")
ftp.login("b7_26300774", "Wxu8dLdV2/")
ftp.cwd("htdocs/roadmap")

def getFastestRecordOnFTP():
    ftp = FTP("ftp.byethost7.com")
    ftp.login("b7_26300774", "Wxu8dLdV2/")
    ftp.cwd("htdocs/roadmap/results")
    files = []
    try:
        files = ftp.nlst()
        files.pop(0)
        files.pop(0)
        temp = files[0]
    except:
        log(0, "FTP", "List", "Read", "CRITICAL: No files found. Creating empty [9999].txt")
        file = open("results/[9999].txt", "w")
        file.write("temp file\n")
        file.close()
        with open("results/[9999].txt", "rb") as localFile:
            ftp.storlines("STOR %s" % "[9999].txt", localFile)
        localFile.close()
        files = ftp.nlst()
        files.pop(0)
        files.pop(0)
        temp = files[0]
    records = []
    for file in files:
        record = int(re.findall("\[([^\s\]]*)\]", file)[0])
        records.append(record)
    records.sort()
    ftp.quit()
    return records[0]

def testRecord(value):
    remoteRecord = getFastestRecordOnFTP()
    localRecord = value
    ftp = FTP("ftp.byethost7.com")
    ftp.login("b7_26300774", "Wxu8dLdV2/")
    ftp.cwd("htdocs/roadmap/results")
    if(localRecord <= remoteRecord):
        with open("results/[" + str(localRecord) + "].txt", "rb") as localFile:
            ftp.storlines("STOR %s" % "[" + str(localRecord) + "]_" + getConfig("Username") + ".txt", localFile)
        localFile.close()
        log(1, "FTP", "File", "Upload", "File [" + str(localRecord) + "].txt has been uploaded.")
    ftp.quit()

def checkForUpdates()
    log(0, "Update", "Check", "", "Checking for updates...")
    ftp = FTP("ftp.byethost7.com")
    ftp.login("b7_26300774", "Wxu8dLdV2/")
    ftp.cwd("htdocs/roadmap")
    try:
        files = ftp.nlst()
        if("[update].txt" in files):
            log(0, "Update", "Check", "", "Newer version found, please download the newest release from github.")
            input()
            raise
    except:
        sys.exit()
    log(0, "Update", "Check", "", "You are running the newest release of this script.\nHappy calculation time!")