import telnetlib3
import asyncio
import functools

async def exit_console_shell(reader, writer):
    writer.write("\r\n")
    await asyncio.sleep(1)
    writer.write("\x03")  # Control+C
    writer.write("\x03")  # Control+C
    writer.write("\x03")  # Control+C
    writer.write("\x1e") 
    await asyncio.sleep(0.5)
    writer.write("\x1e")
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

async def run_traceroute_telnet(reader, writer, target_ip, source_ip, result_lines, device="Unknown"):
    """
    Shell function to run traceroute and capture output.
    """
    # --- Wake up and Enable ---
    writer.write("\r\n")
    await asyncio.sleep(2) 
    writer.write("enable\r\n")
    await asyncio.sleep(2)

    # Clear any banner/login text from buffer so it doesn't mix with results
    await reader.read(10000) 

    # --- Run Traceroute ---
    # We use 'numeric' to disable DNS lookup, which is much faster and safer for automation
    if source_ip == None:
        cmd = f"traceroute {target_ip}\r\n"
    else:
        cmd = f"traceroute {target_ip} numeric source {source_ip}\r\n"
    writer.write(cmd)
    
    print(f"Device {device} executing: {cmd.strip()}", flush=True)

    # Traceroute takes time. 
    # Adjusted sleep to 20s. Increase this if your network hops are very high latency.
    await asyncio.sleep(20) 

    # Read all output generated during the sleep
    outp = await reader.read(100000) 
    
    lines = outp.split('\n')
    
    capture_started = False
    
    for line in lines:
        line = line.rstrip()
        
        # Skip empty lines
        if not line:
            continue

        # Simple logic to filter out the command echo
        if line.startswith("traceroute"):
            capture_started = True
            continue
            
        # Stop if we hit the router prompt (usually ends with # or >)
        # You might need to adjust this regex or logic based on your specific hostname formats
        if line.endswith("#") or line.endswith(">"):
            if "Traceroute" not in line: # Ensure it's not a header line
                break

        # Capture the line
        if capture_started or line[0].isdigit():
            # Most traceroute lines start with the hop number (e.g., "1 10.0.0.1...")
            result_lines.append(line)
            #print(f"Device {device} Trace: {line}", flush=True)

    writer.close()

async def cisco_run_traceroute(ip, port, target_ip, source_ip, device_name="Unknown"):
    """
    Wrapper function to manage the connection lifecycle and retrieve traceroute lines.
    """
    traceroute_results = []
    
    # --- First Connection: Reset/Clean Session ---
    # Reusing the exit_console_shell from your example to ensure a clean state
    # (Assuming exit_console_shell is defined in your scope as per your snippet)
    try:
        reader, writer = await telnetlib3.open_connection(ip, port, shell=exit_console_shell)
        await asyncio.wait_for(asyncio.shield(writer.protocol.waiter_closed), timeout=30)
    except Exception as e:
        print(f"Notice: First connection reset skipped or failed on {device_name}: {e}")
        # We continue anyway, as the second connection might still work
    
    # --- Second Connection: Actual Work ---
    # Create a partial function to pass arguments into the shell handler
    shell_func = functools.partial(
        run_traceroute_telnet, 
        target_ip=target_ip, 
        source_ip=source_ip,
        result_lines=traceroute_results, 
        device=device_name
    )
    
    try:
        reader, writer = await telnetlib3.open_connection(ip, port, shell=shell_func)
        await asyncio.wait_for(asyncio.shield(writer.protocol.waiter_closed), timeout=60)
    except asyncio.TimeoutError:
        print(f"Timeout waiting for traceroute completion on {device_name}")
        writer.close()
    except Exception as e:
        print(f"Error running traceroute on {device_name}: {e}")

    return traceroute_results