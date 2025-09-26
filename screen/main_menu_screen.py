import globals
from globals import term
from screen.device_index_builder import device_index_builder_screen
from tools.terminal_tools import input

def main_menu_screen():
    with term.cbreak(), term.hidden_cursor():
        options = [
            f"1. View Device Index (last indexed: {globals.current_project.get('last_index')})",
            "2. Rebuild Device Index",
            "3. Exit"
        ]
        currently_selected = 0
        while True:
            print(term.clear)
            print(term.bold(f"Current Project: {globals.current_project.get('name')} (ID: {globals.current_project.get('project_id')})"))
            print(term.bold(f""))
            print(term.bold("Main Menu:\n"))
            for index, option in enumerate(options):
                if index == currently_selected:
                    print(term.yellow("> " + option + term.normal))
                else:
                    print(option)
            val = term.inkey()
            if val.code == 258: # Up
                if currently_selected < len(options) - 1:
                    currently_selected += 1
            elif val.code == 259: # Down
                if currently_selected > 0:
                    currently_selected -= 1
            elif val.code == 343: # Enter
                if currently_selected == 0:
                    if globals.current_project.get("last_index") == 'Never':
                        print(term.red("Device index has never been built, so there is nothing to view. Please build the device index first. Press any key to continue..."))
                        term.inkey()  # Wait for a key press
                        continue
                elif currently_selected == 1:
                    result = input(term.yellow("Rebuilding the device index is time consuming, and you cannot use your gns3 project while it is being built. \n!!! Make sure all the devices are running andno one is using the project in GNS3. !!! \nAre you sure you want to continue? (y/N) "))
                    if result.lower() == 'y':
                        device_index_builder_screen()
                elif currently_selected == len(options) - 1:
                    print(term.clear)
                    print(globals.logo)
                    print(term.move_down(1) + term.move_x(0) + term.bold("Exiting..."))
                    print(term.move_x(0) + term.bold("Goodbye! Thank you for using GNS3Tester!"))
                    term.inkey(timeout=3)
                    exit(0)