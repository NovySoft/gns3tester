import asyncio
import globals
from globals import term
from screen.project_selector import select_project

async def display_welcome_screen():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        welcome_message ="""
                                                                                                                          
  ,ad8888ba,   888b      88   ad88888ba    ad888888b,     888888888888                                                    
 d8\"'    `\"8b  8888b     88  d8\"     \"8b  d8\"     \"88          88                           ,d                            
d8'            88 `8b    88  Y8,                  a8P          88                           88                            
88             88  `8b   88  `Y8aaaaa,         aad8\"           88   ,adPPYba,  ,adPPYba,  MM88MMM  ,adPPYba,  8b,dPPYba,  
88      88888  88   `8b  88    `\"\"\"\"\"8b,       \"\"Y8,           88  a8P_____88  I8[    \"\"    88    a8P_____88  88P'   \"Y8  
Y8,        88  88    `8b 88          `8b          \"8b          88  8PP\"\"\"\"\"\"\"   `\"Y8ba,     88    8PP\"\"\"\"\"\"\"  88          
 Y8a.    .a88  88     `8888  Y8a     a8P  Y8,     a88          88  \"8b,   ,aa  aa    ]8I    88,   \"8b,   ,aa  88          
  `\"Y88888P\"   88      `888   \"Y88888P\"    \"Y888888P'          88   `\"Ybbd8\"'  `\"YbbdP\"'    \"Y888  `\"Ybbd8\"'  88          
"""
        print(term.center(welcome_message))
        print(term.move_down(2) + "Welcome to GNS3Tester!")
        print(term.move_down(1) + "Loading your data in the background... Please wait", end="", flush=True)

        task = asyncio.create_task(globals.import_data())
        dots = 0
        while not task.done():
            dots = (dots + 1) % 4
            # Clear the line and re-print the loading message
            print(f"\r{term.move_x(0)}Loading your data in the background... Please wait{'.'*dots}{' '* (3 - dots)}", end="", flush=True)
            await asyncio.sleep(0.5)
        no_prints, is_new_user = await task
        authenticated = False
        while not authenticated:
            if not is_new_user:
                from network_manager import NetworkManager
                try:
                    NetworkManager.authenticate()
                    authenticated = True
                except Exception as e:
                    print(term.move_down(1) + term.red(f"Authentication failed: {e}"))
                    is_new_user = True
                    await asyncio.sleep(3)
            if is_new_user:
                from screen.login_screen import display_login_screen
                await display_login_screen("Please (re)login to continue!")
                is_new_user = False  # Try to authenticate after login screen
        print(term.move_x(0) + term.move_down(no_prints + 2) + term.bold("Data loaded!\nMake sure to run your terminal in fullscreen!\nPress any key to continue..."))
        term.inkey()  # Wait for a key press
        select_project()