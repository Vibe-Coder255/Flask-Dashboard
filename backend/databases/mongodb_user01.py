from pymongo import MongoClient
from pymongo.collection import Collection


MONGODB_URI = "mongodb://localhost:27017"
DATABASE_NAME = "flask_db"
COLLECTION_NAME = "user_01"


def get_user01_collection(client: MongoClient) -> Collection:
	"""Return the user_01 collection from the flask_db database."""
	return client[DATABASE_NAME][COLLECTION_NAME]


def connect_to_user01(timeout_ms: int = 2000) -> tuple[MongoClient, Collection]:
	"""Connect to MongoDB, verify the server, and return the user_01 collection."""
	client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=timeout_ms)
	try:
		client.admin.command("ping")
		return client, get_user01_collection(client)
	except Exception:
		client.close()
		raise
