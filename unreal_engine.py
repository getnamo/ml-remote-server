#compatability script
import shared_globals as g

#todo: re-route logging
def log(text):
	print(text)
	if(g.sio != None):
		g.sio.emit('chatMessage', 'log:' + str(text))
	else:
		print('nope')

def get_content_dir():
	return './unreal/content/'


def set_sio_link(new_sio):
	print('link set')
	g.sio = new_sio