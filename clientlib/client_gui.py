import tkinter
from json import loads
from tkinter.font import Font
class window:
    def __init__(self):
        self.main = tkinter.Tk()
        self.main.title("Chat client")


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




class errorWindow:
    def __init__(self,  errorMsg:str ,windowTitle:str="Error!"):
        self.window = tkinter.Tk()
        self.window.title(windowTitle)
        self.window.minsize(300, 100)
        self.window.resizable(0,0)

        self.message = tkinter.Label(self.window, text=errorMsg)
        self.message.pack(anchor=tkinter.CENTER, pady=10)
        self.message.configure(font="helvetica")

        # Continue button
        self.button = tkinter.Button(self.window, text="Accept", command=lambda: self.window.destroy())
        self.button.pack(anchor=tkinter.CENTER, pady=10)
        self.button.configure(font=Font(size=15))


    def show(self):
        self.window.mainloop()





class askForServer:
    def __init__(self):
        self._information = {}
        self.root = tkinter.Tk()
        self.root.title("Enter credentials for the joining a server.")
        self.root.resizable(False, False)

        # Labels
        self.serverLabel = tkinter.Label(self.root, text="Server address")
        self.serverLabel.grid(column=0, row=0, padx=10, pady=5)
        
        self.portLabel = tkinter.Label(self.root, text="Server port")
        self.portLabel.grid(column=0, row=1, padx=10, pady=5)

        self.nameLabel = tkinter.Label(self.root, text="User name")
        self.nameLabel.grid(column=0, row=2, padx=10, pady=5)

        # Text fields
        self.server = tkinter.Entry(self.root)
        self.server.grid(column=1, row=0, padx=10, pady=5)

        self.port = tkinter.Entry(self.root)
        self.port.grid(column=1, row=1, padx=10, pady=5)

        self.name = tkinter.Entry(self.root)
        self.name.grid(column=1, row=2, padx=10, pady=5)


        self.acceptButton = tkinter.Button(self.root, text="Join server.", command=self._return)
        self.acceptButton.grid()


    def show(self) -> dict:
        self.root.mainloop()
        return self._information

    def _return(self):

        information = {"serveraddr":"", "serverport":0, "userName":""}

        # serveraddr
        information["serveraddr"] = self.server.get()

        # serverport
        information["serverport"] = self.port.get()

        try:
            information["serverport"]  = int(information["serverport"])
        except Exception:
            errorWindow("The port of the server specified its invalid.").show()
            return None

        # username
        information["name"] = self.name.get()

        if len(information["name"]) > 20:
            errorWindow("The name cannot be longer than 20 characters.").show()
            return None


        # If everything went right, this will destroy the root, and the show() function will continue and return the
        # information specified.
        self.root.destroy()
        self._information = information





if __name__ == "__main__":
    w = window()
    w.main.mainloop()