import asyncio
from blessed import Terminal

term = Terminal()

async def import_data():
    with term.location():
        # Simulate a long-running data import task
        await asyncio.sleep(6)  # Replace with actual data import logic