#!/usr/bin/env python3
# No configuration required in here, unless you use Windows (see line 12)

import os

os.chdir('grader')
import grader.config
os.chdir('..')

AssignmentNumber = grader.config.ASSIGNMENT_NUMBER

import sys, platform, subprocess
EDITOR_CMD = os.environ['EDITOR'] if (platform.system() != 'Windows') else 'notepad.exe'
# I don't use Window$, on POSIXy systems this uses the user's $EDITOR (e.g. vim)

# Runs the command `vim a b c ...`
# Where a, b, c, ... are the grading TeX files for the current assignment and
# the current students, and 'vim' is actually the current EDITOR

# get usernames from smallusernames.txt
usernames = []
with open('grader/usernames.txt') as f:
	for line in f:
		usernames += [line.strip()]

# this is the filepath to the grading report TeX file, plug in assignment number
file_template = 'reports/{}/Assignments/Assignment{}.tex'.format('{}', AssignmentNumber)

# and make a list of files after plugging in the usernames
files = []
for username in usernames:
	files += [file_template.format(username)]

# build up the command string
# e.g. cmd = ['vim', 'file1', 'file2', 'file3', ...]
cmd = [EDITOR_CMD]
for f in files:
	cmd += [f]

# and run it
subprocess.run(cmd)
