import backup
import os

RUNNER_PATH = "/usr/local/bin/backup.py.run.sh"
BACKUP_PY_PATH = "/usr/local/bin/backup.py"

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


def setupProgram():
    os.system("cp backup.py {}".format(BACKUP_PY_PATH))
    

def writeSetInterval():
    py_command = backup.readTagFromConf("PY^3_COMMAND")
    with open(RUNNER_PATH , "w") as file:
        file.write("sudo {} {}".format(py_command , BACKUP_PY_PATH))
    os.system("chmod +x {}".format(RUNNER_PATH))
    line = "@reboot {}".format(RUNNER_PATH)
    os.system("(crontab -l; echo {}) | crontab -".format(line))

def installTkinter():
    os.system("sudo apt-get install python3-tk")

if __name__ == "__main__":
    backup.sudoOnly()
    installTkinter()
    createConfFile()
    createLogFile()
    createDbFile()
    setupProgram()
    writeSetInterval()