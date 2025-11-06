import telnetlib3
import asyncio
import functools
import globals

async def get_ip_and_mask_telnet(reader, writer, ip_map, device="Unknown"):
    ip_map.clear()
    writer.write("\r\n")
    writer.write("\r\n")
    writer.write("Cli")
    writer.write("\r\n")
    writer.write("\r\n")
    await asyncio.sleep(10)  # wait for prompt
    writer.write("\r\n")
    writer.write("\r\n")
    writer.write("enable")
    writer.write("\r\n")
    writer.write("\r\n")
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
                #  ip address 10.0.1.6/24
                parts = ip_line.split()
                if len(parts) >= 3:
                    ip = parts[2]
                    if '/' in ip:
                        ip, cidr = ip.split('/')
                        cidr = int(cidr)
                        # Convert CIDR to netmask
                        mask = '.'.join(str((0xffffffff << (32 - cidr) >> i) & 0xff) for i in [24, 16, 8, 0])
                    else:
                        mask = parts[3] if len(parts) > 3 else "Unknown"
                    if ip.lower() == "dhcp":
                        has_dhcp = True
                        dhcp_interfaces.append(interface)
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


async def arista_get_ip_and_mask_telnet(ip, port, device_name="Unknown"):
    ip_map = {}
    reader, writer = await telnetlib3.open_connection(ip, port, shell=exit_console_shell)
    await writer.protocol.waiter_closed # type: ignore
    shell_func = functools.partial(get_ip_and_mask_telnet, ip_map=ip_map, device=device_name)
    reader, writer = await telnetlib3.open_connection(ip, port, shell=shell_func)
    await writer.protocol.waiter_closed # type: ignore
    return ip_map