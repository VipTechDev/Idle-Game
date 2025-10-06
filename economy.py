def upgrade_character(character, coins, multiplier_value):
    total_cost = sum(character.upgrade_cost * (character.level + i) for i in range(multiplier_value))
    if coins >= total_cost:
        character.level += multiplier_value
        return coins - total_cost, True
    return coins, False

def unlock_character(index, characters, coins):
    char = characters[index]
    if coins >= char.cost:
        coins -= char.cost
        return coins, index
    return coins, None

def get_multiplier_value(label):
    return {
        "x1": 1,
        "x10": 10,
        "x20": 20,
        "x50": 50
    }.get(label, None)  # returns None for "max"
    
def calculate_upgrade_cost(character, coins, multiplier_label):
    if multiplier_label == "max":
        temp_cost = 0
        max_levels = 0
        while True:
            next_level = character.level + max_levels
            cost = character.upgrade_cost * next_level
            if temp_cost + cost > coins:
                break
            temp_cost += cost
            max_levels += 1
        return max_levels, temp_cost
    else:
        multiplier_value = get_multiplier_value(multiplier_label)
        total_cost = sum(character.upgrade_cost * (character.level + i) for i in range(multiplier_value))
        return multiplier_value, total_cost