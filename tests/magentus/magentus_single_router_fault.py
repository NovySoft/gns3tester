import os
import asyncio
import re
from time import sleep
from bs4 import BeautifulSoup
import json
import requests

from run_traceroute import cisco_run_traceroute
server_info_file = open('./data/server.json', 'r', encoding='utf-8')
server_info = json.load(server_info_file)
server_info_file.close()
requests_session = requests.Session()
host = server_info.get("host")
server_port = server_info.get("port")
project_id = "e03c636e-8c33-4ca9-a88d-e55dedec8d98"  # Magentus ISP project ID
username = server_info.get("username")
password = server_info.get("password")
# Authenticate
requests_session.auth = (username, password) if username else None
latest_nodes = {}
CUSTOMERS = [
    "MAGENTUS-Customer1",
    "MAGENTUS-Customer2",
    "MAGENTUS-Customer3",
    "MAGENTUS-Customer4"
]
CUSTOMER_IPS = {
    "MAGENTUS-Customer1": "172.16.254.1",
    "MAGENTUS-Customer2": "172.16.254.9",
    "MAGENTUS-Customer3": "172.16.254.17",
    "MAGENTUS-Customer4": "172.16.254.25",
}
final_hop_links = {
    # Edge-R1
    "172.18.111.1": "d5472b6c-d8a5-43aa-8a68-44ff28d6260d",
    "172.18.111.13": "2463004b-6ae1-45b9-8e5e-ef19f9093b6a",
    "172.18.111.21": "d6c7a1a8-cb46-4788-a652-2a26aaaf4194",
    # Edge-R2
    "172.18.111.10": "84207e8f-7e75-4f5a-aec1-e2633da797b2",
    "172.18.111.5": "1de7f299-a4cb-44a3-8d98-31e9bb348b0f",
    "172.18.111.17": "7fd3678a-4eae-4f08-9c22-bbba22832d9d",
    # Edge-R3
    "10.58.2.33": "49bddd15-24c3-4644-99c1-54d153c8d4d4",
    "172.16.0.5": "49bddd15-24c3-4644-99c1-54d153c8d4d4",
    "172.16.0.2": "49bddd15-24c3-4644-99c1-54d153c8d4d4",
    "172.16.0.61": "49bddd15-24c3-4644-99c1-54d153c8d4d4",
    "172.16.0.65": "49bddd15-24c3-4644-99c1-54d153c8d4d4",
    # Edge-R4
    "10.58.2.44": "f33df30e-5211-4448-9e7f-1253748756f3",
    "172.16.0.9": "f33df30e-5211-4448-9e7f-1253748756f3",
    "172.16.0.1": "f33df30e-5211-4448-9e7f-1253748756f3",
    "172.16.0.57": "f33df30e-5211-4448-9e7f-1253748756f3",
    "172.16.0.70": "f33df30e-5211-4448-9e7f-1253748756f3",
    # ip6Broker
    "10.58.2.66": "29fd3ba4-7c9f-4a24-9d3e-8c4e75d9b6b1",
    "172.16.0.66": "29fd3ba4-7c9f-4a24-9d3e-8c4e75d9b6b1",
    "172.16.0.69": "29fd3ba4-7c9f-4a24-9d3e-8c4e75d9b6b1",
    "172.16.0.74": "29fd3ba4-7c9f-4a24-9d3e-8c4e75d9b6b1",
    "172.16.0.78": "29fd3ba4-7c9f-4a24-9d3e-8c4e75d9b6b1",
}

