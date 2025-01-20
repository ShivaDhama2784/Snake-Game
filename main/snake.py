import pygame
import random
import sys
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600  # Adjusted for demonstration
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Game States
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = tuple(min(c + 30, 255) for c in color)
        self.is_hovered = False

    def draw(self, screen, font):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)

        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class PowerUp:
    def __init__(self, position, type):
        self.position = position
        self.type = type
        self.timer = 200  # Power-up disappears after 200 frames

    def update(self):
        self.timer -= 1
        return self.timer <= 0

class Obstacle:
    def __init__(self, position):
        self.position = position

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Enhanced Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 64)
        self.obstacles = []  # Initialize obstacles as an empty list
        self.reset_game()

        button_width = 300
        button_height = 60
        button_x = WINDOW_WIDTH // 2 - button_width // 2

        self.start_button = Button(button_x, WINDOW_HEIGHT // 2, button_width, button_height, "Start Game", DARK_GREEN)
        self.restart_button = Button(button_x, WINDOW_HEIGHT * 2 // 3, button_width, button_height, "Play Again", DARK_GREEN)
        self.reset_game()

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.level = 1
        self.game_speed = 10
        self.game_state = GameState.MENU
        self.paused = False
        self.power_ups = []
        self.obstacles = []
        self.active_power_up = None
        self.power_up_timer = 0
        self.food = self.spawn_food()

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake and food not in [o.position for o in self.obstacles]:
                
                return food

    def spawn_power_up(self):
        if random.random() < 0.1:  # 10% chance to spawn a power-up
            while True:
                pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                if pos not in self.snake and pos not in [o.position for o in self.obstacles] and pos != self.food:
                    return PowerUp(pos, random.choice(["speed", "invincibility", "shrink"]))
        return None

    def spawn_obstacle(self):
        if len(self.obstacles) < self.level:  # Spawn obstacles based on level
            while True:
                pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                if pos not in self.snake and pos != self.food and pos not in [p.position for p in self.power_ups]:
                    return Obstacle(pos)
        return None

    def draw_menu(self):
        self.screen.fill(BLACK)
        title = self.large_font.render("SNAKE GAME", True, GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        self.screen.blit(title, title_rect)

        self.start_button.draw(self.screen, self.font)

    def draw_game_over(self):
        self.screen.fill(BLACK)
        game_over_text = self.large_font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level Reached: {self.level}", True, WHITE)

        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        level_rect = level_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(level_text, level_rect)

        self.restart_button.draw(self.screen, self.font)

    def draw_game(self):
        self.screen.fill(GRAY)

        # Draw snake with gradient, detailed head, and unique tail
        for i, segment in enumerate(self.snake):
            x, y = segment[0] * GRID_SIZE, segment[1] * GRID_SIZE
            if i == 0:  # Snake head
                color = YELLOW if self.active_power_up == "invincibility" else GREEN
                pygame.draw.circle(self.screen, color, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), GRID_SIZE // 2)
                pygame.draw.circle(self.screen, BLACK, (x + GRID_SIZE // 2 - 4, y + GRID_SIZE // 2 - 4), 3)
                pygame.draw.circle(self.screen, BLACK, (x + GRID_SIZE // 2 + 4, y + GRID_SIZE // 2 - 4), 3)
            elif i == len(self.snake) - 1:  # Snake tail
                pygame.draw.circle(self.screen, GREEN, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), GRID_SIZE // 3)
            else:  # Body segments
                color = (0, max(255 - i * 10, 100), 0)
                pygame.draw.rect(self.screen, color, (x, y, GRID_SIZE - 2, GRID_SIZE - 2))

        # Draw food with a pulsing effect
        food_size = GRID_SIZE - 2 + abs(pygame.time.get_ticks() % 1000 - 500) / 500
        food_rect = pygame.Rect(
            self.food[0] * GRID_SIZE + (GRID_SIZE - food_size) / 2,
            self.food[1] * GRID_SIZE + (GRID_SIZE - food_size) / 2,
            food_size, food_size
        )
        pygame.draw.rect(self.screen, RED, food_rect)

        # Draw power-ups
        for power_up in self.power_ups:
            color = BLUE if power_up.type == "speed" else YELLOW if power_up.type == "invincibility" else PURPLE
            pygame.draw.circle(self.screen, color, (power_up.position[0] * GRID_SIZE + GRID_SIZE // 2, 
                                                    power_up.position[1] * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2)

        # Draw obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, WHITE, (obstacle.position[0] * GRID_SIZE, 
                                                  obstacle.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw score and level
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))

        if self.paused:
            s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            s.set_alpha(128)
            s.fill(BLACK)
            self.screen.blit(s, (0, 0))
            pause_text = self.font.render("PAUSED", True, WHITE)
            pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(pause_text, pause_rect)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.game_state == GameState.MENU:
                if self.start_button.handle_event(event):
                    self.game_state = GameState.PLAYING
            elif self.game_state == GameState.GAME_OVER:
                if self.restart_button.handle_event(event):
                    self.reset_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if self.game_state == GameState.PLAYING:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    if not self.paused:
                        if event.key in [pygame.K_UP, pygame.K_w] and self.direction != (0, 1):
                            self.direction = (0, -1)
                        elif event.key in [pygame.K_DOWN, pygame.K_s] and self.direction != (0, -1):
                            self.direction = (0, 1)
                        elif event.key in [pygame.K_LEFT, pygame.K_a] and self.direction != (1, 0):
                            self.direction = (-1, 0)
                        elif event.key in [pygame.K_RIGHT, pygame.K_d] and self.direction != (-1, 0):
                            self.direction = (1, 0)

        return True

    def update(self):
        if self.game_state != GameState.PLAYING or self.paused:
            return

        # Update power-ups
        for power_up in self.power_ups:
            if power_up.update():
                self.power_ups.remove(power_up)

        # Spawn new power-up
        if not self.power_ups:
            new_power_up = self.spawn_power_up()
            if new_power_up:
                self.power_ups.append(new_power_up)

        # Spawn new obstacle
        new_obstacle = self.spawn_obstacle()
        if new_obstacle:
            self.obstacles.append(new_obstacle)

        # Move snake
        move_speed = 2 if self.active_power_up == "speed" else 1
        for _ in range(move_speed):
            new_head = (
                (self.snake[0][0] + self.direction[0]) % GRID_WIDTH,
                (self.snake[0][1] + self.direction[1]) % GRID_HEIGHT
            )

            # Check for collisions
            if (new_head in self.snake[1:] or 
                new_head in [o.position for o in self.obstacles]) and self.active_power_up != "invincibility":
                self.game_state = GameState.GAME_OVER
                return

            self.snake.insert(0, new_head)

            # Check for power-up collection
            for power_up in self.power_ups:
                if new_head == power_up.position:
                    self.active_power_up = power_up.type
                    self.power_up_timer = 100  # Active for 100 frames
                    self.power_ups.remove(power_up)
                    break

            # Check for food collection
            if new_head == self.food:
                self.score += 1
                self.food = self.spawn_food()
                if self.score % 5 == 0:
                    self.level += 1
                    self.game_speed += 1
            else:
                self.snake.pop()

        # Update active power-up
        if self.active_power_up:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                if self.active_power_up == "shrink":
                    self.snake = self.snake[:len(self.snake)//2]
                self.active_power_up = None

    def run(self):
        running = True
        while running:
            running = self.handle_input()

            if self.game_state == GameState.MENU:
                self.draw_menu()
            elif self.game_state == GameState.PLAYING:
                self.update()
                self.draw_game()
            elif self.game_state == GameState.GAME_OVER:
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(self.game_speed)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()