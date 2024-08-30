import unreal_engine as ue
from threading import Thread
import asyncio

# Potential upgrade
# import threading
# import queue

# class ThreadUtility:
#     def __init__(self):
#         self.threads = {}
#         self.queues = {}
#         self.lock = threading.Lock()

#     def _process_messages(self, thread_id):
#         while True:
#             try:
#                 message = self.queues[thread_id].get(timeout=1)
#                 self.handle_message(message)
#                 self.queues[thread_id].task_done()
#             except queue.Empty:
#                 continue

#     def handle_message(self, message):
#         """
#         Override this method in a subclass to define custom message handling.
#         """
#         print(f"Processing message: {message}")

#     def send_message(self, thread_id, message):
#         with self.lock:
#             if thread_id not in self.queues:
#                 # If thread with thread_id doesn't exist, create a new thread and queue
#                 self.queues[thread_id] = queue.Queue()
#                 thread = threading.Thread(target=self._process_messages, args=(thread_id,))
#                 self.threads[thread_id] = thread
#                 thread.start()

#             # Enqueue the message to the appropriate queue
#             self.queues[thread_id].put(message)

#     def stop_thread(self, thread_id):
#         if thread_id in self.threads:
#             self.threads[thread_id].join()
#             del self.threads[thread_id]
#             del self.queues[thread_id]

#     def stop_all_threads(self):
#         for thread_id in list(self.threads.keys()):
#             self.stop_thread(thread_id)

# # Modify the run_on_bt function
# def run_on_bt(actionfunction, functionArgs=None, callback=None, thread_id=None):
#     utility = ThreadUtility()

#     # Create a wrapper to run the action function and optionally the callback
#     def wrapper():
#         result = actionfunction(*functionArgs) if functionArgs else actionfunction()
#         if callback:
#             callback(result)

#     if thread_id:
#         # If thread_id is provided, send the wrapper function to the appropriate thread
#         utility.send_message(thread_id, wrapper)
#     else:
#         # If no thread_id is provided, just run the action function
#         wrapper()



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
		if result!=None:
			ue.run_on_gt(callback, result)
		else:
			ue.run_on_gt(callback)

#run function on a background thread, optional callback when complete on game thread
def run_on_bt(actionfunction, functionArgs=None, callback=None):
	t = Thread(target=backgroundAction, args=([actionfunction, functionArgs, callback],))
	t.start()



