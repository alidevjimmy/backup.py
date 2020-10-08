import backup
import os

RUNNER_PATH = "/usr/local/bin/backup.py.run.sh"
BACKUP_PY_PATH = "/usr/local/bin/backup.py"


def fileExists(path):
    if os.path.isfile(path) and os.access(path, os.R_OK):
        return True
    return False


def createLogFile():
    if (fileExists(backup.LOG_DIR_PATH) is False):
        open(backup.LOG_DIR_PATH, "w")


def createConfFile():
    if(fileExists(backup.CONF_DIR_PATH) is False):
        with open(backup.CONF_DIR_PATH, "w") as f:
            f.write("COMMAND=\"\"")


def createDbFile():
    if(fileExists(backup.DB_DIR_PATH) is False):
        open(backup.DB_DIR_PATH, "w")


def setupProgram():
    os.system("cp backup.py {}".format(BACKUP_PY_PATH))


def writeSetInterval():
    with open(RUNNER_PATH, "w") as file:
        file.write("sudo python3 {}".format(BACKUP_PY_PATH))
    os.system("chmod +x {}".format(RUNNER_PATH))
    user = os.getenv("SUDO_USER")
    line = "@reboot {}".format(RUNNER_PATH)
    os.system(
        "(crontab -u {} -l; echo {}) | crontab -u {} -".format(user, line, user))


def deleteFiles():
    if(fileExists(backup.CONF_DIR_PATH)):
        os.system("rm -f {}".format(backup.CONF_DIR_PATH))
    if(fileExists(backup.DB_DIR_PATH)):
        os.system("rm -f {}".format(backup.DB_DIR_PATH))
    if(fileExists(backup.LOG_DIR_PATH)):
        os.system("rm -f {}".format(backup.LOG_DIR_PATH))
    if(fileExists(RUNNER_PATH)):
        os.system("rm -f {}".format(RUNNER_PATH))
    if(fileExists(BACKUP_PY_PATH)):
        os.system("rm -f {}".format(BACKUP_PY_PATH))


if __name__ == "__main__":
    backup.sudoOnly()
    deleteFiles()
    createConfFile()
    createLogFile()
    createDbFile()
    setupProgram()
    writeSetInterval()
    print("Setup Completed!")
