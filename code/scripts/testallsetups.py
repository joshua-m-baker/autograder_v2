import subprocess   
import os
import csv
from tqdm import tqdm

import sys
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../..')))
import code.cloner.githubcommands as githubcommands

STUDENT_REPO_PATH_TEMPLATE = os.path.realpath(os.path.join(os.path.dirname(__file__), "../../tempdata/repos")) + "/C200-Assignments-{}"

####################
# Done: Update for summer
# github_url = "git@github.iu.edu:CSCI-C200-Summer-2020/C200-Assignments-{}.git" 
github_url = "https://github.iu.edu/CSCI-C200-Summer-2020/C200-Assignments-{}.git"
hello_world_file = "helloworld.py"
# Usernames in data/all_usernames.txt
####################

with open(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../data/all_usernames.txt'))) as f:
    username_list = [line.strip() for line in f.readlines() if line]

def main():    
    due_date = '2021-1-1 23:01'  #Doesn't actually matter since commit time doesn't matter for this
    
    githubcommands.setup_repos(username_list, github_url, STUDENT_REPO_PATH_TEMPLATE, 0, due_date)
    
    with open("results.csv", "w", newline='') as res:
        with open("issues.txt", "w", newline='') as bad:
            writer = csv.writer(res, delimiter=",")
            writer.writerow(["username", "gitignore", "noCodeFolder", "assignment0", "helloworld", "syntax"])
            for name in tqdm(username_list):
                base_path = os.path.realpath(os.path.join(os.path.dirname(__file__), STUDENT_REPO_PATH_TEMPLATE.format(name)))

                a0path = os.path.realpath(os.path.join(base_path, "Assignment0"))
                helloWorldRuns = False

                gitignoreExists = os.path.isfile(os.path.realpath(os.path.join(base_path, ".gitignore")))
                noCode = not os.path.isdir(os.path.realpath(os.path.join(base_path, ".vscode")))
                ass0Exists = os.path.isdir(a0path)
                helloWorldExists = os.path.isfile(os.path.realpath(os.path.join(a0path, hello_world_file)))
                if helloWorldExists:
                    try:
                        #proc = subprocess.Popen("python3 helloworld.py", cwd=a0path, shell=True) #, stdout=subprocess.DEVNULL)
                        proc = subprocess.run(["py", hello_world_file], cwd=a0path, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) # TODO: This is for Windows
                        if proc.stdout: #Check for any output
                            helloWorldRuns = True

                    except Exception as e:
                        print("Exception")
                        print(e)
                        pass    

                if not all([name, gitignoreExists, noCode, ass0Exists, helloWorldExists, helloWorldRuns]):
                    bad.write(str([name, gitignoreExists, noCode, ass0Exists, helloWorldExists, helloWorldRuns]))
                    bad.write("\n")
                print([name, gitignoreExists, noCode, ass0Exists, helloWorldExists, helloWorldRuns])
                writer.writerow([name, gitignoreExists, noCode, ass0Exists, helloWorldExists, helloWorldRuns])

if __name__ == "__main__":
    main()