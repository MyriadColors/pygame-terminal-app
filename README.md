# Pygame Terminal Emulator

## Overview

The Pygame Terminal Emulator is a versatile Python library that allows developers to create interactive command-line interface (CLI) applications and games using Pygame. This library provides a customizable terminal-like interface that can be easily integrated into various projects, offering features such as command history, custom commands, and dynamic visual updates.

## Features

- Customizable terminal-like interface
- Command history navigation
- Easy-to-use command registration system
- Support for custom commands with arguments
- Dynamic text updates and progress bars
- Countdown functionality with custom messages
- Customizable colors for background and text

## Installation

To use the Pygame Terminal Emulator, make sure you have Python and Pygame installed. You can install Pygame using pip:

```
pip install pygame
```

Then, include the `terminal.py` and `color_data.py` files in your project directory.

## Usage

### Basic Setup

To create a basic terminal interface:

```python
from terminal import PygameTerminal

# Initialize the terminal
terminal = PygameTerminal(app_state=None, width=800, height=600, font_size=24)

# Run the terminal
terminal.run()
```

### Registering Custom Commands

You can easily add custom commands to your terminal:

```python
from terminal import PygameTerminal, Argument

def greet(name, term):
    term.write(f"Hello, {name}!")

terminal = PygameTerminal(app_state=None)
terminal.register_command(
    ["greet", "hello"],
    greet,
    [Argument("name", str, False)]
)

terminal.run()
```

Now, users can use the `greet` or `hello` command followed by a name.

### Creating a Simple Game

Here's an example of how to create a simple number guessing game using the Pygame Terminal Emulator:

```python
import random
from terminal import PygameTerminal, Argument

class GameState:
    def __init__(self):
        self.number = random.randint(1, 100)
        self.attempts = 0

def guess(number, term):
    game_state = term.app_state
    game_state.attempts += 1
    
    if int(number) == game_state.number:
        term.write(f"Congratulations! You guessed the number in {game_state.attempts} attempts!")
        game_state.number = random.randint(1, 100)
        game_state.attempts = 0
    elif int(number) < game_state.number:
        term.write("Too low! Try again.")
    else:
        term.write("Too high! Try again.")

terminal = PygameTerminal(app_state=GameState(), width=800, height=800, font_size=24)
terminal.register_command(
    ["guess"],
    guess,
    [Argument("number", int, False)]
)

terminal.write("Welcome to the Number Guessing Game!")
terminal.write("I'm thinking of a number between 1 and 100.")
terminal.write("Use the 'guess' command followed by a number to make a guess.")

terminal.run()
```

### Using Progress Bars and Countdowns

The Pygame Terminal Emulator supports progress bars and countdowns for more dynamic interactions:

```python
import time
from terminal import PygameTerminal

terminal = PygameTerminal(app_state=None)

def simulate_process(term):
    total_steps = 50
    for i in range(total_steps + 1):
        term.progress_bar(total_steps, i)
        time.sleep(0.1)
    term.write("Process completed!")

def start_countdown(term):
    term.countdown_with_message(
        10, 0, 1,
        "Countdown: {} seconds remaining",
        1,
        lambda: term.write("Countdown finished!")
    )

terminal.register_command(["process"], simulate_process)
terminal.register_command(["countdown"], start_countdown)

terminal.run()
```

## Customization

You can customize various aspects of the terminal, such as colors, font size, and dimensions:

```python
terminal = PygameTerminal(
    app_state=None,
    width=1024,
    height=768,
    font_size=32,
    initial_message="Welcome to my custom terminal!"
)

terminal.bg_color = (30, 30, 30)  # Dark gray background
terminal.fg_color = (0, 255, 0)   # Green text

terminal.run()
```

## Contributing

Contributions to the Pygame Terminal Emulator are welcome! Please feel free to submit pull requests, report bugs, or suggest new features.

## License

This project is open source and available under the MIT License.