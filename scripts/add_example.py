import tensorflow.compat.v1 as tf
import unreal_engine as ue #for remote logging only
from mlpluginapi import MLPluginAPI
import asyncio

tf.disable_v2_behavior()

class ExampleAPI(MLPluginAPI):

	#expected optional api: setup your model for training
	def on_setup(self):
		self.sess = tf.compat.v1.InteractiveSession()
		#self.graph = tf.get_default_graph()

		self.a = tf.compat.v1.placeholder(tf.float32)
		self.b = tf.compat.v1.placeholder(tf.float32)

		#operation
		self.c = self.a + self.b

		ue.log('setup complete')
		pass
		
	#expected optional api: parse input object and return a result object, which will be converted to json for UE4
	def on_json_input(self, json_input):
		
		ue.log(json_input)

		feed_dict = {self.a: json_input['a'], self.b: json_input['b']}

		raw_result = self.sess.run(self.c, feed_dict)

		ue.log('raw result: ' + str(raw_result))

		return {'c':raw_result.tolist()}

	#custom function to change the op
	def change_operation(self, type):
		if(type == '+'):
			self.c = self.a + self.b

		elif(type == '-'):
			self.c = self.a - self.b
		ue.log('operation changed to ' + type)


	#expected optional api: start training your network
	def on_begin_training(self):
		pass
    
#NOTE: this is a module function, not a class function. Change your CLASSNAME to reflect your class
#required function to get our api
def get_api():
	#return CLASSNAME.get_instance()
	return ExampleAPI.get_instance()