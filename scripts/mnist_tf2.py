from mlpluginapi import MLPluginAPI
import unreal_engine as ue
import tensorflow as tf
import operator
import numpy as np

class EarlyStopCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
    	pass


#MLPluginAPI
class ExampleAPI(MLPluginAPI):

	#optional api: setup your model for training
	def on_setup(self):
		ue.log('Setup, load data set and prep model ')
		
		#NB: this works in tf 2.11, may be deprecated in the future
		ue.log(f"running tf version: {tf.__version__}")

		mnist = tf.keras.datasets.mnist

		(x_train, y_train), (x_test, y_test) = mnist.load_data()
		x_train, x_test = x_train / 255.0, x_test / 255.0

		#make these available to other class functions
		self.x_train = x_train
		self.y_train = y_train
		self.x_test = x_test
		self.y_test = y_test


		ue.log('setup sequential model...')
		model = tf.keras.models.Sequential([
		  tf.keras.layers.Flatten(input_shape=(28, 28)),
		  tf.keras.layers.Dense(128, activation='relu'),
		  tf.keras.layers.Dropout(0.2),
		  tf.keras.layers.Dense(10)
		])

		#define loss function
		loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

		#prep the model
		model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

		#make it available to class
		self.model = model
		self.is_training = False
		
		pass
		
	#optional api: parse input object and return a result object, which will be converted to json for UE4
	def on_json_input(self, input):
		ue.log('Running input via mnist prediction')

		probability_model = tf.keras.Sequential([
			self.model,
			tf.keras.layers.Softmax()
		])

		pixelarray = input['pixels']

		ue.log('image len: ' + str(len(pixelarray)))

		# ensure our array is properly sized before reshaping
		if len(pixelarray) != 784:
			return {'error':'wrong json shape sent'}

		reshaped = np.array(pixelarray).reshape(1, 28, 28)

		ue.log(f'shape json is {reshaped.shape}')
		ue.log(f'shape test is {self.x_test[:1].shape}')

		#run the mnist inference through the probability model
		result = probability_model(reshaped)

		#convert our raw result probability to a single max prediction
		index, value = max(enumerate(result), key=operator.itemgetter(1))

		ue.log('max: ' + str(value) + 'at: ' + str(index))

		return {'prediction':index}

	#optional api: start training your network
	def on_begin_training(self):
		ue.log('on_begin_training')

		#early exit, only train one at a time
		if self.is_training == True:
			ue.log('early exit')
			return {}

		#local var anything we use to train
		model = self.model
		x_train = self.x_train
		y_train = self.y_train
		x_test = self.x_test
		y_test = self.y_test

		early_stop = EarlyStopCallback()
		self.is_training = True

		#~5 epochs is sufficient to train mnist to 98%
		model.fit(x_train, y_train, epochs=1, callbacks=[early_stop]) #, callbacks=[early_stop])
		model.evaluate(x_test,  y_test, verbose=2)

		

		ue.log('training complete')
		pass
		#return {}

	def on_stop_training(self):
		ue.log('stopping training...')
		self.model.stop_training = True
		self.is_training = False

		return {}


#NOTE: this is a module function, not a class function. Change your CLASSNAME to reflect your class
#required function to get our api
def get_api():
	#return CLASSNAME.get_instance()
	return ExampleAPI.get_instance()