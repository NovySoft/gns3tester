import asyncio
import globals
from globals import term

async def display_login_screen(title: str, red: bool = False):
    with term.cbreak(), term.hidden_cursor():
        print(term.clear)
        if red:
            print(term.red_bold(title))
        else:
            print(term.bold(title))
        print(term.move_down(2) + "Please enter your login details below.\n")
        print(term.move_down(1) + "Server host: ", end="", flush=True)

