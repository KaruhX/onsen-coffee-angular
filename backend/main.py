from flask import Flask
from flask_cors import CORS
import os
import sys
from pathlib import Path

# Agregar el directorio backend al path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def create_app():
    app = Flask(__name__, static_folder='static')
    app.secret_key = os.environ.get('SECRET_KEY', 'onsen-coffee-secret-key-2025')
    
    # CORS para permitir requests del frontend
    CORS(app, supports_credentials=True)
    
    # Usar sesiones simples basadas en cookies (mejor para serverless)
    app.config['SESSION_TYPE'] = 'null'
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # Register blueprints
    from rest.app_rest import register_routes as register_rest_routes
    from admin.admin import register_routes as register_admin_routes
    
    register_rest_routes(app)
    register_admin_routes(app)
    
    return app

# Crear instancia para uso directo
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
