from clientlib import client_gui as c
from time import sleep


e = c.askForServer()

print("1")
print(e.show())
sleep(1)
print("2")
sleep(1)
print(e.show())
sleep(1)
print("3")