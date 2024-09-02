import pygame
import sys

pygame.init()

#Setup Screen Size
cell_size = 40
cell_number = 20
screen_width = cell_number * cell_size
screen_height = cell_number * cell_size
screen = pygame.display.set_mode((screen_width, screen_height))

#Set font
font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 50)

#Define colors
white = (255, 255, 255)
black = (0, 0, 0)
grey = (169, 169, 169)

#Define button positions and sizes
button_width = 250
button_height = 100

play_button_rect = pygame.Rect((screen_width - button_width) // 2, 300, button_width, button_height)
quit_button_rect = pygame.Rect((screen_width - button_width)// 2, 450, button_width, button_height)

#Loadscreen image
background_image = pygame.image.load('assets/loadscreen.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def menu_screen():
    while True:
        screen.blit(background_image, (0, 0))

        draw_text('Snake Game', font, white, screen, screen_width // 2, 150)

        #Draw Play Button
        pygame.draw.rect(screen, grey, play_button_rect)
        draw_text('Play', font, white, screen, play_button_rect.centerx, play_button_rect.centery)

        #Draw Quit Button
        pygame.draw.rect(screen, grey, quit_button_rect)
        draw_text('Quit Game', font, white, screen, quit_button_rect.centerx, quit_button_rect.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return #Start the game
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
    
#Run the menu screen
menu_screen()

#Start the game
import snakegame