import sys
import tkinter as tk
from tkinter import messagebox as tkMessageBox
import re
import subprocess
import datetime

# location of configuration file
# this file in this version nees to command
# 1- COMMAND -> command that run for make backup -> use rsync recommended
# 2- PY3_COMMADN -> command that program can run python code in your pc
CONF_DIR_PATH = "/etc/backup.py.conf"
# location of log files for better debuging and performance
LOG_DIR_PATH  = "/var/log/backup.py.log"
# backup.py.db is file for check today we have backup or not
# this file contain to type lines
# 1- Started DATE
# 2- Completed DATE
DB_DIR_PATH = "/var/log/backup.py.db"
# our code date format standard
DATE_FORMAT = "%Y-%m-%d"

# check user run command using sudo or not
def sudoOnly():
    try:
        open("/etc/foo" , 'a')
    except IOError as _:
        pushLogs("NOTE: delete all your {} file content".format(DB_DIR_PATH))
# send gui alert to user
def alert(title,message):
    root = tk.Tk()
    root.withdraw()
    tkMessageBox.showinfo(title , message)
# ask question from user using gui 
def askQuestion(title , message):
    answer = tkMessageBox.askyesno(title , message)
    return answer
# read tags (commands) from configuration file using regex
# ex : COMMAND="rsync -axv SOURCE DEST"
# in above example tag is COMMAND
def readTagFromConf(tag):
    regex = re.compile(r'^{}=\"(.*)\"'.format(tag))
    cmd = ""
    with open(CONF_DIR_PATH , 'r') as content:
        for c in content:
            checkCmd = re.match(regex , c)
            if checkCmd != None:
                cmd = checkCmd.group(1)
                break
    if cmd == "":
        pushLogs("tag {} not found in {}" .format(tag,CONF_DIR_PATH))
    return cmd           

# write logs in log file that located in LOG_DIR_PATH const
def pushLogs(log):
    with open(LOG_DIR_PATH,"a") as logFile:
        logFile.write(log)

# write data in database file that located in DB_DIR_PATH const
def pushToDB(message):
    with open(DB_DIR_PATH , "a") as db:
        db.write(message)

# checkTodayHaveBackup function check DB_DIR_PATH file and Completed type date for checking
def checkTodayHaveBackup():
    have = False
    with open(DB_DIR_PATH , "r") as db:
        for d in db:
            try:
                if d.split(": ")[0] == "Completed":
                    date = d.split(": ")[1]
                    y,m,d = date.split('-')
                    date = datetime.datetime(int(y),int(m),int(d)).strftime(DATE_FORMAT)
                    if date == datetime.datetime.today().strftime(DATE_FORMAT):
                        have = True
                        break
            except EOFError as _:  
                pushLogs("NOTE: delete all your {} file content".format(DB_DIR_PATH))
                
    return have

# optimaze logs
def createLog(log):
    return '\n'+"-"*20+"\nDate Time: " + str(datetime.datetime.now()) + "\n" + log
  

if __name__ == "__main__":
    sudoOnly()
    if checkTodayHaveBackup() is False:
        if askQuestion("Backup" , "Do you want to get backup now?"):
            pushToDB("Started: {}\n".format(datetime.datetime.today().strftime(DATE_FORMAT)))
            log = subprocess.getoutput(readTagFromConf("COMMAND"))
            log = createLog(log)
            pushLogs(log)
            pushToDB("Completed: {}\n".format(datetime.datetime.today().strftime(DATE_FORMAT)))
            print("Backup Completed!")