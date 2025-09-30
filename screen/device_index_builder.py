from datetime import datetime
import json
import globals
from globals import term
from network_manager import NetworkManager
import asyncio
import tools.cisco.get_ip_and_mask

async def device_index_builder_screen():
    with term.cbreak(), term.hidden_cursor():
        print(term.clear)
        print(term.bold("Device Index Builder"))
        print(term.bold("Starting the device index builder... Please wait!"))
        print(term.move_down(1) + "This may take a while depending on the size of your project. Do *NOT* use GNS3 while the index is being built!")
        print(term.yellow("Getting templates"))
        templates = NetworkManager.get_templates()
        globals.current_project['templates'] = {}
        for template in templates:
            globals.current_project['templates'][template['template_id']] = {
                'name': template['name'],
                'template_type': template['template_type']
            }
        print(term.yellow("Starting to index nodes to their names..."))
        nodes = NetworkManager.get_project_nodes()
        globals.current_project['device_index'] = {}
        globals.current_project['ips'] = {} 
        for index, node in enumerate(nodes):
            print(term.move_x(0) + f"Building index of {node['name']} ({index + 1}/{len(nodes)} nodes)")
            node_links = NetworkManager.get_links(node['node_id'])
            temporary_links = {} # nodeid/adapter/port -> other nodeid/adapter/port
            for link in node_links:
                link_bundle = link['nodes']
                my_half = list(filter(lambda x: x['node_id'] == node['node_id'], link_bundle))
                other_half = list(filter(lambda x: x['node_id'] != node['node_id'], link_bundle))
                if len(my_half) != 1 or len(other_half) != 1:
                    print(term.red("Highly unusual link found!"))
                    print(link)
                temporary_links[f"{my_half[0]['node_id']}/{my_half[0]['adapter_number']}/{my_half[0]['port_number']}"] = f"{other_half[0]['node_id']}/{other_half[0]['adapter_number']}/{other_half[0]['port_number']}"

            globals.current_project['device_index'][node['node_id']] = {
                'name': node['name'],
                'template': globals.current_project['templates'].get(node['template_id'], {'name': 'Unknown', 'template_type': 'Unknown'}),
                'ports': [],
                'console': {
                    'type': node.get('console_type', 'Unknown'),
                    'ip': node.get('console_host', 'Unknown'),
                    'port': node.get('console', 'Unknown'),
                }
            }

            # This section is being modified for concurrency.
            # We will first create all the tasks for fetching IPs,
            # then run them concurrently.

        # --- Start of concurrent IP fetching ---

        tasks = []
        # Create a mapping from node_id to node object for easier lookup later
        node_map = {node['node_id']: node for node in nodes}

        # Use a semaphore to limit concurrent connections to 10
        sem = asyncio.Semaphore(10)

        async def get_ip_for_node(node):
            async with sem:
                if node['status'] == "stopped":
                    print(term.red(f"Node {node['name']} is stopped. Cannot get IP information!"))
                    return node['node_id'], {}
                
                if 'cisco' in globals.current_project['device_index'][node['node_id']]['template']['name'].lower():
                    print(f"Fetching IPs for {node['name']}...")
                    try:
                        port_ip = await tools.cisco.get_ip_and_mask.cisco_get_ip_and_mask_telnet(node['console_host'], node['console'], device_name=node['name'])
                        print(f"Finished fetching IPs for {node['name']}.")
                        return node['node_id'], port_ip
                    except Exception as e:
                        print(term.red(f"Error fetching IPs for {node['name']}: {e}"))
                        return node['node_id'], {}
                
                return node['node_id'], {}

        print(term.move_down(1) + term.yellow("Gathering IP information from running Cisco devices..."))
        for node in nodes:
            tasks.append(get_ip_for_node(node))
        
        # Run all tasks concurrently and wait for them to complete
        results = await asyncio.gather(*tasks)
        # --- End of concurrent IP fetching ---

        # Now process the results for each node
        print(term.yellow("Processing gathered IP information..."))
        for node_id, port_ip in results:
            node = node_map[node_id]
            
            # Re-create temporary_links for the current node
            node_links = NetworkManager.get_links(node['node_id'])
            temporary_links = {}
            for link in node_links:
                link_bundle = link['nodes']
                my_half = list(filter(lambda x: x['node_id'] == node['node_id'], link_bundle))
                other_half = list(filter(lambda x: x['node_id'] != node['node_id'], link_bundle))
                if len(my_half) == 1 and len(other_half) == 1:
                    temporary_links[f"{my_half[0]['node_id']}/{my_half[0]['adapter_number']}/{my_half[0]['port_number']}"] = f"{other_half[0]['node_id']}/{other_half[0]['adapter_number']}/{other_half[0]['port_number']}"

            ip_interfaces = list(port_ip.keys())

            for port in node.get('ports', []):
                ip_used = port_ip.get(port['name'], ('Unassigned', 'Unassigned'))
                if ip_used[0] != 'Unassigned':
                    if port['name'] in ip_interfaces:
                        ip_interfaces.remove(port['name'])
                
                port_info = {
                    'adapter_number': port['adapter_number'],
                    'port_number': port['port_number'],
                    'name': port['name'],
                    'ip': ip_used[0],
                    'mask': ip_used[1],
                    'connected_to': temporary_links.get(f"{node['node_id']}/{port['adapter_number']}/{port['port_number']}", 'Unconnected')
                }
                globals.current_project['device_index'][node_id]['ports'].append(port_info)
                if port_info['ip'] not in ['Unassigned', 'Unknown']:
                    globals.current_project['ips'][port_info['ip']] = {
                        'node': node['name'],
                        'port': port['name'],
                        'mask': port_info['mask']
                    }

            for unused_interface in ip_interfaces:
                # These are probably loopback and virtual ip addresses
                ip_used = port_ip.get(unused_interface, ('Unassigned', 'Unassigned'))
                globals.current_project['device_index'][node_id]['ports'].append({
                    'adapter_number': 'N/A',
                    'port_number': 'N/A',
                    'name': unused_interface,
                    'ip': ip_used[0],
                    'mask': ip_used[1],
                    'connected_to': 'Unconnected'
                })
                if ip_used[0] not in ['Unassigned', 'Unknown']:
                    globals.current_project['ips'][ip_used[0]] = {
                        'node': node['name'],
                        'port': unused_interface,
                        'mask': ip_used[1]
                    }
        

        # Wait for all the ips to be gathered before we start linking
        print(term.move_down(2) + term.yellow("Building link connection index!"))
        for node_id, node_data in globals.current_project['device_index'].items():
            for port in node_data['ports']:
                if port['connected_to'] != 'Unconnected':
                    connected_info = port['connected_to'].split('/')
                    connected_node_id = connected_info[0]
                    connected_adapter = connected_info[1]
                    connected_port = connected_info[2]

                    connected_node =  globals.current_project['device_index'][connected_node_id]
                    connected_port_info = list(filter(lambda x: x['adapter_number'] == int(connected_adapter) and x['port_number'] == int(connected_port), connected_node['ports']))
                    if len(connected_port_info) == 1:
                        connected_port_info = connected_port_info[0]
                        port['connected_to'] = {
                            'name': connected_node['name'],
                            'port': connected_port_info['name']
                        }
                    else:
                        print(term.red("Highly unusual port info found!"))
                        print(connected_port_info)

        globals.current_project['last_index'] = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        json.dump(globals.current_project, open(f'data/{globals.current_project["project_id"]}.json', 'w'), indent=4)
        print(term.move_down(2) + term.green("Device index build complete! Press any key to continue..."))
        term.inkey()  # Wait for a key press or timeout