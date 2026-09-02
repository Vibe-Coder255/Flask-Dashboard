import logging

from flask import Flask, jsonify, request

from databases.mongodb import check_mongodb_connection, get_mongodb_check_logs


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


if __name__ == "__main__":
	app.run(debug=True)
