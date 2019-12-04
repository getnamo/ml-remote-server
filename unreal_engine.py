#compatability script
import shared_globals as g
import asyncio

#loop = asyncio.new_event_loop()
#asyncio.set_event_loop(loop)

def run_on_sio(future):
	asyncio.run_coroutine_threadsafe(future, g.sio_loop)

def sio_future():
	return g.sio_loop.create_future()

#todo: fix events and emitting while in sync mode
def log(text):
	print(text)
	if(g.sio != None):
		run_on_sio(g.sio.emit('log', str(text)))
		run_on_sio(g.sio.emit('chatMessage', 'log:' + str(text)))

def get_content_dir():
	return './unreal/content/'

def custom_event(event, data, use_json):
	if(g.sio != None):
		run_on_sio(g.sio.emit('customEvent', {'event':event, 'data':data, 'useJson': use_json}))

def set_sio_link(link_sio, link_app):
	print('link set')
	g.sio = link_sio
	g.app = link_app
	g.custom_event = custom_event

	#store socket.io loop for callback scheduling, we can get it from calling thread
	g.sio_loop = asyncio.get_event_loop()

# wrap around callbacks
def run_on_gt(callback, param):
	#called directly
	print("run_on_gt callback: " + str(param))
	if(callback != None):
		callback(param)