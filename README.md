**Enhanced Snake Game**

Overview

The Enhanced Snake Game is a Python-based game created using the Pygame library. It is an upgraded version of the classic Snake game, introducing new features such as power-ups, obstacles, and multiple game states (Menu, Playing, and Game Over). Players control the snake to eat food, avoid obstacles, and collect power-ups while aiming for a high score.

Features

Dynamic Menu and Game Over Screens: Includes start and restart buttons.

Power-Ups: Randomly appearing power-ups with unique effects:

Speed Boost: Increases snake speed.

Invincibility: Allows the snake to pass through obstacles and itself without dying.

Shrink: Reduces the size of the snake.

Obstacles: Spawn dynamically based on the current level.

Levels and Score: The game gets progressively harder as the player’s score increases.

Enhanced Visuals:

Gradient snake body.

Animated food with a pulsing effect.

Unique visuals for the snake’s head and tail.

Pause Functionality: Allows players to pause and resume the game.

Requirements

Python 3.7 or higher

Pygame library

Installation

Make sure Python is installed on your system. You can download it from python.org.

Install the Pygame library by running:

pip install pygame

Download or clone this repository.

How to Play

Run the game script:

python snake_game.py

On the main menu, click Start Game to begin.

Use the following keys to control the snake:

Arrow Keys / W, A, S, D: Change direction.

P: Pause or resume the game.

ESC: Quit the game.

Eat the red food to increase your score.

Collect power-ups to gain special abilities.

Avoid running into obstacles, the edges of the screen, or the snake’s body.

When the game ends, click Play Again to restart.

Game States

Menu: The initial screen where you can start the game.

Playing: The main gameplay mode.

Game Over: Displayed when the snake collides with an obstacle, itself, or the boundary.

Code Structure

SnakeGame Class: Main class managing game logic, rendering, and state transitions.

Button Class: For rendering and handling interactions with buttons.

PowerUp Class: Represents power-ups with a timer-based lifecycle.

Obstacle Class: Represents obstacles on the grid.

GameState Enum: Represents different states of the game.

Customization

Window Size: Adjust WINDOW_WIDTH and WINDOW_HEIGHT constants.

Grid Size: Change GRID_SIZE to modify the size of each grid cell.

Game Speed: Modify self.game_speed in the SnakeGame class for different difficulty levels.

Power-Up Types: Add new power-ups or modify existing ones in the spawn_power_up method.

Known Issues

None reported.

Future Enhancements

Multiplayer mode.

Additional power-ups and obstacles.

Save and load game progress.

License

This project is open-source and free to use. Feel free to modify and distribute it.

Credits

Developed by: Shiva Dhama

Python and Pygame documentation and community resources.
