#!/usr/bin/env python3

# One off script for fixing reports that got overwritten

import re
import os
to_copy = []
root = "data/reports"
for d in next(os.walk(root))[1]: 
    master_report = f"{root}/{d}/Assignments/Assignment2.tex"    
    old_report = f"~/dev/temp/grading/data/reports/{d}/Assignment/Assignment2.tex"
    
    try:

        with open(master_report) as f:
            bottom = f.readlines()[-2].strip()
            score = re.search("(\d+)\/\d+", bottom).group(1)

            if int(score) == 0:
                to_copy.append(d)

    except FileNotFoundError:
        pass

import shutil
errors = []
for name in to_copy:

    master_report = f"{root}/{name}/Assignments/Assignment2.tex"    
    old_report = f"/home/josh/dev/temp/grading/data/reports/{name}/Assignments/Assignment2.tex"
    try:
        shutil.copy(old_report, master_report)
    except Exception as e:
        print(e)
        errors.append(name)
print(errors)
