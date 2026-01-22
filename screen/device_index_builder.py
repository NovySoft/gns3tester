from datetime import datetime
import json
import globals
from globals import term
from network_manager import NetworkManager
import asyncio
import tools.cisco.get_ip_and_mask
import tools.cisco.get_ospf_and_bgp_routerid
import tools.arista_ceos.get_ip_and_mask
import tools.arista_ceos.get_ospf_and_bgp_routerid

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
        globals.current_project['ips'] = []  # Changed from {} to []
        globals.current_project['router_ids'] = []
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
                temporary_links[f"{my_half[0]['node_id']}/{my_half[0]['adapter_number']}/{my_half[0]['port_number']}"] = {
                    'target': f"{other_half[0]['node_id']}/{other_half[0]['adapter_number']}/{other_half[0]['port_number']}",
                    'link_id': link['link_id']
                }

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
                    return node['node_id'], {}, []
                
                template_name = globals.current_project['device_index'][node['node_id']]['template']['name'].lower()
                if ('cisco' in template_name and not 'asa' in template_name) or 'ios' in template_name or 'iosxe' in template_name or 'veos' in template_name:
                    print(f"Fetching IPs for {node['name']}...")
                    try:
                        port_ip = await tools.cisco.get_ip_and_mask.cisco_get_ip_and_mask_telnet(node['console_host'], node['console'], device_name=node['name'])
                        print(f"Finished fetching IPs for {node['name']}.")
                        try:
                            print(f"Fetching OSPF/BGP information for {node['name']}...")
                            ospf_bgp_id = await tools.cisco.get_ospf_and_bgp_routerid.get_ospf_and_bgp_routerid_telnet(node['console_host'], node['console'], device_name=node['name'])
                            print(f"Finished fetching OSPF/BGP information for {node['name']}.")
                            return node['node_id'], port_ip, ospf_bgp_id
                        except Exception as e:
                            print(term.red(f"Error fetching OSPF/BGP information for {node['name']}: {e}"))
                            return node['node_id'], port_ip, []
                    except Exception as e:
                        print(term.red(f"Error fetching IPs for {node['name']}: {e}"))
                        return node['node_id'], {}, []
                    
                if 'ceos' in template_name:
                    print(f"Fetching IPs for {node['name']}...")
                    try:
                        port_ip = await tools.arista_ceos.get_ip_and_mask.arista_get_ip_and_mask_telnet(node['console_host'], node['properties']['aux'], device_name=node['name'])
                        print(f"Finished fetching IPs for {node['name']}.")
                        try:
                            print(f"Fetching OSPF/BGP information for {node['name']}...")
                            ospf_bgp_id = await tools.arista_ceos.get_ospf_and_bgp_routerid.get_ospf_and_bgp_routerid_telnet(node['console_host'], node['properties']['aux'], device_name=node['name'])
                            print(f"Finished fetching OSPF/BGP information for {node['name']}.")
                            return node['node_id'], port_ip, ospf_bgp_id
                        except Exception as e:
                            print(term.red(f"Error fetching OSPF/BGP information for {node['name']}: {e}"))
                            return node['node_id'], port_ip, []
                    except Exception as e:
                        print(term.red(f"Error fetching IPs for {node['name']}: {e}"))
                        return node['node_id'], {}, []
                
                return node['node_id'], {}, []

        print(term.move_down(1) + term.yellow("Gathering IP information from running Cisco devices..."))
        for node in nodes:
            tasks.append(get_ip_for_node(node))
        
        # Run all tasks concurrently and wait for them to complete
        results = await asyncio.gather(*tasks)
        # --- End of concurrent IP fetching ---

        # Now process the results for each node
        print(term.yellow("Processing gathered IP information..."))
        for node_id, port_ip, ospf_bgp_id in results:
            node = node_map[node_id]
            
            # Re-create temporary_links for the current node
            node_links = NetworkManager.get_links(node['node_id'])
            temporary_links = {}
            for link in node_links:
                link_bundle = link['nodes']
                my_half = list(filter(lambda x: x['node_id'] == node['node_id'], link_bundle))
                other_half = list(filter(lambda x: x['node_id'] != node['node_id'], link_bundle))
                if len(my_half) == 1 and len(other_half) == 1:
                    temporary_links[f"{my_half[0]['node_id']}/{my_half[0]['adapter_number']}/{my_half[0]['port_number']}"] = {
                        'target': f"{other_half[0]['node_id']}/{other_half[0]['adapter_number']}/{other_half[0]['port_number']}",
                        'link_id': link['link_id']
                    }

            ip_interfaces = list(port_ip.keys())

            for port in node.get('ports', []):
                ip_used = port_ip.get(port['name'], ('Unassigned', 'Unassigned', None, None))
                # Handle both old format (2 items) and new format (4 items)
                if len(ip_used) == 2:
                    ipv4, mask, ipv6, ipv6_ll = ip_used[0], ip_used[1], None, None
                else:
                    ipv4, mask, ipv6, ipv6_ll = ip_used[0], ip_used[1], ip_used[2] if len(ip_used) > 2 else None, ip_used[3] if len(ip_used) > 3 else None
                
                if ipv4 != 'Unassigned':
                    if port['name'] in ip_interfaces:
                        ip_interfaces.remove(port['name'])
                
                port_info = {
                    'adapter_number': port['adapter_number'],
                    'port_number': port['port_number'],
                    'name': port['name'],
                    'ip': ipv4,
                    'mask': mask,
                    'ipv6': ipv6,
                    'ipv6_link_local': ipv6_ll,
                    'connected_to': temporary_links.get(f"{node['node_id']}/{port['adapter_number']}/{port['port_number']}", 'Unconnected')
                }
                globals.current_project['device_index'][node_id]['ports'].append(port_info)
                if port_info['ip'] not in ['Unassigned', 'Unknown']:
                    globals.current_project['ips'].append({
                        'ip': port_info['ip'],
                        'node': node['name'],
                        'port': port['name'],
                        'mask': port_info['mask'],
                        'ipv6': port_info.get('ipv6'),
                        'ipv6_link_local': port_info.get('ipv6_link_local'),
                        'connected_to': port_info['connected_to'] if port_info['connected_to'] != 'Unconnected' else None
                    })

            for unused_interface in ip_interfaces:
                # These are probably loopback and virtual ip addresses
                ip_used = port_ip.get(unused_interface, ('Unassigned', 'Unassigned', None, None))
                if len(ip_used) == 2:
                    ipv4, mask, ipv6, ipv6_ll = ip_used[0], ip_used[1], None, None
                else:
                    ipv4, mask, ipv6, ipv6_ll = ip_used[0], ip_used[1], ip_used[2] if len(ip_used) > 2 else None, ip_used[3] if len(ip_used) > 3 else None
                
                globals.current_project['device_index'][node_id]['ports'].append({
                    'adapter_number': 'N/A',
                    'port_number': 'N/A',
                    'name': unused_interface,
                    'ip': ipv4,
                    'mask': mask,
                    'ipv6': ipv6,
                    'ipv6_link_local': ipv6_ll,
                    'connected_to': 'Unconnected'
                })
                if ipv4 not in ['Unassigned', 'Unknown']:
                    globals.current_project['ips'].append({
                        'ip': ipv4,
                        'node': node['name'],
                        'port': unused_interface,
                        'mask': mask,
                        'ipv6': ipv6,
                        'ipv6_link_local': ipv6_ll,
                        'connected_to': None
                    })

            globals.current_project['router_ids'].extend(ospf_bgp_id)
        

        # Wait for all the ips to be gathered before we start linking
        print(term.move_down(2) + term.yellow("Building link connection index!"))
        for node_id, node_data in globals.current_project['device_index'].items():
            for port in node_data['ports']:
                if port['connected_to'] != 'Unconnected':
                    connected_info = port['connected_to']['target'].split('/')
                    connected_node_id = connected_info[0]
                    connected_adapter = connected_info[1]
                    connected_port = connected_info[2]

                    connected_node =  globals.current_project['device_index'][connected_node_id]
                    connected_port_info = list(filter(lambda x: x['adapter_number'] == int(connected_adapter) and x['port_number'] == int(connected_port), connected_node['ports']))
                    if len(connected_port_info) == 1:
                        connected_port_info = connected_port_info[0]
                        port['connected_to'] = {
                            'name': connected_node['name'],
                            'port': connected_port_info['name'],
                            'link_id': port['connected_to']['link_id']
                        }
                        if port['ip'] not in ['Unassigned', 'Unknown']:
                            #FIXME: Cannot find devices without ip addresses!
                            # Update all matching IPs in the list
                            for ip_entry in globals.current_project['ips']:
                                if ip_entry['ip'] == port['ip'] and ip_entry['node'] == node_data['name'] and ip_entry['port'] == port['name']:
                                    ip_entry['connected_to'] = f"{connected_node['name']}:{connected_port_info['name']}"
                    else:
                        print(term.red("Highly unusual port info found!"))
                        print(connected_port_info)

        globals.current_project['last_index'] = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        json.dump(globals.current_project, open(f'data/{globals.current_project["project_id"]}.json', 'w'), indent=4)
        print(term.move_down(2) + term.green("Device index build complete! Press any key to continue..."))
        term.inkey()  # Wait for a key press or timeout