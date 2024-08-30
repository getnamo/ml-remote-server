#compatability script
import shared_globals as g
import asyncio


def run_on_sio(future):
	if future == None:
	 	pass

	asyncio.run_coroutine_threadsafe(future, g.sio_loop)


	# if g.sio_loop == None:
	#	pass

	#g.sio_loop.call_soon_threadsafe(lambda: await future)

	#if(asyncio.get_event_loop() != None):
		#asyncio.run_coroutine_threadsafe(future, g.sio.eio.event_loop)
		#asyncio.run_coroutine_threadsafe(future, future.get_loop())

def sio_future():
	#return g.sio_loop.create_future()
	return asyncio.get_event_loop().create_future()

def emit_wrapper(event, data):
	#asyncio.get_event_loop().call_soon_threadsafe(lambda:g.sio.emit(event, data))
	#g.sio_loop.call_soon_threadsafe(lambda:g.sio.emit(event, data))
	future = g.sio.emit(event, data)
	asyncio.run_coroutine_threadsafe(future, g.sio_loop)

#todo: fix events and emitting while in sync mode
def log(text):
	print('ue.log: ', text)

	if(g.sio != None):
		emit_wrapper('log', str(text))
		emit_wrapper('chatMessage', 'log:' + str(text))

def get_content_dir():
	return './unreal/content/'

def custom_event(event, data, use_json):
	if(g.sio != None):
		run_on_sio(g.sio.emit('customEvent', {'event':event, 'data':data, 'useJson': use_json}))

def set_sio_link(link_sio, link_app):
	print('link set')
	g.sio = link_sio
	g.app = link_app
	g.eio = g.sio.eio
	g.custom_event = custom_event

	print(g.eio)

	#store socket.io loop for callback scheduling, we can get it from calling thread
	g.sio_loop = asyncio.get_event_loop()

def set_loop_link():
	g.sio_loop = asyncio.get_event_loop()


# wrap around callbacks
def run_on_gt(callback, param=None):
	#called directly
	print("run_on_gt callback: " + str(param))
	if(callback != None):
		callback(param)