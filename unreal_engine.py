#compatability script
import shared_globals as g
import asyncio

#loop = asyncio.new_event_loop()
#asyncio.set_event_loop(loop)

def run_on_sio(future):
	asyncio.run_coroutine_threadsafe(future, g.sio_loop)

#todo: fix events and emitting while in sync mode
def log(text):
	print(text)
	if(g.sio != None):
		run_on_sio(g.sio.emit('chatMessage', 'log:' + str(text)))

def get_content_dir():
	return './unreal/content/'

def _custom_event(event, data, useJson):
	if(g.sio != None):
		run_on_sio(g.sio.emit('customEvent', {'event':event, 'data':data}))

def set_sio_link(link_sio, link_app):
	print('link set')
	g.sio = link_sio
	g.app = link_app
	g.custom_event = _custom_event

	#store socket.io loop
	g.sio_loop = asyncio.get_event_loop()

# wrap around callbacks
def run_on_gt(function, param):
	log('run_on_gt not needed or enabled for server')
	pass