def suspend_router(router_id, suspend: bool):
    if suspend:
        response = requests_session.post(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes/{router_id}/suspend", json={})
        response.raise_for_status()
        #print(response.json())
    else:
        response = requests_session.post(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes/{router_id}/start", json={})
        response.raise_for_status()
        #print(response.json())

async def instant_fail():
    return ["FAIL"]

async def test_customer_connectivity(device_name):
    global latest_nodes
    console = list(filter(lambda n: n["name"] == device_name, latest_nodes))[0]
    for attempt in range(3):
        result = await cisco_run_traceroute(
            console.get("console_host"),
            console.get("console"),
            "1.1.1.1",
            CUSTOMER_IPS[device_name],
            device_name=device_name,
        )
        # Check if successful - logic mirrored from main()
        reversed_result = result[::-1]
        success = False
        if len(reversed_result) > 0 and '1.1.1.1' in reversed_result[0]: success = True
        elif len(reversed_result) > 1 and '1.1.1.1' in reversed_result[1]: success = True
        elif len(reversed_result) > 2 and '1.1.1.1' in reversed_result[2]: success = True
        
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
    # Test magentus ISP
    f = open("./data/e03c636e-8c33-4ca9-a88d-e55dedec8d98.json", "r", encoding="utf-8")
    # Parse the JSON file
    data = f.read()
    f.close()
    json_data = json.loads(data)
    magentus_devices = []
    magentus_links = []
    links_end_devices = {}
    ip_to_link_id = {}
    for device in json_data["device_index"]:
        device_id = device
        device = json_data["device_index"][device]
        device["id"] = device_id
        if "magentus" in device["name"].lower():
            if device["name"] == "MAGENTUS-MGMT-SW" or device["name"] == "Magentus-LibreNMS":
                continue
                
            magentus_devices.append(device)
            print(f"Found Magentus device: {device['name']}")
            for port in device["ports"]:
                if port["connected_to"] != 'Unconnected':
                    ip_to_link_id[port["ip"]] = port["connected_to"]["link_id"]
                    if port["ipv6"] != None:
                        ip_to_link_id[port["ipv6"]] = port["connected_to"]["link_id"]
                    """ magentus_links.append({
                        "device_name": device["name"],
                        "port_name": port["name"],
                        "connected_to": {
                            "device": port["connected_to"]["name"],
                            "id": port["connected_to"]["link_id"]
                        }
                    }) """
                    if port["connected_to"]["link_id"] not in magentus_links:
                        links_end_devices[port["connected_to"]["link_id"]] = {
                            "device1": device["name"],
                            "device2": port["connected_to"]["name"]
                        }
                        if port['connected_to']["name"] == "MAGENTUS-MGMT-SW" or \
                            port['connected_to']["name"] == "HQ-CORE-R1" or \
                                port['connected_to']["name"] == "Bemutat-R1" or\
                                    port['connected_to']["name"].lower().startswith('pppoe-test') or \
                                        port['connected_to']["name"].lower().startswith("magentus-customer") or \
                                            device['name'].lower().startswith("magentus-customer"):
                            continue
                        magentus_links.append(port["connected_to"]["link_id"])

    print(f"Total Magentus devices found: {len(magentus_devices)}")
    print(f"Total Magentus INTRANET links found: {len(magentus_links)}")

    final_output = open('./tests/magentus/magentus_single_router_fault.md', 'w', encoding='utf-8')
    final_output.write("# Magentus \"Single Router Fault\" tesztelési jegyzőkönyv\n\n")
    final_output.write('<div style="page-break-after: always;"></div>\n\n')

    f = open('./tests/magentus/MAGENTUS_TESTING.drawio.svg', 'r', encoding='utf-8')
    svg_data = f.read()
    f.close()
    for router in magentus_devices:
        if "customer" in router['name'].lower():
            continue
        # Make dsabled path red, and save to a new SVG file, and write to documentation
        soup = BeautifulSoup(svg_data, 'xml')
        path = soup.select_one(f'[data-link=\"{router['id']}\"] g[transform] path')
        if router['name'] == "MAGENTUS-CORE-R1":
            # Magentus core-r1 down means customer 2 down
            customer_router = soup.select_one(f'[data-link=\"671cfbcc-5a95-4734-9583-67eff23c785e\"] g[transform] path')
            if customer_router:
                current_style = customer_router.get('style', '')
                customer_router['style'] = f"{current_style}; fill: red; opacity: 0.5"
                customer_router['fill'] = "red"
                customer_router['opacity'] = "0.5"
        if router['name'] == "MAGENTUS-CORE-R3":
            # Magentus core-r1 down means customer 4 down
            customer_router = soup.select_one(f'[data-link=\"72972876-4410-4f66-aee1-22fe34919738\"] g[transform] path')
            if customer_router:
                current_style = customer_router.get('style', '')
                customer_router['style'] = f"{current_style}; fill: red; opacity: 0.5"
                customer_router['fill'] = "red"
                customer_router['opacity'] = "0.5"
        if path:
            current_style = path.get('style', '')
            path['style'] = f"{current_style}; fill: red; opacity: 0.5"
            path['fill'] = "red"
            path['opacity'] = "0.5"
            for port in router['ports']:
                if port['connected_to'] != 'Unconnected':
                    link = port['connected_to']['link_id']
                    link_path = soup.select_one(f'[data-link="{link}"] path')
                    if link_path:
                        current_style = link_path.get('style', '')
                        link_path['style'] = f"{current_style}; stroke: red;"
                        link_path['stroke'] = "red"
            
            if not os.path.exists(f'./tests/magentus/images/fault1_router/{router['id']}/'):
                os.makedirs(f'./tests/magentus/images/fault1_router/{router['id']}/')        
            f = open(f'./tests/magentus/images/fault1_router/{router['id']}/{router['id']}.svg', 'w', encoding='utf-8')
            f.write(str(soup))
            f.close()
            print("Success: SVG Path found and made red, written to docs.")
            print(f"Disabling router {router['name']}, waiting 10 seconds for ospf to converge...")
            suspend_router(router['id'], True)
            final_output.write(f"## Hiba szimuláció: {router['name']}\n\n")
            final_output.write(f"<img src=\"images/fault1_router/{router['id']}/{router['id']}.svg\" style=\"display: block; margin: 0 auto; width: 500px;\">\n\n")
            await asyncio.sleep(10)  # Wait for 10 seconds
            print("Running ping on customer devices...")
            # Run pings in parallel
            if latest_nodes == {}:
                response = requests_session.get(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes")
                response.raise_for_status()
                latest_nodes = response.json()
            if router['name'] == "MAGENTUS-CORE-R1":
                ping_tasks = [
                    test_customer_connectivity("MAGENTUS-Customer1"),
                    instant_fail(),
                    test_customer_connectivity("MAGENTUS-Customer3"),
                    test_customer_connectivity("MAGENTUS-Customer4"),
                ]
            elif router['name'] == "MAGENTUS-CORE-R3":
                ping_tasks = [
                    test_customer_connectivity("MAGENTUS-Customer1"),
                    test_customer_connectivity("MAGENTUS-Customer2"),
                    test_customer_connectivity("MAGENTUS-Customer3"),
                    instant_fail(),
                ]
            else:
                ping_tasks = [test_customer_connectivity(customer) for customer in CUSTOMERS]
            results = await asyncio.gather(*ping_tasks)
            final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">\n')
            for i in range(len(results)):
                red_line_svg_file = open(f'./tests/magentus/images/fault1_router/{router["id"]}/{router["id"]}.svg', 'r', encoding='utf-8')
                soup = BeautifulSoup(red_line_svg_file.read(), 'xml')
                red_line_svg_file.close()
                customer = CUSTOMERS[i]
                result = results[i][::-1]
                
                final_output.write('  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">\n')
                
                if (len(result) > 0 and '1.1.1.1' in result[0]) or \
                   (len(result) > 1 and '1.1.1.1' in result[1]) or \
                   (len(result) > 2 and '1.1.1.1' in result[2]):
                    print(f"✅ {customer} ping successful!")
                    final_output.write(f"    <h4>{customer} ✅</h4>\n")
                    
                    success_line = ""
                    if len(result) > 0 and '1.1.1.1' in result[0]:
                        success_line = result[0]
                    elif len(result) > 1 and '1.1.1.1' in result[1]:
                        success_line = result[1]
                    elif len(result) > 2 and '1.1.1.1' in result[2]:
                        success_line = result[2]
                        
                    success_line = success_line.strip().split(' ')
                    if success_line[0].isdigit():
                        success_line = ' '.join(success_line[1:])
                    else:
                        success_line = ' '.join(success_line)
                    final_output.write(f"    <p><strong>Sikeres ping!</strong> {success_line}</p>\n")
                    
                    result = result[::-1]
                    for j in range(len(result)):
                        hop = result[j]
                        ip_in_line = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', hop)
                        if len(ip_in_line) == 0:
                            continue
                        if ip_in_line[0] in ip_to_link_id:
                            make_path_dotted_orange(soup, ip_to_link_id.get(ip_in_line[0], ''))
                        # Last part of our internal network is
                        # The problem is that this is not in the ip_to_link_id map
                        # We need to figure out the previous hop to highlight the corect link(s)
                        if ip_in_line[0] == '10.58.2.1':
                            # Check if there is a number before the ip in the hop line
                            temp_j = j
                            prev_hop = result[temp_j-1]
                            prev_ip_in_line = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', prev_hop)
                            if len(prev_ip_in_line) > 0 and prev_ip_in_line[0] in final_hop_links:
                               link_id = final_hop_links.get(prev_ip_in_line[0])
                               make_path_dotted_orange(soup, link_id)
                            while not prev_hop.strip().split(' ')[0].isdigit():
                                temp_j -= 1
                                prev_hop = result[temp_j-1]
                                prev_ip_in_line = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', prev_hop)
                                if len(prev_ip_in_line) > 0:
                                    link_id = final_hop_links.get(prev_ip_in_line[0])
                                    make_path_dotted_orange(soup, link_id)
                    f = open(f'./tests/magentus/images/fault1_router/{router["id"]}/{router["id"]}-{customer}.svg', 'w', encoding='utf-8')
                    f.write(str(soup))
                    f.close()
                    final_output.write(f'    <img src="./images/fault1_router/{router["id"]}/{router["id"]}-{customer}.svg" width="100%">\n')
                else:
                    print(f"❌ {customer} ping failed!")
                    final_output.write(f"    <h4>{customer} ❌</h4>\n")
                    final_output.write("    <p><strong>Sikertelen ping!</strong></p>\n")
                
                final_output.write("  </div>\n")
            
            final_output.write("</div>\n\n")
            final_output.write('<div style="page-break-after: always;"></div>\n\n')
            print("Tests finished, Re-enabling the router...")
            suspend_router(router["id"], False)
            await asyncio.sleep(5)  # Wait for 5 seconds to reable the router
        else:
            print(f"Error: Could not find the router with {router['id']}")

    print()
    final_output.close()

asyncio.run(main())