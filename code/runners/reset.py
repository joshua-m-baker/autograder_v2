#!/usr/bin/env python3

# clear grading/tempdata
# relative paths: this file is grading/code/runners/reset.py

import os
import shutil
from time import sleep

tempdata_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../tempdata'))


shutil.rmtree(tempdata_dir, ignore_errors=True)

# try/catch loop needed becuase windows is stupid
for i in range(10):
	try:
		os.mkdir(tempdata_dir)
		break
	except:
		sleep(1)
