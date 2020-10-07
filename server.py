import socket
from threading import Thread
import os
from json import loads, dumps, JSONDecodeError
from share import log, message
import traceback


class globalVars:
	configFile = {}
	configTemplate = {"serveraddr":str, "serverport":int, "listenNo":int}
	userList = {}
	lastId = 0
	threads = {}
	msgSize = 2048




def startup():
	# Here there must the first instructions for the server that will 
	# be executed once its started.

	# Read a configuration from a configuration file.
	# In order to set a configuration for the server, it will search for a file with the name "config.json" and get the configuration from it
	# In case that file doesn't exist, or it's invalid, it will set a default configuration
	
	configFile = None
	if os.path.isfile("config.json"):
		log.printLog("Configuration file founded, reading configuration file...")
		try:
			foo = open("config.json", "r").read()
			foo = loads(foo)
			fooError = False

			# Check that the configuration file it's valid.
			for setting in globalVars.configTemplate:

				# In case that the setting it's not inside the configuration file.
				if not setting in foo:
					log.printError("The configuration file lacks one or more essential settings, setting a default configuration.")
					fooError = True
					break


				# In case that the setting it's invalid
				if type(foo[setting]) != globalVars.configTemplate[setting]:
					log.printError(f"One of the configuration file settings has an invalid type ({setting}'s type is {type(foo[setting])} and it should be {globalVars.configTemplate[setting]})")
					fooError = True
					break

			# If nothing went wrong.
			if not fooError:
				configFile = foo


		except JSONDecodeError:
			log.printError(f"The configuration file it's corrupted or it's invalid, setting a default configuration.")


	# In case that the configuration file wasn't found, or configFile stills being set to "None"
	if configFile == None or not os.path.isfile("config.json"):
		log.printWarn("Configuration file not found in the directory, or if it was found, it was invalid. Setting a default configuration.")

		configFile = {"serveraddr":"127.0.0.1", "serverport":25565, "listenNo":5}

	# Set the configuration
	globalVars.configFile = configFile
	log.printLog("Configuration loaded succesfully.")


	# Bind socket
	# In this part, the socket gets binded, if nothing goes wrong.
	# It gets binded with the configuration set before.

	log.printLog("Binding socket...")

	try: 
		globalVars.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		globalVars.soc.bind((globalVars.configFile["serveraddr"], globalVars.configFile["serverport"]))
		globalVars.soc.listen(globalVars.configFile["listenNo"])

	except Exception as e:
		log.printError(f"There was an error binding the socket.\nRaw error: ")
		traceback.print_exc()
		exit()

def handleUserInput(userId: int, userInput: dict):
	# This function decides what to do with the user's input
	# The user's input MUST be parsed into a dictionary when its specified.

	# If the message doesn't contain a "type" key, the handler cannot know what to do with the rest of the message.
	if not "type" in userInput:
		log.printError(f"The user's ({userId}) input doesn't specify what type of message it is, therefore nothing can be do with it.")
		return

	msgType = userInput["type"]

	# Public message type
	if msgType == "pubmsg":
		# A public message gets sent to all users connected to the server.
		
		targetMsg = dumps(message.createPublicMessage(userId, userInput["msg"]))
		for user in globalVars.userList:
			globalVars.userList[user]["userSocket"].send(bytes(targetMsg, "utf-8"))

		return





def listener():
	# Accepts the incoming connections and creates a user key in the
	# userList dictionary, and starts a thread for it.

	while True:
		c,a = globalVars.soc.accept()
		# Create a new id for the new user.
		globalVars.lastId += 1
		newId = globalVars.lastId

		globalVars.userList[newId] = {"name":newId, "userSocket":c}
		# The name its by default assigned to the id.

		# Create the dedicated thread for the user.
		globalVars.threads[newId] = Thread(target=dedicatedThread, args=[newId], daemon=True)
		globalVars.threads[newId].start()
		log.printLog(f"Dedicated thread for user '{newId}' has been started.")



def dedicatedThread(userId: int) -> None:
	# This is a function that gets executed in a thread for a user,
	# its purpose its to listen to the user and to deal with his input.
	userSoc = globalVars.userList[userId]["userSocket"]
	
	# Loop
	while True:
		try:
			userMsg = userSoc.recv(globalVars.msgSize).decode("utf-8")

			try:
				userMsg = loads(userMsg)

			except JSONDecodeError:
				log.printError(f"The user '{userId}' just sent an invalid message (cannot be parsed into a dictionary).")
				del globalVars.userList[userId]
				del globalVars.threads[userId]
				log.printLog(f"User with id '{userId}' just sent an invalid message and got kicked out.")
				c.close()
				return
				# Kick the user from the server or ignore this message.

			handleUserInput(userId, userMsg)

		except Exception as e:
			log.printError(f"Something happened with the thread of user '{userId}'. \nRaw error:")
			traceback.print_exc()
			return



			



if __name__ == "__main__":
	# Execute the initialization function.
	startup()
	log.printLog(f"Starting server with the following configuration... {globalVars.configFile}")
	listener()