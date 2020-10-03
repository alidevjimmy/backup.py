import sys
import tkinter as tk
from tkinter import messagebox as tkMessageBox
import re
import subprocess


CONF_DIR_PATH = "/etc/backup.py.conf"
LOG_DIR_PATH  = "/var/log/backup.py.log"

def checkSudo():
    try:
        open("/etc/foo" , 'a')
    except IOError as e:
        sys.exit("You should run program as root!")

def alert(title,message):
    root = tk.Tk()
    root.withdraw()
    tkMessageBox.showinfo(title , message)

def askQuestion(title , message):
    answer = tkMessageBox.askyesno(title , message)
    return answer

# makBackup function just run a command which located in /etc/backup.py.conf
def makeBackup(command):
    checkSudo()
    log = subprocess.getoutput(command)
    log = createLog(log)
    pushLogs(log)
    print("Backup Completed!")


def readCommand():
    regex = re.compile(r'^COMMAND=\"(.*)\"')
    cmd = ""
    with open(CONF_DIR_PATH , 'r') as content:
        for c in content:
            checkCmd = re.match(regex , c)
            if checkCmd != None:
                cmd = checkCmd.group(1)
                break
    if len(cmd) == 0:
        sys.exit("COMMAND not found in {}".format(CONF_DIR_PATH)) 

    return cmd           

def pushLogs(log):
    with open(LOG_DIR_PATH,"a") as logFile:
        logFile.write(log)

def checkTodayHaveBackup():
    return True, False

# design logs
def createLogs(log):



makeBackup(readCommand())

