import unreal_engine as ue
from threading import Thread
import asyncio

#internal, don't call directly
def backgroundAction(args=None):
	#ue.log(args)
	
	action = args[0]
	actionArgs = None

	if len(args) >1:
		actionArgs = args[1]

	if len(args) >2:
		callback = args[2]

	#call the blocking action
	if actionArgs:
		result = action(actionArgs)
	else:
		result = action()

	#return the result if we have a callback
	if callback:
		if result:
			ue.run_on_gt(callback, result)
		else:
			ue.run_on_gt(callback)

#run function on a background thread, optional callback when complete on game thread
def run_on_bt(actionfunction, functionArgs=None, callback=None):
	t = Thread(target=backgroundAction, args=([actionfunction, functionArgs, callback],))
	t.start()