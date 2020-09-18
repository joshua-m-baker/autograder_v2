#!/usr/bin/env python3

# Copyright 2019 Trustees of Indiana University
# Written by Subramaniyam Raizada <sub@subraizada.com>
# https://policies.iu.edu/policies/ua-05-intellectual-property/index.html

#    This file is part of C200 Grader GUI.
#
#    C200 Grader GUI is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    C200 Grader GUI is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with C200 Grader GUI.  If not, see <https://www.gnu.org/licenses/>.

# Requirements:
# pip install PyQt5
# pip install qdarkstyle, if using dark mode

# this program assumes it is being run from its directory
# it does not use program-relative paths for all r/w/x operations
# this file is grading/gui/main.py

import random
import sys
import traceback
from time import sleep
from ruamel import yaml

# allows importing stuff from other directories in the parent directory
sys.path.insert(0, '..')
from config.c200config import ConfigReader

cfg = ConfigReader.read()



import os, platform, subprocess
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QUrl, QDir

from ProblemWidget import ProblemWidget
from UserPanel import UserPanel
import Popup # this needs a reference to the Qt app, set at the bottom of this file
import HelpDialog

# ignore pesky warnings about YAML loading bad practices
import warnings
warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)

_get_usernames_memo = None
def get_usernames():
	global _get_usernames_memo
	if _get_usernames_memo != None:
		return _get_usernames_memo
	try: # (file might not exist)
		with open('../tempdata/usernames.txt') as f:
			result = [line.split()[0].strip() for line in f]
	except FileNotFoundError:
		result = []
	_get_usernames_memo = result
	return result



def generate_run_command(filename):
	# There's no cross-platform way to embed a terminal, so programs are launched
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



def show_message(msg):
	# this blocks until the message is accepted with the 'Ok' button
	QMessageBox.about(grader, 'Message', msg)

# tabbed pane for students
# hbox on top with buttons for problems

