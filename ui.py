import pygame
from economy import calculate_upgrade_cost
from graphics import load_coin_purse

WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (40, 40, 40)
YELLOW = (255, 255, 0)
RED = (200, 0, 0)
GREEN = (0, 255, 0)
BUTTON_GREEN = (0, 200, 0)
CHARACTER_BOX = (30, 30, 60)  # deep blue-grey
NAME_COLOR = (255, 215, 0)       # Gold
LEVEL_COLOR = (180, 255, 255)    # Light Cyan
SLAY_COLOR = (255, 200, 120)     # Light Orange
BUY_BUTTON_FILL = (20, 20, 45)  # deeper blue-grey
LOCKED_TEXT = (200, 200, 255)  # Pale Silver
CHAR_NAME_COLOR = (180, 140, 40)  # darker gold




def draw_ui(screen, character, coins, characters, slay_log, multiplier="x1", global_button_x=470, global_button_y=20, upgrade_button_x=470, upgrade_button_y=60, upgrade_button_width=60, upgrade_button_height=55, upgrade_cost=0):
    
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)
    slay_font = pygame.font.SysFont("timesnewroman", 22, italic=True)
    char_font = pygame.font.SysFont("arial", 24, bold=True)
    
    coin_purse_img = load_coin_purse()  # from graphics.py

    # Render coin total
    coin_text = font.render(str(coins), True, NAME_COLOR)

    # Position at top left
    coin_x = 20
    coin_y_img = 15
    coin_y_text = 20

    # Draw image and coin total
    screen.blit(coin_purse_img, (coin_x, coin_y_img))
    screen.blit(coin_text, (coin_x + coin_purse_img.get_width() + 10, coin_y_text + 5))

    # Show each unlocked character's block
    y_offset = 60
    for c in characters:
        if c.unlocked:
            # Character box dimensions
            box_x = 15
            box_y = y_offset - 5
            box_width = 511

            slain = slay_log.get(c.name)
            if slain and slain.get("message"):
                box_height = 95
            else:
                box_height = 65

            # Draw character info box
            pygame.draw.rect(screen, CHARACTER_BOX, (box_x, box_y, box_width, box_height))
            pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height), 2)

            # Character name
            char_text = char_font.render(f"The {c.name}", True, CHAR_NAME_COLOR)
            screen.blit(char_text, (box_x + 10, y_offset))
            y_offset += 25

            # Character level
            level_text = small_font.render(f"Level: {c.level}", True, LEVEL_COLOR)
            screen.blit(level_text, (box_x + 10, y_offset))
            y_offset += 25

            # Slay message
            if slain and slain.get("message"):
                slay_text = slay_font.render(slain.get("message"), True, SLAY_COLOR)
                screen.blit(slay_text, (box_x + 10, y_offset))
                y_offset += 40
            else:
                y_offset += 10

            # Progress bar
            bar_x = 20
            bar_y = y_offset +25
            #progress_bar_y = y_offset + 10  # or +15 for more space
            progress_width = int(400 * (c.progress / 100))
            progress_width = max(0, min(progress_width, 400))

            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, progress_width, 30))
            pygame.draw.rect(screen, BLACK, (bar_x, bar_y, 400, 30), 2)

            # Upgrade button
            upgrade_cost = calculate_upgrade_cost(c, coins, multiplier)[1]
            cost_text = small_font.render(f"{upgrade_cost} coins", True, YELLOW)
            button_width = cost_text.get_width() + 20
            button_height = 55
            upgrade_button_x = bar_x + 420
            upgrade_button_y = y_offset + 10

            pygame.draw.rect(screen, DARK_GREY, (upgrade_button_x, upgrade_button_y, button_width, button_height))
            pygame.draw.rect(screen, BLACK, (upgrade_button_x, upgrade_button_y, button_width, button_height), 2)
            cost_rect = cost_text.get_rect(center=(upgrade_button_x + button_width // 2, upgrade_button_y + button_height // 2))
            screen.blit(cost_text, cost_rect)

            # Final spacing after character block
            y_offset = max(upgrade_button_y + button_height, bar_y + 30) + 10

    y_offset += 10  # after character blocks

    # Measure longest recruit text width
    longest_text_width = 0
    for c in characters:
        if not c.unlocked and c.base_cost > 0:
            recruit_surface = small_font.render(c.recruit_text, True, BLACK)
            longest_text_width = max(longest_text_width, recruit_surface.get_width())

    # Set consistent button dimensions
    button_width = longest_text_width + 20
    button_height = 80

    recruit_blocks = [c for c in characters if not c.unlocked and c.base_cost > 0]
    for i, c in enumerate(recruit_blocks):
            button_x = 20
            button_y = y_offset
            
            pygame.draw.rect(screen, BUY_BUTTON_FILL, (button_x, button_y, button_width, button_height))  # fill
            pygame.draw.rect(screen, BLACK, (button_x, button_y, button_width, button_height), 2) # outline

            line1 = small_font.render(f"Recruit the {c.name}", True, LOCKED_TEXT)
            line2 = small_font.render(f"{c.base_cost} coins", True, LOCKED_TEXT)
            line3 = small_font.render(c.recruit_text, True, LOCKED_TEXT)

            screen.blit(line1, (button_x + 10, button_y + 10))
            screen.blit(line2, (button_x + 10, button_y + 30))
            screen.blit(line3, (button_x + 10, button_y + 50))

            y_offset += button_height + 10

    # Global multiplier button (cyan fill)
    global_button_width = 60
    global_button_height = 30


    pygame.draw.rect(screen, CYAN, (global_button_x, global_button_y, global_button_width, global_button_height))  # fill
    pygame.draw.rect(screen, BLACK, (global_button_x, global_button_y, global_button_width, global_button_height), 2)  # outline
    global_text = small_font.render(multiplier, True, BLACK)  # text stays black
    global_rect = global_text.get_rect(center=(global_button_x + global_button_width // 2, global_button_y + global_button_height // 2))
    screen.blit(global_text, global_rect)

    # Save/Load button dimensions
    save_load_width = 80
    save_load_height = 30

    save_x = screen.get_width() - save_load_width - 20
    save_y = global_button_y
    load_x = save_x
    load_y = save_y + save_load_height + 10

    # Save button
    pygame.draw.rect(screen, BUTTON_GREEN, (save_x, save_y, save_load_width, save_load_height))
    pygame.draw.rect(screen, BLACK, (save_x, save_y, save_load_width, save_load_height), 2)
    save_text = small_font.render("Save", True, BLACK)
    save_rect = save_text.get_rect(center=(save_x + save_load_width // 2, save_y + save_load_height // 2))
    screen.blit(save_text, save_rect)

    # Load button
    pygame.draw.rect(screen, RED, (load_x, load_y, save_load_width, save_load_height))
    pygame.draw.rect(screen, BLACK, (load_x, load_y, save_load_width, save_load_height), 2)
    load_text = small_font.render("Load", True, BLACK)
    load_rect = load_text.get_rect(center=(load_x + save_load_width // 2, load_y + save_load_height // 2))
    screen.blit(load_text, load_rect)