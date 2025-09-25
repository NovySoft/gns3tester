import asyncio
import os
from blessed import Terminal

term = Terminal()

async def import_data() -> tuple[int, bool]:
    print_count = 0
    is_new_user = False
    with term.location():
        await asyncio.sleep(3)  # Simulate some delay for loading
        # Check if data folder exists
        if not os.path.exists('data'):
            print_count += 1
            print(
                term.move_down(1) + term.move_x(0) +
                term.yellow("Data folder not found. Creating 'data' folder...") +
                term.move_up(print_count + 1)
            )
            os.makedirs('data')
            await asyncio.sleep(3)  # Simulate some delay for loading
        else:
            check_files = os.listdir('data')
            if 'server.json' not in check_files:
                print_count += 1
                print(
                    term.move_down(1) + term.move_x(0) +
                    term.yellow("'server.json' not found in 'data' folder. You will need to login in the next screen...") +
                    term.move_up(print_count + 1)
                )
                is_new_user = True
                await asyncio.sleep(3)
    return print_count, is_new_user