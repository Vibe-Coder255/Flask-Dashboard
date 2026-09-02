from datetime import datetime, timezone
from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection


MONGODB_URI = "mongodb://localhost:27017"
DATABASE_NAME = "flask_db"
COLLECTION_NAME = "test_db"


def get_test_collection(client: MongoClient) -> Collection:
	"""Return the collection used for MongoDB connectivity check logs."""
	return client[DATABASE_NAME][COLLECTION_NAME]


def check_mongodb_connection(timeout_ms: int = 2000) -> dict[str, Any]:
	"""Ping MongoDB and record the request/response in the test collection."""
	client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=timeout_ms)
	collection = get_test_collection(client)
	checked_at = datetime.now(timezone.utc)

	try:
		response = client.admin.command("ping")
		log = {
			"checked_at": checked_at,
			"request": {"command": "ping", "database": DATABASE_NAME},
			"response": response,
			"status": "success",
		}
		collection.insert_one(log)
		return log
	except Exception as error:
		log = {
			"checked_at": checked_at,
			"request": {"command": "ping", "database": DATABASE_NAME},
			"response": {"error": str(error)},
			"status": "failure",
		}
		try:
			collection.insert_one(log)
		except Exception:
			pass
		raise
	finally:
		client.close()



def get_mongodb_check_logs(limit: int = 20) -> list[dict[str, Any]]:
	"""Return the most recent MongoDB connectivity check logs."""
	client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
	try:
		logs = get_test_collection(client).find().sort("checked_at", -1).limit(limit)
		return [
			{
				**log,
				"_id": str(log["_id"]),
				"checked_at": log["checked_at"].isoformat(),
			}
			for log in logs
		]
	finally:
		client.close()
