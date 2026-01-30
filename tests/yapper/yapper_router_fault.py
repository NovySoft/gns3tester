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
project_id = "e03c636e-8c33-4ca9-a88d-e55dedec8d98"
username = server_info.get("username")
password = server_info.get("password")
# Authenticate
requests_session.auth = (username, password) if username else None
latest_nodes = {}
CUSTOMERS = [
    "YAPPER-CUSTOMER1",
    "YAPPER-CUSTOMER2",
    "YAPPER-CUSTOMER3",
    "YAPPER-CUSTOMER4"
]
CUSTOMER_IPS = {
    "YAPPER-CUSTOMER1": "172.17.254.1",
    "YAPPER-CUSTOMER2": "172.17.254.9",
    "YAPPER-CUSTOMER3": "172.17.254.17",
    "YAPPER-CUSTOMER4": "172.17.254.25",
}
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
    yapper_devices = []
    all_yapper_devices = []
    yapper_links = []
    links_end_devices = {}
    ip_to_link_id = {}
    for device in json_data["device_index"]:
        device_id = device
        device = json_data["device_index"][device]
        device["id"] = device_id
        if "yapper" in device["name"].lower():
            all_yapper_devices.append(device)
            if device["name"] == "YAPPER-Monitoring-SW" or device["name"] == "GrayLogSrv" or device["name"] == "YAPPER-EDGE-IP6Broker":
                continue
            yapper_devices.append(device)
            for port in device["ports"]:
                if port["connected_to"] != None and port["connected_to"] != "Unconnected":
                    ip_to_link_id[port["ip"]] = port["connected_to"]["link_id"]
                    if port["ipv6"] != None:
                        ip_to_link_id[port["ipv6"]] = port["connected_to"]["link_id"]
            print(f'Found device: {device["name"]}')
    print(f"Total Yapper devices: {len(yapper_devices)}")
    final_output = open('./tests/yapper/yapper_device_fault.md', 'w', encoding='utf-8')
    final_output.write("# Yapper \"Router Fault\" tesztelési jegyzőkönyv\n\n")
    final_output.write('<div style="page-break-after: always;"></div>\n\n')

    f = open('./tests/yapper/YAPPER-TESTING.drawio.svg', 'r', encoding='utf-8')
    svg_data = f.read()
    f.close()
    for router in yapper_devices:
        if "customer" in router['name'].lower():
            continue
        # Make disabled router red, and save to a new SVG file, and write to documentation
        soup = BeautifulSoup(svg_data, 'xml')
        path = soup.select_one(f'[data-link=\"{router['id']}\"] g[transform] path')
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

        if not os.path.exists(f'./tests/yapper/images/fault1_router/{router['id']}/'):
            os.makedirs(f'./tests/yapper/images/fault1_router/{router['id']}/')  
        f = open(f'./tests/yapper/images/fault1_router/{router['id']}/{router['id']}.svg', 'w', encoding='utf-8')
        f.write(str(soup))
        f.close()
        print("Success: SVG Path found and made red, written to docs.")
        print(f"Disabling router {router['name']}, waiting 10 seconds for ospf to converge...")
        await suspend_router(router, router['id'], True)
        final_output.write(f"## Hiba szimuláció: {router['name']}\n\n")
        final_output.write(f"<img src=\"images/fault1_router/{router['id']}/{router['id']}.svg\" style=\"display: block; margin: 0 auto; width: 450px;\">\n\n")
        await asyncio.sleep(10)  # Wait for 10 seconds
        print("Running ping on customer devices...")
        # Run pings in parallel
        if latest_nodes == {}:
            response = requests_session.get(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes")
            response.raise_for_status()
            latest_nodes = response.json()
        ping_tasks = [test_customer_connectivity(customer) for customer in CUSTOMERS]
        results = await asyncio.gather(*ping_tasks)
        final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">\n')
        for i in range(len(results)):
            red_line_svg_file = open(f'./tests/yapper/images/fault1_router/{router["id"]}/{router["id"]}.svg', 'r', encoding='utf-8')
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
                    if ip_in_line[0] == '10.65.1.1':
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
                    elif '172.17.1.' in ip_in_line[0]: # MESH 1 network, is a switch need to find previous link
                        temp_j = j
                        prev_hop = result[temp_j-1]
                        prev_ip_in_line = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', prev_hop)
                        need_prev_hop = (not result[temp_j].strip().split(' ')[0].isdigit())
                        if need_prev_hop:
                            counter = 0
                            print(f"We need to find previous hop for {ip_in_line[0]}")
                            while counter < 1:
                                prev_hop = result[temp_j-1]
                                temp_j -= 1
                                if prev_hop.strip().split(' ')[0].isdigit():
                                    counter += 1
                            print(f"Found previous hop: {prev_hop}")
                            temp_j += 1  # Go back to the last valid hop
                        prev_hop = ""
                        while not prev_hop.strip().split(' ')[0].isdigit():
                            prev_hop = result[temp_j-1]
                            temp_j -= 1
                            prev_ip_in_line = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', prev_hop)
                            if len(prev_ip_in_line) > 0:
                                # Find which router this link belongs to
                                routerp = None
                                for r in all_yapper_devices:
                                    for p in r['ports']:
                                        if p['ip'] == prev_ip_in_line[0]:
                                            routerp = r
                                            break
                                if routerp is None:
                                    raise Exception(f"Router not found for MESH1 previous hop {prev_ip_in_line[0]}")
                                for sport in routerp['ports']:
                                    if sport['connected_to'] != 'Unconnected' and sport['connected_to'] != None:
                                        if sport['connected_to']['name'] == 'YAPPER-MESH1':
                                            link_id = sport['connected_to']['link_id']
                                            make_path_dotted_orange(soup, link_id)
                                            print(f"MESH1 Link {ip_in_line[0]} -> {prev_ip_in_line[0]} belongs to router {routerp['name'] if routerp else 'Unknown'}")
                                            break
                    elif '172.17.2.' in ip_in_line[0]: # MESH 2 network, is a switch need to find previous link
                        temp_j = j
                        prev_hop = result[temp_j-1]
                        prev_ip_in_line = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', prev_hop)
                        need_prev_hop = (not result[temp_j].strip().split(' ')[0].isdigit())
                        if need_prev_hop:
                            counter = 0
                            print(f"We need to find previous hop for {ip_in_line[0]}")
                            while counter < 1:
                                prev_hop = result[temp_j-1]
                                temp_j -= 1
                                if prev_hop.strip().split(' ')[0].isdigit():
                                    counter += 1
                            print(f"Found previous hop: {prev_hop}")
                            temp_j += 1  # Go back to the last valid hop
                        prev_hop = ""
                        while not prev_hop.strip().split(' ')[0].isdigit():
                            prev_hop = result[temp_j-1]
                            temp_j -= 1
                            prev_ip_in_line = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', prev_hop)
                            if len(prev_ip_in_line) > 0:
                                routerp = None
                                for r in all_yapper_devices:
                                    for p in r['ports']:
                                        if p['ip'] == prev_ip_in_line[0]:
                                            routerp = r
                                            break
                                if routerp is None:
                                    raise Exception(f"Router not found for MESH2 previous hop {prev_ip_in_line[0]}")
                                for sport in routerp['ports']:
                                    if sport['connected_to'] != 'Unconnected' and sport['connected_to'] != None:
                                        if sport['connected_to']['name'] == 'YAPPER-MESH2':
                                            link_id = sport['connected_to']['link_id']
                                            make_path_dotted_orange(soup, link_id)
                                            print(f"MESH2 Link {ip_in_line[0]} -> {prev_ip_in_line[0]} belongs to router {routerp['name'] if routerp else 'Unknown'}")
                                            break
                f = open(f'./tests/yapper/images/fault1_router/{router["id"]}/{router["id"]}-{customer}.svg', 'w', encoding='utf-8')
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
        await suspend_router(router, router["id"], False)
        await asyncio.sleep(5)
        
asyncio.run(main())