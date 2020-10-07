from threading import Thread
from time import sleep


def test():

	i = 0

	while True:
		i += 1
		print("This is the number of the cycle: " + str(i))
		sleep(3)

threads = []


threads.append(Thread(target=test, daemon=True))

threads[0].start()
sleep(6)
del threads[0]
print("The thread has been eliminated.")

while True:
	print("I still alive!")
	sleep(1)




