from clientlib import client_gui as c
from time import sleep


msg = input()
command = ""
pars = []
foo = ""
quoteStatus = False
msg += " "

for char in msg[1:]:

    # Item transiction
    if char == " " and not quoteStatus:
        print("test")
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

print(command, pars)