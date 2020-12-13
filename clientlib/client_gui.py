import tkinter
from json import loads
from tkinter.font import Font
class window:
	def __init__(self):
		self.main = tkinter.Tk()
		self.main.title("Chat client")
		self.main.minsize(300,200)


		self.defaultStyle = {
			"userListbg":"#545454",
			"userListfg":"#ffffff",
			"chatOutputbg":"#696969",
			"chatOutputfg":"#ffffff",
			"textBoxbg":"#545454",
			"textBoxfg":"#ffffff",
			"sendButtonbg":"#706b6b",
			"sendButtonfg":"#ffffff",
			"upperSidebg":"#002869",
			"bottomSidebg":"#002869"
		}

		# Upper frame
		self.upperSide = tkinter.Frame(self.main)
		self.upperSide.pack(fill=tkinter.BOTH, expand=1)

		# Menu
		self.barMenu = tkinter.Menu(self.main)
		self.main.config(menu=self.barMenu)
		# This part its not initialized here, and will be initialized in the script that controls the gui


		# Bottom frame
		self.bottomSide = tkinter.Frame(self.main)
		self.bottomSide.pack(fill=tkinter.X, expand=False)


		# Elements of the upper frame
		self.userList = tkinter.Listbox(self.upperSide)
		self.userList.pack(fill=tkinter.Y, expand=False, side=tkinter.LEFT)

		self.chatOutput = tkinter.Text(self.upperSide)
		self.chatOutput.pack(side=tkinter.RIGHT, expand=True, fill=tkinter.BOTH)


		# Elements of the bottom frame
		self.textBox = tkinter.Entry(self.bottomSide)
		self.textBox.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)

		self.sendButton = tkinter.Button(self.bottomSide, text="Send")
		self.sendButton.pack(side=tkinter.RIGHT)


		# Change the colors of the widgets to the defaults
		self.changeStyle(self.defaultStyle)

	def show(self):
		self.main.mainloop()

	def changeStyle(self, newStyle: dict) -> None:
		"""
		Changes the appeareance of the client using a dictionary that contains the configuration
		"""
		self.textBox.config(bg=newStyle["textBoxbg"], fg=newStyle["textBoxfg"])
		self.sendButton.config(bg=newStyle["sendButtonbg"], fg=newStyle["sendButtonfg"])
		self.chatOutput.config(bg=newStyle["chatOutputbg"], fg=newStyle["chatOutputfg"])
		self.userList.config(bg=newStyle["userListbg"], fg=newStyle["userListfg"])
		self.upperSide.config(bg=newStyle["upperSidebg"])
		self.bottomSide.config(bg=newStyle["bottomSidebg"])





def errorWindow(errorMsg:str, windowTitle:str="Error!")-> None:
	window = tkinter.Toplevel()
	window.title(windowTitle)
	window.resizable(0,0)

	# Parse message
	foo = errorMsg
	foo1 = []
	for index, character in enumerate(errorMsg):
		if index % 60 == 0:
			foo1.append(index)
		
		else:
			continue
	
	i = 0
	for x in foo1:
		errorMsg = errorMsg[:x] + "\n" + errorMsg[x:]
		
	message = tkinter.Label(window, text=errorMsg)
	message.pack(anchor=tkinter.CENTER, pady=10)
	message.configure(font="helvetica")

	# Continue button
	button = tkinter.Button(window, text="Accept", command=lambda: window.destroy())
	button.pack(anchor=tkinter.CENTER, pady=10)
	button.configure(font=Font(size=15))



def askForServer(parent:tkinter.Tk) -> dict:

	window = tkinter.Toplevel()
	information = {}
	window.title = "Enter credentials for the joining a server."
	window.resizable(False, False)

		# Labels
	window.serverLabel = tkinter.Label(window, text="Server address")
	window.serverLabel.grid(column=0, row=0, padx=10, pady=5)
	
	window.portLabel = tkinter.Label(window, text="Server port")
	window.portLabel.grid(column=0, row=1, padx=10, pady=5)

	window.nameLabel = tkinter.Label(window, text="User name")
	window.nameLabel.grid(column=0, row=2, padx=10, pady=5)

	# Text fields
	window.server = tkinter.Entry(window)
	window.server.grid(column=1, row=0, padx=10, pady=5)

	window.port = tkinter.Entry(window)
	window.port.grid(column=1, row=1, padx=10, pady=5)

	window.name = tkinter.Entry(window)
	window.name.grid(column=1, row=2, padx=10, pady=5)


	def foo(event=None):
		information["serveraddr"], information["serverport"], information["userName"] = window.server.get(), window.port.get(), window.name.get()
		window.destroy()


	window.acceptButton = tkinter.Button(window, text="Join server.", command=foo)
	window.acceptButton.grid()


	parent.wait_window(window)

	information = information
	try:
		information["serverport"]  = int(information["serverport"])
	except Exception:
		errorWindow("The port of the server specified its invalid.")
		return None


	if len(information["userName"]) > 20:
		errorWindow("The name cannot be longer than 20 characters.")
		return None


	# If everything went right, this will destroy the root, and the show() function will continue and return the
	# information specified.
	window.destroy()

	return information




if __name__ == "__main__":
	w = window()
	w.main.mainloop()
