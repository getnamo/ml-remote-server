import tensorflow as tf
import unreal_engine as ue
from MLPluginAPI import MLPluginAPI

class ExampleAPI(MLPluginAPI):

	#optional api: setup your model for training
	def onSetup(self):
		pass
		
	#optional api: parse input object and return a result object, which will be converted to json for UE4
	def onJsonInput(self, jsonInput):
		result = {}
		return result

	#optional api: start training your network
	def onBeginTraining(self):
		pass
    
#NOTE: this is a module function, not a class function. Change your CLASSNAME to reflect your class
#required function to get our api
def getApi():
	#return CLASSNAME.getInstance()
	return ExampleAPI.getInstance()