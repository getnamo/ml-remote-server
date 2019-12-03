import tensorflow as tf
from mlpluginapi import MLPluginAPI

class ExampleAPI(MLPluginAPI):

	#expected optional api: setup your model for training
	def on_setup(self):
		self.sess = tf.InteractiveSession()
		#self.graph = tf.get_default_graph()

		self.a = tf.placeholder(tf.float32)
		self.b = tf.placeholder(tf.float32)

		#operation
		self.c = self.a + self.b

		print('setup complete')
		pass
		
	#expected optional api: parse input object and return a result object, which will be converted to json for UE4
	def on_json_input(self, jsonInput):
		
		print(jsonInput)

		feed_dict = {self.a: jsonInput['a'], self.b: jsonInput['b']}

		rawResult = self.sess.run(self.c, feed_dict)

		print('raw result: ' + str(rawResult))

		return {'c':rawResult.tolist()}

	#custom function to change the op
	def change_operation(self, type):
		if(type == '+'):
			self.c = self.a + self.b

		elif(type == '-'):
			self.c = self.a - self.b
		print('operation changed to ' + type)


	#expected optional api: start training your network
	def on_begin_training(self):
		pass
    
#NOTE: this is a module function, not a class function. Change your CLASSNAME to reflect your class
#required function to get our api
def get_api():
	#return CLASSNAME.get_instance()
	return ExampleAPI.get_instance()