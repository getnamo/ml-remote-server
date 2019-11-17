from aiohttp import web
import socketio
import sys

import mlpluginapi
import imp
#import importlib

# create a Socket.IO server
sio = socketio.AsyncServer()

#serve a web client for command-like api
async def index(request):
	print('Static request:' + str(request))
	with open('webclient/index.html') as f:
		return web.Response(text=f.read(), content_type='text/html')

app = web.Application()
app.add_routes([web.get('/', index)])
sio.attach(app)

#connect/disconnect etc
@sio.on('connect', namespace="/")
async def connect(sid, data):
	print( "connect ", sid)
	await sio.emit('chatMessage', str(sid)[0:4] + ' connected.')

@sio.on('disconnect', namespace="/")
async def disconnect(sid):
	print('disconnect', sid)
	await sio.emit('chatMessage', str(sid)[0:4] + ' disconnected.')

#main methods
@sio.on('sendInput', namespace="/")
async def sendInput(sid, data):

	#branch targeting for expected functions
	if data.targetFunction == 'onJsonInput':
		pass
	elif data.targetFunction == 'onFloatArrayInput':
		pass

	#it's a custom function
	else:
		pass


	print("message << ", data)
	return data

@sio.on('startScript', namespace="/")
async def startScript(sid, script_name):
	#if script_name == same, reload the script (stop, wait for finish, reimport)

	#todo: reload our script using imp
	pass

@sio.on('stopScript', namespace="/")
async def stopScript(sid, script_name):
	#stop script with given name
	pass

@sio.on('stopServer', namespace="/")
def exit(sid, data):
	print("server exit due to remote request")
	sys.exit()

#Web client messaging, useful for diagnostics and basic commands
@sio.on('chatMessage', namespace="/")
async def chat(sid, data):
	content = str(sid)[0:4] + ':' + data

	if data[0:2] == '/s':
		print('Stop issued remotely by' + sid)
		exit(sid, None)

	print(content)
	await sio.emit('chatMessage', content)

#debug
@sio.on('echo', namespace="/")
async def test(sid, data):
	print("message << ", data)
	return {'echo':data}

if __name__ == '__main__':
	web.run_app(app)
	print('Exit.')