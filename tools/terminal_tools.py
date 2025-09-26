from globals import term

def input(prompt: str) -> str:
    output = ''
    print(prompt, end='', flush=True)
    while True:
        val = term.inkey()
        if val.isprintable():
            print(val, end='', flush=True)
            output += val
        if val.code == 343:  # Enter
            break
        elif val.code == 263:  # Backspace
            if output:
                output = output[:-1]
                print('\b \b', end='', flush=True)
    print() # Move to the next line after input
    return output