# ml-remote-server
Server complement of https://github.com/getnamo/machine-learning-remote-ue4.
Startup the server, point your ```MachineLearningRemote``` component to your server address with the script file name set in ```DefaultScript``` property and it will load on begin play.

## Quick Setup

1. Install [python 3](https://www.python.org/downloads/) recommended version for e.g. tensorflow: 3.7. Run ```pip install -r requirements.txt```
2. Pick a folder, navigate to it
3. ```git clone https://github.com/getnamo/ml-remote-server.git```
4. If you're on windows double click ```StartupServer.bat``` otherwise in terminal type ```python server.py``` to start the server.
5. Server is now ready to use. 

*Optional Steps*

6. Connect your UE4 instance via https://github.com/getnamo/machine-learning-remote-ue4
7. Listen to log events via your browser by going to ```<server ip>:8080``` or [```localhost:8080```](http://localhost:8080) in your browser. There are some debug commands like ```/r <script name>``` to swap script and ```/i``` to send dummy inputs; see https://github.com/getnamo/ml-remote-server/blob/master/server.py#L117 for all supported commands.

## How to use

### Startup event flow

*Begin Play -> (if connect on beginplay) connect to backend -> (if start script on connection) Default Script start*

Listen to the ```OnScriptStarted``` event to know it's safe to send inputs/start training.

### API

See https://github.com/getnamo/machine-learning-remote-ue4 as all interaction beyond debugging is handled by client.

Keep in mind that you can end play, do some code changes, and begin playing again without rebooting your server; the default script will be reloaded. You can also use the debug browser with ```/r <script name>``` or call ```StartScript``` from ```MachineLearningRemote``` component to live reload a script even during play.
