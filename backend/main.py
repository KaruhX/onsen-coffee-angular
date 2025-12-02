from flask import Flask 
from rest import app_rest

app = Flask(__name__)

@app.route("/")
def init():
    return "Python Backend is running"

# Registrar rutas REST
app_rest.register_routes(app)

app.config["DEBUG"] = True
app.run()