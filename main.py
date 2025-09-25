from welcome_screen import display_welcome_screen
import asyncio

try:
    from blessed import Terminal
    import globals
except ImportError:
    print("This program requires the 'blessed' package. Install it via 'py -m pip install blessed'")
    exit(1)

if __name__ == "__main__":
    asyncio.run(display_welcome_screen())