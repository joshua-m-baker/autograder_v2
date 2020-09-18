#!/usr/bin/env python3

# TODO: Write data to csv for uploading to canvas


from ruamel import yaml
import numpy as np
import pandas as pd 
import os
import sys

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../..')))
from config.c200config import ConfigReader

cfg = ConfigReader.read()
assignment_number = cfg.general.assignment

allStudentUsernames = []
allStudentScores = []
#gradersStudentsUsernames = open("tempdata/usernames.txt",'r')
allGrades = pd.DataFrame()

usernames_path = "../../tempdata/usernames.txt"
with open(os.path.realpath(os.path.join(os.path.dirname(__file__), usernames_path))) as gradersStudentsUsernames:
    for studentUsername in gradersStudentsUsernames:
        studentUsername= studentUsername.replace("\n","")
        data_path = "../../data/fragments/{}/Assignment{}.yaml".format(studentUsername, assignment_number)
        with open(os.path.realpath(os.path.join(os.path.dirname(__file__), data_path))) as f:
            allStudentUsernames.append(studentUsername)

            student_grades = yaml.safe_load(f)
            for item,doc in student_grades.items():
                if(type(doc)==list): 
                    studentscore = 0
                    for i in range(len(doc)):
                        for j in range(len(doc[i]["parts"])):
                            studentscore+=doc[i]["parts"][j]["score"]
                    allStudentScores.append(studentscore)

allGrades = pd.DataFrame(allStudentScores,allStudentUsernames)
allGrades.columns=[assignment_number] 
print(allGrades)      