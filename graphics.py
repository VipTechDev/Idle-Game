import pygame

def load_background():
    """Load and return a scaled-down brick wall image for zoom-out effect."""
    original = pygame.image.load("brick_wall6.png")
    zoom_factor = 0.5  # 0.5 = 50% size (zoomed out), try 0.25 for even smaller
    width = int(original.get_width() * zoom_factor)
    height = int(original.get_height() * zoom_factor)

    # Use smoothscale to avoid edge artifacts
    scaled = pygame.transform.smoothscale(original, (width, height))
    return scaled

def draw_tiled_background(screen, background_image):
    """Tile the background image across the screen."""
    bg_width, bg_height = background_image.get_size()
    screen_width, screen_height = screen.get_size()

    for x in range(0, screen_width, bg_width):
        for y in range(0, screen_height, bg_height):
            screen.blit(background_image, (x, y))
            
def load_coin_purse():
    img = pygame.image.load("coin_purse.png").convert_alpha()
    return pygame.transform.scale(img, (40, 40))  # adjust size as needed

