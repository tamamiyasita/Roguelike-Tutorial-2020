import random
import csv

def load_entities(filename):
    monsters = []
    with open(filename) as input_file:
        reader = csv.DictReader(input_file)
        for actor in reader:
            monsters.append(actor)

    return monsters

entities = load_entities("entities.csv")

def convert_to_restore_dict(monster):
    converted = {}
    converted["texture"] = int(monster["texture"])
    converted["name"] = monster["name"]
    converted["fighter"] = {
                            "hp": int(monster["HP"]),
                            "max_hp": int(monster["HP"]),
                            "power": int(monster["Attack"]),
                            "defence": int(monster["Defense"]),
                            "xp_reward": int(monster["XP"])
                            }
    return converted

def get_random_monster_by_challenge(challenge):
    filtered_monsters = [monster for monster in monsters if int(monster["Challenge"]) == challenge]
    m1 = random.choice(filtered_monsters)
    m2 = convert_to_restore_dict(m1)
    return m2

m = get_random_monster_by_challenge(1)
print(m)