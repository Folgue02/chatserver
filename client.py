from clientlib import client_gui as cg
from share.log import noColors
from share import message

import tkinter
from threading import Thread
import socket
from json import loads, dumps, JSONDecodeError
import os
from sys import argv
from time import sleep


class variables:
	serverAddr = "localhost"
	serverPort = 25565
	DEBUG = False
	users = {}
	bufferSize = 512000
	lastOrder = None
	soc = None # When the client its not connected its default value its None
	listenerThread = None
	updaterThread = None

class inputRelatedFunctions:
	@staticmethod
	def iterateOrdersUp(event):
		# Changes the content of the textBox to what was the last message sent
		# There isn't a last order
		if variables.lastOrder == "" or variables.lastOrder == None:
			return
		# Removes what's in the box and inserts what was the last thing written in the box and sent
		variables.window.textBox.delete(0, "end")
		variables.window.textBox.insert(0, variables.lastOrder)    

	@staticmethod
	def sender(event=None):

		# Get the text from the textbox and clear it
		msg = variables.window.textBox.get().strip()
		variables.window.textBox.delete(0, "end")

		variables.lastOrder = msg

		# In case that its a command
		if msg.startswith("/"):
			command = ""
			pars = []
			foo = ""
			quoteStatus = False


			msg += " "
			
			for char in msg[1:]:
				if char == " " and not quoteStatus:
					# If the command haven't been recognized yet
					if command == "":
						command = foo
						foo = ""
						continue

					else:
						pars.append(foo)
						foo = ""
						continue

				if char == "\"" or char == "'":
					quoteStatus = not quoteStatus
					continue

				else:
					foo += char

			variables.soc.send(bytes(dumps(message.createCommandMessage(command, pars)), "utf-8"))
			return

		variables.soc.send(bytes(dumps(message.createPublicMessage(msg)), "utf-8"))

class menuFuncs:
	@staticmethod
	def connectToServer(e=None):
		if variables.soc != None:
			cg.errorWindow("You need to close the connection to the current server in order to establish a new one.")
			return
		
		variables.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


		try:
			serverInfo = cg.askForServer(variables.window.main)

		except Exception as e:
			functions.addOutput(noColors.createError("The pop up window to connect the server has failed or has been closed." + str(e)))
			variables.soc = None
			return

		functions.addOutput(noColors.createLog(f"Connecting to the server ({serverInfo['serveraddr']}, {serverInfo['serverport']})..."))
		try:
			variables.soc.connect((serverInfo["serveraddr"], serverInfo["serverport"]))
			variables.soc.send(bytes(dumps(message.createProfMsg(serverInfo["userName"])), "utf-8"))
		except Exception as e:
			cg.errorWindow(f"An error has occurred while trying to connect to the server.\n{e}")
			variables.soc = None
			return


        # Change widgets
		variables.window.textBox.config(state="normal")
		variables.window.sendButton.config(state="normal")
		
        # Start the threads
		variables.listenerThread = Thread(target=core.listener, daemon=False)
		variables.updaterThread = Thread(target=core.update, daemon=False, args=[2])
		variables.listenerThread.start()
		variables.updaterThread.start()

		functions.addOutput(noColors.createLog("Connection established."))

		
	@staticmethod
	def disconnectFromServer(e=None):
		if variables.soc == None:
			functions.addOutput(noColors.createError("You need to be connected to a server to perform this action."))
			return
		
		# Close the socket
		variables.soc.close()
		variables.soc = None
		
		# Widgets
		variables.window.textBox.config(state="disabled")
		variables.window.sendButton.config(state="disabled")
		functions.addOutput(noColors.createLog("Connection with the server closed."))
		
		# Get rid of the threads
		variables.listenerThread = None
		variables.updaterThread = None
		

	@staticmethod
	def clearChat():
		variables.window.chatOutput.delete(0.0, "end")



class functions:
	"""
	This class contains all the miscellaneous functions that cannot fit in a description.
	"""

	@staticmethod
	def addOutput(string):
		print(string)
		variables.window.chatOutput.yview_moveto(1)
		variables.window.chatOutput.insert("end", string + "\n")

	@staticmethod
	def on_closing():
		if variables.soc != None:
			menuFuncs.disconnectFromServer()

		variables.window.main.destroy()

