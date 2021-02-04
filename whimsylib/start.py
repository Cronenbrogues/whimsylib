from whimsylib import when


def start():
    while True:
        try:
            command = input("> ").strip()
        except EOFError:
            print()
            break

        if not command:
            continue

        when.CommandHandler.handle(command)
