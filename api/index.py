import sys
from pathlib import Path

# Ensure backend package is importable when running as a Vercel function
ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from main import app as app  # noqa: E402
