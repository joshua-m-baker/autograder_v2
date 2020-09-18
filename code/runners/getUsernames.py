#!/usr/bin/env python3

# read grading/data/MasterListAssignments.xlsx
# write grading/tempdata/usernames.txt

# relative paths: this file is grading/code/runners/getUsernames.py

#TODO go back to using data/spreadsheet.py file to keep stuff DRY
import os
import sys
import xlrd
import csv

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../..')))
from config.c200config import ConfigReader

cfg = ConfigReader.read()


spreadsheet_file = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../data/MasterListAssignments.xlsx'))
tempdata_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../tempdata/'))
if not os.path.exists(tempdata_dir):
	os.makedirs(tempdata_dir)
output_filename = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../tempdata/usernames.txt'))


def getUsernames(graderName):
    wb = xlrd.open_workbook(spreadsheet_file)
    sheet = wb.sheet_by_index(0)
    usernameColumn = 1
    assignmentColumn = -1
    usernameList = []
    for col_index in range(sheet.ncols):
        cell = sheet.cell(0, col_index).value
        if cell == "Assignment{}".format(cfg.general.assignment):
            assignmentColumn = col_index
            break

    foundGrader = False
    for row in range(sheet.nrows):
        cell = sheet.cell(row, assignmentColumn).value
        if cell == graderName or (cell == '' and foundGrader):
            foundGrader = True
            usernameList.append(sheet.cell(row, usernameColumn).value)
        else:
            foundGrader = False

    return usernameList



cfg = ConfigReader.read()
usernames_list = getUsernames(cfg.auto.grader)
with open(output_filename, 'w') as f:
	f.writelines([line + '\n' for line in usernames_list])
