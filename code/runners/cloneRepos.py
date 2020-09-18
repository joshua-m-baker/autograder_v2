#!/usr/bin/env python3

# run grading/code/cloner/getRepos.py with its dir as the working directory
# relative paths: this file is grading/code/runners/cloneRepos.py

import os
import platform
import subprocess

getReposScriptDir = os.path.realpath(os.path.join(os.path.dirname(__file__), '../cloner/'))
getReposScript    = os.path.realpath(os.path.join(os.path.dirname(__file__), '../cloner/getRepos.py'))

def generate_run_command(filename):
	# There's no cross-platform way to run a Python file, so programs are launched
	# in Python IDLE.
	if platform.system() == 'Windows':
		cmd = ["py", "-m", "idlelib"]
	elif platform.system() == 'Darwin':
		cmd = ["idle3"]
	else:
		if os.path.isfile('/usr/bin/idle3'):
			cmd = ["idle3"]
		else:
			cmd = ["idle"]
	return cmd + ["-r", filename]

#subprocess.Popen(getReposScript, cwd=getReposScriptDir)
subprocess.Popen(generate_run_command(getReposScript), cwd=getReposScriptDir)
