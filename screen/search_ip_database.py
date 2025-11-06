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
            print(f"Enter IP address/Device name to search (or 'q' to go back): {ip_to_search}", end='', flush=True)

            # Search for IPs - now working with a list
            ips_found = []
            for ip_entry in globals.current_project['ips']:
                if ip_to_search in ip_entry['ip'] or ip_to_search.lower() in ip_entry['node'].lower():
                    ips_found.append(ip_entry)
                if ip_to_search.lower() in (ip_entry.get('ipv6', '') or '').lower() or ip_to_search.lower() in (ip_entry.get('ipv6_link_local', '') or '').lower():
                    ips_found.append(ip_entry)
            
            # Adjust scroll offset if it's beyond the results
            if scroll_offset >= len(ips_found):
                scroll_offset = max(0, len(ips_found) - max_results_per_page)

            # Display results
            print(term.move_y(3))  # Position below prompt
            if len(ips_found) > 0:
                print(term.bold(f"IPs found matching '{ip_to_search}' ({len(ips_found)} total):"))
                
                # Show scrollable results, ordered by IP address
                def ip_key(ip_entry):
                    ip = ip_entry['ip']
                    if ip == 'Unassigned' or ip == 'Unknown':
                        return (float('inf'),)  # Push unassigned/unknown to the end
                    parts = ip.replace(' (dhcp)', '').split('.')
                    return tuple(int(part) for part in parts)
                sorted_ips = sorted(ips_found, key=ip_key)

                start_idx = scroll_offset
                end_idx = min(start_idx + max_results_per_page, len(sorted_ips))

                for i in range(start_idx, end_idx):
                    ip_entry = sorted_ips[i]
                    ipv4_display = f"IP: {ip_entry['ip']}/{netmask_to_cidr(ip_entry['mask'])}"
                    ipv6_display = ""
                    if ip_entry.get('ipv6'):
                        ipv6_display = f", IPv6: {ip_entry['ipv6']}"
                    if ip_entry.get('ipv6_link_local'):
                        ipv6_display += f" (LL: {ip_entry['ipv6_link_local']})"
                    
                    print(
                        f"{ipv4_display}{ipv6_display}, "
                        f"Device: {ip_entry['node']}, "
                        f"Port: {ip_entry['port'].replace('GigabitEthernet', 'Gi').replace('FastEthernet', 'Fa')}, "
                        f"(Connected to: {ip_entry.get('connected_to', 'Unknown')})"
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