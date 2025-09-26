import asyncio
import os
from blessed import Terminal
import json
import requests
from network_manager import NetworkManager

version = "V0.0.1"
logo =f"""                                                                                                                         
  ,ad8888ba,   888b      88   ad88888ba    ad888888b,     888888888888                                                    
 d8\"'    `\"8b  8888b     88  d8\"     \"8b  d8\"     \"88          88                           ,d                            
d8'            88 `8b    88  Y8,                  a8P          88                           88                            
88             88  `8b   88  `Y8aaaaa,         aad8\"           88   ,adPPYba,  ,adPPYba,  MM88MMM  ,adPPYba,  8b,dPPYba,  
88      88888  88   `8b  88    `\"\"\"\"\"8b,       \"\"Y8,           88  a8P_____88  I8[    \"\"    88    a8P_____88  88P'   \"Y8  
Y8,        88  88    `8b 88          `8b          \"8b          88  8PP\"\"\"\"\"\"\"   `\"Y8ba,     88    8PP\"\"\"\"\"\"\"  88          
 Y8a.    .a88  88     `8888  Y8a     a8P  Y8,     a88          88  \"8b,   ,aa  aa    ]8I    88,   \"8b,   ,aa  88          
  `\"Y88888P\"   88      `888   \"Y88888P\"    \"Y888888P'          88   `\"Ybbd8\"'  `\"YbbdP\"'    \"Y888  `\"Ybbd8\"'  88          

GNS3Tester {version} - A terminal based testing tool for GNS3 by NovySoftware"""

term = Terminal()
server_data = {}
session = requests.Session()
current_project = {}

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