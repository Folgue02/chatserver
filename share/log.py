# This file only contains three functions dedicated
# to embedding the way of showing messages


from colorama import init
from termcolor import colored
from datetime import datetime
init()

def _getFormattedDate():
	return datetime.now().strftime("%H:%M:%S")



def printLog(msg):
	print(colored(f"[{_getFormattedDate()} // LOG]: {msg}", "green"))

def printWarn(msg):
	print(colored(f"[{_getFormattedDate()} // WARN]: {msg}", "yellow"))

def printError(msg):
	print(colored(f"[{_getFormattedDate()} // ERROR]: {msg}", "red"))

class noColors:
	@staticmethod
	def _getFormattedDate():
		return datetime.now().strftime("%H:%M:%S")


	@staticmethod
	def createLog(msg):
		return f"[{noColors._getFormattedDate()} // LOG]: {msg}"


	@staticmethod
	def createWarn(msg):
		return f"[{noColors._getFormattedDate()} // WARN]: {msg}"


	@staticmethod
	def createError(msg):
		return f"[{noColors._getFormattedDate()} // ERROR]: {msg}"
