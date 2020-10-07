


# Messages types:
# Public message -> pubmsg



def createPublicMessage(authorId: str, message: str) -> dict:
	return {"type":"pubmsg", "author":authorId, "msg":message}




