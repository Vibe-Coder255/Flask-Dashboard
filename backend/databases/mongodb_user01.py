import json
from typing import Any

from bson import json_util
from bson.objectid import ObjectId
from pymongo import MongoClient, ReturnDocument
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


def get_user01_documents(limit: int = 100) -> list[dict[str, Any]]:
	"""Return the newest documents from the user_01 collection."""
	client, collection = connect_to_user01()
	try:
		documents = collection.find().sort("_id", -1).limit(limit)
		return [serialize_document(document) for document in documents]
	finally:
		client.close()


def insert_user01_document(document: dict[str, Any]) -> dict[str, Any]:
	"""Insert and return one document in user_01."""
	client, collection = connect_to_user01()
	try:
		result = collection.insert_one(document)
		return serialize_document(collection.find_one({"_id": result.inserted_id}))
	finally:
		client.close()


def update_user01_document(document_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
	"""Update one document by ID and return it, or None when it does not exist."""
	client, collection = connect_to_user01()
	try:
		result = collection.find_one_and_update(
			{"_id": ObjectId(document_id)},
			{"$set": updates},
			return_document=ReturnDocument.AFTER,
		)
		return serialize_document(result) if result else None
	finally:
		client.close()


def delete_user01_document(document_id: str) -> bool:
	"""Delete one document by ID and return whether it was removed."""
	client, collection = connect_to_user01()
	try:
		result = collection.delete_one({"_id": ObjectId(document_id)})
		return result.deleted_count == 1
	finally:
		client.close()


def serialize_document(document: dict[str, Any] | None) -> dict[str, Any] | None:
	"""Convert BSON values in a document into JSON-compatible values."""
	if document is None:
		return None
	return json.loads(json_util.dumps(document))
