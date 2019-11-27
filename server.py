from aiohttp import web
import socketio
import sys

#active machine learning script handler
import mlplugin as mlp
import unreal_engine as ue

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

ue.set_sio_link(sio)


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
		return mlp.json_input(data['input'])
		
	elif data['targetFunction'] == 'onFloatArrayInput':
		return mlp.float_input(data['input'])

	#it's a custom function
	else:
		return mlp.custom_function(data['targetFunction'], data['input'])

@sio.on('startScript', namespace="/")
async def start_script(sid, script_name):
	print('loading <' + script_name + '>')
	#if script_name == same, reload the script (stop, wait for finish, reimport)
	valid, err = mlp.load(script_name)
	if (err):
		print(err)
	print('loaded.')
	valid, err = mlp.begin_play()
	if (err):
		print(err)
	print('started.')

@sio.on('stopScript', namespace="/")
async def stop_script(sid, script_name):
	#stop script with given name (name currently ignored)
	mlp.stop_training()
	pass

#stop training if currently being trained.
@sio.on('stopTraining', namespace="/")
async def stop_training(sid, script_name):
	mlp.stop_training()
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
		script_name = data[3:]

		if(script_name == ''):
			script_name = 'hello'

		await start_script(sid, script_name)
		await sio.emit('chatMessage', 'started script' + script_name)

	if data[0:2] == '/i':
		result = await send_input(sid, {'targetFunction':'onJsonInput','input':{'a':1,'b':2}})
		print(result)

	if data[0:2] == '/f':
		command_array = data[3:].split()
		function_name = command_array[0]
		param = {}

		if(len(command_array)>1):
			param = command_array[1]

		await send_input(sid, {'targetFunction':function_name,'input':param})

	print('chatMessage:' + content)
	await sio.emit('chatMessage', content)

#debug
@sio.on('echo', namespace="/")
async def test(sid, data):
	print("message << ", data)
	return {'echo':data}

if __name__ == '__main__':
	try:
		web.run_app(app)
	except KeyboardInterrupt:
		pass
	
	print('Exit.')