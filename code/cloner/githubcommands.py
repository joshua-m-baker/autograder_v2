"""
    Holds functions for bulk repo cloning and checkout
"""
import subprocess
import os
import io
import re
import contextlib
import shutil
from tqdm import tqdm

REPOS_FOLDER = os.path.realpath(os.path.join(os.path.dirname(__file__), "../../tempdata/repos")) #Where student repos will be cloned to

def setup_repos(username_list, repo_url_template, repo_path_template, assignment_number, due_date, commit_dict_path="commit_keys.txt", clone_location=REPOS_FOLDER):
    reset_target_folder(REPOS_FOLDER)
    printBuffer = io.StringIO()
    try:
        sha_dict = get_sha_dict(f"commit_keys{assignment_number}.txt")
    except:
        sha_dict = None
        
    with contextlib.redirect_stdout(printBuffer): #suppress cloning print statements
        #with contextlib.redirect_stderr(printBuffer):
        for name in tqdm(username_list):
            dest = repo_path_template.format(name)

            clone_repo(name, repo_url_template, clone_location, dest)
            checkout_repo_before_date(dest, due_date)
            
    fix_student_spelling_errors(clone_location)
    

def reset_target_folder(path):
    path = os.path.join(path, "tmp.txt")
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass
    os.makedirs(os.path.dirname(path), exist_ok=True)

def clone_repo(username, repo_url_template, repos_dir, target_directory):
    # Don't reclone existing repos
    try:
        if not os.path.exists(target_directory):
            command = "git clone -q " + repo_url_template.format(username)

            proc = subprocess.Popen(command, cwd=repos_dir, shell=True, stdout=subprocess.DEVNULL)
            proc.wait() # This loses the async benefits, but ensures the repo is cloned before checking it out
    except Exception as e:
        print("Exception: {}".format(e))

def checkout_repo(username, path, sha_dict): 
    if username in sha_dict:
        commit_hash = sha_dict[username]

        if len(commit_hash) != 0:
            command = "git checkout -fq {}".format(commit_hash)
            return subprocess.Popen(command, cwd=path, shell=True, stdout=subprocess.PIPE).wait()
        
        else:
            command = "git checkout -fq `git rev-list --max-parents=0 HEAD | tail -n 1`" #If their commit isn't in the pulled file, checkout the initial commit so it's clear to graders
            return subprocess.Popen(command, cwd=path, shell=True, stdout=subprocess.PIPE).wait()

def checkout_repo_before_date(path, date):
    try:
        cmd1 = 'git rev-list -n 1 --before="{0}" master'.format(date) # Credit to Larry Gates for the checkout command
        out, err = subprocess.Popen(cmd1, cwd=path, shell=True, stdout=subprocess.PIPE).communicate()
        commit_hash = out.decode("utf-8").rstrip() #windows returns this as a byte string for some godforsaken reason
        command = "git checkout -fq {}".format(commit_hash) # Credit to Larry Gates for the checkout command

        return subprocess.Popen(command, cwd=path, shell=True, stdout=subprocess.PIPE).wait()
    except Exception as e:
        print("Exception: {}".format(e))
            
def get_sha_dict(path_to_file):
    with open(path_to_file) as f:
        data = eval(f.read())
        return data

# Renames any folders in the target directory with spaces in their name to have no spaces
def fix_student_spelling_errors(repos_dir):

    folders_to_move = set() #prevent duplicates from being added, since os.walk might see the same folder more than once
    for root, dirnames, _ in os.walk(repos_dir):
        for d in dirnames:
            if " " in d and not os.path.exists(root+"/"+d.replace(" ", "")): #make sure there isn't already a correct folder
                folders_to_move.add(root+"/"+d)
    for path in folders_to_move:
        try:
            dest = path.replace(" ", "")
            shutil.move(path, dest)

            print(" - {}".format(path))

        except Exception as e:
            print("Error moving file: {}".format(path))
    print()

def resolveOptional(repos_dir):
    regex="opt.*"
    folders_to_move = set() #prevent duplicates from being added, since os.walk might see the same folder more than once
    for root, dirnames, _ in os.walk(repos_dir):
        for d in dirnames:
            if re.search(regex, d, re.IGNORECASE):
                folders_to_move.add(root+"/"+d)

    for path in folders_to_move:
        try:
            if ("opt" in path) or ("Opt" in path):
                dest = "/".join(path.split("/")[0:-1] + ["Assignment60"] )
                shutil.move(path, dest)

            #print(" - {}".format(path))

        except Exception as e:
            print("Error moving file: {}".format(path))

     
    print()

def resolveFinal(repos_dir):
    regex="final.*"
    folders_to_move = set() #prevent duplicates from being added, since os.walk might see the same folder more than once
    for root, dirnames, _ in os.walk(repos_dir):
        for d in dirnames:
            if re.search(regex, d, re.IGNORECASE):
                folders_to_move.add(root+"/"+d)

    for path in folders_to_move:
        try:
            if ("fin" in path) or ("Fin" in path):
                dest = "/".join(path.split("/")[0:-1] + ["Assignment99"] )
                shutil.move(path, dest)

            #print(" - {}".format(path))

        except Exception as e:
            print("Error moving file: {}".format(path))

     
    print()