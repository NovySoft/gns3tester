import telnetlib3
import asyncio

ip_map = {}  # interface -> (ip, mask)

async def get_ip_and_mask_telnet_shell(reader, writer):
    global ip_map
    ip_map = {}
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
    writer.write("")
    await asyncio.sleep(1)
    writer.write("enable\r\n")

    # go to last line of output
    #FIXME: Any way to make this better/faster?
    outp = await reader.read(100000) # read until EOF
    #print(outp, flush=True)

    writer.write("sh run | include interface | ip address\r\n")
    await asyncio.sleep(5)
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
                    print(f"\tInterface {interface} has IP {ip} with mask {mask}", flush=True)
                    ip_map[interface] = (ip, mask)
    writer.close()


async def cisco_get_ip_and_mask_telnet(ip, port):
    global ip_map
    reader, writer = await telnetlib3.open_connection(ip, port, shell=get_ip_and_mask_telnet_shell)
    await writer.protocol.waiter_closed # type: ignore
    return ip_map