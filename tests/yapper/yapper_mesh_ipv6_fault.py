import os
import asyncio
import re
from time import sleep
from bs4 import BeautifulSoup
import json
import requests
from run_traceroute_v6 import cisco_run_traceroute

# Setup Server Info
server_info_file = open('./data/server.json', 'r', encoding='utf-8')
server_info = json.load(server_info_file)
server_info_file.close()

requests_session = requests.Session()
host = server_info.get("host")
server_port = server_info.get("port")
project_id = "e03c636e-8c33-4ca9-a88d-e55dedec8d98"
username = server_info.get("username")
password = server_info.get("password")

if username:
    requests_session.auth = (username, password)

latest_nodes = {}

# Customers
CUSTOMERS = [
    "YAPPER-USER1",
    "YAPPER-USER2",
    "YAPPER-USER3",
    "YAPPER-USER4"
]

# IPv6 Connectivity Target
IPV6_TARGET = "2001:4860:4860::8888"

# Final Hop Links (from IPv6 file)
final_hop_links = {
    # Yapper Edge R3
    "10.65.1.33": "d66d8ee4-8c0e-4fa8-b2b2-d0f191d6682d",
    "172.17.6.14": "d66d8ee4-8c0e-4fa8-b2b2-d0f191d6682d",
    "172.17.6.1": "d66d8ee4-8c0e-4fa8-b2b2-d0f191d6682d",
    "172.17.6.6": "d66d8ee4-8c0e-4fa8-b2b2-d0f191d6682d",
    "172.17.1.30": "d66d8ee4-8c0e-4fa8-b2b2-d0f191d6682d",
    "172.17.2.30": "d66d8ee4-8c0e-4fa8-b2b2-d0f191d6682d",
    "172.17.6.21": "d66d8ee4-8c0e-4fa8-b2b2-d0f191d6682d",
    # Yapper Edge R4
    "10.65.1.44": "4dfccda3-c54c-48f9-b6da-29e5dcba6564",
    "172.17.6.18": "4dfccda3-c54c-48f9-b6da-29e5dcba6564",
    "172.17.6.2": "4dfccda3-c54c-48f9-b6da-29e5dcba6564",
    "172.17.6.9": "4dfccda3-c54c-48f9-b6da-29e5dcba6564",
    "172.17.1.40": "4dfccda3-c54c-48f9-b6da-29e5dcba6564",
    "172.17.2.40": "4dfccda3-c54c-48f9-b6da-29e5dcba6564",
    "172.17.6.25": "4dfccda3-c54c-48f9-b6da-29e5dcba6564",
    # Magentus-Edge-R1
    "172.18.111.1": "d5472b6c-d8a5-43aa-8a68-44ff28d6260d",
    "172.18.111.13": "2463004b-6ae1-45b9-8e5e-ef19f9093b6a",
    "172.18.111.21": "d6c7a1a8-cb46-4788-a652-2a26aaaf4194",
    # Yapper R1
    "172.18.111.2": "d5472b6c-d8a5-43aa-8a68-44ff28d6260d",
    "172.18.111.9": "84207e8f-7e75-4f5a-aec1-e2633da797b2",
    # Magentus-Edge-R2
    "172.18.111.10": "84207e8f-7e75-4f5a-aec1-e2633da797b2",
    "172.18.111.5": "1de7f299-a4cb-44a3-8d98-31e9bb348b0f",
    "172.18.111.17": "7fd3678a-4eae-4f08-9c22-bbba22832d9d",
    # Yapper-R2
    "172.18.111.6": "1de7f299-a4cb-44a3-8d98-31e9bb348b0f",
    "172.18.111.14": "2463004b-6ae1-45b9-8e5e-ef19f9093b6a",
    # Magentus-Edge-R3
    "10.58.2.33": "49bddd15-24c3-4644-99c1-54d153c8d4d4",
    "172.16.0.5": "49bddd15-24c3-4644-99c1-54d153c8d4d4",
    "172.16.0.2": "49bddd15-24c3-4644-99c1-54d153c8d4d4",
    "172.16.0.61": "49bddd15-24c3-4644-99c1-54d153c8d4d4",
    "172.16.0.65": "49bddd15-24c3-4644-99c1-54d153c8d4d4",
    # Magentus-Edge-R4
    "10.58.2.44": "f33df30e-5211-4448-9e7f-1253748756f3",
    "172.16.0.9": "f33df30e-5211-4448-9e7f-1253748756f3",
    "172.16.0.1": "f33df30e-5211-4448-9e7f-1253748756f3",
    "172.16.0.57": "f33df30e-5211-4448-9e7f-1253748756f3",
    "172.16.0.70": "f33df30e-5211-4448-9e7f-1253748756f3",
    # Magentus-ip6Broker
    "10.58.2.66": "29fd3ba4-7c9f-4a24-9d3e-8c4e75d9b6b1",
    "172.16.0.66": "29fd3ba4-7c9f-4a24-9d3e-8c4e75d9b6b1",
    "172.16.0.69": "29fd3ba4-7c9f-4a24-9d3e-8c4e75d9b6b1",
    "172.16.0.74": "29fd3ba4-7c9f-4a24-9d3e-8c4e75d9b6b1",
    "172.16.0.78": "29fd3ba4-7c9f-4a24-9d3e-8c4e75d9b6b1",
}

