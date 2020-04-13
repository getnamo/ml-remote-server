#MLPluginAPI
#renamed file

import shared_globals as g

#debug
print('MLPluginAPI imported')

class MLPluginAPI():

	@classmethod
	def get_instance(cls):
		#This should return an instance of your class even if you subclassed it
		return cls()


	## Private
	def __init__(self):
		#class scoped variable for stopping
		self.should_stop = False		#check this variable to stop training early
		self.should_retrain = False		#use this variable to force your training
		self.should_train_on_start = True
		self.stored = {}

	#internal don't need to override this
	def _reset_training_trigger(self):
		self.should_stop = False

	#internal don't need to override this: early stopping
	def _stop_training(self):
		self.should_stop = True
		self.on_stop_training()


	## Public
	
	#call this inside your class to emit a custom event on gt, don't override the function
	def call_event(self, event, data = None, useJson = False):
		g.custom_event(event, data, useJson)

	#expected api: setup your model for training
	def on_setup(self):
		#setup or load your model and pass it into stored
		
		#Usually store session, graph, and model if using keras
		#self.sess = tf.InteractiveSession()
		#self.graph = tf.get_default_graph()
		pass

	#expected api: json inputs
	def on_json_input(self, json_input):
		#e.g. our json input could be a pixel array
		#pixelarray = jsonInput['pixels']

		#run input on your graph
		#e.g. sess.run(model['y'], feed_dict)
		# where y is your result graph and feed_dict is {x:[input]}

		#...

		#return a json you will parse e.g. a prediction
		result = {}
		result['prediction'] = 0

		return result

	#expected optional api: expects float array passed in and returned
	def on_float_array_input(self, float_array_input):
		
		#return an array output
		return []

	#expected api: no params forwarded for training? TBC
	def on_begin_training(self):
		#train here

		#...

		#inside your training loop check if we should stop early
		#if(self.shouldStop):
		#	break
		pass

	def on_stop_training(self):
		#you should be listening to self.shouldStop, but you can also receive this call
		pass

	def on_save_model(self, model_name):
		#you should be listening to self.shouldStop, but you can also receive this call
		pass

	def on_load_model(self, model_name):
		#you should be listening to self.shouldStop, but you can also receive this call
		pass


#required function to get our api
def get_api():
	#return CLASSNAME.get_instance()
	return MLPluginAPI.get_instance()
