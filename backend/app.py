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
from databases.mysql import check_mysql_connection, get_mysql_tables, get_mysql_table_data
from databases.postgres import check_postgres_connection, get_postgres_tables, get_postgres_table_data


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


@app.get("/api/mysql/status")
def mysql_status():
	try:
		return jsonify(check_mysql_connection())
	except Exception:
		logger.exception("Unable to check MySQL status")
		return jsonify({"error": "Unable to check MySQL status"}), 503


@app.get("/api/mysql/tables")
def mysql_tables():
	try:
		return jsonify(get_mysql_tables())
	except Exception:
		logger.exception("Unable to get MySQL tables")
		return jsonify({"error": "Unable to get MySQL tables"}), 503


@app.get("/api/mysql/table/<table_name>")
def mysql_table_data(table_name: str):
	try:
		limit = min(max(request.args.get("limit", default=100, type=int), 1), 1000)
		return jsonify(get_mysql_table_data(table_name, limit))
	except Exception:
		logger.exception("Unable to get MySQL table data")
		return jsonify({"error": "Unable to get MySQL table data"}), 503


@app.get("/api/postgres/status")
def postgres_status():
	try:
		return jsonify(check_postgres_connection())
	except Exception:
		logger.exception("Unable to check PostgreSQL status")
		return jsonify({"error": "Unable to check PostgreSQL status"}), 503


@app.get("/api/postgres/tables")
def postgres_tables():
	try:
		return jsonify(get_postgres_tables())
	except Exception:
		logger.exception("Unable to get PostgreSQL tables")
		return jsonify({"error": "Unable to get PostgreSQL tables"}), 503


@app.get("/api/postgres/table/<table_name>")
def postgres_table_data(table_name: str):
	try:
		limit = min(max(request.args.get("limit", default=100, type=int), 1), 1000)
		return jsonify(get_postgres_table_data(table_name, limit))
	except Exception:
		logger.exception("Unable to get PostgreSQL table data")
		return jsonify({"error": "Unable to get PostgreSQL table data"}), 503


if __name__ == "__main__":
	app.run(debug=True)
