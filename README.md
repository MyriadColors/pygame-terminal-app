# Pygame Terminal Emulator

A simple terminal emulator library built with Pygame, allowing you to create interactive terminal-like interfaces in your Pygame applications.

## Description

This library provides a basic terminal emulator that can be integrated into Pygame applications. It includes features such as:

- Command input and processing
- Command history navigation
- Customizable background and foreground colors
- Ability to register custom commands
- Basic text rendering and cursor display

The package also includes an example application demonstrating the usage of the library.

## Requirements

- Python 3.6+
- Pygame

## Installation

First, ensure you have Python installed on your system. Then, install Pygame using pip:

### Windows

```
pip install pygame
```

### macOS

```
pip3 install pygame
```

### Linux (Debian-based, e.g., Ubuntu)

```
sudo apt-get update
sudo apt-get install python3-pygame
```

### Linux (Arch-based)

```
sudo pacman -S python-pygame
```

## Running the Example Application

1. Clone this repository or download the source code.
2. Navigate to the `examples/trivial_app` directory.
3. Run the following command:

```
python main.py
```

On macOS or Linux, you might need to use `python3` instead of `python`.

## Building Applications with the Library

To use this library in your own Pygame application:

1. Copy the `terminal.py` and `color_data.py` files into your project directory.

2. Import the `PygameTerminal` class in your main script:

```python
from terminal import PygameTerminal
```

3. Create an instance of `PygameTerminal`:

```python
terminal = PygameTerminal(width=800, height=600)
```

4. Register your custom commands:

```python
def my_command(term, args):
    term.write(f"Custom command executed with args: {args}")

terminal.register_command("mycommand", my_command)
```

5. Run the terminal in your game loop:

```python
def main():
    terminal = PygameTerminal()
    # Register commands here
    terminal.run()

if __name__ == "__main__":
    main()
```

## Customizing the Terminal

You can customize various aspects of the terminal:

- Change colors using the `color` command in the terminal or by modifying the `bg_color` and `fg_color` attributes of the `PygameTerminal` instance.
- Adjust font size and type by modifying the `font` attribute in the `PygameTerminal` class.
- Add new commands by using the `register_command` method.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).