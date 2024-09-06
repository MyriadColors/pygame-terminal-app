# main.py
from commands import register_commands
from terminal import PygameTerminal

def main():
    terminal = PygameTerminal()
    register_commands(terminal)
    terminal.run()

if __name__ == "__main__":
    main()