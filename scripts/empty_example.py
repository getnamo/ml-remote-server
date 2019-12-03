import tensorflow as tf
from mlpluginapi import MLPluginAPI

class ExampleAPI(MLPluginAPI):

	#optional api: setup your model for training
	def on_setup(self):
		pass
		
	#optional api: parse input object and return a result object, which will be converted to json for UE4
	def on_json_input(self, input):
		result = {}
		return result

	#optional api: start training your network
	def on_begin_training(self):
		pass


#NOTE: this is a module function, not a class function. Change your CLASSNAME to reflect your class
#required function to get our api
def get_api():
	#return CLASSNAME.getInstance()
	return ExampleAPI.get_instance()