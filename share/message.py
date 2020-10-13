


# Messages types:
# Public message -> pubmsg
# Server messages -> servermsg


def createServerPublicMessage(authorId: str, message: str) -> dict:
	return {"type":"pubmsg", "author":authorId, "msg":message}

def createPublicMessage(msg: str) -> dict:
	return {"type":"pubmsg", "msg":msg}


def createGlobalServerMessage(msg: str) -> dict:
	return {"type":"servermsg", "msg":msg}

