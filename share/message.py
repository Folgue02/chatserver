


# Messages types:
# Public message -> pubmsg

# # Special messages from client
# Command message -> command
# Private message -> privmsg
# Request from client -> request
# Profile -> profmsg

# # Server messages
# user list -> userlist
# Server messages -> servermsg



def createServerPublicMessage(authorId: str, authorName: str, message: str) -> dict:
	return {"type":"pubmsg", "authorId":authorId, "authorName":authorName, "msg":message}

def createCommandMessage(command: str, parameters: list) -> dict:
	return {"type":"command", "command":command, "parameters":parameters}


def createServerErrorResponse(msg: str) -> dict:
	return {"type":"servererror", "msg":msg}

def createUserlistResponse(userList: dict) -> dict:
	foo =  {}
	for user in userList:
		foo[user] = userList[user]["name"]
	return {"type":"userlist", "users":foo}

def createPublicMessage(msg: str) -> dict:
	return {"type":"pubmsg", "msg":msg}

def createPrivateMessage(msg: str, userId: int, authorName):
	return {"type":"privmsg", "msg":msg, "authorId":userId, "authorName":authorName}


def createInfoRequest(target: str) -> dict:
	return {"type":"request", "target":target}


def createGlobalServerMessage(msg: str) -> dict:
	return {"type":"servermsg", "msg":msg}

def createProfMsg(username: str)->dict:
	return {"type":"profmsg", "name":username}