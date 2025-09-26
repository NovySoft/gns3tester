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
        loaded_projects = list(filter(lambda p: p.get("status") == "loaded", projects))
        if len(loaded_projects) == 1:
            globals.current_project = loaded_projects[0]
            print(term.green(f"Only one project is open and running: {globals.current_project.get('name')} (ID: {globals.current_project.get('project_id')})"))
            print(term.green("Assuming this is the project you want to work with."))
            print(term.bold("Press any key to continue..."))
            term.inkey()  # Wait for a key press
            return
        else:
            print(term.bold("Select a project to work with:"))
            for idx, project in enumerate(projects):
                status = project.get("status")
                status_color = term.green if status == "loaded" else term.yellow if status == "stopped" else term.red
                print(f"{idx + 1}. {project.get('name')} (ID: {project.get('project_id')}) - {status_color(status)}")
        term.inkey()  # Wait for a key press