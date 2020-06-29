import sys
import os
import subprocess

sys.path.append(os.path.abspath(os.getcwd() + '/tools'))
import embedded_server_utility as util

#list
def pip_list():
	import pkg_resources
	return [p.project_name for p in pkg_resources.working_set]

#read requirements file in server script path
def requirements():
	result = {}
	#open requirements file
	with open(util.script_root('requirements.txt')) as f:
		lines = f.read().splitlines()
		for line in lines:
			nameVer = line.split('==')
			result[nameVer[0]] = nameVer[1]

	return result

#get a list of missing packages
def pip_missing():
	installed = pip_list()
	required = requirements()
	
	missing = {}

	for package in required:
		if package not in installed:
			missing[package] = required[package]
	
	return missing

def install_packages(packages):
	import pip
	for package in packages:
		pip.main(["install", package + '==' + packages[package]])

	#fullcommand = python_root('python.exe -m pip')
	print('packages installed')
	#install_result = subprocess.check_output(fullcommand, shell=True, stderr=subprocess.STDOUT)


def install_missing_packages():
	missing = pip_missing()

	if len(missing) > 0:
		install_packages(missing)
		print('requirements.txt installed')
	else:
		print('requirements.txt already met')


def add_paths():
	sys.path.append(util.python_root('/Lib/site-packages'))
	sys.path.append(util.python_root('/Scripts'))


def startup():
	add_paths()

	#check for pip, we need to use a subprocess loop for this due to import complexity
	fullcommand = util.python_root('python.exe') +  ' "' + util.script_root('/tools/embedded_server_pip_handler.py') + '"'
	output = subprocess.check_output(fullcommand, shell=True, stderr=subprocess.STDOUT, env=util.copy_environment()).decode('UTF-8')

	util.print_output(output)

	install_missing_packages()	

startup()