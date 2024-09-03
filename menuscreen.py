import pygame
import sys

pygame.init()

# Setup Screen Size
cell_size = 40
cell_number = 20
screen_width = cell_number * cell_size
screen_height = cell_number * cell_size
screen = pygame.display.set_mode((screen_width, screen_height))

# Set font
font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 50)

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
grey = (169, 169, 169)
light_grey = (211, 211, 211)
dark_grey = (105, 105, 105)
button_color = (76, 177, 105)
button_hover_color = (70, 177, 105)
transparent_black = (0, 0, 0, 180)

# Define button positions and sizes
button_width = 250
button_height = 80
play_button_rect = pygame.Rect((screen_width - button_width) // 2, 300, button_width, button_height)
quit_button_rect = pygame.Rect((screen_width - button_width) // 2, 450, button_width, button_height)

# Loadscreen image
background_image = pygame.image.load('assets/loadscreen.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def draw_button(rect, color, text, hover_color=None):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        color = hover_color if hover_color else color
    pygame.draw.rect(screen, color, rect, border_radius=20)
    draw_text(text, font, white, screen, rect.centerx, rect.centery)

def menu_screen():
    while True:
        screen.blit(background_image, (0, 0))

        # Draw a transparent overlay on the background image
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill(transparent_black)
        screen.blit(overlay, (0, 0))

        draw_text('Snake Game', font, white, screen, screen_width // 2, 150)

        # Draw Play Button with hover effect
        draw_button(play_button_rect, button_color, 'Play', hover_color=button_hover_color)

        # Draw Quit Button with hover effect
        draw_button(quit_button_rect, button_color, 'Quit Game', hover_color=button_hover_color)

        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    pygame.event.clear()
                    return  # Exit the menu loop and start the game
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Run the menu screen
menu_screen()

# Start the game
import snakegame