async def suspend_router(router, router_id, suspend: bool):
    # (Copied from yapper_ipv6_fault.py)
    if router["template"]["template_type"] == "dynamips":
        if suspend:
            response = requests_session.post(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes/{router_id}/suspend", json={})
            response.raise_for_status()
        else:
            response = requests_session.post(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes/{router_id}/start", json={})
            response.raise_for_status()
    elif router["template"]["template_type"] == "iou":
        if suspend:
            response = requests_session.post(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes/{router_id}/stop", json={})
            response.raise_for_status()
            await asyncio.sleep(2)
            response = requests_session.post(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes/{router_id}/stop", json={})
            response.raise_for_status()
            await asyncio.sleep(2)
        else:
            response = requests_session.post(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes/{router_id}/start", json={})
            response.raise_for_status()
            await asyncio.sleep(10)
    if 'edge' in router['name'].lower():
        print(f"Waiting extra time for edge router {router['name']} to converge OSPF/BGP change...")
        await asyncio.sleep(30)

async def test_customer_connectivity(device_name):
    global latest_nodes
    console = list(filter(lambda n: n["name"] == device_name, latest_nodes))[0]
    for attempt in range(3):
        result = await cisco_run_traceroute(
            console.get("console_host"),
            console.get("console"),
            IPV6_TARGET,
            None,
            device_name=device_name,
        )
        reversed_result = result[::-1]
        success = False
        if len(reversed_result) > 0 and IPV6_TARGET in reversed_result[0]: success = True
        elif len(reversed_result) > 1 and IPV6_TARGET in reversed_result[1]: success = True
        elif len(reversed_result) > 2 and IPV6_TARGET in reversed_result[2]: success = True
        
        if success:
            return result
            
        if attempt < 2:
            print(f"⚠️ {device_name} ping failed (Attempt {attempt+1}/3). Retrying...")
            await asyncio.sleep(2)

    return result

def make_path_dotted_orange(soup, link_id):
    path = soup.select_one(f'[data-link="{link_id}"] path')
    if path:
        current_style = path.get('style', '')
        path['style'] = f"{current_style}; stroke: #FF9800; stroke-dasharray: 10,5"
        path['stroke'] = "#FF9800"
        path['stroke-dasharray'] = "10,5"

async def main():
    global latest_nodes, project_id
    
    # Load Device Index
    f = open("./data/e03c636e-8c33-4ca9-a88d-e55dedec8d98.json", "r", encoding="utf-8")
    data = f.read()
    f.close()
    json_data = json.loads(data)
    
    yapper_devices = []
    all_yapper_devices = []
    ip_to_link_id = {}
    
    for device in json_data["device_index"]:
        device_id = device
        device = json_data["device_index"][device]
        device["id"] = device_id
        
        for port in device["ports"]:
             if port["connected_to"] != None and port["connected_to"] != "Unconnected":
                ip_to_link_id[port["ip"]] = port["connected_to"]["link_id"]
                if port["ipv6"] != None:
                    ip_to_link_id[port["ipv6"].split('/')[0].lower()] = port["connected_to"]["link_id"]
        
        if "yapper" in device["name"].lower():
            all_yapper_devices.append(device)
            if device["name"] == "YAPPER-Monitoring-SW" or device["name"] == "GrayLogSrv" or device["name"] == "YAPPER-EDGE-IP6Broker":
                continue
            yapper_devices.append(device)
            print(f'Found device: {device["name"]}')
            
    print(f"Total Yapper devices: {len(yapper_devices)}")
    
    # Identify Mesh Routers
    mesh_routers = list(filter(lambda d: 'mesh' in d['name'].lower(), yapper_devices))
    print(f"Found Mesh Routers: {[r['name'] for r in mesh_routers]}")

    # Open Markdown report
    final_output = open('./tests/yapper/yapper_mesh_ipv6_fault.md', 'w', encoding='utf-8')
    final_output.write("# Yapper \"Mesh IPv6 Fault\" tesztelési jegyzőkönyv\n\n")
    final_output.write('<div style="page-break-after: always;"></div>\n\n')

    # Load Base SVG
    f = open('./tests/yapper/YAPPER-TESTING.drawio.svg', 'r', encoding='utf-8')
    svg_data = f.read()
    f.close()

    soup = BeautifulSoup(svg_data, 'xml')

    # Disable Mesh Routers and Red-out in SVG
    for router in mesh_routers:
        paths = soup.select(f'[data-link=\"{router['id']}\"] path')
        if paths:
            path = paths[-1]
            current_style = path.get('style', '')
            path['style'] = f"{current_style}; fill: red; opacity: 0.5"
            path['fill'] = "red"
            path['opacity'] = "0.5"
            for port in router['ports']:
                if port['connected_to'] != 'Unconnected' and port['connected_to'] is not None:
                     link = port['connected_to']['link_id']
                     link_path = soup.select_one(f'[data-link="{link}"] path')
                     if link_path:
                        current_style = link_path.get('style', '')
                        link_path['style'] = f"{current_style}; stroke: red;"
                        link_path['stroke'] = "red"
        
        print(f"Disabling router {router['name']}...")
        await suspend_router(router, router['id'], True)
    
    # Save Mesh Fault SVG
    if not os.path.exists(f'./tests/yapper/images/ipv6_mesh/'):
        os.makedirs(f'./tests/yapper/images/ipv6_mesh/')
        
    f = open(f'./tests/yapper/images/ipv6_mesh/mesh.svg', 'w', encoding='utf-8')
    f.write(str(soup))
    f.close()
    
    print("Success: SVG Path modified and saved.")
    print(f"Waiting 10 seconds for routing to converge...")
    
    # Write Header to MD
    final_output.write(f"## Hiba szimuláció: Mesh Routers ({', '.join([r['name'] for r in mesh_routers])})\n\n")
    final_output.write(f"<img src=\"images/ipv6_mesh/mesh.svg\" style=\"display: block; margin: 0 auto; width: 450px;\">\n\n")
    
    await asyncio.sleep(10)

    # Run Connectivity Tests
    print("Running ping on customer devices...")
    if latest_nodes == {}:
        response = requests_session.get(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes")
        response.raise_for_status()
        latest_nodes = response.json()
        
    ping_tasks = [test_customer_connectivity(customer) for customer in CUSTOMERS]
    results = await asyncio.gather(*ping_tasks)
    
    final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">\n')
    
    for i in range(len(results)):
        # Reload red SVG for each customer to draw orange path on top
        f = open(f'./tests/yapper/images/ipv6_mesh/mesh.svg', 'r', encoding='utf-8')
        customer_soup = BeautifulSoup(f.read(), 'xml')
        f.close()
        
        customer = CUSTOMERS[i]
        result = results[i][::-1] # Reverse for easier checking of last hops
        
        final_output.write('  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">\n')

        # Check success
        success = False
        if len(result) > 0 and IPV6_TARGET in result[0]: success = True
        elif len(result) > 1 and IPV6_TARGET in result[1]: success = True
        elif len(result) > 2 and IPV6_TARGET in result[2]: success = True
        
        if success:
            print(f"✅ {customer} ping successful!")
            final_output.write(f"    <h4>{customer} ✅</h4>\n")
            
            # Find RTT
            success_line = ""
            for r in result:
                if IPV6_TARGET in r:
                    success_line = r
                    break
            
            # Formatting success line
            parts = success_line.strip().split(' ')
            if parts[0].isdigit():
                 success_line_txt = ' '.join(parts[1:])
            else:
                 success_line_txt = ' '.join(parts)
            success_line_txt = success_line_txt.replace(' msec', 'ms').replace(' *', '')
            final_output.write(f"    <p><strong>Sikeres ping!</strong> {success_line_txt}</p>\n")
            
            # Trace Path Drawing
            # Reverse back to standard order for path tracing
            trace_result = result[::-1] 
            
            for j in range(len(trace_result)):
                hop = trace_result[j]
                # Extract IPv6 address
                ip_in_line = re.findall(r'[a-fA-F0-9]{1,4}(?::[a-fA-F0-9]{0,4})+', hop)
                
                if len(ip_in_line) == 0:
                    continue
                
                current_ip = ip_in_line[0].lower()
                
                if current_ip in ip_to_link_id:
                     make_path_dotted_orange(customer_soup, ip_to_link_id.get(current_ip, ''))
                elif current_ip in final_hop_links:
                     make_path_dotted_orange(customer_soup, final_hop_links.get(current_ip))
                
                # Special logic for Mesh network (copied from yapper_ipv6_fault.py)
                if '2001:470:2171:aaaa:aaaa:0001::' in current_ip or '2001:470:2171:aaaa:aaaa:1:' in current_ip:
                     # Need to look back to find the link going into the switch
                     temp_j = j
                     # Look for previous valid hop
                     prev_hop = ""
                     while temp_j > 0:
                         temp_j -= 1
                         possible = trace_result[temp_j]
                         if possible.strip().split(' ')[0].isdigit(): # Simple check if line is valid hop line
                             prev_hop = possible
                             break
                     
                     if prev_hop:
                         prev_ips = re.findall(r'[a-fA-F0-9]{1,4}(?::[a-fA-F0-9]{0,4})+', prev_hop)
                         if len(prev_ips) > 0:
                             prev_ip = prev_ips[0].lower()
                             
                             # Search for router/interface connecting to this prev_ip
                             routerp = None
                             for r in all_yapper_devices:
                                 for p in r['ports']:
                                     if p is not None and p.get('ipv6') and p.get('ipv6').lower().split('/')[0] == prev_ip:
                                         routerp = r
                                         break
                             
                             if routerp:
                                 # Find link to MESH
                                 for sport in routerp['ports']:
                                     if sport['connected_to'] != 'Unconnected' and sport['connected_to'] is not None:
                                         if 'YAPPER-MESH1' in sport['connected_to'].get('name', ''):
                                              make_path_dotted_orange(customer_soup, sport['connected_to']['link_id'])
                                              print(f"Highlighting MESH link from {routerp['name']}")

            # Save Customer SVG
            f = open(f'./tests/yapper/images/ipv6_mesh/{customer}.svg', 'w', encoding='utf-8')
            f.write(str(customer_soup))
            f.close()
            final_output.write(f'    <img src="./images/ipv6_mesh/{customer}.svg" width="100%">\n')

        else:
            print(f"❌ {customer} ping failed!")
            final_output.write(f"    <h4>{customer} ❌</h4>\n")
            final_output.write("    <p><strong>Sikertelen ping!</strong></p>\n")
        
        final_output.write("  </div>\n")

    final_output.write("</div>\n\n")
    final_output.write('<div style="page-break-after: always;"></div>\n\n')
    
    # Restore Mesh Routers
    print("Tests finished, Re-enabling mesh routers...")
    for router in mesh_routers:
        await suspend_router(router, router["id"], False)
    
    await asyncio.sleep(5)
    final_output.close()

asyncio.run(main())
