from share import message, log
from json import dumps

def sendGlobalLogMessage(server, msg):
	"""
	Sends a message to all the users connected.
	"""
	for user in server.userList:
		server.userList[user]["userSocket"].send(bytes(dumps(message.createGlobalServerMessage(msg)), "utf-8"))






