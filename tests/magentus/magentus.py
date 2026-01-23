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

def suspend_link(link_id, suspend: bool):
    response = requests_session.put(f"http://{host}:{server_port}/v2/projects/{project_id}/links/{link_id}", json={
        "suspend": suspend
    })
    response.raise_for_status()
    print(response.json())

async def test_customer_connectivity(device_name):
    global latest_nodes
    console = list(filter(lambda n: n["name"] == device_name, latest_nodes))[0]
    result = await cisco_run_traceroute(
        console.get("console_host"),
        console.get("console"),
        "1.1.1.1",
        CUSTOMER_IPS[device_name],
        device_name=device_name,
    )
    return result

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
            f = open(f'./tests/magentus/images/fault1/{link}.svg', 'w', encoding='utf-8')
            f.write(str(soup))
            f.close()
            continue
            print("Success: SVG Path found and made red, written to docs.")
            final_output.write(f"## Hiba szimuláció: {links_end_devices[link]['device1']} - {links_end_devices[link]['device2']}\n\n")
            final_output.write(f"![Hiba szimuláció](./images/fault1/{link}.svg)\n\n")
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
                    for hop in result:
                        ip_in_line = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', hop)
                        print(ip_in_line)
                else:
                    print(f"❌ {customer} ping failed!")
                    final_output.write(f"### {customer} traceroute ❌\n")
                    final_output.write("**Sikertelen ping!**  \n\n")
            print("Tests finished, Re-enabling the link...")
            suspend_link(link, False)
            await asyncio.sleep(5)  # Wait for 5 seconds to reable the link
            break
        else:
            print(f"Error: Could not find the path with {link}")

    print()
    final_output.close()

asyncio.run(main())