# Provide standard interface for getting username/ grading related data. The excel file has the most up to date info on drops

import sys
import os
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
from config.c200config import ConfigReader
import xlrd

GRADING_SPREADSHEET_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "../data/MasterListAssignments.xlsx"))

cfg = ConfigReader.read()

def getAllUsernames():
    usernames = []
    usernameColumn = 1 
    wb = xlrd.open_workbook(GRADING_SPREADSHEET_PATH) 
    sheet = wb.sheet_by_index(0) 

    vals = [sheet.cell(r, usernameColumn).value for r in range(sheet.nrows)]

    return [v for v in vals if v not in ["Username", "username", ""]] # Remove artifacts from spreadsheet

def getMyUsernames(graderName, num=cfg.general.assignment):
    wb = xlrd.open_workbook(GRADING_SPREADSHEET_PATH) 
    sheet = wb.sheet_by_index(0) 
    usernameColumn = 1 
    assignmentColumn = -1
    usernameList = []
    for col_index in range(sheet.ncols):
        cell = sheet.cell(0, col_index).value
        if cell == "Assignment{}".format(num):
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

def get_usernames_real_names():
    res = {}

    wb = xlrd.open_workbook(GRADING_SPREADSHEET_PATH) 
    sheet = wb.sheet_by_index(0) 
    name_column = 0
    usernameColumn = 1 

    for row in range(sheet.nrows):
        username = sheet.cell(row, usernameColumn).value
        real_name = sheet.cell(row, name_column).value

        res[username] = real_name
    return res

