import json
import random
import sys
import time

# ANSI color codes for premium terminal styling
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_RED = "\033[31m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_MAGENTA = "\033[35m"
C_CYAN = "\033[36m"
C_WHITE = "\033[37m"

SAVE_FILE = "rpg_save.json"

# World Map Definition
WORLD_MAP = {
    "Town Square": {
        "description": "The bustling center of Oakhaven. Shopkeepers call out and locals gather near the fountain.",
        "exits": {"north": "Dark Forest", "east": "Armory"},
        "items": [],
        "monster": None
    },
    "Armory": {
        "description": "A smoke-filled blacksmith shop filled with the clanging of steel. You can buy gear here.",
        "exits": {"west": "Town Square"},
        "items": [],
        "monster": None,
        "is_shop": True
    },
    "Dark Forest": {
        "description": "Towering pine trees block out most light. Fog creeps along the damp forest floor.",
        "exits": {"south": "Town Square", "north": "Deep Cave", "east": "Ancient Ruins"},
        "items": ["Health Potion"],
        "monster": "Goblin"
    },
    "Ancient Ruins": {
        "description": "Cracked marble pillars covered in ivy. Eerie arcane whispers float on the wind.",
        "exits": {"west": "Dark Forest"},
        "items": ["Ancient Relic"],
        "monster": "Skeleton"
    },
    "Deep Cave": {
        "description": "A pitch-black cavern dripping with water. A massive shadow moves in the back.",
        "exits": {"south": "Dark Forest"},
        "items": ["Dragon Heart"],
        "monster": "Dragon"
    }
}

MONSTERS = {
    "Goblin": {"hp": 30, "max_hp": 30, "attack": 6, "defense": 2, "xp_reward": 40, "gold_reward": 15},
    "Skeleton": {"hp": 45, "max_hp": 45, "attack": 9, "defense": 3, "xp_reward": 60, "gold_reward": 25},
    "Dragon": {"hp": 120, "max_hp": 120, "attack": 18, "defense": 8, "xp_reward": 200, "gold_reward": 100}
}

SHOP_ITEMS = {
    "Health Potion": {"cost": 10, "desc": "Restores 35 HP"},
    "Iron Sword": {"cost": 30, "desc": "+5 Attack Power"},
    "Steel Armor": {"cost": 45, "desc": "+3 Defense"}
}

class Player:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        self.gold = 20
        self.inventory = ["Health Potion"]
        self.current_room = "Town Square"
        
        # Class-specific starting attributes
        if char_class == "Warrior":
            self.max_hp = 60
            self.hp = 60
            self.attack = 10
            self.defense = 5
        elif char_class == "Mage":
            self.max_hp = 40
            self.hp = 40
            self.attack = 14
            self.defense = 2
        else: # Rogue
            self.max_hp = 50
            self.hp = 50
            self.attack = 12
            self.defense = 3

    def show_status(self):
        print(f"\n{C_BOLD}{C_CYAN}================= PLAYER STATUS ================={C_RESET}")
        print(f"{C_BOLD}Name:{C_RESET} {self.name} the {self.char_class}    | {C_BOLD}Level:{C_RESET} {self.level}")
        print(f"{C_BOLD}HP:{C_RESET} {C_GREEN if self.hp > self.max_hp * 0.4 else C_RED}{self.hp}/{self.max_hp}{C_RESET} | {C_BOLD}XP:{C_RESET} {self.xp}/{self.xp_to_next}")
        print(f"{C_BOLD}Attack:{C_RESET} {self.attack}            | {C_BOLD}Defense:{C_RESET} {self.defense}")
        print(f"{C_BOLD}Gold:{C_RESET} {C_YELLOW}{self.gold}g{C_RESET}             | {C_BOLD}Inventory:{C_RESET} {', '.join(self.inventory) if self.inventory else 'Empty'}")
        print(f"{C_CYAN}================================================={C_RESET}\n")

    def gain_xp(self, amount):
        self.xp += amount
        print(f"{C_GREEN}[+] Gained {amount} XP!{C_RESET}")
        if self.xp >= self.xp_to_next:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next
        self.xp_to_next = int(self.xp_to_next * 1.5)
        
        hp_gain = 10 if self.char_class == "Warrior" else (6 if self.char_class == "Mage" else 8)
        atk_gain = 2 if self.char_class != "Warrior" else 1
        def_gain = 2 if self.char_class == "Warrior" else 1

        self.max_hp += hp_gain
        self.hp = self.max_hp
        self.attack += atk_gain
        self.defense += def_gain

        print(f"\n{C_BOLD}{C_YELLOW}🎉 LEVEL UP! You reached Level {self.level}! 🎉{C_RESET}")
        print(f"Stats increased! HP +{hp_gain}, Attack +{atk_gain}, Defense +{def_gain}. Fully healed!")
        time.sleep(1.5)

    def to_dict(self):
        return {
            "name": self.name,
            "char_class": self.char_class,
            "level": self.level,
            "xp": self.xp,
            "xp_to_next": self.xp_to_next,
            "gold": self.gold,
            "inventory": self.inventory,
            "current_room": self.current_room,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "attack": self.attack,
            "defense": self.defense
        }

    @classmethod
    def from_dict(cls, data):
        player = cls(data["name"], data["char_class"])
        player.level = data["level"]
        player.xp = data["xp"]
        player.xp_to_next = data["xp_to_next"]
        player.gold = data["gold"]
        player.inventory = data["inventory"]
        player.current_room = data["current_room"]
        player.max_hp = data["max_hp"]
        player.hp = data["hp"]
        player.attack = data["attack"]
        player.defense = data["defense"]
        return player


def save_game(player):
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(player.to_dict(), f)
        print(f"{C_GREEN}[✓] Game progress saved successfully.{C_RESET}")
    except Exception as e:
        print(f"{C_RED}[✗] Failed to save game: {e}{C_RESET}")

def load_game():
    try:
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
        player = Player.from_dict(data)
        print(f"{C_GREEN}[✓] Saved game loaded successfully. Welcome back, {player.name}!{C_RESET}")
        time.sleep(1)
        return player
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"{C_RED}[!] Could not load save file (corrupted or old format): {e}{C_RESET}")
        return None


