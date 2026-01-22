import asyncio
import functools
import telnetlib3
import globals

async def get_ospf_and_bgp_routerid_telnet_shell(reader, writer, router_ids, name="Unknown"):
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
    await asyncio.sleep(5)
    writer.write("\r\n")
    writer.write("\r\n")
    await asyncio.sleep(10)  # wait for prompt
    writer.write("enable\r\n")
    await asyncio.sleep(10)  # wait for enable

    outp = await reader.read(100000) # read until EOF
    
    writer.write("sh ip ospf | in ID\r\n")
    await asyncio.sleep(10)  # wait for command to complete
    outp = (await reader.read(10000)).split('\n') # read until EOF
    for line in outp:
        line = line.strip()
        if "with ID" in line:
            parts = line.split()
            if len(parts) >= 5:
                process_id = parts[3].strip('"')
                router_id = parts[-1]
                router_ids.append(f"{name}: OSPF Process {process_id} with Router ID {router_id}")
                print(globals.term.orange(f"{name}: Found OSPF process {process_id} with router ID: {router_id}"))
    
    writer.write("sh ip bgp summary | in ident\r\n")
    await asyncio.sleep(10)  # wait for command to complete
    outp = (await reader.read(10000)).split('\n') # read until EOF
    for line in outp:
        line = line.strip()
        if "BGP router identifier" in line:
            parts = line.split()
            if len(parts) >= 5:
                router_id = parts[3].strip(',')
                as_number = parts[-1]
                router_ids.append(f"{name}: BGP Router ID {router_id} with AS {as_number}")
                print(globals.term.orange(f"{name}: Found BGP router ID {router_id} with AS number {as_number}"))
    writer.close()


async def get_ospf_and_bgp_routerid_telnet(ip, port, device_name="Unknown"):
    router_ids = []
    # Multiple routers may posses the same ID, hence why we are using a single string list
    # sh ip ospf | in ID
    # Routing Process "ospf 20" with ID 2.1.2.2
    # sh ip bgp summary | in ident
    # BGP router identifier 172.18.111.21, local AS number 65101
    shell_func = functools.partial(get_ospf_and_bgp_routerid_telnet_shell, name=device_name, router_ids=router_ids)
    reader, writer = await telnetlib3.open_connection(ip, port, shell=shell_func)
    try:
        await asyncio.wait_for(writer.protocol.waiter_closed, timeout=30) # type: ignore
    except asyncio.TimeoutError:
        pass
    return router_ids