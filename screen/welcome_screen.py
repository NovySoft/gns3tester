import asyncio
import globals
from globals import term
from screen.project_selector import select_project

async def display_welcome_screen():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        print(term.center(globals.logo))
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
        await select_project()