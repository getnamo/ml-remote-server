import sys, os, getopt

#check for embedded startup
opts, args = getopt.getopt(sys.argv[1:],'p:e')

is_embedded = False

for opt, arg in opts:
	#print(opts)
	if(opt in ('-p')):
		sys.path.append(os.path.abspath(arg))
	if(opt in ('-e')):
		is_embedded = True

if(is_embedded):
	print('resolving embedded server dependencies... please wait (~3min)')
	sys.path.append(os.getcwd())
	import embedded_server_startup

#debug pre-server warmup
#raise 'Forced crash.'

from aiohttp import web
import socketio


#active machine learning script handler
import mlplugin as mlp
import unreal_engine as ue
import json

# create a Socket.IO server
sio = socketio.AsyncServer() #async_handlers=True

#serve a web client for command-like api (debug)
async def index(request):
	print('Static request:' + str(request))
	with open('webclient/index.html') as f:
		return web.Response(text=f.read(), content_type='text/html')

app = web.Application()
app.add_routes([web.get('/', index)])
sio.attach(app)

#linkup references for script callbacks via ue.log and ue.custom_event
ue.set_sio_link(sio, app)

inputFieldName = 'inputData'
functionFieldName = 'targetFunction'

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

	global inputFieldName
	global functionFieldName

	#handle callback and wrap around logs
	future = ue.sio_future()
	def callback_lambda(params):
		#print and emit logs
		print('sendInput return: ' + str(params))
		ue.log(params)
		future.set_result(params)

	#branch targeting for expected functions
	if data[functionFieldName] == 'on_json_input':
		#define a future so we can return the callback correctly

		inputData = data[inputFieldName]
		#json decode string if string passed (possible call not using sio object call)
		if type(inputData) is str:
			inputData = json.loads(inputData)

		mlp.json_input(inputData, callback_lambda)
		return await future
		
	elif data[functionFieldName] == 'on_float_array_input':
		mlp.float_input(data[inputFieldName], callback_lambda)
		return await future

	#it's a custom function
	else:
		mlp.custom_function(data[functionFieldName], data[inputFieldName], callback_lambda)
		return await future

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

	await sio.emit('scriptStarted', script_name) #todo: capture script errors
	await sio.emit('chatMessage', 'started script' + script_name)

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

	global inputFieldName
	global functionFieldName

	#debug commands
	if data[0:2] == '/s':
		print('Stop issued remotely by' + sid)
		exit(sid, None)

	if data[0:2] == '/r':
		script_name = data[3:]

		if(script_name == ''):
			script_name = 'hello'

		await start_script(sid, script_name)

	if data[0:2] == '/i':
		result = await send_input(sid, {functionFieldName:'onJsonInput',inputFieldName:{'a':1,'b':2}})
		print(result)

	if data[0:2] == '/f':
		command_array = data[3:].split()
		function_name = command_array[0]
		param = {}

		if(len(command_array)>1):
			param = command_array[1]

		await send_input(sid, {functionFieldName:function_name,inputFieldName:param})

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