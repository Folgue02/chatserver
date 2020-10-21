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






class functions:
    """
    This class contains all the miscellaneous functions that cannot fit in a description.
    """

    @staticmethod
    def addOutput(string):
        print(string)
        variables.window.chatOutput.yview_moveto(1)
        variables.window.chatOutput.insert("end","\n" + string)


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
            msg = variables.soc.recv(1024).decode()
            try:
                msg = loads(msg)
                functions.recieveMessage(msg)
            
            except JSONDecodeError:
                print(3)
                functions.addOutput(noColors.createError("The server has sent an invalid type of message that cannot be decoded."))
                continue

    @staticmethod
    def sender(event=None):
        # Simplified
        msg = variables.window.textBox.get()
        variables.window.textBox.delete(0, "end")
        variables.soc.send(bytes(dumps(message.createPublicMessage(msg)), "utf-8"))
        print("Message sent: " + msg)


if __name__ == "__main__":
    # Create the socket
    variables.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        
        foo = cg.askForServer()
        serverInfo = foo.show()
        

        variables.serverAddr =  serverInfo["serveraddr"]
        variables.serverPort =  serverInfo["serverport"]
        try:
            variables.soc.connect((variables.serverAddr, variables.serverPort))
            break
        except Exception:
            cg.errorWindow("An error has occurred while trying to connect to the server.").show()
            continue
    

    variables.window = cg.window()


    # Start the threads
    variables.listener = Thread(target=functions.listener, daemon=True)
    variables.listener.start()

    # bind textbox to the function
    variables.window.textBox.bind("<Return>", func=functions.sender)
    variables.window.sendButton.config(command=functions.sender)
    variables.window.show()
