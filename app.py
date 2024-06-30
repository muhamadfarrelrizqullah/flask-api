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

if __name__ == '__main__':
    app.run(debug=True)
