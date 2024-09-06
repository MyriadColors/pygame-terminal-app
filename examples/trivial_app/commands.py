import color_data
from terminal import PygameTerminal

def command_help(term, args):
    """Print available commands."""
    if args[0] == "exit":
        term.write("exit: Exits the program.")
    elif args[0] == "clear":
        term.write("clear: Clears the terminal screen.")
    elif args[0] == "greet":
        term.write("greet <name>: Greets the specified name.")
    elif args[0] == "color":
        term.write("color <type> <color>: Changes the background or foreground color.")
        term.write("Types: bg, fg")
        term.write("Colors: black, white, red, green, blue, red[16 to 240], green[16 to 240], blue, gray[16 to 240]")
    elif args[0] == "reset":
        term.write("reset <type>: Resets the terminal to its default settings.")
        term.write("This includes clearing the screen and resetting the color.")
        term.write("Types: color, bg, fg, text, history, all")
        if args[1] == "all":
            term.write("This will also clear the terminal screen and command history.")
        elif args[1] == "history":
            term.write("This will also clear the command history.")
        elif args[1] == "text":
            term.write("This will also clear the terminal screen text.")
        elif args[1] == "color":
            term.write("This will also reset the color to the default.")
        elif args[1] == "bg":
            term.write("This will also reset the background color to the default.")
        elif args[1] == "fg":
            term.write("This will also reset the foreground color to the default.")
        else:
            term.write(f"Unknown argument: {args[1]}")
    elif args[0] == "help":
        term.write("help: Prints this help message.")
    else:
        term.write(f"Unknown command: {args[0]}")


def command_clear(term, _args):
    """Clear the terminal screen."""
    term.clear()


def command_echo(term, args):
    """Echo the input arguments."""
    if args:
        term.write(" ".join(args))
    else:
        term.write("Usage: echo <message>")


def command_exit(term):
    """Exit the terminal."""
    term.write("Exiting...")
    term.running = False


def command_color(term, args):
    if PygameTerminal.args_length(args) != 2:
        term.write("Usage: color <type> <color>")
        command_help(term, ["color"])
        return

    color_type = args[0]
    if color_type not in ["bg", "fg"]:
        term.write(f"Invalid type: {color_type}")
        command_help(term, ["color"])
        return

    color = args[1]
    if not color_data.does_color_exist(color):
        term.write(f"Invalid color: {color}")
        command_help(term, ["color"])
        return

    if color_type == "bg":
        term.bg_color = color_data.get_color(color)
        return

    if color_type == "fg":
        term.fg_color = color_data.get_color(color)
        return


def command_reset(term, type_of_reset: str):
    if type_of_reset == "color":
        term.fg_color = term.default_fg_color
        term.bg_color = term.default_bg_color
    elif type_of_reset == "bg":
        term.bg_color = term.default_bg_color
    elif type_of_reset == "fg":
        term.fg_color = term.default_fg_color
    elif type_of_reset == "text":
        term.clear()
    elif type_of_reset == "history":
        term.command_history.clear()
    elif type_of_reset == "all":
        term.fg_color = term.default_fg_color
        term.bg_color = term.default_bg_color
        term.clear()
    else:
        term.fg_color = term.default_fg_color
        term.bg_color = term.default_bg_color
        term.clear()


def command_greet(term, args):
    """Greet the specified name."""
    if not args:
        command_help(term, ["greet"])
        return

    name = args[0]

    term.write(f"Hello, {name}!")


def register_commands(terminal):
    terminal.register_command("help", command_help)
    terminal.register_command("clear", command_clear)
    terminal.register_command("echo", command_echo)
    terminal.register_command("color", command_color)
    terminal.register_command("reset", command_reset)
    terminal.register_command("greet", command_greet)
    terminal.register_command("exit", command_exit)
