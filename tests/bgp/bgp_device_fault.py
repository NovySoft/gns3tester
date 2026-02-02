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
YAPPER_CUSTOMERS = [
    "YAPPER-CUSTOMER1",
    "YAPPER-CUSTOMER2",
    "YAPPER-CUSTOMER3",
    "YAPPER-CUSTOMER4"
]
MAGENTUS_CUSTOMERS = [
    "MAGENTUS-Customer1",
    "MAGENTUS-Customer2",
    "MAGENTUS-Customer3",
    "MAGENTUS-Customer4"
]
CUSTOMERS = [
    *MAGENTUS_CUSTOMERS,
    *YAPPER_CUSTOMERS,
]
CUSTOMER_IPS = {
    "YAPPER-CUSTOMER1": "172.17.254.1",
    "YAPPER-CUSTOMER2": "172.17.254.9",
    "YAPPER-CUSTOMER3": "172.17.254.17",
    "YAPPER-CUSTOMER4": "172.17.254.25",
    "MAGENTUS-Customer1": "172.16.254.1",
    "MAGENTUS-Customer2": "172.16.254.9",
    "MAGENTUS-Customer3": "172.16.254.17",
    "MAGENTUS-Customer4": "172.16.254.25",
}

BGP_DEVICES = [
    "YAPPER-EDGE-R1",
    "YAPPER-EDGE-R2",
    "MAGENTUS-EDGE-R1",
    "MAGENTUS-EDGE-R2",
    "ICANN-R1",
    "ICANN-R2"
]

YAPPER_R1_IPS = [
    "172.18.111.2",
    "172.18.111.9",
    "172.17.5.37",
    "172.17.5.1",
    "172.17.1.10",
    "172.17.2.10",
    "172.18.111.29",
]

YAPPER_R2_IPS = [
    "172.18.111.6",
    "172.18.111.14",
    "172.17.5.38",
    "172.17.5.33",
    "172.17.1.20",
    "172.17.2.20",
    "172.18.111.25",
]

magentus_destination_ips = [
    '10.58.2.33',
    '172.16.0.5',
    '172.16.0.2',
    '172.16.0.61',
    '172.16.0.65',
    '172.16.255.1',
]
yapper_destination_ips = [
    '172.17.5.14',
    '172.17.5.17',
    '172.17.100.13',
    '172.17.6.13',
    '172.17.1.4',
    '172.17.2.4',
    '172.17.255.1',
]

def suspend_link(link_id, suspend: bool):
    response = requests_session.put(f"http://{host}:{server_port}/v2/projects/{project_id}/links/{link_id}", json={
        "suspend": suspend
    })
    response.raise_for_status()
    #print(response.json())

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

