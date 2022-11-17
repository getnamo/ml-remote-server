#converted for unreal use from
#https://www.tensorflow.org/tutorials/quickstart/beginner and
#https://github.com/fchollet/keras/blob/master/examples/mnist_cnn.py

# Import data
#from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf
import numpy as np
import random

import unreal_engine as ue
from mlpluginapi import MLPluginAPI

import operator



ue.log("TensorFlow version:" + str(tf.__version__))

class MnistSimple(MLPluginAPI):

	#keras stop callback
	class StopCallback(tf.keras.callbacks.Callback):
		def __init__(self, outer):
			self.outer = outer

		def on_train_begin(self, logs={}):
			self.losses = []

		def on_batch_end(self, batch, logs={}):
			if(self.outer.shouldStop):
				#notify on first call
				if not (self.model.stop_training):
					ue.log('Early stop called!')
				self.model.stop_training = True

			else:
				#if(batch % 5 == 0):
					#json convertible types are float64 not float32
				#	logs['acc'] = np.float64(logs['acc'])
				#	logs['loss'] = np.float64(logs['loss'])
				#	self.outer.callEvent('TrainingUpdateEvent', logs, True)

				#callback an example image from batch to see the actual data we're training on
				if((batch*self.outer.batch_size) % 10000 == 0):
					index = random.randint(0,self.outer.batch_size)*batch

					#todo: re-implement image sampling
					#self.outer.jsonPixels['pixels'] = self.outer.x_train[index].ravel().tolist()
					#self.outer.callEvent('PixelEvent', self.outer.jsonPixels, True)
	
	#expected api: storedModel and session, json inputs
	def on_json_input(self, json_data):
		result = {'prediction':-1}

		#expect an image struct in json format
		x_raw = json_data['pixels']
		x_raw = np.reshape(x_raw, (1, 28, 28))

		ue.log('image shape: ' + str(x_raw.shape))

		#embedd the input image pixels as 'x'
		x = np.reshape(x_raw, (len(x_raw), 28, 28, 1))

		#run the input through our network
		if self.model is None:
			ue.log("Warning! No 'model' found. Did training complete?")
			return result

		#restore our saved session and model
		#K.set_session(self.session)

		#with self.session.as_default():
		output = self.model.predict(x)

		ue.log(output)

		#convert output array to prediction
		index, value = max(enumerate(output[0]), key=operator.itemgetter(1))

		result['prediction'] = index
		result['pixels'] = json_data['pixels'] #unnecessary but useful for round trip testing

		return result

	#expected api: no params forwarded for training? TBC
	def on_begin_training(self):

		ue.log("starting mnist simple training")

		#self.scripts_path = ue.get_content_dir() + "Scripts"
		#self.data_dir = self.scripts_path + '/dataset/mnist'

		mnist = tf.keras.datasets.mnist

		(x_train, y_train), (x_test, y_test) = mnist.load_data()
		x_train, x_test = x_train / 255.0, x_test / 255.0

		#pre-fill our callEvent data to optimize callbacks, NB: optional
		jsonPixels = {}
		size = {'x':28, 'y':28}
		jsonPixels['size'] = size
		self.jsonPixels = jsonPixels
		self.x_train = x_train

		self.batch_size = 32
		self.epochs = 10

		tf.config.run_functions_eagerly(True)

		model = tf.keras.models.Sequential([
			tf.keras.layers.Flatten(input_shape=(28, 28)),
			tf.keras.layers.Dense(128, activation='relu'),
			tf.keras.layers.Dropout(0.2),
			tf.keras.layers.Dense(10)
		])

		predictions = model(x_train[:1]).numpy()

		loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
		loss_fn(y_train[:1], predictions).numpy()

		model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

		self.shouldStop = False #this should be changed when we stop unreal client
		self.stopcallback = self.StopCallback(self)

		model.fit(x_train, y_train, 
			epochs=self.epochs, 
			batch_size=self.batch_size,
			callbacks=[self.stopcallback])

		# Test trained model
		model.evaluate(x_test,  y_test, verbose=2)

		# Use a probability_model
		self.model = tf.keras.Sequential([
			model,
			tf.keras.layers.Softmax()
		])

		self.stored['summary'] = 'Trained for ' + str(self.epochs) + 'epochs.'
		return self.stored

#required function to get our api
def get_api():
	#return CLASSNAME.get_instance()
	return MnistSimple.get_instance()
