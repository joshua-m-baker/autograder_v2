import sys
sys.path.insert(0, "../..")

import code.spreadsheet as spreadsheet
import code.cloner.githubcommands as githubcommands
import data.assignment_metadata as data
import subprocess


all_usernames = spreadsheet.getAllUsernames() #spreadsheet.getMyUsernames("Josh") 
real_names = spreadsheet.get_usernames_real_names()

REPO_URL_TEMPLATE = data.SSH_TEMPLATE if cfg.general.clone == 'ssh' else data.HTTPS_TEMPLATE

DATA_FOLDER = "../../data"
REPOS_FOLDER = "../../tempdata/repos" #Where student repos will be cloned to
STUDENT_REPO_PATH = REPOS_FOLDER + "/C200-Assignments-{}"
issues = []

for username in all_usernames:
    try:
        #githubcommands.clone_repo(username, REPO_URL_TEMPLATE, REPOS_FOLDER, STUDENT_REPO_PATH)

        with open("../../Report_Template.tex") as f:
            report = f.read()
            
            name = real_names[username]
            report = report.format(**{"name": name})

            with open("../../data/reports/{}/Report.tex".format(username), 'w') as out_f:
                out_f.write(report)
            
            # add in ignore errors to compile command
            c = subprocess.Popen(["pdflatex", "-interaction", "nonstopmode", "Report.tex"], cwd="../../data/reports/{}".format(username)) #"-interaction=batchmode",
            c.communicate()

        print("Done with" + username)
    except Exception as e:
        #print(e)
        issues.append(username)

print(issues)

