import json
import globals
from globals import term
from network_manager import NetworkManager

def device_index_builder_screen():
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
            for port in node.get('ports', []):
                port_info = {
                    'adapter_number': port['adapter_number'],
                    'port_number': port['port_number'],
                    'name': port['name'],
                    'ip': 'Unknown',
                    'mask': 'Unknown',
                    'connected_to': temporary_links.get(f"{node['node_id']}/{port['adapter_number']}/{port['port_number']}", 'Unconnected')
                }
                globals.current_project['device_index'][node['node_id']]['ports'].append(port_info)

            if node['status'] == "stopped":
                print(term.red(f"Node {node['name']} is stopped. Cannot get IP information!"))
            else:
                if 'cisco' in globals.current_project['device_index'][node['node_id']]['template']['name'].lower():
                    # Cisco device, use telnet and ip interface to check ip address and subnet mask

        
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


        json.dump(globals.current_project, open(f'data/{globals.current_project["project_id"]}.json', 'w'), indent=4)
        term.inkey()  # Wait for a key press or timeout