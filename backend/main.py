from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'onsen-coffee-secret-key-2025')

# Usar sesiones simples basadas en cookies (mejor para serverless)
app.config['SESSION_TYPE'] = 'null'  # Usa sesiones de Flask por defecto (cookies seguras)
app.config['SESSION_COOKIE_SECURE'] = False  # True en producción con HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Register blueprints
from rest.app_rest import register_routes as register_rest_routes
from admin.admin import register_routes as register_admin_routes

register_rest_routes(app)
register_admin_routes(app)


if __name__ == '__main__':
    app.run(debug=True)