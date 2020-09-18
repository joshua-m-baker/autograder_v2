import sys
import os

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../..')))

import code.spreadsheet as spreadsheet
import code.cloner.githubcommands as githubcommands
import data.assignment_metadata as data
import subprocess
import shutil
from tqdm import tqdm

from config.c200config import ConfigReader
cfg = ConfigReader.read()

REPO_URL_TEMPLATE = data.SSH_TEMPLATE if cfg.general.clone == 'ssh' else data.HTTPS_TEMPLATE

DATA_FOLDER = os.path.realpath(os.path.join(os.path.dirname(__file__), "../../data"))
REPOS_FOLDER = os.path.realpath(os.path.join(os.path.dirname(__file__), "../../tempdata/repos")) #Where student repos will be cloned to
STUDENT_REPO_PATH = REPOS_FOLDER + "/C200-Assignments-{}"
issues = []

u_list = spreadsheet.getAllUsernames()

githubcommands.reset_target_folder(REPOS_FOLDER)

for username in tqdm(u_list):

    githubcommands.clone_repo(username, REPO_URL_TEMPLATE, REPOS_FOLDER, STUDENT_REPO_PATH)

    try:
        shutil.copy(DATA_FOLDER + "/reports/{}/Report.pdf".format(username), STUDENT_REPO_PATH.format(username))

        c = subprocess.Popen(['git add .; git commit -m "Assignment report pushed"; git push;'], shell=True, cwd=STUDENT_REPO_PATH.format(username))
        c.communicate()
        #print("success")
    except:
        issues.append(username)
        print("failure")