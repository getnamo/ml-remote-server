from aiohttp import web
import socketio
import sys

#active machine learning script handler
import mlplugin as mlp

# create a Socket.IO server
sio = socketio.AsyncServer()


#serve a web client for command-like api (debug)
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
async def send_input(sid, data):
	print('sendInput: ' + str(data))

	#branch targeting for expected functions
	if data['targetFunction'] == 'onJsonInput':
		return mlp.json_input(data['data'])
		
	elif data['targetFunction'] == 'onFloatArrayInput':
		return mlp.float_input(data['data'])

	#it's a custom function
	else:
		return mlp.custom_function(data)

@sio.on('startScript', namespace="/")
async def start_script(sid, script_name):
	#if script_name == same, reload the script (stop, wait for finish, reimport)
	mlp.load(script_name)
	mlp.start()
	pass

@sio.on('stopScript', namespace="/")
async def stop_script(sid, script_name):
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

	#debug commands
	if data[0:2] == '/s':
		print('Stop issued remotely by' + sid)
		exit(sid, None)

	if data[0:2] == '/r':
		script_name = 'hello'
		await start_script(sid, script_name)
		await sio.emit('chatMessage', 'started script' + script_name)

	if data[0:2] == '/i':
		await send_input(sid, {'targetFunction':'onJsonInput','data':{'hi':'there'}})

	print('chatMessage:' + content)
	await sio.emit('chatMessage', content)

#debug
@sio.on('echo', namespace="/")
async def test(sid, data):
	print("message << ", data)
	return {'echo':data}

if __name__ == '__main__':
	web.run_app(app)
	print('Exit.')


