import telnetlib3
import asyncio
import functools

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
    for i in range(len(outp)):
        line = outp[i].strip()
        if line.startswith("interface"):
            interface = line.split()[1]
            ip_line = outp[i+1].strip() if i+1 < len(outp) else ""
            if ip_line.startswith("ip address"):
                parts = ip_line.split()
                if len(parts) >= 3:
                    ip = parts[2]
                    mask = parts[3] if len(parts) > 3 else "Unknown"
                    print(f"Device {device} Interface {interface} has IP {ip} with mask {mask}", flush=True)
                    ip_map[interface] = (ip, mask)

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
    reader, writer = await telnetlib3.open_connection(ip, port, shell=exit_console_shell)
    await writer.protocol.waiter_closed # type: ignore
    shell_func = functools.partial(get_ip_and_mask_telnet, ip_map=ip_map, device=device_name)
    reader, writer = await telnetlib3.open_connection(ip, port, shell=shell_func)
    await writer.protocol.waiter_closed # type: ignore
    return ip_map