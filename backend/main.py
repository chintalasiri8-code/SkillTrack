"""
SkillTrack Entry Point
Launches the built-in Python HTTP server.
Usage: python backend/main.py [port]
"""

import sys
import os
from http.server import HTTPServer

# Add backend directory to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from server import SkillTrackHTTPRequestHandler
from storage import load_user_data, load_roles

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8000


def run_server(host=DEFAULT_HOST, port=DEFAULT_PORT):
    # Ensure data files are initialized
    load_roles()
    load_user_data()

    server_address = (host, port)
    httpd = HTTPServer(server_address, SkillTrackHTTPRequestHandler)
    
    print("=" * 60)
    print("      SkillTrack - Personal Skill & Career Readiness Tracker")
    print("=" * 60)
    print(f"Server is running successfully!")
    print(f"Access SkillTrack in your browser at:")
    print(f"  --> http://{host}:{port}")
    print("=" * 60)
    print("Press Ctrl+C to stop the server.\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping SkillTrack server gracefully...")
        httpd.server_close()
        print("Server stopped.")


if __name__ == "__main__":
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port argument '{sys.argv[1]}'. Using default port {DEFAULT_PORT}.")
    
    run_server(DEFAULT_HOST, port)
