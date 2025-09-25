try:
    from blessed import Terminal
    import globals
except ImportError:
    print("This program requires the 'blessed' package. Install it via 'py -m pip install blessed'")
    exit(1)

from screen.welcome_screen import display_welcome_screen
import asyncio

if __name__ == "__main__":
    asyncio.run(display_welcome_screen())