class core:
	@staticmethod
	def recieveMessage(msg: dict):
		if not "type" in msg:
			functions.addOutput(noColors.createError("The server's message cannot be identified because it doesn't specify the type."))
			if variables.DEBUG:
				functions.addOutput(noColors.createError(dumps(msg, indent=2)))

			return
		
		else:
			if msg["type"] == "userlist":
				variables.window.userList.delete(0, "end")
				variables.users = msg["users"]
				for user in msg["users"]:
					variables.window.userList.insert("end", str(msg["users"][user])  + "#" + str(user))


			
			elif msg["type"] == "pubmsg":
				functions.addOutput(f"[{noColors._getFormattedDate()} // {msg['authorName']}#{msg['authorId']}]: {msg['msg']}")

			elif msg["type"] == "servermsg":
				functions.addOutput(f"[{noColors._getFormattedDate()} // SERVER]: {msg['msg']}")

			elif msg["type"] == "servererror":
				functions.addOutput(f"[{noColors._getFormattedDate()} // SERVER ERROR]: {msg['msg']}")
			
			elif msg["type"] == "privmsg":
				functions.addOutput(f"[{noColors._getFormattedDate()} // PRIVATE MESSAGE FROM {msg['authorName']}#{msg['authorId']}]: {msg['msg']}")

			else:
				functions.addOutput(noColors.createWarn(f"The server has sent a message of an unknown type. '{msg['type']}'"))


	@staticmethod
	def update(delay):
		"""
		Refreshes the user list
		"""
		while variables.soc != None:
			sleep(delay)
			try:
				variables.soc.send(bytes(dumps(message.createInfoRequest("userlist")),"utf-8"))
			except AttributeError as e:
				if variables.soc != None:
					functions.addOutput(noColors.createError(f"An error has occurred in the update thread, '{e}'"))
					return None
				
				return None

	@staticmethod
	def listener():
		while variables.soc != None:
			
			# When the server its closed, the function cannot know be stopped, so it will trigger an error
			try:
				msg = variables.soc.recv(variables.bufferSize).decode()
			except ConnectionAbortedError as e:
				if variables.soc != None:
					functions.addOutput(noColors.createError(f"An error has occurred in the listener thread, '{e}'"))
					return None
				
				return None

			try:

				msg = loads(msg)
				core.recieveMessage(msg)
			
			except JSONDecodeError:
				print(3)
				functions.addOutput(noColors.createError("The server has sent an unintelligible message which cannot be decoded."))
				print(msg)
				continue

	@staticmethod
	def sender(event=None):

		# Get the text from the textbox and clear it
		msg = variables.window.textBox.get().strip()
		variables.window.textBox.delete(0, "end")

		# In case that its a command
		if msg.startswith("/"):
			command = ""
			pars = []
			foo = ""
			quoteStatus = False


			msg += " "
			
			for char in msg[1:]:
				if char == " " and not quoteStatus:
					# If the command haven't been recognized yet
					if command == "":
						command = foo
						foo = ""
						continue

					else:
						pars.append(foo)
						foo = ""
						continue

				if char == "\"" or char == "'":
					quoteStatus = not quoteStatus
					continue

				else:
					foo += char

			variables.soc.send(bytes(dumps(message.createCommandMessage(command, pars)), "utf-8"))
			return



		
		variables.soc.send(bytes(dumps(message.createPublicMessage(msg)), "utf-8"))


if __name__ == "__main__":
	variables.window = cg.window()
	# bind textbox to the function
	variables.window.textBox.bind("<Return>", func=inputRelatedFunctions.sender)
	variables.window.textBox.bind("<Shift-Up>", func=inputRelatedFunctions.iterateOrdersUp)
	variables.window.sendButton.config(command=inputRelatedFunctions.sender)
	variables.window.textBox.config(state="disabled")
	variables.window.sendButton.config(state="disabled")

	# Add the menu bar
	variables.connectionMenu = tkinter.Menu(variables.window.barMenu, tearoff=0)
	variables.miscellaneousMenu = tkinter.Menu(variables.window.barMenu, tearoff=0)


	# connectionMenu
	variables.window.barMenu.add_cascade(label="Connection", menu=variables.connectionMenu)
	variables.connectionMenu.add_command(label="Connect to a server", command=menuFuncs.connectToServer)
	variables.connectionMenu.add_command(label="Disconnect from server", command=menuFuncs.disconnectFromServer)

	# miscellaneousMenu
	variables.window.barMenu.add_cascade(label="Miscellaneous", menu=variables.miscellaneousMenu)
	variables.miscellaneousMenu.add_command(label="Clear chat", command=menuFuncs.clearChat)




	if variables.soc == None:
		functions.addOutput(noColors.createError("You are currently not connected to any server."))

	variables.window.main.wm_protocol("WM_DELETE_WINDOW", functions.on_closing)
	variables.window.show()
