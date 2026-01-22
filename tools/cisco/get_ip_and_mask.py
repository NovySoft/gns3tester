import telnetlib3
import asyncio
import functools
import globals

async def get_ip_and_mask_telnet(reader, writer, ip_map, device="Unknown"):
    ip_map.clear()
    writer.write("\r\n")
    writer.write("\r\n")
    await asyncio.sleep(10)  # wait for prompt
    writer.write("enable\r\n")
    await asyncio.sleep(10)  # wait for enable


    # go to last line of output
    #FIXME: Any way to make this better/faster?
    outp = await reader.read(100000) # read until EOF
    #print(outp, flush=True)

    writer.write("sh run | include interface | ip address\r\n")
    await asyncio.sleep(30)  # wait for command to complete
    outp = (await reader.read(10000)).split('\n') # read until EOF
    has_dhcp = False
    dhcp_interfaces = []
    for i in range(len(outp)):
        line = outp[i].strip()
        if line.startswith("interface"):
            interface = line.split()[1]
            ip_line = outp[i+1].strip() if i+1 < len(outp) else ""
            if ip_line.startswith("ip address"):
                parts = ip_line.split()
                if len(parts) >= 3:
                    ip = parts[2]
                    if ip.lower() == "dhcp":
                        has_dhcp = True
                        dhcp_interfaces.append(interface)
                    mask = parts[3] if len(parts) > 3 else "Unknown"
                    print(f"Device {device} Interface {interface} has IP {ip} with mask {mask}", flush=True)
                    ip_map[interface] = (ip, mask)
    if has_dhcp:
        print(globals.term.yellow(f"Device {device} has DHCP assigned IPs, fetching via 'sh ip int'"), flush=True)
        for interface in dhcp_interfaces:
            writer.write(f"sh ip int {interface}\r\n")
            await asyncio.sleep(10)  # wait for command to complete
            outp = (await reader.read(10000)).split('\n') # read until EOF
            for line in outp:
                line = line.strip()
                if line.startswith("Internet address is"):
                    parts = line.split()
                    if len(parts) >= 4:
                        ip_mask = parts[3]
                        if '/' in ip_mask:
                            ip, cidr = ip_mask.split('/')
                            cidr = int(cidr)
                            # Convert CIDR to netmask
                            mask = '.'.join(str((0xffffffff << (32 - cidr) >> i) & 0xff) for i in [24, 16, 8, 0])
                        else:
                            ip = ip_mask
                            mask = "Unknown"
                        print(globals.term.orange(f"Device {device} Interface {interface} has DHCP IP {ip} with mask {mask}"), flush=True)
                        ip_map[interface] = (ip + " (dhcp)", mask)

    # Fetch IPv6 addresses
    writer.write("\r\n")
    writer.write("                        \r\n")
    writer.write("\r\n")
    writer.write("sh run | include interface | ipv6 address\r\n")
    await asyncio.sleep(30)  # wait for command to complete
    outp = (await reader.read(10000)).split('\n')
    
    if "IP6" in device:
        print()

    for i in range(len(outp)):
        line = outp[i].strip()
        if line.startswith("interface"):
            interface = line.split()[1]
            ipv6_line = outp[i+1].strip() if i+1 < len(outp) else ""
            if ipv6_line.startswith("ipv6 address"):
                parts = ipv6_line.split()
                if len(parts) >= 3:
                    ipv6_addr = parts[2]  # Will be in format 2001:470:216F:AAAA::67/127
                    print(f"Device {device} Interface {interface} has IPv6 {ipv6_addr}", flush=True)
                    # Store IPv6 with a special key to distinguish from IPv4
                    if interface not in ip_map:
                        ip_map[interface] = ("Unassigned", "Unassigned")
                    # Add ipv6 info to the tuple
                    current = ip_map.get(interface, ("Unassigned", "Unassigned"))
                    ip_map[interface] = (*current, ipv6_addr, None)  # (ipv4, mask, ipv6, ipv6_link_local)
    
    # Fetch IPv6 link-local addresses
    writer.write("sh ipv6 int br\r\n")
    await asyncio.sleep(10)
    outp = (await reader.read(10000)).split('\n')
    
    current_interface = None
    for line in outp:
        line = line.strip()
        # Interface line contains [up/up] or similar
        if '[' in line and '/' in line:
            parts = line.split()
            if len(parts) >= 1:
                current_interface = parts[0]
        # IPv6 address lines (both link-local FE80:: and global)
        elif current_interface and line.startswith('FE80::'):
            link_local = line.split()[0] if line.split() else line
            print(f"Device {device} Interface {current_interface} has IPv6 link-local {link_local}", flush=True)
            if current_interface in ip_map:
                current = ip_map[current_interface]
                if len(current) == 4:
                    # Replace None with actual link-local
                    ip_map[current_interface] = (current[0], current[1], current[2], link_local)
                elif len(current) == 2:
                    # No global IPv6, just add link-local
                    ip_map[current_interface] = (*current, None, link_local)
            else:
                ip_map[current_interface] = ("Unassigned", "Unassigned", None, link_local)
        

async def exit_console_shell(reader, writer):
    writer.write("\r\n")
    await asyncio.sleep(1)
    writer.write("\x03")  # Control+C
    writer.write("\x03")  # Control+C
    writer.write("\x03")  # Control+C
    writer.write("exit\r\n")
    await asyncio.sleep(1)
    writer.write("\r\n\r\n")
    writer.write("\r\n")
    writer.write("\r\n")
    # SEND RETURN TO WAKE UP THE DEVICE
    await asyncio.sleep(1)
    writer.write("\r\n")
    writer.write("")
    await asyncio.sleep(3)
    writer.close()

async def cisco_get_ip_and_mask_telnet(ip, port, device_name="Unknown"):
    ip_map = {}
    
    # --- First Connection ---
    reader, writer = await telnetlib3.open_connection(ip, port, shell=exit_console_shell)
    try:
        await asyncio.wait_for(asyncio.shield(writer.protocol.waiter_closed), timeout=60)
    except asyncio.TimeoutError:
        print(f"Timeout waiting for first connection on {device_name}")
        # Ideally, close the writer if you are abandoning it
        writer.close() 
    
    # --- Second Connection ---
    shell_func = functools.partial(get_ip_and_mask_telnet, ip_map=ip_map, device=device_name)
    reader, writer = await telnetlib3.open_connection(ip, port, shell=shell_func)
    try:
        await asyncio.wait_for(asyncio.shield(writer.protocol.waiter_closed), timeout=60)
    except asyncio.TimeoutError:
        print(f"Timeout waiting for second connection on {device_name}")
        writer.close()

    return ip_map