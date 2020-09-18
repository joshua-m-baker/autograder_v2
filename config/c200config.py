# Copyright 2019 Trustees of Indiana University
# Written by Subramaniyam Raizada <sub@subraizada.com>
# https://policies.iu.edu/policies/ua-05-intellectual-property/index.html

# config dict structure
#   (make sure to keep this in sync with the default config file template!)
# general (ini General):
#   str grader       # name of grader that this computer belongs to
#   int assignment   # assignment number
#   str clone        # ssh or https
# auto[mation] (ini Automation):
#   str grader       # grader whose students are being graded (may == general.grader)
# gui (ini GUI):
#   bool dark_mode   # dark theme

import os
import platform
from configparser import RawConfigParser

class dotdict(dict):
	# https://stackoverflow.com/a/23689767
	"""dot.notation access to dictionary attributes"""
	__getattr__ = dict.get
	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__


# the config.ini file is always in the same directory as this script
# this line gets the config.ini filepath regardless of which working
#   directory this script is run from
config_fname = os.path.realpath(os.path.join(os.path.dirname(__file__), 'config.ini'))
default_config_fname = os.path.realpath(os.path.join(os.path.dirname(__file__), 'default_config.ini'))

class ConfigReader:
	@staticmethod
	def read():
		if not os.path.isfile(config_fname):
			ConfigReader.reset()
		return ConfigReader.read_inner()

	@staticmethod
	def reset(): # write the default config (or create file if it doesn't exist)
		with open(default_config_fname) as f:
			ConfigReader.write(f.read())

	@staticmethod
	def read_inner():
		# returns a dotdict with the redd config
		cp = RawConfigParser()

		cp.read(config_fname)

		r = dotdict({})
		r.general = dotdict({})
		r.auto = dotdict({})
		r.gui = dotdict({})

		r.general.grader = cp['General']['grader']
		r.general.assignment = int(cp['General']['assignment'])
		r.general.clone = cp['General']['clone']
		r.auto.grader = cp['Automation']['grader']
		r.gui.dark_ui = eval(cp['GUI']['dark_ui'])
		r.gui.dark_syntax_highlighting = eval(cp['GUI']['dark_syntax_highlighting'])

		return r


	@staticmethod
	def write(newcfg):
		# write a string into the existing config file
		with open(config_fname, 'w') as f:
			f.write(newcfg)
