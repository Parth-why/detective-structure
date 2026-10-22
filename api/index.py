"""
Vercel Serverless Function entrypoint for Social Detective Flask App.
Exposes 'app' for the @vercel/python serverless runtime.
"""
import sys
import os

try:
    # Ensure the root directory of the project is in the Python module search path
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

    # Import the configured Flask instance from app.py
    from app import app
except Exception as err:
    import traceback
    sys.stderr.write(f"[FATAL] Failed to initialize Flask application in api/index.py: {err}\n")
    traceback.print_exc()
    raise err
