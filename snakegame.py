import pygame, sys, random
from pygame.math import Vector2
import time
import math
from menuscreen import menu_screen

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        # Load snake body parts
        self.load_graphics()

    def load_graphics(self):
        #Snake head
        self.head_up = pygame.image.load('assets/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('assets/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('assets/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('assets/head_left.png').convert_alpha()

        #Snake tail
        self.tail_up = pygame.image.load('assets/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('assets/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('assets/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('assets/tail_left.png').convert_alpha()

        #Snake body segments
        self.body_vertical = pygame.image.load('assets/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('assets/body_horizontal.png').convert_alpha()
        self.body_tr = pygame.image.load('assets/body_topright.png').convert_alpha()
        self.body_tl = pygame.image.load('assets/body_topleft.png').convert_alpha()
        self.body_br = pygame.image.load('assets/body_bottomright.png').convert_alpha()
        self.body_bl = pygame.image.load('assets/body_bottomleft.png').convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                self.draw_body_part(index, block_rect)

    def draw_body_part(self, index, block_rect):
        previous_block = self.body[index + 1] - self.body[index]
        next_block = self.body[index - 1] - self.body[index]

        if previous_block.x == next_block.x:
            screen.blit(self.body_vertical, block_rect)
        elif previous_block.y == next_block.y:
            screen.blit(self.body_horizontal, block_rect)
        else:
            self.draw_corner(index, block_rect, previous_block, next_block)

    def draw_corner(self, index, block_rect, previous_block, next_block):
        if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
            screen.blit(self.body_tl, block_rect)
        elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
            screen.blit(self.body_bl, block_rect)
        elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
            screen.blit(self.body_tr, block_rect)
        elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
            screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

class Fruit:
    def __init__(self, snake):
        self.snake = snake
        self.border_offset = 1 #Minimum distance from the border
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        while True:
            self.x = random.randint(self.border_offset, cell_number - 1 - self.border_offset)
            self.y = random.randint(1 + self.border_offset, cell_number - 1 - self.border_offset)
            self.pos = Vector2(self.x, self.y)

            # Check if the new position overlaps with the snake's body
            if self.pos not in self.snake.body:
                break

class PowerFruit:
    def __init__(self, snake):
        self.snake = snake
        self.border_offset = 1 #Minimum distance from the border
        self.randomize()
        self.active = False

    def draw_fruit(self):
        if self.active:
            fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
            screen.blit(power_apple, fruit_rect)

    def randomize(self):
        while True:
            self.x = random.randint(self.border_offset, cell_number - 1 - self.border_offset)
            self.y = random.randint(1 + self.border_offset, cell_number - 1 - self.border_offset)
            self.pos = Vector2(self.x, self.y)

            # Check if the new position overlaps with the snake's body
            if self.pos not in self.snake.body:
                break

    def activate(self):
        self.active = True
        self.randomize()

    def deactivate(self):
        self.active = False

class SpikeBall:
    def __init__(self, snake):
        self.snake = snake
        self.spikes = [] #List to hold active spikes
        self.spike_image = pygame.image.load('assets/spike.png').convert_alpha()  # Load the spike image
        self.min_distance = 3
        self.border_margin = 1 #Minimum distance from the border 

    def draw_spikes(self):
        for spike in self.spikes:
            spike_rect = pygame.Rect(int(spike['pos'].x * cell_size), int(spike['pos'].y * cell_size), cell_size, cell_size)
            screen.blit(self.spike_image, spike_rect)

    def randomize(self):
        while True:
            spike_data = {
                'pos': Vector2(random.randint(0 + self.border_margin, cell_number - 1 - self.border_margin), 
                               random.randint(1 + self.border_margin, cell_number - 1 - self.border_margin)),
                'spawn_time': time.time()
            }

            # Check if the new position overlaps with the snake's body
            if (self.pos_valid(spike_data['pos']) and
                all(self.distance_between(spike_data['pos'], spike['pos']) >= self.min_distance for spike in self.spikes)):
                self.spikes.append(spike_data)
                break

    def pos_valid(self, pos):
        return pos not in self.snake.body
    
    def distance_between(self, pos1, pos2):
        return math.sqrt((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2)

    def update(self):
        current_time = time.time()
        self.spikes = [spike for spike in self.spikes if current_time - spike['spawn_time'] <= 10]

class RottenFruit:
    def __init__(self, snake):
        self.snake = snake
        self.rotten_fruits = []  # List to hold active rotten fruits
        self.rotten_image = pygame.image.load('assets/rotten_apple.png').convert_alpha()  # Load the rotten fruit image
        self.min_distance = 3
        self.border_margin = 1  # Minimum distance from the border 

    def draw_rotten_fruits(self):
        for fruit in self.rotten_fruits:
            fruit_rect = pygame.Rect(int(fruit['pos'].x * cell_size), int(fruit['pos'].y * cell_size), cell_size, cell_size)
            screen.blit(self.rotten_image, fruit_rect)

    def randomize(self):
        while True:
            fruit_data = {
                'pos': Vector2(random.randint(0 + self.border_margin, cell_number - 1 - self.border_margin), 
                               random.randint(1 + self.border_margin, cell_number - 1 - self.border_margin)),
                'spawn_time': time.time()
            }

            # Check if the new position overlaps with the snake's body
            if (self.pos_valid(fruit_data['pos']) and
                all(self.distance_between(fruit_data['pos'], fruit['pos']) >= self.min_distance for fruit in self.rotten_fruits)):
                self.rotten_fruits.append(fruit_data)
                break

    def pos_valid(self, pos):
        return pos not in self.snake.body
    
    def distance_between(self, pos1, pos2):
        return math.sqrt((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2)

    def update(self):
        current_time = time.time()
        self.rotten_fruits = [fruit for fruit in self.rotten_fruits if current_time - fruit['spawn_time'] <= 15]  # Remove after 5 seconds

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit(self.snake)
        self.power_fruit = PowerFruit(self.snake)
        self.spike_ball = SpikeBall(self.snake)  # Add spike ball
        self.rotten_fruit = RottenFruit(self.snake)
        self.score = 0
        self.high_score = 0
        self.paused = False
        self.start_time = time.time()  # Track when the game starts
        self.elapsed_time = 0  # Initialize elapsed time

        # Load sounds
        self.fruit_sound = pygame.mixer.Sound('sound/Sound_crunch.wav')
        self.power_fruit_sound = pygame.mixer.Sound('sound/Sound_crunch.wav')
        self.rotten_fruit_sound = pygame.mixer.Sound('sound/Sound_crunch.wav')

        self.fruit_sound.set_volume(0.5)  # Set volume to 50%
        self.power_fruit_sound.set_volume(0.5)  # Set volume to 50%
        self.rotten_fruit_sound.set_volume(0.5)  # Set volume to 50%

        # Health system
        self.max_health = 3
        self.current_health = self.max_health
        self.heart_image = pygame.image.load('assets/heart.png').convert_alpha()
        self.empty_heart_image = pygame.image.load('assets/empty_heart.png').convert_alpha()
        
        # Define buttons for the pause screen
        self.resume_button_rect = pygame.Rect((screen.get_width() - 250) // 2, 300, 250, 100)
        self.back_button_rect = pygame.Rect((screen.get_width() - 250) // 2, 450, 250, 100)

        # Load the background image and scale it to fit the screen
        self.background_image = pygame.image.load('assets/background4.png')
        self.background_image = pygame.transform.scale(self.background_image, (cell_number * cell_size, cell_number * cell_size))

    def draw_pause_screen(self):
        # Draw a semi-transparent background overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(180)  # Set transparency level (0 is fully transparent, 255 is fully opaque)
        overlay.fill((0, 0, 0))  # Black overlay
        screen.blit(overlay, (0, 0))

        # Draw the pause menu box
        box_width, box_height = 400, 400
        box_x = (screen.get_width() - box_width) // 2
        box_y = (screen.get_height() - box_height) // 2
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

        # Draw a semi-transparent box for the menu
        pygame.draw.rect(screen, (50, 50, 50, 200), box_rect, border_radius=10)  # Dark gray box with rounded corners
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2, border_radius=10)  # White border with rounded corners

        # Draw the "Resume" button with modern styling
        pygame.draw.rect(screen, (100, 100, 100), self.resume_button_rect, border_radius=10)  # Grey rounded button
        pygame.draw.rect(screen, (255, 255, 255), self.resume_button_rect, 2, border_radius=10)  # White border

        self.draw_text("Resume", game_font, white, screen, self.resume_button_rect.centerx, self.resume_button_rect.centery)

        # Draw the "Back to Menu" button with modern styling
        pygame.draw.rect(screen, (100, 100, 100), self.back_button_rect, border_radius=10)  # Grey rounded button
        pygame.draw.rect(screen, (255, 255, 255), self.back_button_rect, 2, border_radius=10)  # White border

        self.draw_text("Back to Menu", game_font, white, screen, self.back_button_rect.centerx, self.back_button_rect.centery)
    
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))
        surface.blit(textobj, textrect)

    def check_pause_screen_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.resume_button_rect.collidepoint(event.pos):
                self.paused = False  # Resume the game
            if self.back_button_rect.collidepoint(event.pos):
                menu_screen()  # Go back to the main menu
                self.__init__()  # Reinitialize the game state

    def update(self):
        if not self.paused:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()
            self.update_timer()
            self.spike_ball.update()  # Update spike ball
            self.rotten_fruit.update()

            # Start spawning spike balls after 10 seconds
            if self.elapsed_time > 10:
                # Randomly spawn a spike ball with a 3% chance every update cycle
                if random.random() < 0.03:
                    self.spike_ball.randomize()

            # Start spawning rotten fruits after 15 seconds
            if self.elapsed_time > 5:
                if random.random() < 0.02:  # 2% chance to spawn rotten fruit
                    self.rotten_fruit.randomize()

    def update_timer(self):
        # Update the elapsed time if the game is not paused
        self.elapsed_time = time.time() - self.start_time


    def draw_elements(self):
        screen.blit(self.background_image, (0, 50))
        self.fruit.draw_fruit()
        self.power_fruit.draw_fruit()
        self.spike_ball.draw_spikes()  # Draw spike ball
        self.rotten_fruit.draw_rotten_fruits()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_timer()
        self.draw_health()
        if self.paused:
            self.draw_pause_screen() #Draw pause screen

    def draw_timer(self):
        # Convert elapsed time to minutes and seconds
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        timer_text = f"{minutes:02}:{seconds:02}"

        # Render the timer text
        timer_surface = game_font.render(timer_text, True, (255, 255, 255))
        timer_x = screen.get_width() // 2
        timer_y = 25  # Position it at the top center

        timer_rect = timer_surface.get_rect(center=(timer_x, timer_y))
        screen.blit(timer_surface, timer_rect)

    def draw_health(self):
        for i in range(self.max_health):
            heart_x = 4 + i * 25
            heart_y = 4
            if i < self.current_health:
                screen.blit(self.heart_image, (heart_x, heart_y))
            else:
                screen.blit(self.empty_heart_image, (heart_x, heart_y))
    
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.score += 10  # Increment score by 10

            # Update the high score
            if self.score > self.high_score:
                self.high_score = self.score

            #Play fruit sound
            self.fruit_sound.play()

            # Check if power fruit should be activated
            if self.score % 100 == 0:
                self.power_fruit.activate()

        # Check for collision with the power fruit
        if self.power_fruit.active and self.power_fruit.pos == self.snake.body[0]:
            self.power_fruit.deactivate()
            self.score += 20  # Increase score by 20 for collecting power fruit

            #Play fruit sound
            self.power_fruit_sound.play()
            
            # Update the high score
            if self.score > self.high_score:
                self.high_score = self.score

        # Check for collision with any spike ball
        for spike in self.spike_ball.spikes:
            if spike['pos'] == self.snake.body[0]:
                self.game_over()  # End the game if the snake hits a spike ball

        for fruit in self.rotten_fruit.rotten_fruits:
            if fruit['pos'] == self.snake.body[0]:
                self.current_health -= 1
                self.rotten_fruit.rotten_fruits.remove(fruit)  # Remove rotten fruit after collision
                
                #Play fruit sound
                self.rotten_fruit_sound.play()
                
                if self.current_health == 0:
                    self.game_over()  # End game if no health is left
        
        # Avoid fruit spawning inside the snake's body
        #for block in self.snake.body[1:]:
            #if block == self.fruit.pos:
                #self.fruit.randomize()

    def check_fail(self):
        # Check if the snake hits the wall
        if not 0 <= self.snake.body[0].x < cell_number or not 1 <= self.snake.body[0].y < cell_number:
            self.game_over()

        # Check if the snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()
        self.score = 0  # Reset score after game over
        self.start_time = time.time()  # Reset the start time when the game is over
        self.elapsed_time = 0  # Reset the elapsed time
        self.spike_ball.spikes = []  # Clear spike balls after game over
        self.current_health = self.max_health  # Reset health after game over
    
    def draw_score(self):
        # Set the height of the score area
        score_area_height = 50

        # Draw the black background for the score
        score_background_rect = pygame.Rect(0, 0, screen.get_width(), score_area_height)
        pygame.draw.rect(screen, (0, 0, 0), score_background_rect)

        # Render the score and high score texts
        score_text = f"Score: {self.score}"
        high_score_text = f"High Score: {self.high_score}"

        score_surface = game_font.render(score_text, True, (255, 255, 255))
        high_score_surface = game_font.render(high_score_text, True, (255, 255, 255))

        # Calculate positions to center the text at the top of the screen
        score_x = screen.get_width() // 4
        score_y = score_area_height // 2

        high_score_x = 3 * screen.get_width() // 4
        high_score_y = score_area_height // 2

        score_rect = score_surface.get_rect(center=(score_x, score_y))
        high_score_rect = high_score_surface.get_rect(center=(high_score_x, high_score_y))

        screen.blit(score_surface, score_rect)
        screen.blit(high_score_surface, high_score_rect)

    
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Define colors
white = (255, 255, 255)
grey = (169, 169, 169)

cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('assets/apple.png').convert_alpha()
power_apple = pygame.image.load('assets/power_apple2.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if main_game.paused:
            main_game.check_pause_screen_events(event)
        else:
            if event.type == SCREEN_UPDATE:
                main_game.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_game.paused = not main_game.paused  # Toggle pause state

                if not main_game.paused:  # Only handle movement when not paused
                    if event.key == pygame.K_UP:
                        if main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_DOWN:
                        if main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT:
                        if main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        if main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1, 0)
        
                    if event.key == pygame.K_w:
                        if main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_s:
                        if main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_a:
                        if main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_d:
                        if main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1, 0)

    main_game.draw_elements()
    if main_game.paused:
        main_game.draw_pause_screen()
    pygame.display.update()
    clock.tick(60)
