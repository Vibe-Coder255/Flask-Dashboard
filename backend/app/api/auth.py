from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    # Demo bypass for initial setup
    if username == "admin" and password == "admin":
        token = create_access_token(identity={"username": username, "role": "admin"})
        return jsonify(access_token=token), 200

    return jsonify({"error": "Invalid credentials"}), 401