import random

from terminal import PygameTerminal, Argument


class Character:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.exp = 0
        self.exp_to_level = 100
        self.level = 1
        self.gold = 0

    def level_up(self):
        self.level += 1
        self.max_hp += 5
        self.hp = self.max_hp
        self.attack += 2
        self.defense += 1
        self.exp_to_level *= 1.1

    def attack(self, target: 'Enemy', term: PygameTerminal):
        damage = self.attack - target.defense
        if damage < 0:
            damage = 0
        target.hp -= damage
        term.write(f"You attack the {target.name} for {damage} damage.")
        term.write(f"The {target.name} has {target.hp} HP remaining.")

class Enemy:
    def __init__(self, name, hp, attack, defense, exp_reward, gold_reward):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward

    def attack(self, target: 'Character', term: PygameTerminal):
        damage = self.attack - target.defense
        if damage < 0:
            damage = 0
        target.hp -= damage
        term.write(f"The {self.name} attacks you for {damage} damage.")
        term.write(f"You have {target.hp} HP remaining.")

class GameState:
    def __init__(self):
        self.player = None
        self.current_room = 0
        self.total_rooms = 5

    @staticmethod
    def generate_enemy():
        enemies = [
            Enemy("Goblin", 20, 5, 2, 10, 5),
            Enemy("Orc", 30, 7, 3, 15, 10),
            Enemy("Skeleton", 25, 6, 1, 12, 8),
            Enemy("Troll", 40, 8, 4, 20, 15),
        ]
        return random.choice(enemies)


def create_character(name, class_type, term: PygameTerminal):
    if class_type.lower() == "warrior":
        term.app_state.player = Character(name, 50, 15, 5)
    elif class_type.lower() == "mage":
        term.app_state.player = Character(name, 35, 25, 3)
    elif class_type.lower() == "rogue":
        term.app_state.player = Character(name, 45, 20, 4)
    else:
        term.write("Invalid class. Please choose warrior, mage, or rogue.")
        return

    term.write(f"Welcome, {name} the {class_type}!")
    term.write(
        f"Stats: HP: {term.app_state.player.hp}, Attack: {term.app_state.player.attack}, Defense: {term.app_state.player.defense}")
    term.write("Type 'explore' to begin your adventure!")


def explore(term):
    if term.app_state.player is None:
        term.write("Please create a character first using the 'create' command.")
        return

    term.app_state.current_room += 1
    if term.app_state.current_room > term.app_state.total_rooms:
        term.write("Congratulations! You've cleared all the rooms and won the game!")
        return

    term.write(f"You enter room {term.app_state.current_room} of {term.app_state.total_rooms}.")

    if random.random() < 0.7:  # 70% chance of encountering an enemy
        enemy = term.app_state.generate_enemy()
        term.write(f"You encounter a {enemy.name}!")
        term.write("Type 'fight' to engage in combat or 'run' to try to escape.")
    else:
        term.write("The room is empty. You can safely rest here.")
        term.write("Type 'rest' to recover some HP or 'explore' to continue.")


def fight(term: PygameTerminal):
    player: Character = term.app_state.player
    enemy: Enemy = term.app_state.generate_enemy()

    term.write("============================================")
    term.write(f"You engage in combat with the {enemy.name}!")

    while player.hp > 0 and enemy.hp > 0:
        term.write("============================================")
        term.write(f"HP: {player.hp}/{player.max_hp} | {enemy.name} HP: {enemy.hp}/{enemy.hp}")
        term.write(f"Attack: {player.attack} | Defense: {player.defense}")
        term.write(f"Attack: {enemy.attack} | Defense: {enemy.defense}")
        term.write("============================================")

        player.attack(enemy, term)
        if enemy.hp > 0:
            enemy.attack(player, term)

        term.write("Type 'fight' to continue the battle or 'run' to try to escape.")

    if player.hp <= 0:
        term.write("============================================")
        term.write("You have been defeated by the enemy. You lose the game.")
    else:
        term.write("============================================")
        term.write("You have defeated the enemy. You win the game.")
        player.exp += enemy.exp_reward
        player.gold += enemy.gold_reward
        term.write(f"You gained {enemy.exp_reward} exp and {enemy.gold_reward} gold.")

def run(term):
    if random.random() < 0.5:
        term.write("You successfully escaped!")
    else:
        term.write("You failed to escape. Prepare for combat!")
        fight(term)


def rest(term):
    player = term.app_state.player
    heal_amount = min(player.max_hp - player.hp, 20)
    player.hp += heal_amount
    term.write(f"You rest and recover {heal_amount} HP. Your current HP: {player.hp}/{player.max_hp}")
    term.write("Type 'explore' to continue your adventure.")


def status(term):
    player = term.app_state.player
    if player:
        term.write(f"Name: {player.name}")
        term.write(f"Class: {player.__class__.__name__}")
        term.write(f"Level: {player.level}")
        term.write(f"HP: {player.hp}/{player.max_hp}")
        term.write(f"Attack: {player.attack}")
        term.write(f"Defense: {player.defense}")
        term.write(f"EXP: {player.exp}/{player.exp_to_level}")
        term.write(f"Current room: {term.app_state.current_room}/{term.app_state.total_rooms}")
    else:
        term.write("No character created yet. Use the 'create' command to start your adventure.")

def help_command(term):
    term.write("Available commands:")
    for command_name in term.app_state.commands.keys():
        term.write(f"  {command_name}")

def main():
    terminal = PygameTerminal(app_state=GameState(), width=1024, height=768, font_size=28)

    terminal.register_command(
        ["create"],
        create_character,
        [Argument("name", str, False), Argument("class", str, False)]
    )
    terminal.register_command(["explore", "ex"], explore)
    terminal.register_command(["fight", "fg"], fight)
    terminal.register_command(["run", "ru"], run)
    terminal.register_command(["rest", "re"], rest)
    terminal.register_command(["status", "st"], status)
    terminal.register_command(["help", "h"], help_command)

    terminal.write("Welcome to Terminal Dungeon Crawler!")
    terminal.write("Create your character using the 'create' command.")
    terminal.write("Example: create John warrior")
    terminal.write("Available classes: warrior, mage, rogue")

    terminal.run()


if __name__ == "__main__":
    main()
