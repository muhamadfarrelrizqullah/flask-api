import os
from flask import Flask, request, jsonify
from sqlalchemy import text
from config import Config
from models import db, User
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# Tes Koneksi
@app.route('/test-connection', methods=['GET'])
def test_connection():
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify({'status': 'Connection successful!'}), 200
    except Exception as e:
        return jsonify({'status': 'Connection failed', 'error': str(e)}), 500

# Read Data
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Create Data
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'email' not in data:
            return jsonify({"error": "Missing 'username' or 'email'"}), 400

        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update Data
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request must be JSON"}), 400
        user = User.query.get(id)

        if not user:
            return jsonify({"error": "User not found"}), 404
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete Data
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        # Tangani kesalahan yang mungkin terjadi
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
