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
    def listWorker():
        """
        Refreshes the user list
        """
        while True:
            sleep(5)
            variables.soc.send(bytes(dumps(message.createInfoRequest("userlist")),"utf-8"))


    @staticmethod
    def listener():
        while True:
            msg = variables.soc.recv(variables.bufferSize).decode()
            try:
                msg = loads(msg)
                functions.recieveMessage(msg)
            
            except JSONDecodeError:
                print(3)
                functions.addOutput(noColors.createError("The server has sent an invalid type of message that cannot be decoded."))
                print(msg)
                continue

    @staticmethod
    def sender(event=None):
        # Simplified

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
    # Create the socket
    variables.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        
        foo = cg.askForServer()
        serverInfo = foo.show()
        

        variables.serverAddr =  serverInfo["serveraddr"]
        variables.serverPort =  serverInfo["serverport"]
        try:
            variables.soc.connect((variables.serverAddr, variables.serverPort))
            variables.soc.send(bytes(dumps(message.createProfMsg(serverInfo["name"])), "utf-8"))
            break
        except Exception as e:
            cg.errorWindow(f"An error has occurred while trying to connect to the server.\n{e}").show()
            continue
    

    variables.window = cg.window()


    # Start the threads
    variables.listener = Thread(target=functions.listener, daemon=True)
    variables.listener.start()
    variables.listWorker = Thread(target=functions.listWorker, daemon=True)
    variables.listWorker.start()

    # bind textbox to the function
    variables.window.textBox.bind("<Return>", func=functions.sender)
    variables.window.sendButton.config(command=functions.sender)
    variables.window.show()
