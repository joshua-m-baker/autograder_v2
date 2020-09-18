#!/usr/local/bin/python3

#Script that runs on silo to pull commits at deadline and upload them to the grading repo. The token variable would need to be filled in with your personal github token

import csv
from github import Github
import base64
from datetime import datetime

token = ""
g = Github(base_url="https://github.iu.edu/api/v3", login_or_token=token)

org = g.get_organization("CSCI-C200-Summer-2020")
repos = org.get_repos(type='all')


def get_commits():
    res = {}
    with open("commit_keys.txt", 'w') as commits_file:
        with open("missing.txt", 'w') as missing_file:
            for repo in repos:
                username = repo.name.split("-")[-1]
                commits = repo.get_commits()

                try:
                    if commits.totalCount > 0:
                        res[username] = commits[0].sha

                except Exception as e:

                    res[username] = ''
                    missing_file.write(username)
                    missing_file.write("\n")

            print(res, file=commits_file)
    return res
r = get_commits()

grading_repo = g.get_repo("CSCI-C200-Support/grading")

data = f"#{datetime.now()}\n{str(r)}"
contents = grading_repo.get_contents("code/cloner/commit_keys.txt", ref='s20')

grading_repo.update_file("code/cloner/commit_keys.txt", "Updating commit keys from script", data, sha=contents.sha, branch='s20')
