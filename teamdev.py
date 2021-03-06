#!/usr/bin/env python3

import logging
import sys
import argparse
import commands
import socket
from pathlib import Path
from subprocess import Popen,PIPE
import messages



REMOTE_SERVER = "www.github.com"

def setup_logging():
 logger = logging.getLogger()
 for h in logger.handlers:
     logger.removeHandler(h)
 h = logging.StreamHandler(sys.stdout)
 #FORMAT = "[%(levelname)s %(asctime)s %(filename)s:%(lineno)s - %(funcName)21s() ] %(message)s"
 FORMAT = "%(message)s"
 h.setFormatter(logging.Formatter(FORMAT))
 logger.addHandler(h)
 logger.setLevel(logging.INFO)
 return logger

def is_connected(REMOTE_SERVER):
 try:
     host = socket.gethostbyname(REMOTE_SERVER)
     s = socket.create_connection((host, 80), 2)
     #print("Here is the ip address the server is running on {} ".format([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] \
     #if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]))
     return True
 except:
     print("Not connected to the internet")
 return False


def setup_folder_structure():
    pass
    #path = Path('backups')
    #path.mkdir(exist_ok=True)



if __name__ == "__main__":
 logger = setup_logging() # sets up logging
 logger.info("Welcome to Open Source Development Platform!")
 #print("Welcome to Open Source Development Platform for Teams")
 is_connected(REMOTE_SERVER) # checks to see if connected to the internet
 setup_folder_structure()
 test = commands.OSDPBase()

 # sets up command line arguments
 parser = argparse.ArgumentParser(description='Open Source Development Platform')
 parser.add_argument("--init","-i", required=False, dest='init',action='store_true',help='Initialize new project folder')
 parser.add_argument("--build","-n", required=False, dest='build',action='store_true',help='Create new project from template file')
 parser.add_argument("--update","-u", required=False, dest='update',action='store_true',help='Update settings')
 parser.add_argument("--backup","-b", required=False,dest='backup',action='store',help='Sync project to backup device')
 parser.add_argument("--destroy","-e", required=False,dest='destroy',action='store',help='Delete project from folder')
 parser.add_argument("--start","-s", required=False,dest='start',action='store',help='Start services')
 parser.add_argument("--stop","-d", required=False,dest='stop',action='store',help='Stop services')
 parser.add_argument("--clean","-c", required=False,dest='clean',action='store_true',help='Generates clean config file')
 parser.add_argument("--list","-l", required=False,dest='list',action='store_true',help='List all projects on team server')
 parser.add_argument("--status","-r", required=False,dest='status',action='store_true',help='Get status of all running vagrant boxes')
 parser.add_argument("--destroyall","-x", required=False,dest='destroyall',action='store_true',help='Destroy all running vagrant boxes')
 parser.add_argument("--dockerps","-ps", required=False,dest='dockerps',action='store_true',help='Gives the status of all running docker containers')
 parser.add_argument("--dropbox","-db", required=False,dest='dropbox',action='store_true',help='Does an rsync to your Dropbox folder')
 parser.add_argument("--killserver","-k", required=False,dest='killserver',action='store_true',help='Kill local server')
 parser.add_argument("--add","-a", required=False,dest='add',action='store',help='Add project from team server')
 parser.add_argument("--connect","-o", required=False,dest='connect',action='store',help='Connect to your kubernetes IDE')
 parser.add_argument("--delete","-t", required=False,dest='delete',action='store',help='Delete project from API')
 # run in server mode only
 parser.add_argument("--server","-p", required=False,dest='server',action='store_true',help='Start server mode')
 result = parser.parse_args()

 if result.init:
     logger.info("Pulling down yaml file so you can customize your environment!")
     #print("Pulling down yaml file so you can customize your development environment.")
     test.init()
     messages.send_message("User just initialized a new project")
 elif result.build:
     test.build()
 elif result.update:
     test.update()
 elif result.backup:
     logger.info("We are backing up all your projects to S3!")
     test.backup_to_S3()
 elif result.destroy:
     project = result.destroy
     logger.info("We are destroying your vagrant box now!")
     #print("We are destroying your vagrant box and removing your project folder.")
     test.destroy(projectname=project)
 elif result.start:
     project = result.start
     logger.info("We are starting your development environment now!")
     #print("We are starting your development environment now!")
     test.start(projectname=project)
 elif result.stop:
     project = result.stop
     logger.info("We are stopping your vagrant box now!")
     #print("We are stopping y our vagrant box now!")
     test.stop(projectname=project)
 elif result.clean:
     Popen(["python3","configs.py"])
 elif result.server:
     Popen(["python3","apiserver.py"], stdout=PIPE)
 elif result.list:
     test.list()
 elif result.status:
     test.get_status()
 elif result.dockerps:
     test.dockerps()
 elif result.destroyall:
     test.destroy_all()
 elif result.dropbox:
     test.backup_to_dropbox()
 elif result.killserver:
     test.kill_server()
 elif result.add:
     project = result.add
     test.add(project)
 elif result.delete:
     project = result.delete
     test.delete_project_from_db(project)
 elif result.connect:
     project = result.connect
     test.connect(project)

