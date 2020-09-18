#!/usr/bin/env python3

# reads TeX and calculates total score from sum of scores for each part

# if it gives an error uncomment the commented part and indent the 'try' body

import os
import re
import sys
#from c200config import ConfigReader

cfg = ConfigReader.read()
ASSIGNMENT_NUMBER = cfg.general.assignment

#report_filename_template = 'reports/{}/Assignments/Assignment' + str(grader.config.ASSIGNMENT_NUMBER) + '.tex'
report_filename_template = 'reports/{}/Assignments/Assignment' + str(ASSIGNMENT_NUMBER) + '.tex'

with open('grader/usernames.txt') as f:
	usernames = [x.strip() for x in f.readlines()]

result = ''
wasError = False

for username in usernames:
	report_filename = report_filename_template.format(username)
	with open(report_filename) as f:
		lines = [x.strip() for x in f.readlines()]
		total = 0
		for i in range(len(lines)):
			line = lines[i]
			if line.startswith('\\begin{flushright}\\textbf{Score}: ') and line.endswith('\\end{flushright}'):
				try:
					total += int(line.split('/')[0].split(' ')[1])
				except:
					print('MISSING SCORE ON LINE {} OF {}'.format(i, username))
					wasError = True
			i += 1
		result += '{} {}\n'.format(username, total)

if wasError:
	print()
print(result, end='')
