from mlpluginapi import MLPluginAPI
import unreal_engine as ue
import torch

#MLPluginAPI
class ExampleAPI(MLPluginAPI):

	#optional api: setup your model for training
	def on_setup(self):
		ue.log('hello on_setup')
		pass
		
	#optional api: parse input object and return a result object, which will be converted to json for UE4
	def on_json_input(self, input):
		ue.log('hello on_json_input')
		return {}#{'something':'something'}

	#optional api: start training your network
	def on_begin_training(self):
		ue.log('hello on_begin_training')
		pass


#NOTE: this is a module function, not a class function. Change your CLASSNAME to reflect your class
#required function to get our api
def get_api():
	#return CLASSNAME.get_instance()
	return ExampleAPI.get_instance()