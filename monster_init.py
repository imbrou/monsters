import random
import time
import json
import os
from faker import Faker

# Global variables
DB_FILE = "monsters.json"
MONSTER_COUNT = 10000
fake = Faker()

# Harry Potter characters
hp_characters = [
    "Harry Potter", "Hermione Granger", "Ron Weasley", "Albus Dumbledore", 
    "Severus Snape", "Sirius Black", "Remus Lupin", "Draco Malfoy", 
    "Luna Lovegood", "Neville Longbottom", "Ginny Weasley", "Fred Weasley", 
    "George Weasley", "Minerva McGonagall", "Rubeus Hagrid", "Bellatrix Lestrange", 
    "Voldemort", "Dobby", "Cedric Diggory", "Cho Chang"
]

# French politicians
french_politicians = [
    "Emmanuel Macron", "Marine Le Pen", "François Hollande", "Nicolas Sarkozy", 
    "Jacques Chirac", "François Mitterrand", "Valéry Giscard d'Estaing", 
    "Jean-Luc Mélenchon", "Édouard Philippe", "Jean Castex", "Gabriel Attal",
    "Ségolène Royal", "Dominique de Villepin", "Lionel Jospin", "Alain Juppé", 
    "François Fillon", "Éric Zemmour", "Anne Hidalgo", "Yannick Jadot", "Jean-Marie Le Pen"
]

# Monster types
monster_types = ["Dragon", "Goblin", "Troll", "Giant", "Vampire", "Werewolf", "Ghost", "Zombie", "Demon", "Elemental"]

# Monster abilities
monster_abilities = [
    "Fire Breath", "Ice Blast", "Lightning Strike", "Poison Spit", "Mind Control", 
    "Invisibility", "Teleportation", "Regeneration", "Flight", "Super Strength", 
    "Shapeshifting", "Summoning", "Necromancy", "Time Manipulation", "Illusion"
]

def create_database():
    """Create the monsters database structure"""
    if os.path.exists(DB_FILE):
        print(f"Database file {DB_FILE} already exists. Removing it...")
        os.remove(DB_FILE)
    
    # Initialize empty database
    database = {
        "monsters": [],
        "monster_abilities": [],
        "monster_inventory": []
    }
    
    # Save empty database
    with open(DB_FILE, 'w') as f:
        json.dump(database, f)
    
    print("Database created successfully!")

def generate_random_monster(monster_id):
    """Generate a random monster with complex attributes"""
    # Generate a random name by combining Harry Potter character and French politician
    first_name = random.choice(hp_characters).split()[0]
    last_name = random.choice(french_politicians).split()[-1]
    name = f"{first_name} {last_name}"
    
    monster = {
        "id": monster_id,
        "name": name,
        "type": random.choice(monster_types),
        "level": random.randint(1, 100),
        "health": random.randint(50, 1000),
        "mana": random.randint(0, 500),
        "strength": random.randint(1, 100),
        "intelligence": random.randint(1, 100),
        "dexterity": random.randint(1, 100),
        "charisma": random.randint(1, 100),
        "wisdom": random.randint(1, 100),
        "constitution": random.randint(1, 100),
        "experience": random.randint(0, 10000),
        "gold": random.randint(0, 1000),
        "is_boss": random.random() < 0.05,  # 5% chance to be a boss
        "location": fake.city(),
        "description": fake.paragraph(),
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Generate 1-5 abilities for the monster
    abilities = []
    num_abilities = random.randint(1, 5)
    for i in range(num_abilities):
        ability = {
            "id": monster_id * 100 + i,
            "monster_id": monster_id,
            "ability_name": random.choice(monster_abilities),
            "ability_level": random.randint(1, 10),
            "ability_damage": random.randint(10, 200),
            "ability_cooldown": random.randint(1, 30),
            "ability_description": fake.sentence()
        }
        abilities.append(ability)
    
    # Generate 0-3 inventory items
    inventory = []
    num_items = random.randint(0, 3)
    item_types = ["Weapon", "Armor", "Potion", "Scroll", "Gem", "Artifact"]
    rarities = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]
    
    for i in range(num_items):
        item = {
            "id": monster_id * 100 + i,
            "monster_id": monster_id,
            "item_name": fake.word().capitalize() + " of " + fake.word().capitalize(),
            "item_type": random.choice(item_types),
            "item_value": random.randint(1, 1000),
            "item_rarity": random.choice(rarities)
        }
        inventory.append(item)
    
    return monster, abilities, inventory

def populate_database():
    """Fill the database with a large number of random monsters"""
    # Load the empty database
    with open(DB_FILE, 'r') as f:
        database = json.load(f)
    
    start_time = time.time()
    
    monsters = []
    all_abilities = []
    all_inventory = []
    
    for i in range(1, MONSTER_COUNT + 1):
        monster, abilities, inventory = generate_random_monster(i)
        monsters.append(monster)
        all_abilities.extend(abilities)
        all_inventory.extend(inventory)
        
        # Save progress every 1000 monsters
        if i % 1000 == 0:
            elapsed_time = time.time() - start_time
            print(f"Generated {i} monsters. Elapsed time: {elapsed_time:.2f} seconds")
    
    # Update database
    database["monsters"] = monsters
    database["monster_abilities"] = all_abilities
    database["monster_inventory"] = all_inventory
    
    # Save the populated database
    with open(DB_FILE, 'w') as f:
        json.dump(database, f)
    
    total_time = time.time() - start_time
    print(f"Database populated with {MONSTER_COUNT} monsters in {total_time:.2f} seconds!")

if __name__ == "__main__":
    create_database()
    populate_database()