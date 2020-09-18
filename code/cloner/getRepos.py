#!/usr/bin/env python3

# Clones repos and creates autograder runner files
# This should be run from its folder so paths work properly

import platform
import os
import re
import shutil
import sys
from string import Template

sys.path.insert(0, "../..")
from config.c200config import ConfigReader
from data.assignment_metadata import ASSIGNMENTS
import githubcommands
import code.report_writer.writer as writer
import data.assignment_metadata as data

from ruamel import yaml

cfg = ConfigReader.read()

DATA_FOLDER = "../../data"
STUDENT_REPO_PATH = "tempdata/repos/C200-Assignments-{}"
REPO_URL_TEMPLATE = data.SSH_TEMPLATE if cfg.general.clone == 'ssh' else data.HTTPS_TEMPLATE


#Defaults to selecting proper assignment folder, but can be replaced with a misspelled folder.
_default_folder = f'Assignment{cfg.general.assignment}'
_default_template_path = 'test_template.txt'
def writeTestCodeToFolder(username, repoPath=STUDENT_REPO_PATH, folder=_default_folder, path_to_template=_default_template_path):
    studentPath = os.path.join(repoPath.format(username), folder,"gradingTests.py")
    grader_path = os.path.abspath("..") # path to the grading folder

    write_to_grading_template(studentPath, grader_path, username, cfg.general.assignment)


_default_typo_re = "[asignmet\s]+{}\s?".format(cfg.general.assignment)
def findMisspelledAssignmentFolder(username, repo_path=STUDENT_REPO_PATH, regex=_default_typo_re):
    for folder in os.listdir(os.path.join(repo_path.format(username))):
        if re.search(regex, folder, re.IGNORECASE):
            return folder
    return ""

def resolveOptional(username):

    folder = findMisspelledAssignmentFolder(username)
    if folder:
        return folder
    folder = findMisspelledAssignmentFolder(username, regex="opt.*")
    if folder:
        return folder
    return ""



def write_to_grading_template(destination, grader_path, username, assignment_number):
    with open("test_template.txt") as f:

        template_string = Template(f.read())
        template_data = {
            "grader_path": grader_path,
            "username": username,
            "assignment_number": assignment_number
        }
        formatted_string = template_string.substitute(template_data)

        with open(destination, 'w') as fout:
            fout.write(formatted_string)


def deployScriptForUsernames(usernamesList):
    for student in usernamesList:
        student = student.replace("\n", "")
        try:
            writeTestCodeToFolder(student)

        except Exception as e:
            try:
                #Use a regular expression to look for a misspelled folder
                misspelledFolder = findMisspelledAssignmentFolder(student) #TODO: Possibly unneeded since folders should get renamed?

                if not misspelledFolder and cfg.general.assignment == 60:
                    misspelledFolder = resolveOptional(student)

                if misspelledFolder:
                    #print("!!!!! Found folder with typo in name. Make sure to take off points for {} !!!!!".format(student))
                    writeTestCodeToFolder(student, folder=misspelledFolder)
                else:
                    print("No folder {} for {}. No tests generated.".format(_default_folder, student))
            except Exception as e:
                print("No tests generated because of exception: {}".format(e))

def clear_folder(path):
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass
    os.makedirs(os.path.dirname(path), exist_ok=True)

def header(title):
    return "\n{0}{1}{0}".format("-"*5, title)

def main():
    with open('../../tempdata/usernames.txt') as f:
        username_list = [line.strip() for line in f.readlines()]

    if not username_list:
        print("No usernames to grade found. Run config/config_editor.py if you haven't yet. If you have, the grading list might not have been updated yet.")

    print(header("Cloning and checking out repos"))
    githubcommands.setup_repos(username_list, REPO_URL_TEMPLATE, STUDENT_REPO_PATH,cfg.general.assignment, ASSIGNMENTS[cfg.general.assignment]['due'])
    print(header("Writing test files"))
    deployScriptForUsernames(username_list)

    print("Done!")


if __name__ == "__main__":
    main()