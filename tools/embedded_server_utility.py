import sys, os

python_folder_name = 'python3.7'

def python_root(relative=None):
	if(relative == None):
		relative = ''
	return os.path.abspath(os.getcwd() + '../../' + python_folder_name + '/' +  relative)

def script_root(relative=None):
	if(relative == None):
		relative = ''
	return os.path.abspath(os.getcwd() + '/' + relative)

#of array of lines
def print_output(string):
	lines = string.splitlines()
	for line in lines:
		print(line)

def copy_environment():
	env = os.environ.copy()
	env["PATH"] = "/usr/sbin:/sbin:" + env["PATH"]
	return env

sys.path.append(python_root('/Lib/site-packages'))
sys.path.append(python_root('/Scripts'))
sys.path.append(script_root('/tools'))



