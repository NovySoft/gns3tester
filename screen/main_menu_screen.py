import globals
from globals import term

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
                break
        term.inkey()  # Wait for a key press