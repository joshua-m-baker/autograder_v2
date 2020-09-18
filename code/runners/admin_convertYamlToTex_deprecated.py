#!/usr/bin/env python3

# DEPCRECATED use admin_yamlToPdf.py instead
import os 
import sys

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../..')))
from config.c200config import ConfigReader

cfg = ConfigReader.read()

import code.report_writer.writer as writer

usernames_file_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../tempdata/usernames.txt'))

reports_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../data/reports'))

data_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../data/fragments'))
data_folder += "/{}"

errors = []

# Generate tex for all students
for username in os.listdir(reports_folder):
    try:
        #cfg.general.assignment
        writer.create_tex(username, cfg.general.assignment_number, data_folder)   
    except Exception  as e:
        print(e)
        errors.append(username)

print("Errors writing reports")
print(errors)     
