import json
import os
import asyncio
import globals
from globals import term
from tools import input

async def display_login_screen(title: str, red: bool = False):
    with term.cbreak(), term.hidden_cursor():
        print(term.clear)
        if red:
            print(term.red_bold(title))
        else:
            print(term.bold(title))
        print(term.move_down(2) + "Please enter your gns3 server login details below.\n")
        server_host = input("Server host: ")
        server_port = input("Server port: ")
        server_username = input("Username (leave empty for no authentication): ")
        server_password = ''
        if server_username:
            server_password = input("Password: ")
        # Save to server.json
        server_data = {
            "host": server_host,
            "port": server_port,
            "username": server_username,
            "password": server_password
        }
        globals.server_data = server_data
        with open(os.path.join('data', 'server.json'), 'w') as f:
            json.dump(server_data, f, indent=4)
        print(term.move_down(2) + term.green_bold("Server details saved successfully!"))
        term.inkey(timeout=2)  # Wait for a key press or timeout after 2 seconds