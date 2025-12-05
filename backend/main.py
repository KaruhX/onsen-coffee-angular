from flask import Flask
from flask_session import Session
from rest import app_rest
import os

app = Flask(__name__)
app.secret_key = 'onsen-coffee-secret-key-2025'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(__file__), 'sessions')
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True

Session(app)

@app.route("/")
def init():
    return "Python Backend is running"

app_rest.register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)