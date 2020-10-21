


# Messages types:
# Public message -> pubmsg
# Server messages -> servermsg


def createServerPublicMessage(authorId: str, authorName: str, message: str) -> dict:
	return {"type":"pubmsg", "authorId":authorId, "authorName":authorName, "msg":message}



def createPublicMessage(msg: str) -> dict:
	return {"type":"pubmsg", "msg":msg}


def createGlobalServerMessage(msg: str) -> dict:
	return {"type":"servermsg", "msg":msg}

