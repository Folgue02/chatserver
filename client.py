from clientlib import client_gui as cg
from threading import Thread
import socket
from json import loads, dumps, JSONDecodeError
import os
from sys import argv
from share.log import noColors
from time import sleep

class variables:
    serverAddr = "localhost"
    serverPort = 25565
    DEBUG = False
    users = {}






class functions:
    """
    This class contains all the miscellaneous functions that cannot fit in a description.
    """

    @staticmethod
    def addOutput(string):
        variables.mainWindow.chatOutput.yview_moveto(1)
        variables.mainWindow.chatOutput.insert(0,"\n" + string)



    @staticmethod
    def recieveMessage(msg: dict):
        if not "type" in msg:
            functions.addOutput(noColors.createError("The server's message cannot be identified because it doesn't specify the type."))
            if variables.DEBUG:
                functions.addOutput(noColors.createError(dumps(msg, indent=2)))

            return
        
        else:
            if msg["type"] == "pubmsg":
                functions.addOutput(f"[{noColors._getFormattedDate()} // {msg['authorName']}@{msg['authorId']}]: {msg['msg']}")
                return

            elif msg["type"] == "servermsg":
                functions.addOutput(f"[{noColors._getFormattedDate()} // SERVER]: {msg['msg']}")
                return

            else:
                functions.addOutput(noColors.createWarn(f"The server has sent a message of an unknown type. ('{msg['type']}')"))



    @staticmethod
    def listener():
        while True:
            msg = variables.soc.recv(5000)

            try:
                msg = loads(msg)
            
            except JSONDecodeError:
                functions.addOutput(noColors.createError("The server has sent an invalid type of message that cannot be decoded."))
                continue



                
def startup():
    """
    This is the first thing to be executed
    """
    # Check if debug mode its activated
    if "debug" in argv:
        variables.DEBUG = True

    serverInfo = {"serveraddr":"127.0.0.1", "serverport":25565}

    # Create the mainwindow of the client
    variables.mainWindow = cg.window()
    print("sd")

    variables.mainWindow.show()
    print("sd")
    # Create the socket
    variables.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Ask for the server
    while True:
        """
        foo = cg.askForServer()
        serverInfo = foo.show()
        """

        variables.serverAddr =  serverInfo["serveraddr"]
        variables.serverPort =  serverInfo["serverport"]
        try:
            variables.soc.connect((variables.serverAddr, variables.serverPort))
            break
        except Exception:
            cg.errorWindow("An error has occurred while trying to connect to the server.").show()
            continue

    variables.listener = Thread(target=functions.listener, daemon=True)
    variables.listener.start()

    







startup()