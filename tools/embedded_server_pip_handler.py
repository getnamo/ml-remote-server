#handles checking and installing pip correctly. Some duplication between embedded_server_startup persists

import os
import sys
import subprocess

sys.path.append(os.path.abspath(os.getcwd() + '/tools'))

import embedded_server_utility as util

def rerun_self():
	fullcommand = util.python_root('python.exe') + ' "' + util.script_root('tools/embedded_server_pip_handler.py') + '"'

	return subprocess.check_output(fullcommand, shell=True, stderr=subprocess.STDOUT, env=util.copy_environment()).decode('UTF-8')


def ensure_pip():
	missing = []

	# check if we can import pip
	try:
		import pip
		print('Pip dependency met.')

	except:
		print("Didn't find pip module. Fetching pip, stand by... (~30sec)")

		#filename = python_root() + '/get-pip.py'
		fullcommand = util.python_root('python.exe') +  ' "' + util.python_root('get-pip.py') + '"'

		#print(fullcommand)

		getpip_result = subprocess.check_output(fullcommand, shell=True, stderr=subprocess.STDOUT, env=util.copy_environment()).decode('UTF-8')

		util.print_output(getpip_result)

		print('Pip installed.')

		#rerun self as subprocess to guarantee we suceeded
		rerun_result = rerun_self() 
		util.print_output(rerun_result)

ensure_pip()