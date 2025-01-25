from flask import Blueprint, request, jsonify
from backend.apps.models.users import User
from backend.apps.utils.db import db
from flask_cors import CORS
user_bp = Blueprint('users', __name__)
CORS(user_bp)
@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201
