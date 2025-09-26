import globals
import requests

class NetworkManager:
    def __init__(self):
        pass

    @staticmethod
    def authenticate():
        # Use globals.server_data for authentication
        server_data = globals.server_data
        if not server_data:
            return False
        host = server_data.get("host")
        port = server_data.get("port")
        username = server_data.get("username")
        password = server_data.get("password")
        globals.session.auth = (username, password) if username else None
        print(globals.term.move_down(2) + globals.term.move_x(0) + f"Authenticating to {host}:{port} with {f'username {username}' if len(username) > 0 else 'no authentication'}")
        response = globals.session.get(f"http://{host}:{port}/v2/version")
        response.raise_for_status()
        print(globals.term.move_down(1) + globals.term.move_x(0) + globals.term.green(f"Authentication successful! Server version: {response.json().get('version')}"))