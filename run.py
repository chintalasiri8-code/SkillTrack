"""
SkillTrack Root Launcher
Allows running `python run.py` directly from the repository root directory.
"""
import sys
import os

# Add backend directory to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(BASE_DIR, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from main import run_server, DEFAULT_HOST, DEFAULT_PORT

if __name__ == "__main__":
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port '{sys.argv[1]}'. Using default port {DEFAULT_PORT}.")
    
    run_server(DEFAULT_HOST, port)
