import importlib
from mlpluginapi import MLPluginAPI

#Script data
active_script = None
active_script_name = None
mlobject = None
script_folder = 'examples'

#begins setup and training if marked as should_train_on_start
def start():
	if(mlobject == None):
		error_msg = 'mlplugin Error: No valid active script, run load first'
		print(error_msg)
		return None, error_msg
	else:
		try:
			#call startup sequence
			mlobject.on_setup()
			if(mlobject.should_train_on_start):
				mlobject.on_begin_training()
		except:
			error_msg = 'mlplugin Error: Incorrect api for' + active_script_name
			return None, error_msg


#load script into memory. Ready to call start().
def load(script_name):
	global active_script
	global active_script_name
	global mlobject

	status_msg = 'unknown'
	active_script_name = script_name

	if(active_script != None):
		importlib.reload(active_script)
	else:
		active_script = importlib.import_module(script_folder + '.' + script_name)

	#grab an instance and check api
	try:
		mlobject = active_script.get_api()
		if issubclass(mlobject.__class__, MLPluginAPI):
			status_msg = 'valid script loaded'
			return status_msg, None #its valid reverse tuple
		else:
			status_msg = 'invalid script class, please subclass MLPluginAPI'
			return None, status_msg
	except BaseException as e:
		status_msg = e
		return None, status_msg


#run inputs on our class
def json_input(input):
	if(mlobject != None):
		mlobject.on_json_input(input)

def float_input(input):
	if(mlobject != None):
		mlobject.on_float_array_input(input)

def custom_function(name, param):
	if(mlobject != None):
		method_to_call = getattr(mlobject, name)
		if(method_to_call):
			method_to_call(param)