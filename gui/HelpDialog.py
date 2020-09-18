# Copyright 2019 Trustees of Indiana University
# Written by Subramaniyam Raizada <sub@subraizada.com>
# https://policies.iu.edu/policies/ua-05-intellectual-property/index.html

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

def create_help_dialog(self): # literally need to pass in self to this method
	HelpDialog = QDialog(self)
	HelpDialog.setModal(True)
	layout = QVBoxLayout(HelpDialog)
	tabs = QTabWidget()
	layout.addWidget(tabs)



	tabs.addTab(QLabel("""\

TODO: make sure this is up-to-date

Ctrl+R
  Run current file

Ctrl+Shift+R
  Run autograder for this student

Ctrl+S
  Save all grade reports

Ctrl+Shift+V
  Insert a random encouraging message
  The default is 'Great job 100%', you can add an array to config/ui_configs.py with the messages you want!

Menu => Config
  Run the config editor to change the assignment you are grading. Do this before running getRepos.

Menu => Get repos
  Clone the repos you need to grade

Menu => Calculate totals
  When grading, just enter the grade for each individual problem. This will sum them up to give the final grade for every student.

Menu => Export CSV
  Creates a grades.csv file on your Desktop; go to the Canvas gradebook => Actions => Import
  This way you don't need to manually type grades into the Canvas gradebook
"""), 'Using the GUI')



	tabs.addTab(QLabel("""\
Message if you have any questions
"""), 'Grading Tutorial')

	HelpDialog.exec()
