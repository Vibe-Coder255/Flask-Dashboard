from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
def get_stats():
    return jsonify({
        "total_users": 1280,
        "active_sessions": 342,
        "server_load": "23%",
        "recent_alerts": 2
    }), 200