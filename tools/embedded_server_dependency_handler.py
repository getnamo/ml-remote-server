import os
import sys
import subprocess

python_folder_name = 'python3.7.8'

def python_root(relative=None):
	if(relative == None):
		relative = ''
	return os.path.abspath(os.getcwd() + '../../' + python_folder_name + '/' +  relative)

def script_root(relative=None):
	if(relative == None):
		relative = ''
	return os.path.abspath(os.getcwd() + '/' + relative)

def copy_environment():
	env = os.environ.copy()
	env["PATH"] = "/usr/sbin:/sbin:" + env["PATH"]
	return env

# Ensure our pip lib/site-packages is in path
sys.path.append(python_root('/Lib/site-packages'))
sys.path.append(python_root('/Scripts'))
sys.path.append(script_root())
sys.path.append(script_root('/tools'))

def rerun_self():
	fullcommand = python_root('python.exe') + ' "' + script_root('tools/embedded_server_dependency_handler.py') + '"'

	return subprocess.check_output(fullcommand, shell=True, stderr=subprocess.STDOUT, env=copy_environment()).decode('UTF-8')

#of array of lines
def print_output(string):
	lines = string.splitlines()
	for line in lines:
		print(line)


def ensure_pip():
	missing = []

	# check if we can import pip
	try:
		import pip
		print('Pip dependency met.')

	except:
		print("Didn't find pip module. Fetching pip, stand by... (~30sec)")

		#filename = python_root() + '/get-pip.py'
		fullcommand = python_root('python.exe') +  ' "' + python_root('get-pip.py') + '"'

		#print(fullcommand)

		getpip_result = subprocess.check_output(fullcommand, shell=True, stderr=subprocess.STDOUT, env=copy_environment()).decode('UTF-8')

		print_output(getpip_result)

		print('Pip installed.')

		#rerun self as subprocess to guarantee we suceeded
		rerun_result = rerun_self() 
		print_output(rerun_result)

ensure_pip()