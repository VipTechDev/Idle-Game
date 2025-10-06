from monsters import monster_tiers

class Character:
    def __init__(self, name, level, speed, base_cost, monsters, upgrade_cost, starting_tier, recruit_text, upgraded=False):
        self.name = name
        self.level = level
        self.speed = speed
        self.base_cost = base_cost
        self.cost = base_cost  # can be scaled later
        
        self.starting_tier = starting_tier
        self.monsters = monsters
        self.upgrade_cost = upgrade_cost
        self.recruit_text = recruit_text
        self.upgraded = upgraded
        self.progress = 0
        self.unlocked = (name == "Bard")  # Bard starts unlocked

def get_characters():
    names = ["Bard", "Knight", "Rogue", "Mage", "Paladin"]
    base_speed = [1.0, 0.5, 0.8, 0.6, 0.4]
    starting_tiers = [0, 1, 2, 3, 4]  # Bard starts on easy, Knight on moderate, etc.
    
    recruit_texts = [
    "Tunes up for trouble — sings monsters to sleep.",
    "Armor polished. Blade ready. Justice incoming.",
    "Slips through shadows. Strikes before you blink.",
    "Wields storms and secrets. Magic answers the call.",
    "Light-bound and unshaken. Smite first, ask later."
    ]

    characters = []
    for i, name in enumerate(names):
        cost = 1000 * (10 ** (i - 1)) if i > 0 else 0
        tier = starting_tiers[i]
        characters.append(Character(
            name=name,
            level=1,
            speed=base_speed[i],
            base_cost=cost,
            monsters=monster_tiers[tier],
            upgrade_cost=20 * (i + 1),
            starting_tier=tier,
            recruit_text=recruit_texts[i]
        ))
    return characters