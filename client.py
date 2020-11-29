from clientlib import client_gui as cg
from share.log import noColors
from share import message

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
    soc = None # When the client its not connected its default value its Noneº

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
        variables.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        foo = cg.askForServer()

        try:
            serverInfo = foo.show()


        except Exception:
            variables.soc = None
            return

        functions.addOutput(noColors.createLog(f"Connecting to the server ({serverInfo['serveraddr']}, {serverInfo['serverport']})..."))
        try:
            variables.soc.connect((serverInfo["serveraddr"], serverInfo["serverport"]))
            variables.soc.send(bytes(dumps(message.createProfMsg(serverInfo["name"])), "utf-8"))
        except Exception as e:
            cg.errorWindow(f"An error has occurred while trying to connect to the server.\n{e}").show()
            variables.soc = None
            return

        variables.window.textBox.config(state="normal")
        variables.window.sendButton.config(state="normal")
        functions.addOutput(noColors.createLog("Connection stablished."))

        
    @staticmethod
    def disconnectFromServer(e=None):
        if variables.soc == None:
            functions.addOutput(noColors.createError("You need to be connected to a server to perform this action."))
            return
        
        variables.soc.close()
        variables.soc = None
        variables.window.textBox.config(state="disabled")
        variables.window.sendButton.config(state="disabled")
        functions.addOutput(noColors.createLog("Connection with the server closed."))
        


class functions:
    """
    This class contains all the miscellaneous functions that cannot fit in a description.
    """

    @staticmethod
    def addOutput(string):
        print(string)
        variables.window.chatOutput.yview_moveto(1)
        variables.window.chatOutput.insert("end","\n" + string)

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
                functions.addOutput(noColors.createWarn(f"The server has sent a message of an unknown type. ('{msg['type']}')"))


    @staticmethod
    def update(delay):
        """
        Refreshes the user list
        """
        while True:
            sleep(delay)
            variables.soc.send(bytes(dumps(message.createInfoRequest("userlist")),"utf-8"))


    @staticmethod
    def listener():
        while True:
            msg = variables.soc.recv(variables.bufferSize).decode()
            try:
                msg = loads(msg)
                core.recieveMessage(msg)
            
            except JSONDecodeError:
                print(3)
                functions.addOutput(noColors.createError("The server has sent an invalid type of message that cannot be decoded."))
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

    if variables.soc == None:
        functions.addOutput(noColors.createError("You are currently not connected to any server."))


    variables.window.show()
