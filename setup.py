import backup
import os

def fileExists(path):
    if os.path.isfile(path) and os.access(path , os.R_OK):
        return True
    return False    

def createLogFile():
    if (fileExists(backup.LOG_DIR_PATH) is False):
        open(backup.LOG_DIR_PATH ,"w")

def createConfFile():
    if(fileExists(backup.CONF_DIR_PATH) is False):
        open(backup.CONF_DIR_PATH ,"w")

def createDbFile():
    if(fileExists(backup.DB_DIR_PATH) is False):
        with open(backup.DB_DIR_PATH ,"w") as db:
            db.write("COMMAND=\"\"")

if __name__ == "__main__":
    backup.checkSudo()
    createConfFile()
    createLogFile()
    createLogFile()
    # install tk 
    # dont use backup when you does not have tkinter