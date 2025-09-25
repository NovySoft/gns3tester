import asyncio
from blessed import Terminal

async def import_data(term):
    with term.location():
        # Simulate a long-running data import task
        await asyncio.sleep(6)  # Replace with actual data import logic