import pygame
import sys
from pygame import *

pygame.init()

class TerminalState:
    def __init__(self):
        self.terminal_lines = ["Welcome to Pygame Terminal Emulator"]
        self.current_line = ""
        self.cursor_pos = 0
        self.command_history = []
        self.history_index = -1
        self.default_bg_color = color["black"]
        self.bg_color = self.default_bg_color
        self.default_fg_color = color["white"]
        self.fg_color = self.default_fg_color
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 32)

color = {
    "black" : (0, 0, 0),
    "white" : (255, 255, 255),
    "red" : (255, 0, 0),
    "green" : (0, 255, 0),
    "blue" : (0, 0, 255),
    "yellow" : (255, 255, 0),
    "cyan" : (0, 255, 255),
    "magenta" : (255, 0, 255),
    "gray64" : (64, 64, 64),
}

def does_color_exist(color_str: str):
    return color_str in color

pygame.display.set_caption("Pygame Terminal Emulator")
state = TerminalState()

def draw_terminal():
    state.screen.fill(state.bg_color)
    y = 10
    for line in state.terminal_lines[-18:]:  # Show last 18 lines
        text = state.font.render(line, True, state.fg_color)
        state.screen.blit(text, (10, y))
        y += 30

    prompt = "> " + state.current_line
    text = state.font.render(prompt, True, state.fg_color)
    state.screen.blit(text, (10, state.height - 40))

    cursor_x = 10 + state.font.size("> " + state.current_line[:state.cursor_pos])[0]
    pygame.draw.line(state.screen, state.fg_color, (cursor_x, state.height - 40), (cursor_x, state.height - 10), 2)

    pygame.display.flip()

def write(text):
    global state
    state.terminal_lines.append(text)

def handle_return():
    if state.current_line.strip():
        state.command_history.append(state.current_line)
    process_command(state.current_line)
    state.current_line = ""
    state.cursor_pos = 0
    state.history_index = -1

def handle_backspace():
    if state.cursor_pos > 0:
        state.current_line = state.current_line[:state.cursor_pos-1] + state.current_line[state.cursor_pos:]
        state.cursor_pos -= 1

def handle_left_arrow():
    state.cursor_pos = max(0, state.cursor_pos - 1)

def handle_right_arrow():
    state.cursor_pos = min(len(state.current_line), state.cursor_pos + 1)

def handle_up_arrow():
    if state.history_index < len(state.command_history) - 1:
        state.history_index += 1
        state.current_line = state.command_history[-(state.history_index + 1)]
        state.cursor_pos = len(state.current_line)

def handle_down_arrow():
    if state.history_index > -1:
        state.history_index -= 1
        if state.history_index == -1:
            state.current_line = ""
        else:
            state.current_line = state.command_history[-(state.history_index + 1)]
        state.cursor_pos = len(state.current_line)

def handle_printable(char):
    state.current_line = state.current_line[:state.cursor_pos] + char + state.current_line[state.cursor_pos:]
    state.cursor_pos += 1

def handle_greet(args):
    if args:
        write(f"Hello, {args[0]}!")
    else:
        write("Hello! Please provide a name to greet.")

def parse_command(command):
    parts = command.split()
    cmd = parts[0].lower() if parts else ""
    args = parts[1:]
    args = [arg.lower() for arg in args]
    return cmd, args


def args_length(args):
    if args:
        return len(args[0])
    else:
        return 0

def handle_change_bg_color(color_param: str):
    if not does_color_exist(color_param):
        write(f"Unknown color: {color_param}")
        return

    state.bg_color = color[color_param]
    write(f"Background color changed to {color_param}")

def handle_change_fg_color(color_param: str):
    if not does_color_exist(color_param):
        write(f"Unknown color: {color_param}")
        return

    state.fg_color = color[color_param]
    write(f"Foreground color changed to {color_param}")

def reset_terminal(type_of_reset: str):
    if type_of_reset == "colors":
        state.fg_color = state.default_fg_color
        state.bg_color = state.default_bg_color
    elif type_of_reset == "bg":
        state.bg_color = state.default_bg_color
    elif type_of_reset == "fg":
        state.fg_color = state.default_fg_color
    else:
        write(f"Unknown type of reset: {type_of_reset}")

def process_command(command_string):
    cmd, args = parse_command(command_string)
    if cmd == "exit":
        pygame.quit()
        sys.exit()
    elif cmd == "clear":
        state.terminal_lines.clear()
    elif cmd == "greet":
        handle_greet(args)
    elif cmd == "color":
        if args_length(args) != 2:
            write("Usage: color <type> <color>")
            write("Types: bg, fg")
            write("Colors: black, white, red, green, blue, yellow, cyan, magenta, gray64")
            return
        if args[0] == "bg":
            handle_change_bg_color(args[1])
        elif args[0] == "fg":
            handle_change_fg_color(args[1])
        else:
            write("Unknown type of color: " + args[0])
    elif cmd == "reset":
        if not args_length(args) == 1:
            write("Usage: reset <type>")
            write("Types: colors, bg, fg")
            return
        reset_terminal(args[0])
    elif cmd == "help":
        if args_length(args) == 0:
            write("Available commands: exit, clear, greet, bg_color, fg_color, help")
            write("Type 'help <command>' for more information on a specific command.")
            return
        handle_command_help(args)
    else:
        write(f"Unknown command: {command_string}")


def handle_command_help(args):
    if args[0] == "exit":
        write("exit: Exits the program.")
    elif args[0] == "clear":
        write("clear: Clears the terminal screen.")
    elif args[0] == "greet":
        write("greet <name>: Greets the specified name.")
    elif args[0] == "color":
        write("color <type> <color>: Changes the background or foreground color.")
        write("Types: bg, fg")
        write("Colors: black, white, red, green, blue, yellow, cyan, magenta, gray64")
    elif args[0] == "reset":
        write("reset <type>: Resets the background or foreground color to default.")
        write("Types: colors, bg, fg")
    elif args[0] == "help":
        write("help: Prints this help message.")
    else:
        write(f"Unknown command: {args[0]}")

def handle_event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            handle_return()
        elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
            handle_backspace()
        elif event.key == pygame.K_LEFT:
            handle_left_arrow()
        elif event.key == pygame.K_RIGHT:
            handle_right_arrow()
        elif event.key == pygame.K_UP:
            handle_up_arrow()
        elif event.key == pygame.K_DOWN:
            handle_down_arrow()
        elif event.unicode.isprintable():
            handle_printable(event.unicode)

def main():

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                handle_event(event)

        draw_terminal()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()