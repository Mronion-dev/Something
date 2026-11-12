# snake.py
import pygame
import random

# Initialize Pygame
pygame.init()

# Game constants
WIDTH = 640
HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        # Start snake in the middle of the screen
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = [(start_x, start_y), (start_x, start_y + 1), (start_x, start_y + 2)]
        self.direction = (0, 1)
        self.grow = False
    
    def move(self):
        # Calculate new head position
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        # Check for game over (hitting wall or itself)
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in self.body):
            return False
        
        # Insert new head
        self.body.insert(0, new_head)
        
        # If not growing, remove tail
        if not self.grow:
            self.body.pop()
        
        # Handle growth
        if self.grow:
            self.grow = False
        
        return True
    
    def grow_snake(self):
        self.grow = True
    
    def change_direction(self, new_direction):
        # Prevent 180-degree turns
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def draw(self, surface):
        for i, segment in enumerate(self.body):
            color = GREEN if i == 0 else DARK_GREEN
            rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1)
            pygame.draw.rect(surface, color, rect)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()
    
    def spawn(self, snake_body=None):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                self.position = pos
                break
    
    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1)
        pygame.draw.rect(surface, RED, rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    return True
                
                if not self.game_over:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
        
        return True