import globals
from globals import term
from tools.netmask import netmask_to_cidr

def search_ip_database_screen():
    with term.cbreak(), term.hidden_cursor():
        ip_to_search = ''
        scroll_offset = 0
        
        print(term.clear)
        print(term.move_y(0) + term.bold("Search IP Database (Press 'q' to quit): "))
        
        while True:
            # Calculate available space for results (leave space for prompt and header)
            max_results_per_page = term.height - 6  # Reserve lines for prompt, header, instructions
            
            val = term.inkey()
            print(term.move_y(0) + term.bold("Search IP Database (Press 'q' to quit)"))
            print(term.clear)
            
            # Display search prompt at top

            if val.lower() == 'q':
                break
            elif val.isprintable():
                ip_to_search += val
                scroll_offset = 0  # Reset scroll when search changes
            elif val.code == 263:  # Backspace
                if ip_to_search:
                    ip_to_search = ip_to_search[:-1]
                    scroll_offset = 0  # Reset scroll when search changes
            elif val.code == term.KEY_UP:
                scroll_offset = max(0, scroll_offset - 1)
            elif val.code == term.KEY_DOWN:
                scroll_offset += 1
            elif val.code == term.KEY_PGUP:
                scroll_offset = max(0, scroll_offset - max_results_per_page)
            elif val.code == term.KEY_PGDN:
                scroll_offset += max_results_per_page
            print(f"Enter IP address to search (or 'q' to go back): {ip_to_search}", end='', flush=True)

            # Search for IPs
            ips_found = list(filter(lambda x: ip_to_search in x, globals.current_project['ips'].keys()))
            
            # Adjust scroll offset if it's beyond the results
            if scroll_offset >= len(ips_found):
                scroll_offset = max(0, len(ips_found) - max_results_per_page)

            # Display results
            print(term.move_y(3))  # Position below prompt
            if len(ips_found) > 0:
                print(term.bold(f"IPs found matching '{ip_to_search}' ({len(ips_found)} total):"))
                
                # Show scrollable results
                start_idx = scroll_offset
                end_idx = min(start_idx + max_results_per_page, len(ips_found))
                
                for i in range(start_idx, end_idx):
                    ip = ips_found[i]
                    print(
                        f"IP: {ip}/{netmask_to_cidr(globals.current_project['ips'][ip]['mask'])}, "
                        f"Device: {globals.current_project['ips'][ip]['node']}, "
                        f"Port: {globals.current_project['ips'][ip]['port'].replace('GigabitEthernet', 'Gi').replace('FastEthernet', 'Fa')}, "
                        f"(Connected to: {globals.current_project['ips'][ip].get('connected_to', 'Unknown')})"
                    )
                
                # Show scroll indicators
                if len(ips_found) > max_results_per_page:
                    scroll_info = f"Showing {start_idx + 1}-{end_idx} of {len(ips_found)}"
                    if scroll_offset > 0:
                        scroll_info += " | ↑ Up/PgUp for more"
                    if end_idx < len(ips_found):
                        scroll_info += " | ↓ Down/PgDn for more"
                    scroll_info += " | 'q' to quit"
                    print(term.dim + scroll_info + term.normal)
            else:
                if ip_to_search:
                    print(term.red(f"No IPs found matching '{ip_to_search}'"))
                else:
                    print("No IPs to display.")
                    print(term.dim + "Use arrow keys or Page Up/Down to scroll results" + term.normal)