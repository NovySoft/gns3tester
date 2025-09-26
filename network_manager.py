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

    @staticmethod
    def load_projects():
        server_data = globals.server_data
        if not server_data:
            raise Exception("Server data not set.")
        host = server_data.get("host")
        port = server_data.get("port")
        response = globals.session.get(f"http://{host}:{port}/v2/projects")
        response.raise_for_status()
        projects = response.json()
        return projects
    
    @staticmethod
    def get_project_nodes():
        server_data = globals.server_data
        current_project = globals.current_project
        if not server_data or not current_project:
            raise Exception("Server data or current project not set.")
        host = server_data.get("host")
        port = server_data.get("port")
        project_id = current_project.get("project_id")
        response = globals.session.get(f"http://{host}:{port}/v2/projects/{project_id}/nodes")
        response.raise_for_status()
        nodes = response.json()
        return nodes
    
    @staticmethod
    def get_node_info(node_id):
        server_data = globals.server_data
        current_project = globals.current_project
        if not server_data or not current_project:
            raise Exception("Server data or current project not set.")
        host = server_data.get("host")
        port = server_data.get("port")
        project_id = current_project.get("project_id")
        response = globals.session.get(f"http://{host}:{port}/v2/projects/{project_id}/nodes/{node_id}")
        response.raise_for_status()
        node_info = response.json()
        return node_info
    
    @staticmethod
    def get_templates():
        server_data = globals.server_data
        if not server_data:
            raise Exception("Server data not set.")
        host = server_data.get("host")
        port = server_data.get("port")
        response = globals.session.get(f"http://{host}:{port}/v2/templates")
        response.raise_for_status()
        templates = response.json()
        return templates
    
    @staticmethod
    def get_links(node_id):
        server_data = globals.server_data
        current_project = globals.current_project
        if not server_data or not current_project:
            raise Exception("Server data or current project not set.")
        host = server_data.get("host")
        port = server_data.get("port")
        project_id = current_project.get("project_id")
        response = globals.session.get(f"http://{host}:{port}/v2/projects/{project_id}/nodes/{node_id}/links")
        response.raise_for_status()
        links = response.json()
        return links