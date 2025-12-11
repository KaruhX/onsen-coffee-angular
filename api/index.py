import sys
import os
import traceback
import logging
from pathlib import Path
from flask import Flask

# Configure logging to print to stderr (visible in Vercel logs)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vercel_handler")

try:
    # Ensure backend package is importable when running as a Vercel function
    ROOT_DIR = Path(__file__).resolve().parents[1]
    BACKEND_DIR = ROOT_DIR / "backend"
    
    logger.info(f"Adding {BACKEND_DIR} to sys.path")
    
    if str(BACKEND_DIR) not in sys.path:
        sys.path.append(str(BACKEND_DIR))
        
    # Also add root dir to sys.path just in case
    if str(ROOT_DIR) not in sys.path:
        sys.path.append(str(ROOT_DIR))

    logger.info(f"sys.path: {sys.path}")
    logger.info("Attempting to import main.app")

    from main import app as app  # noqa: E402
    
    logger.info("Successfully imported app")

except Exception as e:
    logger.error(f"Failed to import backend: {e}")
    logger.error(traceback.format_exc())
    
    # Fallback app to display error in production
    app = Flask(__name__)
    
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        error_msg = traceback.format_exc()
        return f"""
        <h1>Error importing backend application</h1>
        <p>Check Vercel logs for more details.</p>
        <pre>{error_msg}</pre>
        <h2>Debug Info</h2>
        <pre>
CWD: {os.getcwd()}
sys.path: {sys.path}
        </pre>
        """, 500
