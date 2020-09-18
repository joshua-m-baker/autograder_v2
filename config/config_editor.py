#!/usr/bin/env python3

# Copyright 2019 Trustees of Indiana University
# Written by Subramaniyam Raizada <sub@subraizada.com>
# https://policies.iu.edu/policies/ua-05-intellectual-property/index.html

import os
import sys
from c200config import ConfigReader
from syntaxini import IniHighlighter

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

# the config.ini file is always in the same directory as this script
# this line gets the config.ini filepath regardless of which working
#   directory this script is run from
config_fname = os.path.join(os.path.dirname(__file__), 'config.ini')

class Editor(QWidget):
	def __init__(self):
		super().__init__()

		try:
			cfg = ConfigReader.read() # creates the config file if it doesn't exist
		except:
			pass

		self.te = QPlainTextEdit()
		self.highlight = IniHighlighter(self.te.document())
		self.read_cfg()

		self.saveBtn = QPushButton('Save')
		self.saveBtn.clicked.connect(self.save)
		self.resetBtn = QPushButton('Reset to defaults')
		self.resetBtn.clicked.connect(self.reset)

		self.save_shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
		self.save_shortcut.activated.connect(self.save)

		layout = QVBoxLayout()
		layout.addWidget(self.te)
		layout.addWidget(self.saveBtn)
		layout.addWidget(self.resetBtn)
		self.setLayout(layout)
		self.resize(1000, 700)

	def read_cfg(self):
		with open(config_fname) as f:
			self.te.setPlainText(f.read())

	def save(self):
		ConfigReader.write(self.te.toPlainText())
		app.quit()

	def reset(self):
		ConfigReader.reset()
		self.read_cfg()

app = QApplication(sys.argv)
app.setApplicationName('C200 Config Editor')
app.setWindowIcon(QIcon('gui/our_glorious_leader.jpg'))

editor = Editor()
editor.show()
app.exec_()
