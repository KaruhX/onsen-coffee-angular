import sys
import os
import traceback
import logging
from pathlib import Path

# Configure logging to print to stderr (visible in Vercel logs)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("vercel_handler")

try:
    # Ensure backend package is importable when running as a Vercel function
    ROOT_DIR = Path(__file__).resolve().parents[1]
    BACKEND_DIR = ROOT_DIR / "backend"
    
    logger.info(f"ROOT_DIR: {ROOT_DIR}")
    logger.info(f"BACKEND_DIR: {BACKEND_DIR}")
    logger.info(f"Adding {BACKEND_DIR} to sys.path")
    
    if str(BACKEND_DIR) not in sys.path:
        sys.path.insert(0, str(BACKEND_DIR))
        
    # Also add root dir to sys.path just in case
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))

    logger.info(f"sys.path: {sys.path}")
    logger.info("Attempting to import main.app")

    # Import the Flask app
    from main import app
    
    logger.info("Successfully imported app from main")
    logger.info(f"App routes: {[str(rule) for rule in app.url_map.iter_rules()]}")

except Exception as e:
    logger.error(f"Failed to import backend: {e}")
    logger.error(traceback.format_exc())
    
    # Capture error for display
    import_error_msg = traceback.format_exc()
    
    # Fallback app to display error in production
    from flask import Flask
    app = Flask(__name__)
    
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        cwd = os.getcwd()
        backend_files = os.listdir(str(BACKEND_DIR)) if os.path.exists(str(BACKEND_DIR)) else 'Backend dir not found'
        return f"""
        <h1>Error importing backend application</h1>
        <p>Check Vercel logs for more details.</p>
        <pre style="background: #f4f4f4; padding: 10px; overflow: auto;">{import_error_msg}</pre>
        <h2>Debug Info</h2>
        <ul>
            <li>CWD: {cwd}</li>
            <li>Python Path: {sys.path}</li>
            <li>Files in CWD: {os.listdir(cwd)}</li>
            <li>Backend files: {backend_files}</li>
        </ul>
        """, 500

# This is the entry point for Vercel
# Vercel will look for an 'app' variable
logger.info("API handler ready")
