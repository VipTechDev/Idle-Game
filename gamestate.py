import random
from monsters import monster_tiers  # includes all 6 tiers

def update_progress(character):
    # Scale speed by level
    scaled_speed = character.speed * (1 + 0.1 * (character.level - 1))
    character.progress += scaled_speed

    if character.progress >= 100:
        character.progress = 0

        # Determine accessible monster tiers
        tier = character.starting_tier
        if character.level >= 100 and tier + 1 < len(monster_tiers):
            # Merge current and next tier
            monster_pool = {**monster_tiers[tier], **monster_tiers[tier + 1]}
        else:
            monster_pool = monster_tiers[tier]

        monster = random.choice(list(monster_pool.keys()))
        reward = monster_pool[monster]
        return monster, reward

    return None, 0