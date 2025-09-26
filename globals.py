import asyncio
import os
from blessed import Terminal
import json
import requests
from network_manager import NetworkManager

term = Terminal()
server_data = {}
session = requests.Session()

async def import_data() -> tuple[int, bool]:
    global server_data
    print_count = 0
    is_new_user = False
    with term.location():
        # Check if data folder exists
        if not os.path.exists('data'):
            print_count += 1
            print(
                term.move_down(1) + term.move_x(0) +
                term.yellow("Data folder not found. Creating 'data' folder...") +
                term.move_up(print_count + 1)
            )
            os.makedirs('data')
        else:
            check_files = os.listdir('data')
            # Authentication details
            if 'server.json' not in check_files:
                print_count += 1
                print(
                    term.move_down(1) + term.move_x(0) +
                    term.yellow("'server.json' not found in 'data' folder. You will need to login in the next screen...") +
                    term.move_up(print_count + 1)
                )
                is_new_user = True
                await asyncio.sleep(2)  # Give user time to read the message
            else:
                print_count += 1
                print(
                    term.move_down(1) + term.move_x(0) +
                    term.green("'server.json' found in 'data' folder.") +
                    term.move_up(print_count + 1)
                )
                with open(os.path.join('data', 'server.json'), 'r') as f:
                    server_data = json.load(f)
                if not server_data.get("host") or not server_data.get("port"):
                    print_count += 1
                    print(
                        term.move_down(1) + term.move_x(0) +
                        term.red("'server.json' is missing required fields. You will need to login in the next screen...") +
                        term.move_up(print_count + 1)
                    )
                    is_new_user = True
    return print_count, is_new_user