async def test_customer_connectivity(device_name, ip_to_test, destination_ips=[], delay=5):
    global latest_nodes
    console = list(filter(lambda n: n["name"] == device_name, latest_nodes))[0]
    for attempt in range(3):
        result = await cisco_run_traceroute(
            console.get("console_host"),
            console.get("console"),
            ip_to_test,
            CUSTOMER_IPS[device_name],
            device_name=device_name,
            delay=delay
        )
        if len(destination_ips) == 0:
            destination_ips.append(ip_to_test)
        # Check if successful - logic mirrored from main()
        reversed_result = result[::-1]
        success = False
        if len(reversed_result) > 0 and len(list(filter(lambda ip: ip in reversed_result[0], destination_ips))) > 0: success = True
        elif len(reversed_result) > 1 and len(list(filter(lambda ip: ip in reversed_result[1], destination_ips))) > 0: success = True
        elif len(reversed_result) > 2 and len(list(filter(lambda ip: ip in reversed_result[2], destination_ips))) > 0: success = True
        
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
    all_bgp_devices = []
    magentus_yapper_interconnect = []
    ip_to_link_id = {
        '172.16.0.46': 'magentus-r1',
        '172.16.0.45': 'magentus-r1',
        '172.16.0.38': 'magentus-r1',
        '172.16.0.37': 'magentus-r1',

        '172.16.0.42': 'magentus-r2',
        '172.16.0.41': 'magentus-r2',
        '172.16.0.30': 'magentus-r2',
        '172.16.0.29': 'magentus-r2',

        '172.17.5.1': 'yapper-r1',
        '172.17.5.2': 'yapper-r1',
        '172.17.1.10': 'yapper-r1',
        '172.17.2.10': 'yapper-r1',

        '172.17.5.33': 'yapper-r2',
        '172.17.5.34': 'yapper-r2',
        '172.17.1.20': 'yapper-r2',
        '172.17.2.20': 'yapper-r2',

        '172.29.29.30': 'bbf1591a-5019-416b-91e7-b81b336491ef',
        '172.30.30.30': 'fe42b4ad-4807-4eb8-a4f0-529db353c591',
    }
    for device in json_data["device_index"]:
        device_id = device
        device = json_data["device_index"][device]
        if device['name'] not in BGP_DEVICES:
            continue
        device["id"] = device_id
        all_bgp_devices.append(device)
        print(f'Found device: {device["name"]}')
        for port in device["ports"]:
            if port["connected_to"] != None and port["connected_to"] != "Unconnected":
                if port['connected_to']['name'] in BGP_DEVICES or 'icann' in port['connected_to']['name'].lower():
                    ip_to_link_id[port["ip"]] = port["connected_to"]["link_id"]
                    print("\tBGP peer found:", port['connected_to']['name'])
                if 'magentus' in device['name'].lower() and 'yapper' in port['connected_to']['name'].lower():
                    magentus_yapper_interconnect.append(port)
                    print("\tISP interconnect found:", port['connected_to']['name'])
    if latest_nodes == {}:
        response = requests_session.get(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes")
        response.raise_for_status()
        latest_nodes = response.json()
    print(f"Total BGP devices: {len(all_bgp_devices)}")
    final_output = open('./tests/bgp/bgp_device_fault.md', 'w', encoding='utf-8')
    final_output.write("# BGP tesztelési jegyzőkönyv\n\n")
    final_output.write("## BGP router hiba\n\n")
    final_output.write('<div style="page-break-after: always;"></div>\n\n')

    f = open('./tests/bgp/BGP-TESTING.drawio.svg', 'r', encoding='utf-8')
    svg_data = f.read()
    f.close()
    """
    for router in all_bgp_devices:
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
        if not os.path.exists(f'./tests/bgp/images/{router['id']}/'):
            os.makedirs(f'./tests/bgp/images/{router['id']}/')  
        f = open(f'./tests/bgp/images/{router['id']}/{router['id']}.svg', 'w', encoding='utf-8')
        f.write(str(soup))
        f.close()
        print("Success: SVG Path found and made red, written to docs.")
        print(f"Disabling router {router['name']}, waiting 20 seconds for BGP to converge...")
        await suspend_router(router, router['id'], True)
        final_output.write(f"### Hiba szimuláció: {router['name']} - Magentus ping\n\n")
        final_output.write(f"<img src=\"images/{router['id']}/{router['id']}.svg\" style=\"display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 100%\">\n\n")
        await asyncio.sleep(20)
        ping_tasks = []
        for customer in CUSTOMERS:
            if 'yapper' in customer.lower():
                destination_ips = magentus_destination_ips[::]
                ping_tasks.append(test_customer_connectivity(customer, '172.16.255.1', destination_ips=destination_ips[::]))
            elif 'magentus' in customer.lower():
                destination_ips = yapper_destination_ips[::]
                ping_tasks.append(test_customer_connectivity(customer, '172.17.255.1', destination_ips=destination_ips[::]))
        results = await asyncio.gather(*ping_tasks)
        final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">\n')
        for i in range(len(results)):
            red_line_svg_file = open(f'./tests/bgp/images/{router["id"]}/{router["id"]}.svg', 'r', encoding='utf-8')
            soup = BeautifulSoup(red_line_svg_file.read(), 'xml')
            red_line_svg_file.close()
            customer = CUSTOMERS[i]
            destination_ips = []
            if 'yapper' in customer.lower():
                destination_ips = magentus_destination_ips[::]
                # Make yapper router (source) green
                path = soup.select_one(f'[data-link=\"yapper-device\"] g[transform] path')
                if path:
                    current_style = path.get('style', '')
                    path['style'] = f"{current_style}; fill: #8BC34A;"
                    path['fill'] = "#8BC34A"
                path = soup.select_one(f'[data-link="yapper-device"] foreignObject>div>div>div')
                if path:
                    path.string = customer
                path = soup.select_one(f'[data-link="magentus-device"] foreignObject>div>div>div')
                if path:
                    path.string = "Magnetus-MGMT"
            elif 'magentus' in customer.lower():
                destination_ips = yapper_destination_ips[::]
                # Make magentus router (source) green
                path = soup.select_one(f'[data-link=\"magentus-device\"] g[transform] path')
                if path:
                    current_style = path.get('style', '')
                    path['style'] = f"{current_style}; fill: #8BC34A;"
                    path['fill'] = "#8BC34A"
                path = soup.select_one(f'[data-link="magentus-device"] foreignObject>div>div>div')
                if path:
                    path.string = customer
                path = soup.select_one(f'[data-link="yapper-device"] foreignObject>div>div>div')
                if path:
                    path.string = "Yapper-MGMT"
            make_path_dotted_orange(soup, 'magentus-link')
            make_path_dotted_orange(soup, 'magentus-cloud')
            make_path_dotted_orange(soup, 'yapper-link')
            make_path_dotted_orange(soup, 'yapper-cloud')

            result = results[i][::-1]
            
            final_output.write('  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">\n')
            
            if (len(result) > 0 and len(list(filter(lambda ip: ip in result[0], destination_ips))) > 0) or \
                (len(result) > 1 and len(list(filter(lambda ip: ip in result[1], destination_ips))) > 0) or \
                (len(result) > 2 and len(list(filter(lambda ip: ip in result[2], destination_ips))) > 0):
                print(f"✅ {customer} ping successful!")
                final_output.write(f"    <h4>{customer} ✅</h4>\n")
                
                success_line = ""
                if len(result) > 0 and len(list(filter(lambda ip: ip in result[0], destination_ips))) > 0:
                    success_line = result[0]
                elif len(result) > 1 and len(list(filter(lambda ip: ip in result[1], destination_ips))) > 0:
                    success_line = result[1]
                elif len(result) > 2 and len(list(filter(lambda ip: ip in result[2], destination_ips))) > 0:
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
                    if ip_in_line[0] in YAPPER_R1_IPS:
                        make_path_dotted_orange(soup, 'yapper-r1')
                    if ip_in_line[0] in YAPPER_R2_IPS:
                        make_path_dotted_orange(soup, 'yapper-r2')
                f = open(f'./tests/bgp/images/{router["id"]}/{router["id"]}-{customer}.svg', 'w', encoding='utf-8')
                f.write(str(soup))
                f.close()
                final_output.write(f'    <img src="./images/{router["id"]}/{router["id"]}-{customer}.svg" width="100%">\n')
            else:
                print(f"❌ {customer} ping failed!")
                final_output.write(f"    <h4>{customer} ❌</h4>\n")
                final_output.write("    <p><strong>Sikertelen ping!</strong></p>\n")
            
            final_output.write("  </div>\n")
            if i == 3:
                final_output.write("</div>\n\n")
                final_output.write('<div style="page-break-after: always;"></div>\n\n')
                final_output.write(f"### Hiba szimuláció: {router['name']} - Yapper ping\n\n")
                final_output.write(f"<img src=\"images/{router['id']}/{router['id']}.svg\" style=\"display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 100%\">\n\n")
                final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">\n')

        final_output.write("</div>\n\n")
        final_output.write('<div style="page-break-after: always;"></div>\n\n')
        print("Tests finished, Re-enabling the router...")
        await suspend_router(router, router["id"], False)
        await asyncio.sleep(5) """

    """ print("---- BGP Device Fault Testing Finished ----")
    print("Testing Magentus internet fault...")
    final_output.write('## Magentus internet hiba\n\n')
    final_output.write('Magentus közvetlen összekötetése az internet felé megszakítva, internet elérés Yapper-en keresztül\n\n')
    final_output.write('<img src=\"images/magentus-internet/magentus-internet.svg\" style=\"display: block; margin: 0 auto; width: 400px;\">\n\n')
    MAGENTUS_INTERNET_LINKS = [
        "49bddd15-24c3-4644-99c1-54d153c8d4d4",
        "29fd3ba4-7c9f-4a24-9d3e-8c4e75d9b6b1",
        "f33df30e-5211-4448-9e7f-1253748756f3"
    ]
    soup = BeautifulSoup(svg_data, 'xml')
    for link in MAGENTUS_INTERNET_LINKS:
        suspend_link(link, True)
    path = soup.select_one(f'[data-link="magentus-internet-cloud"] path')
    if path:
        current_style = path.get('style', '')
        path['style'] = f"{current_style}; stroke: red;"
        path['stroke'] = "red"
    path = soup.select_one(f'[data-link="magentus-internet-link"] path')
    if path:
        current_style = path.get('style', '')
        path['style'] = f"{current_style}; stroke: red;"
        path['stroke'] = "red"
    if not os.path.exists(f'./tests/bgp/images/magentus-internet/'):
        os.makedirs(f'./tests/bgp/images/magentus-internet/')  
    f = open(f'./tests/bgp/images/magentus-internet/magentus-internet.svg', 'w', encoding='utf-8')
    f.write(str(soup))
    f.close()
    print("Magentus internet links cut, waiting 10 seconds for BGP to converge...")
    await asyncio.sleep(10)
    tests_to_run = [
        test_customer_connectivity(customer, '1.1.1.1', delay=25) for customer in MAGENTUS_CUSTOMERS
    ]
    results = await asyncio.gather(*tests_to_run)
    final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">\n')
    for i in range(len(results)):
        customer = MAGENTUS_CUSTOMERS[i]
        result = results[i][::-1]
        red_line_svg_file = open(f'./tests/bgp/images/magentus-internet/magentus-internet.svg', 'r', encoding='utf-8')
        soup = BeautifulSoup(red_line_svg_file.read(), 'xml')
        red_line_svg_file.close()
        
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
                if ip_in_line[0] in YAPPER_R1_IPS:
                        make_path_dotted_orange(soup, 'yapper-r1')
                if ip_in_line[0] in YAPPER_R2_IPS:
                       make_path_dotted_orange(soup, 'yapper-r2')
            # Make magentus router (source) green
            path = soup.select_one(f'[data-link=\"magentus-device\"] g[transform] path')
            if path:
                current_style = path.get('style', '')
                path['style'] = f"{current_style}; fill: #8BC34A;"
                path['fill'] = "#8BC34A"
            path = soup.select_one(f'[data-link="magentus-device"] foreignObject>div>div>div')
            if path:
                path.string = customer
            make_path_dotted_orange(soup, 'magentus-link')
            make_path_dotted_orange(soup, 'magentus-cloud')
            make_path_dotted_orange(soup, 'yapper-internet-link')
            make_path_dotted_orange(soup, 'yapper-internet-cloud')
            make_path_dotted_orange(soup, 'yapper-cloud')
            f = open(f'./tests/bgp/images/magentus-internet/{customer}.svg', 'w', encoding='utf-8')
            f.write(str(soup))
            f.close()
            final_output.write(f'    <img src="./images/magentus-internet/{customer}.svg" width="100%">\n')
        else:
            print(f"❌ {customer} ping failed!")
            final_output.write(f"    <h4>{customer} ❌</h4>\n")
            final_output.write("    <p><strong>Sikertelen ping!</strong></p>\n")

        final_output.write("  </div>\n")
            
    final_output.write("</div>\n\n")
    final_output.write('<div style="page-break-after: always;"></div>\n\n')
    print("Tests finished, Re-enabling the link...")
    for link in MAGENTUS_INTERNET_LINKS:
        suspend_link(link, False) """
    
    """ print("Magentus internet fault testing finished.")
    print("Starting yapper internet fault testing...")
    final_output.write('## Yapper internet hiba\n\n')
    final_output.write('Yapper közvetlen összekötetése az internet felé megszakítva, internet elérés Magentus-on keresztül\n\n')
    final_output.write('<img src=\"images/yapper-internet/yapper-internet.svg\" style=\"display: block; margin: 0 auto; width: 400px;\">\n\n')
    YAPPER_INTERNET_LINKS = [
        "d66d8ee4-8c0e-4fa8-b2b2-d0f191d6682d",
        "4dfccda3-c54c-48f9-b6da-29e5dcba6564",
    ]
    soup = BeautifulSoup(svg_data, 'xml')
    for link in YAPPER_INTERNET_LINKS:
        suspend_link(link, True)
    path = soup.select_one(f'[data-link="yapper-internet-cloud"] path')
    if path:
        current_style = path.get('style', '')
        path['style'] = f"{current_style}; stroke: red;"
        path['stroke'] = "red"
    path = soup.select_one(f'[data-link="yapper-internet-link"] path')
    if path:
        current_style = path.get('style', '')
        path['style'] = f"{current_style}; stroke: red;"
        path['stroke'] = "red"
    if not os.path.exists(f'./tests/bgp/images/yapper-internet/'):
        os.makedirs(f'./tests/bgp/images/yapper-internet/')  
    f = open(f'./tests/bgp/images/yapper-internet/yapper-internet.svg', 'w', encoding='utf-8')
    f.write(str(soup))
    f.close()
    print("Yapper internet links cut, waiting 10 seconds for BGP to converge...")
    await asyncio.sleep(10)
    tests_to_run = [
        test_customer_connectivity(customer, '1.1.1.1', delay=25) for customer in YAPPER_CUSTOMERS
    ]
    results = await asyncio.gather(*tests_to_run)
    final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">\n')
    for i in range(len(results)):
        customer = YAPPER_CUSTOMERS[i]
        result = results[i][::-1]
        red_line_svg_file = open(f'./tests/bgp/images/yapper-internet/yapper-internet.svg', 'r', encoding='utf-8')
        soup = BeautifulSoup(red_line_svg_file.read(), 'xml')
        red_line_svg_file.close()
        
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
                if ip_in_line[0] in YAPPER_R1_IPS:
                        make_path_dotted_orange(soup, 'yapper-r1')
                if ip_in_line[0] in YAPPER_R2_IPS:
                       make_path_dotted_orange(soup, 'yapper-r2')
            # Make yapper router (source) green
            path = soup.select_one(f'[data-link=\"yapper-device\"] g[transform] path')
            if path:
                current_style = path.get('style', '')
                path['style'] = f"{current_style}; fill: #8BC34A;"
                path['fill'] = "#8BC34A"
            path = soup.select_one(f'[data-link="yapper-device"] foreignObject>div>div>div')
            if path:
                path.string = customer
            make_path_dotted_orange(soup, 'yapper-link')
            make_path_dotted_orange(soup, 'yapper-cloud')
            make_path_dotted_orange(soup, 'magentus-internet-link')
            make_path_dotted_orange(soup, 'magentus-internet-cloud')
            make_path_dotted_orange(soup, 'magentus-cloud')
            f = open(f'./tests/bgp/images/yapper-internet/{customer}.svg', 'w', encoding='utf-8')
            f.write(str(soup))
            f.close()
            final_output.write(f'    <img src="./images/yapper-internet/{customer}.svg" width="100%">\n')
        else:
            print(f"❌ {customer} ping failed!")
            final_output.write(f"    <h4>{customer} ❌</h4>\n")
            final_output.write("    <p><strong>Sikertelen ping!</strong></p>\n")

        final_output.write("  </div>\n")
            
    final_output.write("</div>\n\n")
    final_output.write('<div style="page-break-after: always;"></div>\n\n')
    print("Tests finished, Re-enabling the link...")
    for link in YAPPER_INTERNET_LINKS:
        suspend_link(link, False) """
    
    """ print('Yapper internet fault testing finished.')
    print('MAGENTUS - Yapper interconnect failure testing')

    final_output.write('## Magentus-Yapper interconnect hiba - Magentus Ping\n\n')
    final_output.write('Yapper és Magentus BGP peer linkjei nem működik, kapcsolat ICANN-en keresztül\n\n')
    final_output.write('<img src=\"images/yapper-magentus-bgpfail/yapper-internet.svg\" style=\"display: block; margin: 0 auto; width: 400px;\">\n\n')
    BGP_ISP_INTER_LINKS = [
        "d5472b6c-d8a5-43aa-8a68-44ff28d6260d",
        "2463004b-6ae1-45b9-8e5e-ef19f9093b6a",
        "84207e8f-7e75-4f5a-aec1-e2633da797b2",
        "1de7f299-a4cb-44a3-8d98-31e9bb348b0f",
    ]
    soup = BeautifulSoup(svg_data, 'xml')
    for link in BGP_ISP_INTER_LINKS:
        suspend_link(link, True)
        path = soup.select_one(f'[data-link="{link}"] path')
        if path:
            current_style = path.get('style', '')
            path['style'] = f"{current_style}; stroke: red;"
            path['stroke'] = "red"
    if not os.path.exists(f'./tests/bgp/images/yapper-magentus-bgpfail/'):
        os.makedirs(f'./tests/bgp/images/yapper-magentus-bgpfail/')
    f = open(f'./tests/bgp/images/yapper-magentus-bgpfail/yapper-magentus-bgpfail.svg', 'w', encoding='utf-8')
    f.write(str(soup))
    f.close()
    print("Magentus-Yapper interconnect links cut, waiting 20 seconds for BGP to converge...")
    await asyncio.sleep(20)
    ping_tasks = []
    for customer in CUSTOMERS:
        if 'yapper' in customer.lower():
            destination_ips = magentus_destination_ips[::]
            ping_tasks.append(test_customer_connectivity(customer, '172.16.255.1', destination_ips=destination_ips[::]))
        elif 'magentus' in customer.lower():
            destination_ips = yapper_destination_ips[::]
            ping_tasks.append(test_customer_connectivity(customer, '172.17.255.1', destination_ips=destination_ips[::]))
    results = await asyncio.gather(*ping_tasks)
    final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">\n')
    for i in range(len(results)):
        red_line_svg_file = open(f'./tests/bgp/images/yapper-magentus-bgpfail/yapper-magentus-bgpfail.svg', 'r', encoding='utf-8')
        soup = BeautifulSoup(red_line_svg_file.read(), 'xml')
        red_line_svg_file.close()
        customer = CUSTOMERS[i]
        destination_ips = []
        if 'yapper' in customer.lower():
            destination_ips = magentus_destination_ips[::]
            # Make yapper router (source) green
            path = soup.select_one(f'[data-link=\"yapper-device\"] g[transform] path')
            if path:
                current_style = path.get('style', '')
                path['style'] = f"{current_style}; fill: #8BC34A;"
                path['fill'] = "#8BC34A"
            path = soup.select_one(f'[data-link="yapper-device"] foreignObject>div>div>div')
            if path:
                path.string = customer
            path = soup.select_one(f'[data-link="magentus-device"] foreignObject>div>div>div')
            if path:
                path.string = "Magnetus-MGMT"
        elif 'magentus' in customer.lower():
            destination_ips = yapper_destination_ips[::]
            # Make magentus router (source) green
            path = soup.select_one(f'[data-link=\"magentus-device\"] g[transform] path')
            if path:
                current_style = path.get('style', '')
                path['style'] = f"{current_style}; fill: #8BC34A;"
                path['fill'] = "#8BC34A"
            path = soup.select_one(f'[data-link="magentus-device"] foreignObject>div>div>div')
            if path:
                path.string = customer
            path = soup.select_one(f'[data-link="yapper-device"] foreignObject>div>div>div')
            if path:
                path.string = "Yapper-MGMT"
        make_path_dotted_orange(soup, 'magentus-link')
        make_path_dotted_orange(soup, 'magentus-cloud')
        make_path_dotted_orange(soup, 'yapper-link')
        make_path_dotted_orange(soup, 'yapper-cloud')

        result = results[i][::-1]
        
        final_output.write('  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">\n')
        
        if (len(result) > 0 and len(list(filter(lambda ip: ip in result[0], destination_ips))) > 0) or \
            (len(result) > 1 and len(list(filter(lambda ip: ip in result[1], destination_ips))) > 0) or \
            (len(result) > 2 and len(list(filter(lambda ip: ip in result[2], destination_ips))) > 0):
            print(f"✅ {customer} ping successful!")
            final_output.write(f"    <h4>{customer} ✅</h4>\n")
            
            success_line = ""
            if len(result) > 0 and len(list(filter(lambda ip: ip in result[0], destination_ips))) > 0:
                success_line = result[0]
            elif len(result) > 1 and len(list(filter(lambda ip: ip in result[1], destination_ips))) > 0:
                success_line = result[1]
            elif len(result) > 2 and len(list(filter(lambda ip: ip in result[2], destination_ips))) > 0:
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
                if ip_in_line[0] in YAPPER_R1_IPS:
                    make_path_dotted_orange(soup, 'yapper-r1')
                if ip_in_line[0] in YAPPER_R2_IPS:
                    make_path_dotted_orange(soup, 'yapper-r2')
            f = open(f'./tests/bgp/images/yapper-magentus-bgpfail/{customer}.svg', 'w', encoding='utf-8')
            f.write(str(soup))
            f.close()
            final_output.write(f'    <img src="./images/yapper-magentus-bgpfail/{customer}.svg" width="100%">\n')
        else:
            print(f"❌ {customer} ping failed!")
            final_output.write(f"    <h4>{customer} ❌</h4>\n")
            final_output.write("    <p><strong>Sikertelen ping!</strong></p>\n")
        
        final_output.write("  </div>\n")
        if i == 3:
            final_output.write("</div>\n\n")
            final_output.write('<div style="page-break-after: always;"></div>\n\n')
            final_output.write(f"## Magentus-Yapper interconnect hiba - Yapper Ping\n\n")
            final_output.write(f"<img src=\"images/yapper-magentus-bgpfail/yapper-magentus-bgpfail.svg\" style=\"display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 400px\">\n\n")
            final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">\n')

    final_output.write("</div>\n\n")
    final_output.write('<div style="page-break-after: always;"></div>\n\n')
    print("Tests finished, Re-enabling the links...")
    for link in BGP_ISP_INTER_LINKS:
        suspend_link(link, False)
    """

    print("ISP Interconnect fail test ended")
    print("Beginning ICANN direct connection fail tests")
    final_output.write('## ICANN R1 közvetlen kapcsolat hiba\n\n')
    final_output.write('ICANN R1 közvetlen összekötetése Magentus részéről megszakítva, kapcsolat Yapper-en keresztül\n\n')
    final_output.write('<img src=\"images/icann-r1-fail/icann-r1-fail.svg\" style=\"display: block; margin: 0 auto; width: 400px;\">\n\n')
    ICANN_R1_links = [
        "d6c7a1a8-cb46-4788-a652-2a26aaaf4194",
        "7fd3678a-4eae-4f08-9c22-bbba22832d9d",
    ]

    soup = BeautifulSoup(svg_data, 'xml')
    for link in ICANN_R1_links:
        suspend_link(link, True)
        path = soup.select_one(f'[data-link="{link}"] path')
        if path:
            current_style = path.get('style', '')
            path['style'] = f"{current_style}; stroke: red;"
            path['stroke'] = "red"
    if not os.path.exists(f'./tests/bgp/images/icann-r1-fail/'):
        os.makedirs(f'./tests/bgp/images/icann-r1-fail/')
    f = open(f'./tests/bgp/images/icann-r1-fail/icann-r1-fail.svg', 'w', encoding='utf-8')
    f.write(str(soup))
    f.close()
    print("ICANN R1 links cut, waiting 20 seconds for BGP to converge...")
    await asyncio.sleep(20)
    ping_tasks = [
        test_customer_connectivity(customer, '172.29.29.30', delay=7) for customer in MAGENTUS_CUSTOMERS
    ]
    results = await asyncio.gather(*ping_tasks)
    final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">\n')
    for i in range(len(results)):
        customer = MAGENTUS_CUSTOMERS[i]
        result = results[i][::-1]
        red_line_svg_file = open(f'./tests/bgp/images/icann-r1-fail/icann-r1-fail.svg', 'r', encoding='utf-8')
        soup = BeautifulSoup(red_line_svg_file.read(), 'xml')
        red_line_svg_file.close()
        
        final_output.write('  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">\n')

        if (len(result) > 0 and '172.29.29.30' in result[0]) or \
            (len(result) > 1 and '172.29.29.30' in result[1]) or \
            (len(result) > 2 and '172.29.29.30' in result[2]):
            print(f"✅ {customer} ping successful!")
            final_output.write(f"    <h4>{customer} ✅</h4>\n")
            
            success_line = ""
            if len(result) > 0 and '172.29.29.30' in result[0]:
                success_line = result[0]
            elif len(result) > 1 and '172.29.29.30' in result[1]:
                success_line = result[1]
            elif len(result) > 2 and '172.29.29.30' in result[2]:
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
            # Make yapper router (source) green
            path = soup.select_one(f'[data-link=\"magentus-device\"] g[transform] path')
            if path:
                current_style = path.get('style', '')
                path['style'] = f"{current_style}; fill: #8BC34A;"
                path['fill'] = "#8BC34A"
            path = soup.select_one(f'[data-link="magentus-device"] foreignObject>div>div>div')
            if path:
                path.string = customer
            make_path_dotted_orange(soup, 'magentus-link')
            f = open(f'./tests/bgp/images/icann-r1-fail/{customer}.svg', 'w', encoding='utf-8')
            f.write(str(soup))
            f.close()
            final_output.write(f'    <img src="./images/icann-r1-fail/{customer}.svg" width="100%">\n')
        else:
            print(f"❌ {customer} ping failed!")
            final_output.write(f"    <h4>{customer} ❌</h4>\n")
            final_output.write("    <p><strong>Sikertelen ping!</strong></p>\n")

        final_output.write("  </div>\n")
            
    final_output.write("</div>\n\n")
    final_output.write('<div style="page-break-after: always;"></div>\n\n')
    print("Tests finished, Re-enabling the link...")
    for link in ICANN_R1_links:
        suspend_link(link, False)
    final_output.close()


asyncio.run(main())