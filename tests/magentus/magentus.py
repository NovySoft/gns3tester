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

def suspend_link(link_id, suspend: bool):
    response = requests_session.put(f"http://{host}:{server_port}/v2/projects/{project_id}/links/{link_id}", json={
        "suspend": suspend
    })
    response.raise_for_status()
    print(response.json())

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
        device = json_data["device_index"][device]
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

    final_output = open('./tests/magentus/magentus.md', 'w', encoding='utf-8')
    final_output.write("# Magentus tesztelési jegyzőkönyv\n\n")

    f = open('./tests/magentus/MAGENTUS_TESTING.drawio.svg', 'r', encoding='utf-8')
    svg_data = f.read()
    f.close()
    for link in magentus_links:
        parent_id = link

        # Make dsabled path red, and save to a new SVG file, and write to documentation
        soup = BeautifulSoup(svg_data, 'xml')
        path = soup.select_one(f'[data-link="{parent_id}"] path')
        if path:
            current_style = path.get('style', '')
            path['style'] = f"{current_style}; stroke: red"
            path['stroke'] = "red"
            if not os.path.exists(f'./tests/magentus/images/fault1/{link}/'):
                os.makedirs(f'./tests/magentus/images/fault1/{link}/')
            f = open(f'./tests/magentus/images/fault1/{link}/{link}.svg', 'w', encoding='utf-8')
            f.write(str(soup))
            f.close()
            print("Success: SVG Path found and made red, written to docs.")
            final_output.write(f"## Hiba szimuláció: {links_end_devices[link]['device1']} - {links_end_devices[link]['device2']}\n\n")
            final_output.write(f"![Hiba szimuláció](./images/fault1/{link}/{link}.svg)\n\n")
            print("Disabling link waiting 10 seconds for ospf to converge...")
            suspend_link(link, True)
            await asyncio.sleep(10)  # Wait for 10 seconds
            print("Running ping on customer devices...")
            # Run pings in parallel
            if latest_nodes == {}:
                response = requests_session.get(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes")
                response.raise_for_status()
                latest_nodes = response.json()
            ping_tasks = [test_customer_connectivity(customer) for customer in CUSTOMERS]
            results = await asyncio.gather(*ping_tasks)
            for i in range(len(results)):
                red_line_svg_file = open(f'./tests/magentus/images/fault1/{link}/{link}.svg', 'r', encoding='utf-8')
                soup = BeautifulSoup(red_line_svg_file.read(), 'xml')
                red_line_svg_file.close()
                customer = CUSTOMERS[i]
                result = results[i][::-1]
                if '1.1.1.1' in result[0] or '1.1.1.1' in result[1] or '1.1.1.1' in result[2]:
                    print(f"✅ {customer} ping successful!")
                    final_output.write(f"### {customer} traceroute ✅\n")
                    final_output.write("**Sikeres ping!**  ")
                    if '1.1.1.1' in result[0]:
                        final_output.write(result[0] + "  \n")
                    elif '1.1.1.1' in result[1]:
                        final_output.write(result[1] + "  \n")
                    elif '1.1.1.1' in result[2]:
                        final_output.write(result[2] + "  \n")
                    final_output.write("\n")
                    result = result[::-1]
                    for i in range(len(result)):
                        hop = result[i]
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
                            prev_hop = result[i-1]
                            prev_ip_in_line = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', prev_hop)
                            if prev_ip_in_line[0] in final_hop_links:
                               link_id = final_hop_links.get(prev_ip_in_line[0])
                               make_path_dotted_orange(soup, link_id)
                            while not prev_hop.strip().split(' ')[0].isdigit():
                                i -= 1
                                prev_hop = result[i-1]
                                prev_ip_in_line = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', prev_hop)
                                link_id = final_hop_links.get(prev_ip_in_line[0])
                                make_path_dotted_orange(soup, link_id)
                    f = open(f'./tests/magentus/images/fault1/{link}/{link}-{customer}.svg', 'w', encoding='utf-8')
                    f.write(str(soup))
                    f.close()
                    final_output.write("Traceroute útvonal:  \n")
                    final_output.write(f"![Traceroute útvonal](./images/fault1/{link}/{link}-{customer}.svg)\n\n")
                else:
                    print(f"❌ {customer} ping failed!")
                    final_output.write(f"### {customer} traceroute ❌\n")
                    final_output.write("**Sikertelen ping!**  \n\n")
            print("Tests finished, Re-enabling the link...")
            suspend_link(link, False)
            await asyncio.sleep(5)  # Wait for 5 seconds to reable the link
        else:
            print(f"Error: Could not find the path with {link}")

    print()
    final_output.close()

asyncio.run(main())