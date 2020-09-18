import sys
import os

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../..')))

import code.spreadsheet as spreadsheet
import code.cloner.githubcommands as githubcommands
import data.assignment_metadata as data
import subprocess
import shutil


all_usernames = spreadsheet.getAllUsernames() #spreadsheet.getMyUsernames("Josh") 
real_names = spreadsheet.get_usernames_real_names()

REPO_URL_TEMPLATE = data.SSH_TEMPLATE if cfg.general.clone == 'ssh' else data.HTTPS_TEMPLATE

DATA_FOLDER = "../../data"
REPOS_FOLDER = "../../tempdata/repos" #Where student repos will be cloned to
STUDENT_REPO_PATH = REPOS_FOLDER + "/C200-Assignments-{}"
issues = []

for username in all_usernames:
    
    githubcommands.clone_repo(username, REPO_URL_TEMPLATE, REPOS_FOLDER, STUDENT_REPO_PATH)

    try:
        shutil.copy("../../data/reports/{}/Report.pdf".format(username), "../../tempdata/repos/C200-Assignments-{}".format(username))

        c = subprocess.Popen(['git add .; git commit -m "Assignment report pushed"; git push;'], shell=True, cwd="../../tempdata/repos/C200-Assignments-{}".format(username))
        c.communicate()
        #print("success")
    except:
        issues.append(username)
        print("failure")