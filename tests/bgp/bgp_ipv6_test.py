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

YAPPER_CUSTOMERS = [
    "YAPPER-USER1",
    "YAPPER-USER2",
    "YAPPER-USER3",
    "YAPPER-USER4"
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

BGP_DEVICES = [
    "YAPPER-EDGE-R1",
    "YAPPER-EDGE-R2",
    "MAGENTUS-EDGE-R1",
    "MAGENTUS-EDGE-R2",
    "ICANN-R1",
    "ICANN-R2"
]

MAGENTUS_R1_IPS = [
    "2001:470:216F:AAAA::47",
    "2001:470:216F:AAAA::46",
    "2001:470:216F:AAAA::39",
    "2001:470:216F:AAAA::38"
]

MAGENTUS_R2_IPS = [
    "2001:470:216F:AAAA::43",
    "2001:470:216F:AAAA::42",
    "2001:470:216F:AAAA::31",
    "2001:470:216F:AAAA::30"
]

YAPPER_R1_IPS = [
    "2001:470:2171:AAAA:AAAA:1:0:10",
    "2001:470:2171:AAAA:AAAA:2:0:10",
    "2001:470:2171:AAAA:AAAA:A:0:2",
    "2001:470:2171:AAAA:AAAA:A:0:3",
    "2001:DB8:DEAD:BEEF::2",
    "2001:DB8:DEAD:BEEF::3",
    "2001:DB8:DEAD:BEEF::10",
    "2001:DB8:DEAD:BEEF::11",
    "2001:DB8:DEAD:BEEF::30",
    "2001:DB8:DEAD:BEEF::31",
]

YAPPER_R2_IPS = [
    "2001:470:2171:AAAA:AAAA:1:0:20",
    "2001:470:2171:AAAA:AAAA:2:0:20",
    "2001:470:2171:AAAA:AAAA:A:0:34",
    "2001:470:2171:AAAA:AAAA:A:0:35",
    "2001:DB8:DEAD:BEEF::7",
    "2001:DB8:DEAD:BEEF::6",
    "2001:DB8:DEAD:BEEF::15",
    "2001:DB8:DEAD:BEEF::14",
    "2001:DB8:DEAD:BEEF::26",
    "2001:DB8:DEAD:BEEF::27",
]

def suspend_link(link_id, suspend: bool):
    response = requests_session.put(f"http://{host}:{server_port}/v2/projects/{project_id}/links/{link_id}", json={
        "suspend": suspend
    })
    response.raise_for_status()

async def suspend_router(router, router_id, suspend: bool):
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

async def test_customer_connectivity(device_name, ip_to_test, success_targets):
    global latest_nodes
    console = list(filter(lambda n: n["name"] == device_name, latest_nodes))[0]
    for attempt in range(3):
        try:
            result = await cisco_run_traceroute(
                console.get("console_host"),
                console.get("console"),
                ip_to_test,
                None, # Source IP
                device_name=device_name
            )
            
            reversed_result = result[::-1]
            success = False
            if len(reversed_result) > 0 and any(ip in reversed_result[0] for ip in success_targets): success = True
            elif len(reversed_result) > 1 and any(ip in reversed_result[1] for ip in success_targets): success = True
            elif len(reversed_result) > 2 and any(ip in reversed_result[2] for ip in success_targets): success = True
            
            if success:
                return result
        except Exception as e:
            print(f"Error during traceroute for {device_name}: {e}")
            
        if attempt < 2:
            print(f"⚠️ {device_name} ping failed (Attempt {attempt+1}/3). Retrying...")
            await asyncio.sleep(2)

    return result if 'result' in locals() else []

def make_path_dotted_orange(soup, link_id):
    path = soup.select_one(f'[data-link="{link_id}"] path')
    if path:
        current_style = path.get('style', '')
        path['style'] = f"{current_style}; stroke: #FF9800; stroke-dasharray: 10,5"
        path['stroke'] = "#FF9800"
        path['stroke-dasharray'] = "10,5"

async def main():
    global latest_nodes, project_id
    
    # -------------------------------------------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------------------------------------------
    
    f = open("./data/e03c636e-8c33-4ca9-a88d-e55dedec8d98.json", "r", encoding="utf-8")
    data = f.read()
    f.close()
    json_data = json.loads(data)
    
    all_bgp_devices = []
    ip_to_link_id = {}
    
    for device in json_data["device_index"]:
        device_id = device
        device = json_data["device_index"][device]
        device["id"] = device_id
        
        if device['name'] in BGP_DEVICES:
            all_bgp_devices.append(device)
            print(f'Found BGP device: {device["name"]}')
            
        for port in device["ports"]:
             if port["connected_to"] != None and port["connected_to"] != "Unconnected":
                if port.get("ip"):
                    ip_to_link_id[port["ip"]] = port["connected_to"]["link_id"]
                if port.get("ipv6"):
                    # Handle CIDR notation if present
                    ip6 = port["ipv6"].split('/')[0].lower()
                    ip_to_link_id[ip6] = port["connected_to"]["link_id"]

    if latest_nodes == {}:
        response = requests_session.get(f"http://{host}:{server_port}/v2/projects/{project_id}/nodes")
        response.raise_for_status()
        latest_nodes = response.json()
        
    print(f"Total BGP devices: {len(all_bgp_devices)}")
    final_output = open('./tests/bgp/bgp_ipv6_test.md', 'w', encoding='utf-8')
    final_output.write("# BGP IPv6 tesztelési jegyzőkönyv\n\n")
    final_output.write("## BGP router hiba (IPv6)\n\n")
    final_output.write('<div style="page-break-after: always;"></div>\n\n')

    f = open('./tests/bgp/BGP-TESTING.drawio.svg', 'r', encoding='utf-8')
    svg_data = f.read()
    f.close()
    
    # -------------------------------------------------------------------------------------------------------------
    # Test 1: BGP Router Failures
    # -------------------------------------------------------------------------------------------------------------
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
        
        if not os.path.exists(f'./tests/bgp/images/ipv6/{router['id']}/'):
            os.makedirs(f'./tests/bgp/images/ipv6/{router['id']}/')  
        f = open(f'./tests/bgp/images/ipv6/{router['id']}/{router['id']}.svg', 'w', encoding='utf-8')
        f.write(str(soup))
        f.close()
        
        print(f"Disabling router {router['name']}, waiting 20 seconds for BGP to converge...")
        await suspend_router(router, router['id'], True)
        
        final_output.write(f"### Hiba szimuláció: {router['name']} - IPv6 Ping\n\n")
        final_output.write(f"<img src=\"images/ipv6/{router['id']}/{router['id']}.svg\" style=\"display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 500px\">\n\n")
        await asyncio.sleep(20)
        
        ping_targets = []
        ping_tasks = []
        for customer in CUSTOMERS:
            if 'yapper' in customer.lower():
                target = "2001:470:216F:AAAA::66" # This is a Magentus IP in the topology, but not a customer IP. We just want to see if it can reach Magentus side.
                ping_targets.append([
                    "2001:470:216F:AAAA::6",
                    "2001:470:216F:AAAA::3",
                    "2001:470:216F:AAAA::62",
                    "2001:470:216F:AAAA::66",
                ])
                ping_tasks.append(test_customer_connectivity(customer, target, ping_targets[-1]))
            else:
                 # Magentus users ping Google just to verify general connectivity since we lack known Yapper IPs
                 target = '2001:470:2171:BBBB:BBBB::14' # This is a Yapper IP in the topology, but not a customer IP. We just want to see if it can reach Yapper side.
                 ping_targets.append([
                    "2001:470:2171:AAAA:AAAA:A:0:15",
                    "2001:470:2171:AAAA:AAAA:A:0:18",
                    "2001:470:2171:BBBB:BBBB::14",
                    "2001:470:2171:AAAA:AAAA:B:0:14",
                    "2001:470:2171:AAAA:AAAA:1:0:4",
                    "2001:470:2171:AAAA:AAAA:2:0:4",
                 ])
                 ping_tasks.append(test_customer_connectivity(customer, target, ping_targets[-1]))
            
        results = await asyncio.gather(*ping_tasks)
        final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">\n')
        
        for i in range(len(results)):
            customer = CUSTOMERS[i]
            result = results[i][::-1]
            
            red_line_svg_file = open(f'./tests/bgp/images/ipv6/{router["id"]}/{router["id"]}.svg', 'r', encoding='utf-8')
            soup = BeautifulSoup(red_line_svg_file.read(), 'xml')
            red_line_svg_file.close()

            # Color setup for visual report
            if 'yapper' in customer.lower():
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

            final_output.write('  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">\n')
            
            ip_found = False
            if len(result) > 0 and any(ip in result[0] for ip in ping_targets[i]): ip_found = True
            elif len(result) > 1 and any(ip in result[1] for ip in ping_targets[i]): ip_found = True
            elif len(result) > 2 and any(ip in result[2] for ip in ping_targets[i]): ip_found = True
            
            if ip_found:
                print(f"✅ {customer} ping successful!")
                final_output.write(f"    <h4>{customer} ✅</h4>\n")
                
                success_line = next((line for line in result if any(ip in line for ip in ping_targets[i])), result[0] if result else "")
                success_line = success_line.strip().replace(' msec', 'ms').replace(' *', '')
                final_output.write(f"    <p><strong>Sikeres ping!</strong> {success_line}</p>\n")
                
                # Trace drawing
                for hop in result[::-1]:
                    ip_in_line = re.findall(r'[a-fA-F0-9]{1,4}(?::[a-fA-F0-9]{0,4})+', hop)
                    if not ip_in_line: continue
                    ip = ip_in_line[0].lower()
                    if ip in ip_to_link_id:
                        make_path_dotted_orange(soup, ip_to_link_id[ip])
                    if ip.upper()=="2001:470:1F1A:51::1" or ip.upper()=="2001:470:1F1A:51::2":
                        make_path_dotted_orange(soup, 'magentus-internet-link')
                        make_path_dotted_orange(soup, 'magentus-internet-cloud')
                    if ip.upper() in MAGENTUS_R1_IPS:
                        make_path_dotted_orange(soup, 'magentus-r1')
                    if ip.upper() in MAGENTUS_R2_IPS:
                        make_path_dotted_orange(soup, 'magentus-r2')
                    if ip.upper() in YAPPER_R1_IPS:
                        make_path_dotted_orange(soup, 'yapper-r1')
                    if ip.upper() in YAPPER_R2_IPS:
                        make_path_dotted_orange(soup, 'yapper-r2')
                        
                
                f = open(f'./tests/bgp/images/ipv6/{router["id"]}/{router["id"]}-{customer}.svg', 'w', encoding='utf-8')
                f.write(str(soup))
                f.close()
                final_output.write(f'    <img src="./images/ipv6/{router["id"]}/{router["id"]}-{customer}.svg" width="100%">\n')
            else:
                 print(f"❌ {customer} ping failed!")
                 final_output.write(f"    <h4>{customer} ❌</h4>\n")
                 final_output.write("    <p><strong>Sikertelen ping!</strong></p>\n")
            
            final_output.write("  </div>\n")
            # Break page after 4 items (grid assumes 2 columns)
            if i == 3:
                final_output.write("</div>\n\n")
                final_output.write('<div style="page-break-after: always;"></div>\n\n')
                if i < len(results) - 1:
                     final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">\n')

        final_output.write("</div>\n\n")
        
        print("Tests finished, Re-enabling the router...")
        await suspend_router(router, router["id"], False)
        # Give some time for BGP/OSPF to recover before next router test
        await asyncio.sleep(30)
        
    final_output.write('<div style="page-break-after: always;"></div>\n\n')

    # ---------------- ISP Interconnect Failure (IPv6) ----------------
    print("Testing Magentus-Yapper Interconnect Failure (IPv6)...")
    final_output.write('## Magentus-Yapper interconnect hiba (IPv6)\n\n')
    final_output.write('Yapper és Magentus BGP peer linkjei nem működik, kapcsolat ICANN-en keresztül\n\n')
    
    if not os.path.exists(f'./tests/bgp/images/ipv6/yapper-magentus-bgpfail/'):
        os.makedirs(f'./tests/bgp/images/ipv6/yapper-magentus-bgpfail/')
        
    final_output.write('<img src=\"images/ipv6/yapper-magentus-bgpfail/yapper-magentus-bgpfail.svg\" style=\"display: block; margin: 10px auto; width: 500px;\">\n\n')
    
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
        if path: path['style'] = f"{path.get('style', '')}; stroke: red;"

    f = open(f'./tests/bgp/images/ipv6/yapper-magentus-bgpfail/yapper-magentus-bgpfail.svg', 'w', encoding='utf-8')
    f.write(str(soup))
    f.close()
    
    print("Interconnect links cut, waiting 20 seconds for BGP to converge...")
    await asyncio.sleep(20)
    
    # Yapper customers trace to Magentus Customers (IPv6)
    ping_tasks_interconnect = []
    ping_targets_interconnect = []
    
    for customer in CUSTOMERS:
        if 'yapper' in customer.lower():
            target = "2001:470:216F:AAAA::66" # This is a Magentus IP in the topology, but not a customer IP. We just want to see if it can reach Magentus side.
            ping_targets_interconnect.append([
                "2001:470:216F:AAAA::6",
                "2001:470:216F:AAAA::3",
                "2001:470:216F:AAAA::62",
                "2001:470:216F:AAAA::66",
            ])
            ping_tasks_interconnect.append(test_customer_connectivity(customer, target, ping_targets_interconnect[-1]))
        else:
             # Magentus users ping Google just to verify general connectivity since we lack known Yapper IPs
             target = '2001:470:2171:BBBB:BBBB::14' # This is a Yapper IP in the topology, but not a customer IP. We just want to see if it can reach Yapper side.
             ping_targets_interconnect.append([
                "2001:470:2171:AAAA:AAAA:A:0:15",
                "2001:470:2171:AAAA:AAAA:A:0:18",
                "2001:470:2171:BBBB:BBBB::14",
                "2001:470:2171:AAAA:AAAA:B:0:14",
                "2001:470:2171:AAAA:AAAA:1:0:4",
                "2001:470:2171:AAAA:AAAA:2:0:4",
            ])
             ping_tasks_interconnect.append(test_customer_connectivity(customer, target, ping_targets_interconnect[-1]))

    results = await asyncio.gather(*ping_tasks_interconnect)
    
    final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">\n')
    for i in range(len(results)):
        customer = CUSTOMERS[i]
        target = ping_targets_interconnect[i]
        result = results[i][::-1]
        
        # Load and prep base SVG
        red_line_svg_file = open(f'./tests/bgp/images/ipv6/yapper-magentus-bgpfail/yapper-magentus-bgpfail.svg', 'r', encoding='utf-8')
        soup = BeautifulSoup(red_line_svg_file.read(), 'xml')
        red_line_svg_file.close()
        
        # Color setup for visual report
        if 'yapper' in customer.lower():
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
        
        final_output.write('  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">\n')
        ip_found = False
        if len(result) > 0 and any(ip in result[0] for ip in target): ip_found = True
        elif len(result) > 1 and any(ip in result[1] for ip in target): ip_found = True
        elif len(result) > 2 and any(ip in result[2] for ip in target): ip_found = True

        if ip_found:
            print(f"✅ {customer} to {target} successful!")
            final_output.write(f"    <h4>{customer} ✅</h4>\n")
            success_line = next((line for line in result if any(ip in line for ip in target)), result[0] if result else "")
            success_line = success_line.strip().replace(' msec', 'ms').replace(' *', '')
            final_output.write(f"    <p><strong>Sikeres ping!</strong> {success_line}</p>\n")
            for hop in result[::-1]:
                ip_in_line = re.findall(r'[a-fA-F0-9]{1,4}(?::[a-fA-F0-9]{0,4})+', hop)
                if not ip_in_line: continue
                ip = ip_in_line[0].lower()
                if ip in ip_to_link_id:
                    make_path_dotted_orange(soup, ip_to_link_id[ip])
                if ip.upper()=="2001:470:1F1A:51::1" or ip.upper()=="2001:470:1F1A:51::2":
                    make_path_dotted_orange(soup, 'magentus-internet-link')
                    make_path_dotted_orange(soup, 'magentus-internet-cloud')
                if ip.upper() in MAGENTUS_R1_IPS:
                    make_path_dotted_orange(soup, 'magentus-r1')
                if ip.upper() in MAGENTUS_R2_IPS:
                    make_path_dotted_orange(soup, 'magentus-r2')
                if ip.upper() in YAPPER_R1_IPS:
                    make_path_dotted_orange(soup, 'yapper-r1')
                if ip.upper() in YAPPER_R2_IPS:
                    make_path_dotted_orange(soup, 'yapper-r2')

            
            f = open(f'./tests/bgp/images/ipv6/yapper-magentus-bgpfail/{customer}.svg', 'w', encoding='utf-8')
            f.write(str(soup))
            f.close()
            final_output.write(f'    <img src="./images/ipv6/yapper-magentus-bgpfail/{customer}.svg" width="100%">\n')
        else:
            print(f"❌ {customer} ping failed!")
            final_output.write(f"    <h4>{customer} ❌</h4>\n")
            final_output.write("    <p><strong>Sikertelen ping!</strong></p>\n")
        final_output.write("  </div>\n")
        
    final_output.write("</div>\n\n")
    final_output.write('<div style="page-break-after: always;"></div>\n\n')
    print("Tests finished, Re-enabling the link...")
    for link in BGP_ISP_INTER_LINKS: suspend_link(link, False)

    # ---------------- ISP ICANN R1 Direct Connection Failure (IPv6) ----------------
    print("Beginning ICANN direct connection fail tests (IPv6)")
    final_output.write('## ICANN R1 közvetlen kapcsolat hiba (IPv6)\n\n')
    final_output.write('ICANN R1 közvetlen összekötetése Magentus részéről megszakítva, kapcsolat Yapper-en keresztül\n\n')
    final_output.write('<img src=\"images/ipv6/icann-r1-fail/icann-r1-fail.svg\" style=\"display: block; margin: 10px auto; width: 400px;\">\n\n')
    
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
            
    if not os.path.exists(f'./tests/bgp/images/ipv6/icann-r1-fail/'):
        os.makedirs(f'./tests/bgp/images/ipv6/icann-r1-fail/')
        
    f = open(f'./tests/bgp/images/ipv6/icann-r1-fail/icann-r1-fail.svg', 'w', encoding='utf-8')
    f.write(str(soup))
    f.close()
    
    print("ICANN R1 links cut, waiting 20 seconds for BGP to converge...")
    await asyncio.sleep(20)
    
    ping_tasks_icann1 = []
    target_ip = '172:29:29::30'
    
    for customer in MAGENTUS_CUSTOMERS:
        ping_tasks_icann1.append(test_customer_connectivity(customer, target_ip, [target_ip]))
            
    results = await asyncio.gather(*ping_tasks_icann1)
    
    final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">\n')
    for i in range(len(results)):
        customer = MAGENTUS_CUSTOMERS[i]
        result = results[i][::-1]
        
        red_line_svg_file = open(f'./tests/bgp/images/ipv6/icann-r1-fail/icann-r1-fail.svg', 'r', encoding='utf-8')
        soup = BeautifulSoup(red_line_svg_file.read(), 'xml')
        red_line_svg_file.close()

        # Color setup
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
        
        final_output.write('  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">\n')
        
        ip_found = False
        target_check_list = [target_ip]
        if len(result) > 0 and any(ip in result[0] for ip in target_check_list): ip_found = True
        elif len(result) > 1 and any(ip in result[1] for ip in target_check_list): ip_found = True
        elif len(result) > 2 and any(ip in result[2] for ip in target_check_list): ip_found = True
        
        if ip_found:
            print(f"✅ {customer} ping successful!")
            final_output.write(f"    <h4>{customer} ✅</h4>\n")
            success_line = next((line for line in result if any(ip in line for ip in target_check_list)), result[0] if result else "")
            success_line = success_line.strip().replace(' msec', 'ms').replace(' *', '')
            final_output.write(f"    <p><strong>Sikeres ping!</strong> {success_line}</p>\n")
            
            for hop in result[::-1]:
                ip_in_line = re.findall(r'[a-fA-F0-9]{1,4}(?::[a-fA-F0-9]{0,4})+', hop)
                if not ip_in_line: continue
                ip = ip_in_line[0].lower()
                if ip in ip_to_link_id:
                    make_path_dotted_orange(soup, ip_to_link_id[ip])
                if ip.upper()=="2001:470:1F1A:51::1" or ip.upper()=="2001:470:1F1A:51::2":
                    make_path_dotted_orange(soup, 'magentus-internet-link')
                    make_path_dotted_orange(soup, 'magentus-internet-cloud')
                if ip.upper() in MAGENTUS_R1_IPS:
                    make_path_dotted_orange(soup, 'magentus-r1')
                if ip.upper() in MAGENTUS_R2_IPS:
                    make_path_dotted_orange(soup, 'magentus-r2')

            make_path_dotted_orange(soup, 'bbf1591a-5019-416b-91e7-b81b336491ef') 
            f = open(f'./tests/bgp/images/ipv6/icann-r1-fail/{customer}.svg', 'w', encoding='utf-8')
            f.write(str(soup))
            f.close()
            final_output.write(f'    <img src="./images/ipv6/icann-r1-fail/{customer}.svg" width="100%">\n')
        else:
             print(f"❌ {customer} ping failed!")
             final_output.write(f"    <h4>{customer} ❌</h4>\n")
             final_output.write("    <p><strong>Sikertelen ping!</strong></p>\n")
            
        final_output.write("  </div>\n")
    final_output.write("</div>\n\n")
    final_output.write('<div style="page-break-after: always;"></div>\n\n')
    
    print("Tests finished, Re-enabling the link...")
    for link in ICANN_R1_links: suspend_link(link, False)

    # ---------------- ISP ICANN R2 Direct Connection Failure (IPv6) ----------------
    print("Beginning ICANN direct connection fail tests R2 (IPv6)")
    final_output.write('## ICANN R2 közvetlen kapcsolat hiba (IPv6)\n\n')
    final_output.write('ICANN R2 közvetlen összekötetése Yapper részéről megszakítva, kapcsolat Magentus-on keresztül\n\n')
    final_output.write('<img src=\"images/ipv6/icann-r2-fail/icann-r2-fail.svg\" style=\"display: block; margin: 10px auto; width: 400px;\">\n\n')
    
    ICANN_R2_links = [
        "fc241f25-068f-45f5-b94e-d3148797bf9b",
        "bea110a7-66e4-47d0-8071-3930953f7593",
    ]

    soup = BeautifulSoup(svg_data, 'xml')
    for link in ICANN_R2_links:
        suspend_link(link, True)
        path = soup.select_one(f'[data-link="{link}"] path')
        if path:
            current_style = path.get('style', '')
            path['style'] = f"{current_style}; stroke: red;"
            path['stroke'] = "red"
            
    if not os.path.exists(f'./tests/bgp/images/ipv6/icann-r2-fail/'):
        os.makedirs(f'./tests/bgp/images/ipv6/icann-r2-fail/')
        
    f = open(f'./tests/bgp/images/ipv6/icann-r2-fail/icann-r2-fail.svg', 'w', encoding='utf-8')
    f.write(str(soup))
    f.close()
    
    print("ICANN R2 links cut, waiting 20 seconds for BGP to converge...")
    await asyncio.sleep(20)
    
    ping_tasks_icann2 = []
    target_ip_r2 = '172:30:30::30'
    
    for customer in YAPPER_CUSTOMERS:
        ping_tasks_icann2.append(test_customer_connectivity(customer, target_ip_r2, [target_ip_r2]))
            
    results = await asyncio.gather(*ping_tasks_icann2)
    
    final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">\n')
    for i in range(len(results)):
        customer = YAPPER_CUSTOMERS[i]
        result = results[i][::-1]
        
        red_line_svg_file = open(f'./tests/bgp/images/ipv6/icann-r2-fail/icann-r2-fail.svg', 'r', encoding='utf-8')
        soup = BeautifulSoup(red_line_svg_file.read(), 'xml')
        red_line_svg_file.close()

        # Color setup
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
        
        final_output.write('  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">\n')
        
        ip_found = False
        target_check_list = [target_ip_r2]
        if len(result) > 0 and any(ip in result[0] for ip in target_check_list): ip_found = True
        elif len(result) > 1 and any(ip in result[1] for ip in target_check_list): ip_found = True
        elif len(result) > 2 and any(ip in result[2] for ip in target_check_list): ip_found = True
        
        if ip_found:
            print(f"✅ {customer} ping successful!")
            final_output.write(f"    <h4>{customer} ✅</h4>\n")
            success_line = next((line for line in result if any(ip in line for ip in target_check_list)), result[0] if result else "")
            success_line = success_line.strip().replace(' msec', 'ms').replace(' *', '')
            final_output.write(f"    <p><strong>Sikeres ping!</strong> {success_line}</p>\n")
            
            for hop in result[::-1]:
                ip_in_line = re.findall(r'[a-fA-F0-9]{1,4}(?::[a-fA-F0-9]{0,4})+', hop)
                if not ip_in_line: continue
                ip = ip_in_line[0].lower()
                if ip in ip_to_link_id:
                    make_path_dotted_orange(soup, ip_to_link_id[ip])
                if ip.upper()=="2001:470:1F1A:51::1" or ip.upper()=="2001:470:1F1A:51::2":
                    make_path_dotted_orange(soup, 'magentus-internet-link')
                    make_path_dotted_orange(soup, 'magentus-internet-cloud')
                if ip.upper() in YAPPER_R1_IPS:
                    make_path_dotted_orange(soup, 'yapper-r1')
                if ip.upper() in YAPPER_R2_IPS:
                    make_path_dotted_orange(soup, 'yapper-r2')

            make_path_dotted_orange(soup, 'fe42b4ad-4807-4eb8-a4f0-529db353c591')   
            f = open(f'./tests/bgp/images/ipv6/icann-r2-fail/{customer}.svg', 'w', encoding='utf-8')
            f.write(str(soup))
            f.close()
            final_output.write(f'    <img src="./images/ipv6/icann-r2-fail/{customer}.svg" width="100%">\n')
        else:
             print(f"❌ {customer} ping failed!")
             final_output.write(f"    <h4>{customer} ❌</h4>\n")
             final_output.write("    <p><strong>Sikertelen ping!</strong></p>\n")
            
        final_output.write("  </div>\n")
    final_output.write("</div>\n\n")
    final_output.write('<div style="page-break-after: always;"></div>\n\n')
    
    print("Tests finished, Re-enabling the link...")
    for link in ICANN_R2_links: suspend_link(link, False)

    # ---------------- Single Path Via ICANN (All Direct Links Disabled) ----------------
    print("Beginning Single Path Via ICANN tests (IPv6)")
    final_output.write('## Egyetlen útvonal ICANN-en keresztül (IPv6)\n\n')
    final_output.write('Minden közvetlen kapcsolat megszakítva, ICANN kapcsolatok redundanciája megszüntetve (1-1 link aktív)\n\n')
    final_output.write('<img src=\"images/ipv6/icann-single-path/icann-single-path.svg\" style=\"display: block; margin: 10px auto; width: 400px;\">\n\n')
    
    DIRECT_LINKS = [
        "d5472b6c-d8a5-43aa-8a68-44ff28d6260d",
        "2463004b-6ae1-45b9-8e5e-ef19f9093b6a",
        "84207e8f-7e75-4f5a-aec1-e2633da797b2",
        "1de7f299-a4cb-44a3-8d98-31e9bb348b0f"
    ]
    
    MAG_ICANN_LINKS = [
        {"id": "d6c7a1a8-cb46-4788-a652-2a26aaaf4194", "name": "Mag-R1"},
        {"id": "7fd3678a-4eae-4f08-9c22-bbba22832d9d", "name": "Mag-R2"}
    ]
    
    YAP_ICANN_LINKS = [
        {"id": "fc241f25-068f-45f5-b94e-d3148797bf9b", "name": "Yap-R1"},
        {"id": "bea110a7-66e4-47d0-8071-3930953f7593", "name": "Yap-R2"}
    ]
    
    if not os.path.exists(f'./tests/bgp/images/ipv6/icann-single-path/'):
        os.makedirs(f'./tests/bgp/images/ipv6/icann-single-path/')
        
    soup = BeautifulSoup(svg_data, 'xml')
    # Visual setup base
    for link in DIRECT_LINKS:
        path = soup.select_one(f'[data-link="{link}"] path')
        if path:
            current_style = path.get('style', '')
            path['style'] = f"{current_style}; stroke: red;"
            path['stroke'] = "red"
            
    f = open(f'./tests/bgp/images/ipv6/icann-single-path/icann-single-path.svg', 'w', encoding='utf-8')
    f.write(str(soup))
    f.close()

    # Disable Direct Links permanently for this section
    for link in DIRECT_LINKS: suspend_link(link, True)
    
    for mag_link in MAG_ICANN_LINKS:
        for yap_link in YAP_ICANN_LINKS:
            print(f"Testing combination: {mag_link['name']} <-> ICANN <-> {yap_link['name']}")
            
            # Disable other Magentus links
            for l in MAG_ICANN_LINKS:
                if l['id'] != mag_link['id']: suspend_link(l['id'], True)
            
            # Disable other Yapper links
            for l in YAP_ICANN_LINKS:
                if l['id'] != yap_link['id']: suspend_link(l['id'], True)
                
            print("Links configured, waiting 20s for convergence...")
            await asyncio.sleep(20)
            
            ping_tasks_single = []
            ping_targets_single = []
            
            for customer in CUSTOMERS:
                if 'yapper' in customer.lower():
                    # Yapper -> Magentus
                    target = "2001:470:216F:AAAA::66" 
                    ping_targets_single.append([
                        "2001:470:216F:AAAA::6",
                        "2001:470:216F:AAAA::3",
                        "2001:470:216F:AAAA::62",
                        "2001:470:216F:AAAA::66",
                    ])
                    ping_tasks_single.append(test_customer_connectivity(customer, target, ping_targets_single[-1]))
                else:
                     # Magentus -> Yapper
                     target = '2001:470:2171:BBBB:BBBB::14'
                     ping_targets_single.append([
                        "2001:470:2171:AAAA:AAAA:A:0:15",
                        "2001:470:2171:AAAA:AAAA:A:0:18",
                        "2001:470:2171:BBBB:BBBB::14",
                        "2001:470:2171:AAAA:AAAA:B:0:14",
                        "2001:470:2171:AAAA:AAAA:1:0:4",
                        "2001:470:2171:AAAA:AAAA:2:0:4",
                     ])
                     ping_tasks_single.append(test_customer_connectivity(customer, target, ping_targets_single[-1]))
                 
            results = await asyncio.gather(*ping_tasks_single)
            
            final_output.write(f"### Útvonal: {mag_link['name']} - ICANN - {yap_link['name']}\n\n")
            final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">\n')
            
            for i in range(len(results)):
                customer = CUSTOMERS[i]
                result = results[i][::-1]
                
                # SVG per case
                red_line_svg_file = open(f'./tests/bgp/images/ipv6/icann-single-path/icann-single-path.svg', 'r', encoding='utf-8')
                soup = BeautifulSoup(red_line_svg_file.read(), 'xml')
                red_line_svg_file.close()

                make_path_dotted_orange(soup, 'magentus-link')
                make_path_dotted_orange(soup, 'magentus-cloud')
                make_path_dotted_orange(soup, 'yapper-link')
                make_path_dotted_orange(soup, 'yapper-cloud')
                
                # Mark disabled ICANN links as red for this specific SVG
                for l in MAG_ICANN_LINKS:
                    if l['id'] != mag_link['id']:
                        path = soup.select_one(f'[data-link="{l["id"]}"] path')
                        if path: path['style'] = f"{path.get('style', '')}; stroke: red;"
                for l in YAP_ICANN_LINKS:
                     if l['id'] != yap_link['id']:
                        path = soup.select_one(f'[data-link="{l["id"]}"] path')
                        if path: path['style'] = f"{path.get('style', '')}; stroke: red;"

                # Highlight Source
                if 'yapper' in customer.lower():
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
                
                final_output.write('  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">\n')
                
                ip_found = False
                target_check_list = ping_targets_single[i]
                if len(result) > 0 and any(ip in result[0] for ip in target_check_list): ip_found = True
                elif len(result) > 1 and any(ip in result[1] for ip in target_check_list): ip_found = True
                elif len(result) > 2 and any(ip in result[2] for ip in target_check_list): ip_found = True
                
                if ip_found:
                    print(f"✅ {customer} ping successful!")
                    final_output.write(f"    <h4>{customer} ✅</h4>\n")
                    success_line = next((line for line in result if any(ip in line for ip in target_check_list)), result[0] if result else "")
                    success_line = success_line.strip().replace(' msec', 'ms').replace(' *', '')
                    final_output.write(f"    <p><strong>Sikeres ping!</strong> {success_line}</p>\n")
                    
                    for hop in result[::-1]:
                        ip_in_line = re.findall(r'[a-fA-F0-9]{1,4}(?::[a-fA-F0-9]{0,4})+', hop)
                        if not ip_in_line: continue
                        ip = ip_in_line[0].lower()
                        if ip in ip_to_link_id:
                            make_path_dotted_orange(soup, ip_to_link_id[ip])
                        if ip.upper()=="2001:470:1F1A:51::1" or ip.upper()=="2001:470:1F1A:51::2":
                            make_path_dotted_orange(soup, 'magentus-internet-link')
                            make_path_dotted_orange(soup, 'magentus-internet-cloud')
                        if ip.upper() in MAGENTUS_R1_IPS:
                            make_path_dotted_orange(soup, 'magentus-r1')
                        if ip.upper() in MAGENTUS_R2_IPS:
                            make_path_dotted_orange(soup, 'magentus-r2')
                        if ip.upper() in YAPPER_R1_IPS:
                            make_path_dotted_orange(soup, 'yapper-r1')
                        if ip.upper() in YAPPER_R2_IPS:
                            make_path_dotted_orange(soup, 'yapper-r2')
                    
                    id_combo = f"{mag_link['name']}-{yap_link['name']}-{customer}"
                    f = open(f'./tests/bgp/images/ipv6/icann-single-path/{id_combo}.svg', 'w', encoding='utf-8')
                    f.write(str(soup))
                    f.close()
                    final_output.write(f'    <img src="./images/ipv6/icann-single-path/{id_combo}.svg" width="100%">\n')
                else:
                    print(f"❌ {customer} ping failed!")
                    final_output.write(f"    <h4>{customer} ❌</h4>\n")
                    final_output.write("    <p><strong>Sikertelen ping!</strong></p>\n")
                
                final_output.write("  </div>\n")
                # Break page after 4 items (grid assumes 2 columns)
                if i == 3:
                     final_output.write("</div>\n\n")
                     final_output.write('<div style="page-break-after: always;"></div>\n\n')
                     if i < len(results) - 1:
                          final_output.write('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">\n')
            
            final_output.write("</div>\n\n")
            
            # Re-enable the specific ICANN links for next iteration (Direct links stay disabled)
            for l in MAG_ICANN_LINKS:
                if l['id'] != mag_link['id']: suspend_link(l['id'], False)
            for l in YAP_ICANN_LINKS:
                if l['id'] != yap_link['id']: suspend_link(l['id'], False)

    final_output.write('<div style="page-break-after: always;"></div>\n\n')
    
    print("Tests finished, Re-enabling all links...")
    for link in DIRECT_LINKS: suspend_link(link, False)
    
    final_output.close()

asyncio.run(main())