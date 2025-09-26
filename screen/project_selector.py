import globals
from globals import term
from network_manager import NetworkManager

def select_project():
    with term.cbreak(), term.hidden_cursor():
        print(term.clear)
        print(term.yellow("Loading projects... Please wait"))
        success = False
        projects = []
        while not success:
            try:
                projects = NetworkManager.load_projects()
                if not projects:
                    print(term.red("No projects found on the server. Please create a project in GNS3 and restart the application."))
                    print(term.bold("Press any key to retry..."))
                    term.inkey()  # Wait for a key press
                    continue
                success = True
            except Exception as e:
                print(term.red(f"Error loading projects: {e} Press any key to retry... (auto retry in 5 seconds)"))
                term.inkey(timeout=5)  # Wait for a key press
                return
        print(term.clear)
        if len(projects) == 0:
            print(term.red("No projects found on the server. Please create a project in GNS3 and restart the application."))
            print(term.bold("Press any key to exit..."))
            term.inkey()  # Wait for a key press
            exit(1)
        currently_selected = 0
        while True:
            print(term.clear)
            print(term.bold("Select a project to work with (up/down, enter):"))
            for idx, project in enumerate(projects):
                status = project.get("status")
                status_color = term.green if status == "opened" else term.red
                if idx == currently_selected:
                    print(term.yellow("> " + f"{idx + 1}. {project.get('name')} (ID: {project.get('project_id')}) - {status_color(status)}" + term.normal))
                else:
                    print(f"{idx + 1}. {project.get('name')} (ID: {project.get('project_id')}) - {status_color(status)}")
            val = term.inkey()
            if val.code == 258: # Up
                if currently_selected < len(projects) - 1:
                    currently_selected += 1
            elif val.code == 259: # Down
                if currently_selected > 0:
                    currently_selected -= 1
            elif val.code == 343: # Enter
                if projects[currently_selected].get("status") != "opened":
                    print(term.red("Warning: The selected project is not currently loaded on the server. Open it first in GNS3 please. Then press any key to continue."))
                    term.inkey()  # Wait for a key press
                    print(term.yellow("Reloading projects... Please wait"))
                    projects = NetworkManager.load_projects()
                    continue
                break
        globals.current_project = projects[currently_selected].get("project_id")
        print(term.green("Project selected successfully!"))
        term.inkey()  # Wait for a key press