import os
from sys import argv as arg


commands = {
    "help":"Prints this message.",
    "runtest=n":"Runs a debugging test launching one server window, and n client windows.",
    "server":"Launches the server.",
    "testclient":"Launches a clienttest.py script, if its equal to N it will open as many as specified.",
    "client":"Launches an embedded client window, if it equals to N it will open as many as specified."
}



# Im going to rush this code, i want to be done with this part of the project asap since its really irrelevant

if "help" in arg:
    for command in commands:
        print("·" + command)
        print("\t"+ commands[command])
    exit()

for command in arg:

    if command.startswith("runtest"):
        if command.startswith("runtest=") and len(command) > len("runtest="):
            foo = command[len("runtest="):]

            try:
                foo = int(foo)
            except Exception:
                print(f"The N specified its not valid. ({foo})")
                continue
            
            os.system("start python -i server.py")
            for x in range(foo):
                os.system("start python clienttest.py")

            continue

        else:
            os.system("start python -i server.py")
            os.system("start python clienttest.py")
            os.system("start python clienttest.py")
            continue

    if command == "server":
        os.system("start python -i server.py")
        continue


    if command.startswith("client"):
        if command.startswith("client=") and len(command) > len("client="):
            foo = command[len("client="):]
            print(command[len("client="):])

            try:
                foo = int(foo)
            except Exception:
                print(f"The N specified its not valid. ({foo})")
            
            for x in range(foo):
                os.system("start python client.pyw")
                continue

            continue

        else:
            os.system("start python client.pyw")
            continue



    if command.startswith("testclient"):
        if command.startswith("testclient=") and len(command) > len("testclient="):
            foo = command[len("testclient="):]
            print(command[len("testclient="):])

            try:
                foo = int(foo)
            except Exception:
                print(f"The N specified its not valid. ({foo})")
            
            for x in range(foo):
                os.system("start python clienttest.py")
                continue

            continue

        else:
            os.system("start python clienttest.py")
            continue

        