def type_scroll(text, delay=0.015):
    """Prints text with a retro typewriter scroll effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def start_combat(player, monster_name):
    monster_info = MONSTERS[monster_name]
    m_hp = monster_info["hp"]
    m_max_hp = monster_info["max_hp"]
    m_atk = monster_info["attack"]
    m_def = monster_info["defense"]

    print(f"\n{C_BOLD}{C_RED}⚔️ A feral {monster_name} blocks your path! ⚔️{C_RESET}")
    time.sleep(0.5)

    while m_hp > 0 and player.hp > 0:
        print(f"\n--- Combat State ---")
        print(f"{player.name}: {C_GREEN}{player.hp}/{player.max_hp} HP{C_RESET}")
        print(f"{monster_name}: {C_RED}{m_hp}/{m_max_hp} HP{C_RESET}")
        print("--------------------")
        
        print(f"What will you do? ({C_BOLD}A{C_RESET}ttack | {C_BOLD}H{C_RESET}eal | {C_BOLD}R{C_RESET}un)")
        choice = input("> ").strip().lower()

        if choice == 'a' or choice == 'attack':
            # Player hits monster
            damage_to_monster = max(2, player.attack - m_def + random.randint(-2, 2))
            m_hp -= damage_to_monster
            print(f"\n{C_GREEN}» You strike the {monster_name} for {damage_to_monster} damage!{C_RESET}")
            time.sleep(0.6)
            
            if m_hp <= 0:
                break
        
        elif choice == 'h' or choice == 'heal':
            if "Health Potion" in player.inventory:
                player.inventory.remove("Health Potion")
                heal_amount = 35
                player.hp = min(player.max_hp, player.hp + heal_amount)
                print(f"\n{C_GREEN}» You drank a Health Potion and recovered {heal_amount} HP!{C_RESET}")
                time.sleep(0.6)
            else:
                print(f"\n{C_RED}» You don't have any Health Potions in your inventory!{C_RESET}")
                time.sleep(0.6)
                continue # don't waste turn

        elif choice == 'r' or choice == 'run':
            if random.random() < 0.4:
                print(f"\n{C_YELLOW}» You successfully escaped back to safety!{C_RESET}")
                time.sleep(1)
                player.current_room = "Town Square"
                return
            else:
                print(f"\n{C_RED}» You tried to flee, but the {monster_name} cornered you!{C_RESET}")
                time.sleep(0.6)
        
        else:
            print("Invalid command.")
            continue

        # Monster's turn to hit player
        damage_to_player = max(1, m_atk - player.defense + random.randint(-1, 1))
        player.hp -= damage_to_player
        print(f"{C_RED}» The {monster_name} attacks you for {damage_to_player} damage!{C_RESET}")
        time.sleep(0.8)

    if player.hp <= 0:
        print(f"\n{C_BOLD}{C_RED}💀 YOU DIED! 💀{C_RESET}")
        print("Your adventure ends here... You respawn at Town Square with half gold and full health.")
        player.hp = player.max_hp
        player.gold = int(player.gold / 2)
        player.current_room = "Town Square"
        time.sleep(2.5)
    else:
        print(f"\n{C_BOLD}{C_GREEN}🏆 VICTORY! You defeated the {monster_name}! 🏆{C_RESET}")
        gold_reward = monster_info["gold_reward"] + random.randint(-2, 3)
        xp_reward = monster_info["xp_reward"]
        
        player.gold += gold_reward
        print(f"Collected: {C_YELLOW}{gold_reward}g{C_RESET}")
        player.gain_xp(xp_reward)
        
        # Remove monster from the room so it doesn't immediately spawn again on next enter
        WORLD_MAP[player.current_room]["monster"] = None
        time.sleep(1.5)

def enter_shop(player):
    print(f"\n{C_BOLD}{C_YELLOW}🏪 Armory Blacksmith Shop 🏪{C_RESET}")
    print("Welcome traveler! Buy something to increase your survival odds:")
    
    while True:
        print(f"\nYour Gold: {C_YELLOW}{player.gold}g{C_RESET}")
        for idx, (item, details) in enumerate(SHOP_ITEMS.items(), 1):
            print(f"{idx}. {C_BOLD}{item}{C_RESET} ({details['desc']}) - {C_YELLOW}{details['cost']}g{C_RESET}")
        print(f"4. Leave Shop")
        
        choice = input("Enter item number: ").strip()
        
        if choice == '1':
            item_name = "Health Potion"
            cost = SHOP_ITEMS[item_name]["cost"]
            if player.gold >= cost:
                player.gold -= cost
                player.inventory.append(item_name)
                print(f"{C_GREEN}[+] Purchased {item_name}!{C_RESET}")
            else:
                print(C_RED + "Insufficient gold." + C_RESET)
        elif choice == '2':
            item_name = "Iron Sword"
            cost = SHOP_ITEMS[item_name]["cost"]
            if player.gold >= cost:
                player.gold -= cost
                player.attack += 5
                print(f"{C_GREEN}[+] Purchased {item_name}! Attack increased by 5!{C_RESET}")
            else:
                print(C_RED + "Insufficient gold." + C_RESET)
        elif choice == '3':
            item_name = "Steel Armor"
            cost = SHOP_ITEMS[item_name]["cost"]
            if player.gold >= cost:
                player.gold -= cost
                player.defense += 3
                print(f"{C_GREEN}[+] Purchased {item_name}! Defense increased by 3!{C_RESET}")
            else:
                print(C_RED + "Insufficient gold." + C_RESET)
        elif choice == '4' or choice.lower() == 'leave':
            print("Thanks for stopping by! Be safe out there.")
            break
        else:
            print("Invalid option.")

def start_new_game():
    print(f"\n{C_BOLD}{C_BLUE}--- NEW JOURNEY CHARACTER CREATION ---{C_RESET}")
    name = input("Enter your hero's name: ").strip()
    if not name:
        name = "Hero"
        
    print("\nSelect your character class:")
    print(f"1. {C_BOLD}Warrior{C_RESET} (High Health, Sturdy Defense)")
    print(f"2. {C_BOLD}Mage{C_RESET} (High Spell Attack, Frail Defense)")
    print(f"3. {C_BOLD}Rogue{C_RESET} (Balanced Stats, Fast Strike)")
    
    choice = input("Enter number: ").strip()
    if choice == '1':
        char_class = "Warrior"
    elif choice == '2':
        char_class = "Mage"
    else:
        char_class = "Rogue"
        
    player = Player(name, char_class)
    print(f"\nCreated character {C_BOLD}{player.name}{C_RESET} the {player.char_class}!")
    time.sleep(1)
    return player

def main():
    print(f"{C_BOLD}{C_MAGENTA}")
    print(" ▄▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ")
    print(" █       █      █       █ █       █       █      █       █")
    print(" █   ▄▄▄▄█  ▄   █   ▄   █ █       █    ▄▄▄█  ▄   █   ▄   █")
    print(" █  █  ▄▄█ █▄█  █  █ █  █ █     ▄▄█   █▄▄▄█ █▄█  █  █ █  █")
    print(" █  █ █  █      █  █▄█  █ █    █  █    ▄▄▄█      █  █▄█  █")
    print(" █  █▄▄█ █  ▄   █       █ █    █▄▄█   █▄▄▄█  ▄   █       █")
    print(" █▄▄▄▄▄▄▄█▄█ █▄▄█▄▄▄▄▄▄▄█ █▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄█ █▄▄█▄▄▄▄▄▄▄█")
    print("             - Text Adventure Engine v1.0 -             ")
    print(f"{C_RESET}")

    player = load_game()
    if not player:
        player = start_new_game()

    while True:
        room_name = player.current_room
        room_info = WORLD_MAP[room_name]
        
        # Display current room details
        print(f"\n{C_BOLD}📍 CURRENT LOCATION: {room_name}{C_RESET}")
        type_scroll(room_info["description"], delay=0.005)
        
        # Check items in room
        if room_info["items"]:
            print(f"You spot something here: {C_GREEN}{', '.join(room_info['items'])}{C_RESET}")

        # Check for monsters in room
        if room_info["monster"]:
            start_combat(player, room_info["monster"])
            continue # Combat loop handles death/win, reload room

        # Input Prompt
        print(f"\n[Command Options]:")
        print(f"» Move: {C_BOLD}{', '.join(room_info['exits'].keys())}{C_RESET}")
        if room_info["items"]:
            print(f"» Take item: {C_BOLD}take{C_RESET}")
        if room_info.get("is_shop"):
            print(f"» Enter shop: {C_BOLD}shop{C_RESET}")
        print(f"» Game: {C_BOLD}status{C_RESET} | {C_BOLD}save{C_RESET} | {C_BOLD}exit{C_RESET}")
        
        action = input("\nWhat do you want to do? > ").strip().lower()

        if action in room_info["exits"]:
            player.current_room = room_info["exits"][action]
            print(f"\nYou travel {action}...")
            time.sleep(0.5)
            
        elif action == "take" and room_info["items"]:
            taken_item = room_info["items"].pop(0)
            player.inventory.append(taken_item)
            print(f"\n{C_GREEN}[+] Added {taken_item} to your inventory.{C_RESET}")
            time.sleep(0.5)

        elif action == "shop" and room_info.get("is_shop"):
            enter_shop(player)

        elif action == "status":
            player.show_status()

        elif action == "save":
            save_game(player)

        elif action == "exit":
            save_choice = input("Would you like to save before exiting? (y/n): ").strip().lower()
            if save_choice == 'y':
                save_game(player)
            print(f"\n{C_BOLD}Thanks for playing RPG Adventure! Farewell, Hero.{C_RESET}")
            sys.exit(0)
        else:
            print(f"\n{C_RED}[!] Invalid command. Try again.{C_RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[-] Adventure interrupted... Farewell, Hero.")