class Grader(QWidget):
	def __init__(self):
		super().__init__()

		self.tabs = QTabWidget()
		self.tabs.setUsesScrollButtons(True)
		self.tabs.setMovable(True)

		self.userPanels = []

		self.problem_selectors_layout = QVBoxLayout()
		self.problem_selectors_layout.setAlignment(Qt.AlignTop)

		if get_usernames() == []: # if not yet setup for grading
			y = None
			num_problems = 0
		else:
			try:
				fragments_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../data/fragments/'))
				templates_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../report_templates/'))

				yaml_filename = os.path.join(templates_path, f'Assignment{cfg.general.assignment}.yaml')
				with open(yaml_filename) as f:
					y = yaml.load(f.read(), Loader=yaml.RoundTripLoader)
				num_problems = len(y['problems'])
				problem_names = []
				for problem in y['problems']:
					problem_names.append(problem['name'])

				for username in get_usernames():
					yaml_filename = os.path.join(fragments_path, username, f'Assignment{cfg.general.assignment}.yaml')
					with open(yaml_filename) as f:
						y = yaml.load(f.read(), Loader=yaml.RoundTripLoader)
					self.userPanels.append(UserPanel(username, yaml_filename, y))
					self.tabs.addTab(self.userPanels[-1], username)

			except Exception as e:
				y = None
				num_problems = 0
				print(f'Error loading problems for assignment {cfg.general.assignment}')
				print(e)
				traceback.print_exc()


		def setProblem(num):
			for panel in self.userPanels:
				panel.setProblem(num)

		for i in range(num_problems):
			button = QPushButton(str(i) + '\n' + problem_names[i])
			# some idiot decided lambdas should be (effectively) dynamically scoped in Python
			# so we need this double lambda bs to make it work
			button.clicked.connect((lambda x: lambda: setProblem(x))(i))
			self.problem_selectors_layout.addWidget(button)

		layout = QVBoxLayout()
		main_layout = QHBoxLayout()
		main_layout.addLayout(self.problem_selectors_layout)
		main_layout.addWidget(self.tabs)
		layout.addLayout(main_layout)


		action_button_layout = QHBoxLayout()

		button = QPushButton('Run file')
		button.clicked.connect(self.run_file)
		action_button_layout.addWidget(button)
		QShortcut(QKeySequence('Ctrl+R'), self).activated.connect(self.run_file)

		button = QPushButton('Autograde student')
		button.clicked.connect(self.grade_student)
		action_button_layout.addWidget(button)
		QShortcut(QKeySequence('Ctrl+Shift+R'), self).activated.connect(self.grade_student)

		button = QPushButton('Save grades')
		button.clicked.connect(self.write)
		action_button_layout.addWidget(button)
		QShortcut(QKeySequence('Ctrl+S'), self).activated.connect(self.write)

		button = QPushButton('Menu')
		menu = QMenu()
		menu.addSection('Grading')
		menu.addAction('1: Edit config').triggered.connect(self.menu_edit_config)
		menu.addAction('2: Setup for grading && clone').triggered.connect(self.menu_setup_and_clone)
		menu.addAction('3: Autograde students').triggered.connect(self.menu_autograde)
		#menu.addAction('4: Export CSV').triggered.connect(self.menu_export)
		menu.addAction('4: Calculate Grades').triggered.connect(self.menu_export)
		menu.addSection('Miscellaneous')
		menu.addAction('Open student repo folder').triggered.connect(self.menu_open_student_repo)
		menu.addAction('Grader configuration').triggered.connect(self.menu_edit_grader_config)
		menu.addAction('Help').triggered.connect(self.menu_help)
		menu.addSection('Admin')
		menu.addAction('Open assignmnents file').triggered.connect(self.menu_admin_open_assignments_file)
		menu.addAction('Open template directory').triggered.connect(self.menu_admin_open_template_dir)
		menu.addAction('Copy YAML templates').triggered.connect(self.menu_admin_copy_yaml)
		menu.addAction('Compile YAML to PDF').triggered.connect(self.menu_admin_compile_yaml)
		menu.addAction('Push Reports').triggered.connect(self.menu_admin_push_reports)
		button.setMenu(menu)
		action_button_layout.addWidget(button)

		layout.addLayout(action_button_layout)

		self.setLayout(layout)

	def show_yes_no(self, message):
		buttonReply = QMessageBox.question(self, 'Admin Confirm', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		return buttonReply == QMessageBox.Yes

	def write(self):
		for p in self.userPanels:
			p.write()

	def run_file(self):
		self.tabs.currentWidget().run_current_file(generate_run_command)

	def grade_student(self):
		self.tabs.currentWidget().autograde_student(generate_run_command)

	def menu_help(self):
		HelpDialog.create_help_dialog(self)

	def menu_edit_config(self):
		editor = '../config/config_editor.py'
		subprocess.Popen(generate_run_command(editor))

	def menu_setup_and_clone(self):
		Popup.show_message_blocking('''\
You must wait for the scripts in *all* four IDLE windows to finish successfully (display a second '>>>' prompt with no errors).

Then, your students' grade reports have been loaded and their repositories cloned.
Restart the GUI to view the data.

Click OK to continue.
''')
		runner_path = '../code/runners/reset.py'
		s = subprocess.Popen(generate_run_command(runner_path))
		sleep(2) #s.wait()
		runner_path = '../code/runners/getUsernames.py'
		s = subprocess.Popen(generate_run_command(runner_path))
		sleep(2) #s.wait()
		runner_path = '../code/runners/cloneRepos.py'
		subprocess.Popen(generate_run_command(runner_path))

	def menu_autograde(self):
		pass # TODO

	def menu_export(self):
		runner_path = '../code/runners/exportCsv.py'
		s = subprocess.Popen(generate_run_command(runner_path))

	def menu_open_student_repo(self):
		username = self.tabs.currentWidget().username
		student_path = UserPanel.get_submissions_directory(username)
		if os.path.exists(student_path):
			path = QDir.toNativeSeparators(student_path)
			QDesktopServices.openUrl(QUrl.fromLocalFile(path))
		else:
			student_path = os.path.realpath(os.path.join(student_path, "..")) #if the assignment folder doesn't exist, we'll assume their repo does and try to open that
			path = QDir.toNativeSeparators(student_path)
			QDesktopServices.openUrl(QUrl.fromLocalFile(path))
			
	def menu_edit_grader_config(self):
		templates_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../config/ui_configs.py'))
		path = QDir.toNativeSeparators(templates_path)
		QDesktopServices.openUrl(QUrl.fromLocalFile(path))

	def menu_admin_open_assignments_file(self):
		templates_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../data/assignment_metadata.py'))
		path = QDir.toNativeSeparators(templates_path)
		QDesktopServices.openUrl(QUrl.fromLocalFile(path))

	def menu_admin_open_template_dir(self):
		templates_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../report_templates/'))
		path = QDir.toNativeSeparators(templates_path)
		QDesktopServices.openUrl(QUrl.fromLocalFile(path))

	def menu_admin_copy_yaml(self):
		if self.show_yes_no("This will overwrite uncommitted yaml files. Are you sure?"):
			runner_path = '../code/runners/admin_copyYamlTemplates.py'
			subprocess.Popen(generate_run_command(runner_path))

	def menu_admin_compile_yaml(self):
		if self.show_yes_no("Are you sure?"):
			runner_path = '../code/runners/admin_yamlToPdf.py'
			subprocess.Popen(generate_run_command(runner_path))


	def menu_admin_push_reports(self):
		if self.show_yes_no("Are you sure?"):
			runner_path = '../code/runners/admin_copyPushReports.py'
			subprocess.Popen(generate_run_command(runner_path))







app = QApplication(sys.argv)
app.setApplicationName(f'C200 Grader, Assignment {cfg.general.assignment}')
app.setWindowIcon(QIcon('our_glorious_leader.jpg'))



# see comments in the config file
if cfg.gui.dark_ui:
	import qdarkstyle
	app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())



# Display license notice before starting the application
print("""
	C200 Grader GUI  Copyright 2019 Trustees of Indiana University
	This program comes with ABSOLUTELY NO WARRANTY; for details see the file
	COPYING. This is free software, and you are welcome to redistribute it
	under certain conditions; see the file COPYING for details.
""")

grader = Grader()
Popup.QT_APP_REFERENCE = grader
#grader.showMaximized()
grader.resize(QDesktopWidget().availableGeometry(grader).size() * 0.9)
grader.show()

app.exec_()
