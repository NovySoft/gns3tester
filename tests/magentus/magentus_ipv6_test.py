import os
import asyncio
import re
from time import sleep
from bs4 import BeautifulSoup
import json
import requests
from run_traceroute_v6 import cisco_run_traceroute
server_info_file = open('./data/server.json', 'r', encoding='utf-8')
server_info = json.load(server_info_file)
server_info_file.close()
requests_session = requests.Session()
host = server_info.get("host")
server_port = server_info.get("port")
project_id = "e03c636e-8c33-4ca9-a88d-e55dedec8d98"
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
    "MAGENTUS-Customer1": "2001:470:216f:1ff0::1",
    "MAGENTUS-Customer2": "2001:470:216f:2ff0::1",
    "MAGENTUS-Customer3": "2001:470:216f:3ff0::1",
    "MAGENTUS-Customer4": "2001:470:216f:4ff0::1",
}
final_hop_links = {

}

async def instant_fail():
    return ["FAIL"]

async def suspend_router(router, router_id, suspend: bool):
    if router["template"]["template_type"] == "dynamips":
        if suspend:
            response = requests_session.post(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes/{router_id}/suspend", json={})
            response.raise_for_status()
            #print(response.json())
        else:
            response = requests_session.post(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes/{router_id}/start", json={})
            response.raise_for_status()
            #print(response.json())
    elif router["template"]["template_type"] == "iou":
        if suspend:
            response = requests_session.post(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes/{router_id}/stop", json={})
            response.raise_for_status()
            #print(response.json())
            await asyncio.sleep(2)
            response = requests_session.post(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes/{router_id}/stop", json={})
            response.raise_for_status()
            await asyncio.sleep(2)
        else:
            response = requests_session.post(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes/{router_id}/start", json={})
            response.raise_for_status()
            #print(response.json())
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
            "2001:4860:4860::8888",
            CUSTOMER_IPS[device_name],
            device_name=device_name,
        )
        # Check if successful - logic mirrored from main()
        reversed_result = result[::-1]
        success = False
        if len(reversed_result) > 0 and '2001:4860:4860::8888' in reversed_result[0]: success = True
        elif len(reversed_result) > 1 and '2001:4860:4860::8888' in reversed_result[1]: success = True
        elif len(reversed_result) > 2 and '2001:4860:4860::8888' in reversed_result[2]: success = True
        
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
    core_devices = []
    all_devices = []
    yapper_links = []
    links_end_devices = {}
    ip_to_link_id = {}
    for device in json_data["device_index"]:
        device_id = device
        device = json_data["device_index"][device]
        device["id"] = device_id
        if "magentus" in device["name"].lower():
            if device["name"] == "MAGENTUS-MGMT-SW" or device["name"] == "Magentus-LibreNMS":
                continue
                
            all_devices.append(device)
            for port in device["ports"]:
                if port["connected_to"] != 'Unconnected':
                    ip_to_link_id[port["ip"]] = port["connected_to"]["link_id"]
                    if port["ipv6"] != None:
                        ip_to_link_id[port["ipv6"]] = port["connected_to"]["link_id"]
            print(f'Found device: {device["name"]}')
    print(f"Total Magentus devices: {len(all_devices)}")
    final_output = open('./tests/magentus/magentus_ipv6_fault.md', 'w', encoding='utf-8')
    final_output.write("# Magentus \"IPv6\" tesztelési jegyzőkönyv\n\n")
    final_output.write('<div style="page-break-after: always;"></div>\n\n')

    f = open('./tests/magentus/MAGENTUS_TESTING.drawio.svg', 'r', encoding='utf-8')
    svg_data = f.read()
    f.close()
    for router in all_devices:
        if "customer" in router['name'].lower() or "ip6" in router['name'].lower():
            continue
        # Make disabled router red, and save to a new SVG file, and write to documentation
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

        if not os.path.exists(f'./tests/magentus/images/ipv6/{router['id']}/'):
            os.makedirs(f'./tests/magentus/images/ipv6/{router['id']}/')  
        f = open(f'./tests/magentus/images/ipv6/{router['id']}/{router['id']}.svg', 'w', encoding='utf-8')
        f.write(str(soup))
        f.close()
        print("Success: SVG Path found and made red, written to docs.")
        print(f"Disabling router {router['name']}, waiting 10 seconds for ospf to converge...")
        await suspend_router(router, router['id'], True)
        final_output.write(f"## Hiba szimuláció: {router['name']}\n\n")
        final_output.write(f"<img src=\"images/ipv6/{router['id']}/{router['id']}.svg\" style=\"display: block; margin: 0 auto; width: 450px;\">\n\n")
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
            red_line_svg_file = open(f'./tests/magentus/images/ipv6/{router["id"]}/{router["id"]}.svg', 'r', encoding='utf-8')
            soup = BeautifulSoup(red_line_svg_file.read(), 'xml')
            red_line_svg_file.close()
            customer = CUSTOMERS[i]
            result = results[i][::-1]
            
            final_output.write('  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">\n')
            
            if (len(result) > 0 and '2001:4860:4860::8888' in result[0]) or \
                (len(result) > 1 and '2001:4860:4860::8888' in result[1]) or \
                (len(result) > 2 and '2001:4860:4860::8888' in result[2]):
                print(f"✅ {customer} ping successful!")
                final_output.write(f"    <h4>{customer} ✅</h4>\n")
                
                success_line = ""
                if len(result) > 0 and '2001:4860:4860::8888' in result[0]:
                    success_line = result[0]
                elif len(result) > 1 and '2001:4860:4860::8888' in result[1]:
                    success_line = result[1]
                elif len(result) > 2 and '2001:4860:4860::8888' in result[2]:
                    success_line = result[2]
                    
                success_line = success_line.strip().split(' ')
                if success_line[0].isdigit():
                    success_line = ' '.join(success_line[1:])
                else:
                    success_line = ' '.join(success_line)
                success_line = success_line.replace(' msec', 'ms').replace(' *', '')
                final_output.write(f"    <p><strong>Sikeres ping!</strong> {success_line}</p>\n")
                
                result = result[::-1]
                for j in range(len(result)):
                    hop = result[j]
                    ip_in_line = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', hop)
                    if len(ip_in_line) == 0:
                        continue
                    if ip_in_line[0] in ip_to_link_id:
                        make_path_dotted_orange(soup, ip_to_link_id.get(ip_in_line[0], ''))
                    elif ip_in_line[0] in final_hop_links:
                        link_id = final_hop_links.get(ip_in_line[0])
                        make_path_dotted_orange(soup, link_id)
                f = open(f'./tests/magentus/images/ipv6/{router["id"]}/{router["id"]}-{customer}.svg', 'w', encoding='utf-8')
                f.write(str(soup))
                f.close()
                final_output.write(f'    <img src="./images/ipv6/{router["id"]}/{router["id"]}-{customer}.svg" width="100%">\n')
            else:
                print(f"❌ {customer} ping failed!")
                final_output.write(f"    <h4>{customer} ❌</h4>\n")
                final_output.write("    <p><strong>Sikertelen ping!</strong></p>\n")
            
            final_output.write("  </div>\n")
        
        final_output.write("</div>\n\n")
        final_output.write('<div style="page-break-after: always;"></div>\n\n')
        print("Tests finished, Re-enabling the router...")
        await suspend_router(router, router["id"], False)
        await asyncio.sleep(5)
        
asyncio.run(main())