import pygame
import random
import sys
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
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

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.match_font("arial"), 36)
        self.large_font = pygame.font.Font(pygame.font.match_font("arial"), 64)

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
        self.game_speed = 10
        self.game_state = GameState.MENU
        self.paused = False

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

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

        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)

        self.restart_button.draw(self.screen, self.font)

    def draw_game(self):
        self.screen.fill(GRAY)

        # Draw snake with gradient, detailed head, and unique tail
        for i, segment in enumerate(self.snake):
            x, y = segment[0] * GRID_SIZE, segment[1] * GRID_SIZE
            if i == 0:  # Snake head
                pygame.draw.circle(self.screen, YELLOW, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), GRID_SIZE // 2)
                pygame.draw.circle(self.screen, BLACK, (x + GRID_SIZE // 2 - 4, y + GRID_SIZE // 2 - 4), 3)
                pygame.draw.circle(self.screen, BLACK, (x + GRID_SIZE // 2 + 4, y + GRID_SIZE // 2 - 4), 3)
            elif i == len(self.snake) - 1:  # Snake tail
                pygame.draw.circle(self.screen, ORANGE, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), GRID_SIZE // 3)
            else:  # Body segments
                color = (0, max(255 - i * 10, 100), 0)
                pygame.draw.rect(self.screen, color, (x, y, GRID_SIZE - 2, GRID_SIZE - 2))

        # Draw food with a pulsing effect and shadow
        food_size = GRID_SIZE - 2 + abs(pygame.time.get_ticks() % 1000 - 500) / 500
        shadow_offset = 4
        food_rect = pygame.Rect(
            self.food[0] * GRID_SIZE + (GRID_SIZE - food_size) / 2,
            self.food[1] * GRID_SIZE + (GRID_SIZE - food_size) / 2,
            food_size, food_size
        )
        shadow_rect = food_rect.move(shadow_offset, shadow_offset)
        pygame.draw.rect(self.screen, BLACK, shadow_rect)
        pygame.draw.rect(self.screen, RED, food_rect)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

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

        new_head = (
            self.snake[0][0] + self.direction[0],
            self.snake[0][1] + self.direction[1]
        )

        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in self.snake):
            self.game_state = GameState.GAME_OVER
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
            if self.score % 5 == 0:
                self.game_speed += 1
        else:
            self.snake.pop()

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
