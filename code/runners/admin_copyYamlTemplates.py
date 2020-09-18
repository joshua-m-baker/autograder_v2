#!/usr/bin/env python3

# copy the YAML template from
#  grading/report_templates/AssignmentX.yaml
# to *all* students (into:
#  grading/data/fragments/USERNAME/AssignmentX.yaml

# this assumes that all the USERNAME directories already exist in the
#   grading/data/fragments folder

# relative paths: this file is grading/code/runners/admin_copyYamlTemplates.py

# TODO pull assigned, due date from metadata file

import os
import shutil
import sys
from ruamel import yaml

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../..')))
from config.c200config import ConfigReader
import code.spreadsheet as spreadsheet

cfg = ConfigReader.read()



template_file_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../report_templates/'))

template_filename = f'Assignment{cfg.general.assignment}.yaml'

template_file = os.path.join(template_file_dir, template_filename)

frag_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../data/fragments'))

u_list = spreadsheet.getAllUsernames()

for username in u_list: 
    dest_path = os.path.join(frag_dir, username, template_filename)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(template_file) as source_file:
        template_source = yaml.safe_load(source_file)
        
        for problem in template_source["problems"]:
            for sub in problem["parts"]:
                sub["score"] = 0

            problem["comments"] = ""

        if "instructions" not in problem.keys():
            problem["instructions"] = ""
                
    with open(dest_path, 'w') as dest_file:
        dest_file.write(yaml.dump(template_source))
