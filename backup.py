import sys
import tkinter as tk
from tkinter import messagebox as tkMessageBox
import re
import subprocess
import datetime


CONF_DIR_PATH = "/etc/backup.py.conf"
LOG_DIR_PATH  = "/var/log/backup.py.log"
DB_DIR_PATH = "/var/log/backup.py.db"
DATE_FORMAT = "%Y-%m-%d"

# check user run command using sudo
def sudoOnly():
    try:
        open("/etc/foo" , 'a')
    except IOError as _:
        pushLogs("NOTE: delete all your {} file content".format(DB_DIR_PATH))

def alert(title,message):
    root = tk.Tk()
    root.withdraw()
    tkMessageBox.showinfo(title , message)

def askQuestion(title , message):
    answer = tkMessageBox.askyesno(title , message)
    return answer


def readTagFromConf(tag):
    regex = re.compile(r'^{}=\"(.*)\"'.format(tag))
    cmd = ""
    with open(CONF_DIR_PATH , 'r') as content:
        for c in content:
            checkCmd = re.match(regex , c)
            if checkCmd != None:
                cmd = checkCmd.group(1)
                break
    if len(cmd) == 0:
        pushLogs("NOTE: delete all your {} file content".format(DB_DIR_PATH))
    return cmd           

def pushLogs(log):
    with open(LOG_DIR_PATH,"a") as logFile:
        logFile.write(log)

def pushToDB(message):
    with open(DB_DIR_PATH , "a") as db:
        db.write(message)

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