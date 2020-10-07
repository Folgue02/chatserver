import socket
from threading import Thread
from termcolor import colored
from colorama import init
init()
from json import dumps, loads
from share import message


config = loads(open("config.json", "r").read())


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", config["serverport"]))

def listen():
	msg = s.recv(2048).decode("utf-8")

	print(colored(msg, "green"))



def send():
	msg = dumps(message.createPublicMessage(1, input(">>")))
	print(msg)
	s.send(bytes(msg, "utf-8"))



Thread(target=listen, daemon=True).start()
send()
s.close()