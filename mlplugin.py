import importlib
from mlpluginapi import MLPluginAPI
from threading import Timer
import traceback
import unreal_engine as ue
import upythread_server as ut

#Script data
active_script = None
active_script_name = None
mlobject = None
script_folder = 'scripts'
USE_MULTITHREADING = True

#load script into memory. Ready to call begin_play/setup().
def load(script_name):
	global active_script
	global active_script_name
	global mlobject

	if(active_script_name != script_name):
		del active_script
		active_script = None
		mlobject = None
		active_script_name = None

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

#begins setup and training if marked as should_train_on_start
async def begin_play_events():
	if(mlobject.should_train_on_start):
		start_training()

#Typically called shortly after loading script 
def begin_play():
	if(mlobject == None):
		error_msg = 'mlplugin Error: No valid active script, run load first'
		print(error_msg)
		return None, error_msg
	else:
		try:
			#call startup sequence
			mlobject.on_setup()

			#schedule this event for next tick to unblock messaging
			ue.run_on_sio(begin_play_events())

			return True, None
		except BaseException as e:
			error_stack = traceback.format_exc()
			error_msg = 'mlplugin Error: Incorrect api for ' + active_script_name + ': ' + str(error_stack)
			return None, error_msg


#wrap a function call with checks and local options
def call_with_checks(function, input_params=None, callback=None):
	#capture any errors
	try:
		#ensure we call only when we have a valid mlobject (loaded script)
		if(mlobject != None):
			#swap between threaded operation
			if(USE_MULTITHREADING):
				ut.run_on_bt(function, input_params, callback)
			else:
				if(input_params == None):
					return function(None, callback)
				else:
					return function(input_params, callback)
	except BaseException as e:
			error_stack = traceback.format_exc()
			ue.log(error_s)

#def input_callback(input):
	

def start_training():
	call_with_checks(mlobject.on_begin_training)

def stop_training():
	if(mlobject != None):
		#flip the internal state
		mlobject._stop_training()

#run inputs on our class
def json_input(input_params, callback=None):
	call_with_checks(mlobject.on_json_input, input_params, callback)

def float_input(input_params, callback=None):
	call_with_checks(mlobject.on_float_array_input, input_params, callback)
		
def custom_function(name, param, callback=None):
	if(mlobject != None):
		#check for valid method first
		method_to_call = getattr(mlobject, name)
		if(method_to_call):
			return call_with_checks(method_to_call, param, callback)
		else:
			return None, "No such function" + str(name)
		