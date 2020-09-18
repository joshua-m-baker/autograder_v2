# Copyright 2019 Trustees of Indiana University
# Written by Subramaniyam Raizada <sub@subraizada.com>
# https://policies.iu.edu/policies/ua-05-intellectual-property/index.html

import random

from config.c200config import ConfigReader
import config.ui_configs as ui_configs

import Popup

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from ruamel import yaml

cfg = ConfigReader.read()
if cfg.general.grader in ui_configs._100_messages_all:
	_100_messages = ui_configs._100_messages_all[cfg.general.grader]
else:
	_100_messages = ui_configs._100_messages_all['default']

ZERO_MESSAGE = 'Not submitted / incorrect'


class ProblemWidget(QWidget):
	def __init__(self, problem_number, yaml_filename, y):
		super().__init__()
		self.setMaximumWidth(600)

		self.problem_number = problem_number
		self.yaml_filename = yaml_filename
		self.yaml_autograder_filename = yaml_filename.split(".")[0] + "-autograder.yaml"
		self.y = y['problems'][problem_number]

		self.problem_name = self.y['name']
		self.problem_filename = self.y['filename']
		self.grading_instructions = self.y['instructions']

		self.comments = ''

		self.spinboxes = []

		self.layout = QVBoxLayout()

		titlebox = QHBoxLayout()
		title = QLabel(f'{self.problem_number}: {self.problem_name} ({self.problem_filename})')
		titlebox.addWidget(title)
		titlebox.addStretch()
		button = QPushButton('0')
		button.setMaximumWidth(25)
		button.clicked.connect(self.zero_all)
		titlebox.addWidget(button)
		button = QPushButton('+')
		button.setMaximumWidth(25)
		button.clicked.connect(self.max_all)
		titlebox.addWidget(button)
		titlebox.setSpacing(0)
		self.layout.addLayout(titlebox)

		separator = QFrame()
		separator.setFrameShape(QFrame.HLine)
		self.layout.addWidget(separator)

		if self.grading_instructions != '':
			instructionsLabel = QLabel(self.grading_instructions)
			instructionsLabel.setWordWrap(True)
			self.layout.addWidget(instructionsLabel)

			separator = QFrame()
			separator.setFrameShape(QFrame.HLine)
			self.layout.addWidget(separator)

		for i in range(len(self.y['parts'])):
			name = self.y['parts'][i]['description']
			score = self.y['parts'][i]['score']
			maxScore = self.y['parts'][i]['point_value']

			partLayout = QHBoxLayout()
			partNameLabel = QLabel(name)
			partNameLabel.setWordWrap(True)
			partLayout.addWidget(partNameLabel)
			partLayout.addStretch()
			spinbox = QSpinBox()
			partLayout.addWidget(spinbox)
			self.spinboxes.append(spinbox)

			#spinbox.setMaximum(maxScore)
			spinbox.setMinimum(0)
			if cfg.general.grader in ui_configs.spinbox_step:
				spinbox.setSingleStep(ui_configs.spinbox_step[cfg.general.grader])
			else:
				spinbox.setSingleStep(ui_configs.spinbox_step['default'])
			spinbox.setValue(score)

			spinbox.valueChanged.connect((lambda partnum: lambda score: self.spinbox_changed(partnum, score))(i))

			partLayout.addWidget(QLabel(f'/{maxScore}   '))

			button = QPushButton('0')
			button.setMaximumWidth(25)
			button.clicked.connect((lambda partnum: lambda: self.zero(partnum))(i))
			partLayout.addWidget(button)
			button = QPushButton('+')
			button.setMaximumWidth(25)
			button.clicked.connect((lambda partnum: lambda: self.max(partnum))(i))
			partLayout.addWidget(button)

			partLayout.setSpacing(0)
			self.layout.addLayout(partLayout)

		self.textedit = QPlainTextEdit()
		if self.y['comments'] != '':
			self.textedit.setPlainText(self.y['comments'])
		self.textedit.setPlaceholderText('Comments...')
		self.textedit.textChanged.connect(self.textedit_changed)
		self.layout.addWidget(self.textedit)

		separator = QFrame()
		separator.setFrameShape(QFrame.HLine)
		self.layout.addWidget(separator)

		# this is deleted and reinitialized in reload_autograder_results, so
		#   initialize it to an empty layout at the beginning
		self.autograder_results_layout = QVBoxLayout()
		self.layout.addLayout(self.autograder_results_layout)

		self.reload_autograder_results()

		self.setLayout(self.layout)


	def textedit_changed(self):
		self.y['comments'] = self.textedit.toPlainText()


	def spinbox_changed(self, partnum, score):
		self.y['parts'][partnum]['score'] = score


	def dump(self):
		return self.y


	def reload_autograder_results(self):
		return #TODO fix
		# recreate the VBoxLayout that displays the test results
		self.autograder_results_layout.deleteLater()
		self.autograder_results_layout = QVBoxLayout()
		arl = self.autograder_results_layout # shortcut

		log = 'ERROR LOG:\n'
		try:
			with open(self.yaml_autograder_filename) as f:
				d = yaml.load(f.read())
				module_name = self.problem_filename.split('.py')[0]
				log += f'Read YAML file, going to examine module {module_name}\n'
				d = d[module_name]
				log += f'Found module results in YAML, going to analyze result data\n'
				for function, test_cases in d.items():
					arl.addWidget(QLabel(function))
					for test_case in test_cases:
						name, passed = test_case['name'], test_case['passed']
						hlayout = QHBoxLayout()
						hlayout.setAlignment(Qt.AlignLeft)

						input_value = test_case['input_value']
						input_value_type = type(input_value)
						solution_result = test_case['solution_result']
						solution_result_type = type(solution_result)
						student_result = test_case['student_result']
						student_result_type = type(student_result)

						function_results_str = f'''\
INPUT
type {input_value_type}
{input_value}

SOLUTION RESULT
type {solution_result_type}
{solution_result}

STUDENT RESULT
type {student_result_type}
{student_result}'''

						show_results_button = QPushButton('+')
						show_results_button.setMaximumWidth(25)
						# some idiot decided lambdas should be (effectively) dynamically scoped in Python
						# so we need this double lambda bs to make it work
						show_results_button.clicked.connect((lambda x: lambda: Popup.show_message_nonblocking(x))(function_results_str))
						hlayout.addWidget(show_results_button)

						fail_label = QLabel('FAIL')
						hlayout.addWidget(fail_label)
						sp = fail_label.sizePolicy()
						sp.setRetainSizeWhenHidden(True)
						fail_label.setSizePolicy(sp)
						if passed:
							fail_label.setVisible(False)
						hlayout.addWidget(QLabel(name))
						arl.addLayout(hlayout)

		except:
			log += f'Failed to load autograder results from file {self.yaml_autograder_filename}\n'
			label = QLabel(log)
			label.setWordWrap(True)
			self.autograder_results_layout.addWidget(label)

		self.layout.addLayout(self.autograder_results_layout)


	def zero(self, partnum):
		self.spinboxes[partnum].setValue(0)


	def max(self, partnum):
		self.spinboxes[partnum].setValue(self.y['parts'][partnum]['point_value'])


	def zero_all(self):
		for i in range(len(self.spinboxes)):
			self.zero(i)

		msgs_to_overwrite = ['']
		for x in _100_messages:
			msgs_to_overwrite.append(x)

		if self.textedit.toPlainText() in msgs_to_overwrite:
			self.textedit.setPlainText(ZERO_MESSAGE)


	def max_all(self):
		for i in range(len(self.spinboxes)):
			self.max(i)

		msgs_to_overwrite = ['', ZERO_MESSAGE]
		if self.textedit.toPlainText() in msgs_to_overwrite:
			self.textedit.setPlainText(random.choice(_100_messages))
