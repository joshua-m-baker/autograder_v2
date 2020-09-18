# Copyright 2019 Trustees of Indiana University
# Written by Subramaniyam Raizada <sub@subraizada.com>
# https://policies.iu.edu/policies/ua-05-intellectual-property/index.html

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QUrl, QDir


# set this from main.py when importing for the first time
QT_APP_REFERENCE = None


def show_message_blocking(msg, title='Message'):
	# this blocks the application until the message is accepted with the 'Ok' button
	QMessageBox.about(QT_APP_REFERENCE, 'Message', msg)


class NonBlockingPopup(QDialog):
	def __init__(self, msg, title):
		super().__init__(QT_APP_REFERENCE)

		self.setWindowTitle(title)

		layout = QVBoxLayout(self)
		self.label = QLabel(msg)
		layout.addWidget(self.label)


def show_message_nonblocking(msg, title='Message'):
	NonBlockingPopup(msg, title).show()
