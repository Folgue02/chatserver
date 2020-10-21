from clientlib import client_gui as cg
from threading import Thread


class variables:
    pass

def startup():
    """
    Its the first thing to be executed
    """



    cg.askForServer().window.mainloop()









startup()