#!/usr/bin/env python3

# adapted from issues at https://github.com/albertosottile/darkdetect
# issue #2 on the project presents a simple solution for windows
# issue #3 on the project presents a simple solution for macOS

# file can be run directly to print the current detected stats

# contains two methods, is_dark() and is_light()
# they return True/False on macOS (and Windows, untested), and None on other OSs

import platform
import subprocess


def is_dark():
	if platform.system() == 'Darwin':
		try:
			get_status = 'defaults read -g AppleInterfaceStyle'
			status = subprocess.check_output(
				get_status.split(),
				stderr = subprocess.STDOUT
			).decode()
			status = status.replace('\n', '')
		except subprocess.CalledProcessError as e:
			return False
		return status.lower() == 'dark'
# TODO: this is Windows detection logic
# But this should only be used if Qt can automatically enable its own dark mode
#  when the Windows dark mode is enabled. In that case, we use this to switch
#  the syntax highlighting theme to dark-mode-compatible. But until Qt adds
#  that, it needs to be explicitly enabled in the config which will set both
#  the widget theme as well as the highlighting theme.
#	if platform.system() == 'Windows':
#		import winreg
#		value = 1 # default to light theme
#		try:
#			with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize') as key:
#				value, value_type = winreg.QueryValueEx(key, 'AppsUseLightTheme')
#		except OSError as e:
#			pass
#		return value > 0
	return None


def is_light():
	x = is_dark()
	return x if x == None else not x


if __name__ == '__main__':
	print('Is dark : ', is_dark())
	print('Is light: ', is_light())
