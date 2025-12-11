from flask import Flask
from flask_session import Session
from rest import app_rest
from admin import admin
import os
import tempfile

app = Flask(__name__)
app.secret_key = 'onsen-coffee-secret-key-2025'

# Persist sessions in /tmp so it works on ephemeral file systems (e.g., serverless)
session_dir = os.path.join(tempfile.gettempdir(), 'onsen-coffee-sessions')
os.makedirs(session_dir, exist_ok=True)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = session_dir
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True

Session(app)

@app.route("/")
def init():
    return "Python Backend is running"

app_rest.register_routes(app)
admin.register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)