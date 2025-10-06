import pygame
import time
import random
from characters import get_characters
from monsters import easy_monsters, moderate_monsters, hard_monsters
from economy import upgrade_character, unlock_character, get_multiplier_value, calculate_upgrade_cost
from gamestate import update_progress
from ui import draw_ui
from graphics import load_background, draw_tiled_background
background_image = load_background()

def autosave(coins, characters):
    with open("savegame.txt", "w") as f:
        f.write(str(coins) + "\n")
        f.write(str(int(time.time())) + "\n")
        for c in characters:
            f.write(f"{c.name},{c.level},{int(c.unlocked)}\n")
    print("Autosave complete.")
    
clock = pygame.time.Clock()

# Global multiplier button position (shared with UI)
global_button_x = 470
global_button_y = 20
global_button_width = 60
global_button_height = 30

multipliers = ["x1", "x10", "x20", "x50", "max"]
multiplier_index = 0

# Upgrade button
upgrade_button_width = 60
upgrade_button_height = 55
upgrade_button_x = 470
upgrade_button_y = 60

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
current_height = HEIGHT  # track current window height
pygame.display.set_caption("Modular Monster Slayer")

# Save/Load button positions (aligned to right of multiplier)
save_load_width = 80
save_load_height = 30
save_x = WIDTH - save_load_width - 20
save_y = global_button_y
load_x = save_x
load_y = save_y + save_load_height + 10

# Fonts and colors
font = pygame.font.SysFont(None, 36)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Game state
coins = 0
characters = get_characters()
slay_log = {c.name: {"monster": None, "reward": 0} for c in characters}
total_height = 60  # initial y_offset
current_char_index = 0
clock = pygame.time.Clock()


# Main loop
running = True

while running:
    character = characters[current_char_index]
    multiplier = multipliers[multiplier_index]
    levels_to_buy, upgrade_cost = calculate_upgrade_cost(character, coins, multiplier)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            autosave(coins, characters)
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Cycle multiplier
            if (global_button_x <= mouse_x <= global_button_x + global_button_width and
                global_button_y <= mouse_y <= global_button_y + global_button_height):
                multiplier_index = (multiplier_index + 1) % len(multipliers)

            # Handle upgrade clicks for each unlocked character
            current_y_offset = 60
            for c in characters:
                if c.unlocked:
                    current_y_offset += 25  # name
                    current_y_offset += 25  # level

                    slain = slay_log.get(c.name)
                    if slain and slain["monster"]:
                        current_y_offset += 40  # slay message
                    else:
                        current_y_offset += 10  # spacer

                    bar_y = current_y_offset + 25
                    upgrade_button_x = 20 + 420
                    upgrade_button_y = current_y_offset + 10
                    upgrade_button_width = 60
                    upgrade_button_height = 55

                    if (upgrade_button_x <= mouse_x <= upgrade_button_x + upgrade_button_width and
                        upgrade_button_y <= mouse_y <= upgrade_button_y + upgrade_button_height):

                        levels_to_buy, upgrade_cost = calculate_upgrade_cost(c, coins, multiplier)
                        if coins >= upgrade_cost:
                            coins -= upgrade_cost
                            c.level += levels_to_buy
                            print(f"{c.name} upgraded {levels_to_buy} levels! -{upgrade_cost} coins")
                        else:
                            print("Not enough coins to upgrade.")

                    current_y_offset = max(upgrade_button_y + upgrade_button_height, bar_y + 30) + 10

            # Unlock characters
            recruit_blocks = [c for c in characters if not c.unlocked and c.base_cost > 0]
            button_x = 20
            button_width = 250
            button_height = 80
            y_offset = 60

            # Advance y_offset past unlocked characters
            for c in characters:
                if c.unlocked:
                    y_offset += 25  # name
                    y_offset += 25  # level
                    if slay_log.get(c.name) and slay_log[c.name].get("message"):
                        y_offset += 40
                    else:
                        y_offset += 10
                    y_offset += 40  # progress bar
                    y_offset += 55  # upgrade button
                    y_offset += 10  # spacing

            # Now check recruit buttons
            for c in recruit_blocks:
                button_y = y_offset
                if (button_x <= mouse_x <= button_x + button_width and
                    button_y <= mouse_y <= button_y + button_height):

                    if coins >= c.base_cost:
                        coins -= c.base_cost
                        c.unlocked = True
                        print(f"The {c.name} has joined your quest!")
                    else:
                        print(f"Not enough coins to recruit the {c.name}.")
                y_offset += button_height + 10

            # Save game
            if (save_x <= mouse_x <= save_x + save_load_width and
                save_y <= mouse_y <= save_y + save_load_height):
                with open("savegame.txt", "w") as f:
                    f.write(str(coins) + "\n")
                    f.write(str(int(time.time())) + "\n")
                    for c in characters:
                        f.write(f"{c.name},{c.level},{int(c.unlocked)}\n")
                print("Game saved!")

            # Load game
            if (load_x <= mouse_x <= load_x + save_load_width and
                load_y <= mouse_y <= load_y + save_load_height):
                try:
                    with open("savegame.txt", "r") as f:
                        lines = f.readlines()
                        coins = int(lines[0])
                        last_time = int(lines[1])
                        current_time = int(time.time())
                        elapsed = min(current_time - last_time, 3600)

                        if elapsed < 10:
                            print("No meaningful offline time detected.")
                        else:
                            offline_coins = 0
                            for c in characters:
                                if c.unlocked:
                                    earnings = c.speed * c.level * (elapsed / 4)
                                    offline_coins += int(earnings)
                            coins += offline_coins
                            minutes = elapsed // 60
                            print(f"🧭 Your party returns from the wilds after {minutes} minutes.")
                            print(f"💰 Coin-stuffed satchels delivered: +{offline_coins} coins earned while you were away.")

                        for line in lines[2:]:
                            name, level, unlocked = line.strip().split(",")
                            for c in characters:
                                if c.name == name:
                                    c.level = int(level)
                                    c.unlocked = bool(int(unlocked))
                    print("Game loaded!")
                except FileNotFoundError:
                    print("No save file found.")

    # Monster progress and slay log
    for c in characters:
        if c.unlocked:
            new_monster, new_reward = update_progress(c)
            coins += new_reward
            if new_monster:
                slay_log[c.name]["monster"] = new_monster
                slay_log[c.name]["reward"] = new_reward
                slay_log[c.name]["message"] = f"The {c.name} slayed a {new_monster}! +{new_reward} coins"

    # Recalculate total height dynamically
    total_height = 60
    for c in characters:
        if c.unlocked:
            total_height += 25
            total_height += 25
            if slay_log.get(c.name) and slay_log[c.name].get("message"):
                total_height += 40
            else:
                total_height += 10
            total_height += 40
            total_height += 55
            total_height += 10

    recruit_blocks = [c for c in characters if not c.unlocked and c.base_cost > 0]
    total_height += len(recruit_blocks) * (80 + 10)

    new_height = max(600, total_height + 20)
    if new_height != current_height:
        current_height = new_height
        screen = pygame.display.set_mode((WIDTH, current_height), pygame.RESIZABLE)

    draw_tiled_background(screen, background_image)

    draw_ui(
        screen,
        character,
        coins,
        characters,
        slay_log,
        multiplier,
        global_button_x,
        global_button_y,
        upgrade_button_x,
        upgrade_button_y,
        upgrade_button_width,
        upgrade_button_height,
        upgrade_cost
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()