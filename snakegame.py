import pygame, sys, random
from pygame.math import Vector2

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        # Load snake body parts
        self.load_graphics()

    def load_graphics(self):
        self.head_up = pygame.image.load('assets/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('assets/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('assets/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('assets/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('assets/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('assets/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('assets/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('assets/tail_left.png').convert_alpha()

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
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class PowerFruit:
    def __init__(self):
        self.randomize()
        self.active = False

    def draw_fruit(self):
        if self.active:
            fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
            screen.blit(power_apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def activate(self):
        self.active = True
        self.randomize()

    def deactivate(self):
        self.active = False


class MAIN:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.power_fruit = PowerFruit()
        self.score = 0
        self.high_score = 0

        # Load the background image and scale it to fit the screen
        self.background_image = pygame.image.load('assets/background.png')
        self.background_image = pygame.transform.scale(self.background_image, (cell_number * cell_size, cell_number * cell_size))

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        screen.blit(self.background_image, (0, 0))
        self.fruit.draw_fruit()
        self.power_fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.score += 10  # Increment score by 10

            # Update the high score
            if self.score > self.high_score:
                self.high_score = self.score

            # Check if power fruit should be activated
            if self.score % 100 == 0:
                self.power_fruit.activate()

        if self.power_fruit.active and self.power_fruit.pos == self.snake.body[0]:
            self.power_fruit.deactivate()
            self.snake.add_block()
            self.score += 20  # Increment score by 20 for power fruit

        # Avoid fruit spawning inside the snake's body
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        # Check if the snake hits the wall
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        # Check if the snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()
        self.score = 0  # Reset score after game over

    def draw_score(self):
        score_text = f"Score: {self.score}"
        high_score_text = f"High Score: {self.high_score}"

        score_surface = game_font.render(score_text, True, (56, 74, 12))
        high_score_surface = game_font.render(high_score_text, True, (56, 74, 12))

        # Calculate positions to center the text at the bottom of the screen
        score_x = screen.get_width() // 2
        score_y = screen.get_height() - 45  # Positioning score above the high score

        high_score_x = screen.get_width() // 2
        high_score_y = screen.get_height() - 20  # Positioning high score at the bottom

        score_rect = score_surface.get_rect(center=(score_x, score_y))
        high_score_rect = high_score_surface.get_rect(center=(high_score_x, high_score_y))

        screen.blit(score_surface, score_rect)
        screen.blit(high_score_surface, high_score_rect)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('assets/apple.png').convert_alpha()
power_apple = pygame.image.load('assets/power_apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

smoothness_factor = 10

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
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
        if event.type == pygame.KEYDOWN:
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
    pygame.display.update()
    clock.tick(60)
