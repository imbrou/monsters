import json
import time
import random
import os

# Global variables
DB_FILE = "monsters.json"
#DB_NAME = "monsters"
#DB_USER = "monster-user"
#DB_PASSWORD = "kjdq32ed'é!çuydfdz@8293,i'"
QUERY_LIMIT = 20
SORT_FIELD = "level"
SORT_ORDER = "DESC"

def load_database():
    """Load the monsters database from file"""
    if not os.path.exists(DB_FILE):
        print(f"Database file {DB_FILE} not found. Please run monster_db.py first.")
        return None
    
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def fetch_all_monsters():
    """Fetch all monsters from the database"""
    database = load_database()
    if database:
        return database["monsters"]
    return []

def fetch_monster_details(monster_id):
    """Fetch detailed information about a specific monster"""
    database = load_database()
    if not database:
        return None
    
    # Find the monster
    monster = None
    for m in database["monsters"]:
        if m["id"] == monster_id:
            monster = m
            break
    
    if not monster:
        return None
    
    # Find monster abilities
    abilities = []
    for ability in database["monster_abilities"]:
        if ability["monster_id"] == monster_id:
            abilities.append(ability)
    
    # Find monster inventory
    inventory = []
    for item in database["monster_inventory"]:
        if item["monster_id"] == monster_id:
            inventory.append(item)
    
    # Create a complete monster object
    monster_dict = dict(monster)
    monster_dict["abilities"] = abilities
    monster_dict["inventory"] = inventory
    
    return monster_dict

def sort_monsters(monsters, sort_by="level", reverse=True):
    """Sort monsters according to a criterion"""
    # Make a copy of the monsters list to avoid modifying the original
    monster_list = [dict(monster) for monster in monsters]
    
    n = len(monster_list)
    for i in range(n):
        #time.sleep(0.001)
        
        # Flag to optimize if no swaps occur
        swapped = False
        
        for j in range(0, n - i - 1):
            val1 = str(monster_list[j][sort_by])
            val2 = str(monster_list[j + 1][sort_by])
            
            try:
                val1 = int(val1)
                val2 = int(val2)
            except ValueError:
                # If conversion fails, keep as strings
                pass
            
            if reverse:
                should_swap = val1 < val2
            else:
                should_swap = val1 > val2
            
            if should_swap:
                temp_monster1 = dict(monster_list[j])
                temp_monster2 = dict(monster_list[j + 1])
                monster_list[j] = temp_monster2
                monster_list[j + 1] = temp_monster1
                swapped = True
        
        if not swapped:
            break
    
    result = [dict(monster) for monster in monster_list]
    return result

def print_monster_list(monsters, limit=10):
    """Print a list of monsters with basic information"""
    print(f"\n{'=' * 80}")
    print(f"{'ID':<5} {'NAME':<30} {'TYPE':<15} {'LEVEL':<6} {'HEALTH':<8} {'STRENGTH':<8}")
    print(f"{'-' * 80}")
    
    for i, monster in enumerate(monsters[:limit]):
        print(f"{monster['id']:<5} {monster['name']:<30} {monster['type']:<15} {monster['level']:<6} {monster['health']:<8} {monster['strength']:<8}")
    
    if len(monsters) > limit:
        print(f"\n... and {len(monsters) - limit} more monsters")
    
    print(f"{'=' * 80}")
    print(f"Total monsters: {len(monsters)}")

def print_monster_details(monster):
    """Print detailed information about a monster"""
    if not monster:
        print("Monster not found!")
        return
    
    print(f"\n{'=' * 80}")
    print(f"MONSTER DETAILS: {monster['name']} (ID: {monster['id']})")
    print(f"{'=' * 80}")
    
    print(f"Type: {monster['type']}")
    print(f"Level: {monster['level']}")
    print(f"Health: {monster['health']}")
    print(f"Mana: {monster['mana']}")
    print(f"Location: {monster['location']}")
    print(f"Boss: {'Yes' if monster['is_boss'] else 'No'}")
    
    print(f"\nAttributes:")
    print(f"  Strength: {monster['strength']}")
    print(f"  Intelligence: {monster['intelligence']}")
    print(f"  Dexterity: {monster['dexterity']}")
    print(f"  Charisma: {monster['charisma']}")
    print(f"  Wisdom: {monster['wisdom']}")
    print(f"  Constitution: {monster['constitution']}")
    
    print(f"\nEconomy:")
    print(f"  Experience: {monster['experience']}")
    print(f"  Gold: {monster['gold']}")
    
    print(f"\nDescription:")
    print(f"  {monster['description']}")
    
    print(f"\nAbilities ({len(monster['abilities'])}):")
    for ability in monster['abilities']:
        print(f"  - {ability['ability_name']} (Level {ability['ability_level']})")
        print(f"    Damage: {ability['ability_damage']}, Cooldown: {ability['ability_cooldown']}s")
        print(f"    {ability['ability_description']}")
    
    print(f"\nInventory ({len(monster['inventory'])}):")
    for item in monster['inventory']:
        print(f"  - {item['item_name']} ({item['item_type']}, {item['item_rarity']})")
        print(f"    Value: {item['item_value']} gold")
    
    print(f"{'=' * 80}")

def main():
    """Main function to demonstrate monster sorting"""
    print("Monster Database Query Tool")
    print("==========================")
    
    # Fetch all monsters (this could be a lot of data)
    print("\nFetching monsters from database...")
    all_monsters = fetch_all_monsters()
    
    if not all_monsters:
        print("No monsters found. Please run monster_init.py first to create the database.")
        return
    
    # Benchmark the sorting function
    print("\nSorting monsters...")
    sorted_monsters = sort_monsters(all_monsters, "level", True)
    
    # Print a sample of the sorted monsters
    print("\nSample of sorted monsters:")
    print_monster_list(sorted_monsters, QUERY_LIMIT)
    
    # Get details for a random monster
    if all_monsters:
        random_monster = random.choice(all_monsters)
        monster_id = random_monster["id"]
        
        print(f"\nFetching details for monster ID: {monster_id}")
        monster_details = fetch_monster_details(monster_id)
        print_monster_details(monster_details)
    
    print("\nDone!")

if __name__ == "__main__":
    main()