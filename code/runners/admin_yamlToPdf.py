#!/usr/bin/env python3

# Running: if invoked directly the assignment number will be taken from config file
# Or pass assignment number as a cmdline argument

import os 
import sys
import subprocess
from tqdm import tqdm

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../..')))
from config.c200config import ConfigReader

cfg = ConfigReader.read()

import code.report_writer.writer as writer
import code.spreadsheet as spreadsheet

usernames_file_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../tempdata/usernames.txt'))
template_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../report_templates/Report_Template.tex'))
reports_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../data/reports'))
data_folder = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../data/fragments'))
data_folder += "/{}"

u_list = spreadsheet.getAllUsernames()
real_names = spreadsheet.get_usernames_real_names()

# real_names = spreadsheet.get_usernames_real_names()
with open(template_path) as f:
    report_template = f.read()

def compile_report(username):
        
    name = real_names[username]
    report = report_template.format(**{"name": name})

    with open(reports_folder + "/{}/Report.tex".format(username), 'w') as out_f:
        out_f.write(report)
    
    
    command = ["pdflatex", "-quiet", "-interaction", "nonstopmode", "Report.tex"] 

    try:
        x = subprocess.check_call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, cwd=reports_folder+"/{}".format(username))
        return True

    except subprocess.CalledProcessError:
        return False

if len(sys.argv) == 2:
    assignment_number = int(sys.argv[1])
else:
    assignment_number = cfg.general.assignment

tex_errors = []
pdf_compile_errors = []

# Generate tex for all students
for username in tqdm(u_list): #os.listdir(reports_folder):
    try:
        writer.create_tex(username, assignment_number, data_folder) 
        
    except Exception  as e:
        #print(e)
        tex_errors.append(username)
    try:
        r = compile_report(username)
        if not r:
            pdf_compile_errors.append(username)
    except Exception as e:
        print(e)
        pdf_compile_errors.append(username)

if len(tex_errors) > 0:
    print("Errors creating tex files: ")
    print(tex_errors)

if len(pdf_compile_errors) > 0:
    print("Errors compiling pdf files: ")
    print(pdf_compile_errors)