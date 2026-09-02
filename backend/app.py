import logging

from bson.errors import InvalidId
from flask import Flask, jsonify, request

from databases.mongodb import check_mongodb_connection, get_mongodb_check_logs
from databases.mongodb_user01 import (
	delete_user01_document,
	get_user01_documents,
	insert_user01_document,
	update_user01_document,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def check_startup_databases() -> None:
	"""Run the database request/response checks when the program starts."""
	try:
		check_mongodb_connection()
		logger.info("MongoDB startup check succeeded")
	except Exception:
		logger.exception("MongoDB startup check failed")


check_startup_databases()


@app.get("/api/mongodb/logs")
def mongodb_logs():
	try:
		limit = min(max(request.args.get("limit", default=20, type=int), 1), 100)
		return jsonify(get_mongodb_check_logs(limit))
	except Exception:
		logger.exception("Unable to read MongoDB check logs")
		return jsonify({"error": "Unable to read MongoDB check logs"}), 503


@app.get("/api/mongodb/user01")
def user01_documents():
	try:
		limit = min(max(request.args.get("limit", default=100, type=int), 1), 1000)
		return jsonify(get_user01_documents(limit))
	except Exception:
		logger.exception("Unable to read user_01 documents")
		return jsonify({"error": "Unable to read user_01 documents"}), 503


@app.post("/api/mongodb/user01")
def create_user01_document():
	document = request.get_json(silent=True)
	if not isinstance(document, dict):
		return jsonify({"error": "Request body must be a JSON object"}), 400
	try:
		return jsonify(insert_user01_document(document)), 201
	except Exception:
		logger.exception("Unable to insert user_01 document")
		return jsonify({"error": "Unable to insert user_01 document"}), 503


@app.patch("/api/mongodb/user01/<document_id>")
def update_user01(document_id: str):
	updates = request.get_json(silent=True)
	if not isinstance(updates, dict):
		return jsonify({"error": "Request body must be a JSON object"}), 400
	try:
		document = update_user01_document(document_id, updates)
	except InvalidId:
		return jsonify({"error": "Invalid document ID"}), 400
	except Exception:
		logger.exception("Unable to update user_01 document")
		return jsonify({"error": "Unable to update user_01 document"}), 503
	if document is None:
		return jsonify({"error": "Document not found"}), 404
	return jsonify(document)


@app.delete("/api/mongodb/user01/<document_id>")
def delete_user01(document_id: str):
	try:
		deleted = delete_user01_document(document_id)
	except InvalidId:
		return jsonify({"error": "Invalid document ID"}), 400
	except Exception:
		logger.exception("Unable to delete user_01 document")
		return jsonify({"error": "Unable to delete user_01 document"}), 503
	if not deleted:
		return jsonify({"error": "Document not found"}), 404
	return "", 204


if __name__ == "__main__":
	app.run(debug=True)
