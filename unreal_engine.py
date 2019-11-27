#compatability script
import shared_globals as g
import asyncio

#todo: fix events and emitting while in sync mode
def log(text):
	print(text)
	if(g.sio != None):
		asyncio.create_task(g.sio.emit('chatMessage', 'log:' + str(text)))
		#g.sio.emit('chatMessage', 'log:' + str(text))

def get_content_dir():
	return './unreal/content/'

def _custom_event(event, data, useJson):
	if(g.sio != None):
		asyncio.create_task(g.sio.emit('customEvent', {'event':event, 'data':data}))

def set_sio_link(link_sio, link_app):
	print('link set')
	g.sio = link_sio
	g.app = link_app
	g.custom_event = _custom_event