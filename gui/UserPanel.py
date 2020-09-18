# Copyright 2019 Trustees of Indiana University
# Written by Subramaniyam Raizada <sub@subraizada.com>
# https://policies.iu.edu/policies/ua-05-intellectual-property/index.html

import os
import subprocess
from ruamel import yaml

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from config.c200config import ConfigReader

from ProblemWidget import ProblemWidget
from syntaxpy import PythonHighlighter

cfg = ConfigReader.read()

# relative paths: this file is grading/gui/UserPanel.py
# this reads/writes/executes the submitted Python files in
#   grading/tempdata/repos/C200-Assignments-USERNAME/AssignmentX/

FILE_NOT_FOUND_MESSAGE = '# FILE NOT FOUND\n'

class UserPanel(QWidget):
	def __init__(self, username, yaml_filename, y):
		super().__init__()

		self.username = username
		self.yaml_filename = yaml_filename
		self.y = y

		num_problems = len(y['problems'])

		self.layout = QHBoxLayout()

		self.problems = []
		self.textedits = []
		# need to keep a reference to these outside of __init__ or they get GC'd
		self.highlights = [] # <--- took a while to figure out that pesky bug
		self.filepaths = []
		self.problems_layout = QStackedLayout()
		self.textedits_layout = QStackedLayout()

		submissions_directory = UserPanel.get_submissions_directory(self.username)

		for i in range(num_problems):
			problem = ProblemWidget(i, yaml_filename, y)
			self.problems.append(problem)
			self.problems_layout.addWidget(problem)

			textedit = QPlainTextEdit()
			self.textedits.append(textedit)
			self.textedits_layout.addWidget(textedit)


			fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
			textedit.setFont(fixedfont)

			if y['problems'][i]['filename'] == '':
				# If the problem doesn't have a filename associated with it, then this
				#   is problem 0: General/Structuring.
				# For convenience, fill the textedit with the list of submitted files.
				try:
					dir_contents = os.listdir(submissions_directory)
					text = 'Files found in student submissions directory:\n'
					for fname in dir_contents:
						text += '   ' + fname + '\n'
					textedit.setPlainText(text)
				except:
					textedit.setPlainText('The student submissions directory either does not exist or contains no files')
			else:
				# If the problem does have a filename associated with it, load the file.

				# enable Python syntax highlighting
				highlight = PythonHighlighter(self.textedits[i].document())
				self.highlights.append(highlight)

				path = os.path.join(submissions_directory, y['problems'][i]['filename'])
				self.filepaths.append(path)
				try:
					with open(path, encoding="utf8") as f:
						textedit.setPlainText(f.read())
				# TODO Currently this overwites the file when the grader is re-opened. Need to fix
				except FileNotFoundError:
					pass
					#textedit.setPlainText(FILE_NOT_FOUND_MESSAGE)
					#textedit.setReadOnly(True)
					#problem.zero_all()
				except IsADirectoryError:
					pass
					#textedit.setPlainText(FILE_NOT_FOUND_MESSAGE)
					#textedit.setReadOnly(True)
					#problem.zero_all()
				except NotADirectoryError:
					pass
					#textedit.setPlainText(FILE_NOT_FOUND_MESSAGE)
					#textedit.setReadOnly(True)
					#problem.zero_all()

		self.layout.addLayout(self.problems_layout)
		self.layout.addLayout(self.textedits_layout)
		self.layout.setStretch(0, 1) # index 0 (problems) has strech factor 1
		self.layout.setStretch(1, 2) # index 1 (textedits) has strech factor 2
		#self.layout.setStretchFactor(self.problems_layout, 1)
		#self.layout.setStretchFactor(self.textedits_layout, 2)

		self.setLayout(self.layout)

	#Make this a class method so it can be accessed where UserPanel is accessed
	@staticmethod
	def get_submissions_directory(username):
		# ../tempdata/repos/C200-Assignments-USERNAME/AssignmentX/
		#return os.path.realpath(os.path.join(os.path.dirname(__file__), f'../tempdata/repos/C200-Assignments-{username}/Assignment{cfg.general.assignment}'))
		return os.path.realpath(os.path.join(os.path.dirname(__file__), f'../tempdata/repos/C200-Assignments-{username}/Assignment{cfg.general.assignment}'))


	def setProblem(self, num):
		self.problems_layout.setCurrentIndex(num)
		self.textedits_layout.setCurrentIndex(num)

	def write(self):
		# replace the 'problem' parts of the yaml with the dumped objects from ProblemWidgets
		for i in range(len(self.problems)):
			self.y['problems'][i] = self.problems[i].dump()
		with open(self.yaml_filename, 'w') as f:
			f.write(yaml.dump(self.y, Dumper=yaml.RoundTripDumper))

	def run_current_file(self, generate_run_command_method):
		# generate_run_command_method is a function that exists in main.py
		textedit = self.textedits_layout.currentWidget()
		bad_files = [FILE_NOT_FOUND_MESSAGE, '', '\n']
		if textedit.toPlainText() in bad_files:
			return

		submissions_directory = UserPanel.get_submissions_directory(self.username)
		filename = self.problems_layout.currentWidget().problem_filename

		filepath = os.path.join(submissions_directory, filename)
		run_path = os.path.join(submissions_directory, '..') #match how vsc runs files

		print(f'{filename} in {submissions_directory}')

		# save the file in case the grader edited it
		with open(filepath, 'w', encoding="utf8") as f:
			f.write(textedit.toPlainText())

		subprocess.Popen(generate_run_command_method(filepath), cwd=run_path)

	def autograde_student(self, generate_run_command_method):

		submissions_directory = UserPanel.get_submissions_directory(self.username)
		tests_file = submissions_directory + "/gradingTests.py"

		proc = subprocess.Popen(generate_run_command_method(tests_file))
		#proc.wait()

		for problem_widget in self.problems:
			problem_widget.reload_autograder_results()
