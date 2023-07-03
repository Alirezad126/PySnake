
import pygame
from pygame.surfarray import array3d
from pygame import display
import numpy as np
import matplotlib.pyplot as plt
import random
import sys
import time
import gym
from gym import error,spaces,utils
from gym.utils import seeding

# Setting game colors:
# Define color constants using pygame.Color

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(225, 230, 230)
RED = pygame.Color(255, 0, 0)
LIGHT_BLUE = pygame.Color(48, 44, 245)
DARK_BLUE = pygame.Color(5, 3, 107)
GRAY = pygame.Color(209, 209, 209)
DARK_GRAY = pygame.Color(174, 176, 176)

# Define the SnakeEnv class that inherits from gym.Env

class SnakeEnv(gym.Env):
    def __init__(self):
        # Initialize the action space as a Discrete space with 4 actions
        self.action_space = spaces.Discrete(4)
        self.frame_size_x = 400
        self.frame_size_y = 400
        self.cell_size = 20
        self.STEP_LIMIT = 1000

        self.game_window = None  # Game window is not opened by default

        # Reset the game:
        self.reset()

        # Limit the play time for agent
        self.STEP_LIMIT = 1000
        self.sleep = 0

    def reset(self):
        # Reset the game state
        # Initialize the game window surface with gray color and draw the boundaries
        # Set initial snake position, body, and food position
        # Reset direction, score, and steps
        # Return the initial state

        self.game_window = pygame.Surface((self.frame_size_x, self.frame_size_y))
        self.game_window.fill(GRAY)
        pygame.draw.rect(self.game_window, DARK_GRAY, pygame.Rect(0, 0, self.frame_size_x, self.cell_size))
        pygame.draw.rect(self.game_window, DARK_GRAY, pygame.Rect(0, self.frame_size_y - self.cell_size, self.frame_size_x, self.cell_size))
        pygame.draw.rect(self.game_window, DARK_GRAY, pygame.Rect(0, 0, self.cell_size, self.frame_size_y))
        pygame.draw.rect(self.game_window, DARK_GRAY, pygame.Rect(self.frame_size_x - self.cell_size, 0, self.cell_size, self.frame_size_y))
        
        for x in range(self.cell_size, self.frame_size_x, self.cell_size):
            pygame.draw.line(self.game_window, WHITE, (x, 0), (x, self.frame_size_y))
        
        for y in range(self.cell_size, self.frame_size_y, self.cell_size):
            pygame.draw.line(self.game_window, WHITE, (0, y), (self.frame_size_x, y))

        self.snake_pos = [5*self.cell_size, 3*self.cell_size]
        self.snake_body = [[5*self.cell_size, 3*self.cell_size], [4*self.cell_size, 3*self.cell_size], [3*self.cell_size, 3*self.cell_size]]
        self.food_pos = self.spawn_food()
        self.food_spawn = True

        self.direction = "RIGHT"
        self.action = self.direction
        self.score = 0
        self.steps = 0

        state = self.get_state_array_from_game()
        return state

    @staticmethod
    def change_direction(action, direction):
        # Helper function to change the direction based on the current action

        if action == 0 and direction != "DOWN":
            direction = "UP"
        if action == 1 and direction != "UP":
            direction = "DOWN"
        if action == 2 and direction != "LEFT":
            direction = "RIGHT"
        if action == 3 and direction != "RIGHT":
            direction = "LEFT"
        return direction

    @staticmethod
    def move(direction, snake_pos,cell_size):
        # Helper function to move the snake position based on the current direction

        if direction == "UP":
            snake_pos[1] -= cell_size 
        if direction == "DOWN":
            snake_pos[1] += cell_size 
        if direction == "LEFT":
            snake_pos[0] -= cell_size 
        if direction == "RIGHT":
            snake_pos[0] += cell_size 
        return snake_pos

    def spawn_food(self):
        # Calculate the valid range for food spawning
        min_x = self.cell_size
        max_x = (self.frame_size_x - 2 * self.cell_size) // self.cell_size * self.cell_size
        min_y = self.cell_size
        max_y = (self.frame_size_y - 2 * self.cell_size) // self.cell_size * self.cell_size

        # Generate a list of all possible food positions within the valid range
        possible_positions = [
            [x, y]
            for x in range(min_x, max_x, self.cell_size)
            for y in range(min_y, max_y, self.cell_size)
        ]

        # Filter out positions that overlap with the snake's body
        valid_positions = [
            pos
            for pos in possible_positions
            if pos not in self.snake_body
        ]

        # Randomly select a position from the valid positions
        food_position = random.choice(valid_positions)

        return food_position

    def eat(self):
        # Check if the position of snake and food is the same
        return (
            self.snake_pos[0] == self.food_pos[0]
            and self.snake_pos[1] == self.food_pos[1]
        )
    
    def step(self, action):
        # Take a step in the game based on the given action
        # Update the direction and move the snake
        # Handle food, update game state, and calculate reward and done flag
        # Return the new state, reward, done flag, and additional information
        
        scoreholder = self.score
        reward = 0
        current_pos = self.snake_pos

        self.direction = self.change_direction(action, self.direction)
        self.snake_pos = self.move(self.direction, self.snake_pos, self.cell_size)
        self.snake_body.insert(0, list(self.snake_pos))
        reward = self.food_handler() + self.distance_reward(self.food_pos, current_pos, self.snake_pos)- 0.2 # reward_handler

        self.update_game_state()

        reward, done = self.game_over(self.snake_pos,reward)

        state = self.get_state_array_from_game()  # Get the observation

        info = {"score": self.score}

        self.steps += 1
        time.sleep(self.sleep)

        return state, reward, done, info
        
    def get_state_array_from_game(self):
        # Get the state array from the current game state
        # The state includes danger indicators for each direction, snake direction, and food position
        
        head_x, head_y = self.snake_pos[0], self.snake_pos[1]
    
        point_l = [head_x - self.cell_size, head_y]
        point_r = [head_x + self.cell_size, head_y]
        point_u = [head_x, head_y - self.cell_size]
        point_d = [head_x, head_y + self.cell_size]

        dir_l = self.direction == "LEFT"
        dir_r = self.direction == "RIGHT"
        dir_u = self.direction == "UP"
        dir_d = self.direction == "DOWN"

        state = [
            #Danger Straight
            (dir_r and self.game_over(point_r,None)) or
            (dir_l and self.game_over(point_l,None)) or
            (dir_u and self.game_over(point_u,None)) or
            (dir_d and self.game_over(point_d,None)),

            #Danger Right
            (dir_u and self.game_over(point_r,None)) or
            (dir_d and self.game_over(point_l,None)) or
            (dir_r and self.game_over(point_d,None)) or
            (dir_l and self.game_over(point_u,None)),

            #Danger Left
            (dir_d and self.game_over(point_r,None)) or
            (dir_u and self.game_over(point_l,None)) or
            (dir_r and self.game_over(point_u,None)) or
            (dir_l and self.game_over(point_d,None)),

            #Move Direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            #Food Position
            self.food_pos[0] < head_x,  #Food Left
            self.food_pos[0] > head_x,  #Food Right
            self.food_pos[1] < head_y,  #Food Up
            self.food_pos[1] > head_y,  #Food Down
        ]

        return np.array(state, dtype=int)


    
    def distance_reward(self, food_pos, current_pos, new_pos):
        # Calculate the distance-based reward for moving closer or farther away from the food

        current_distance = np.linalg.norm(np.array(current_pos) - np.array(food_pos))
        new_distance = np.linalg.norm(np.array(new_pos) - np.array(food_pos))

        if new_distance < current_distance:
            return 2
        else:
            return -2


    def food_handler(self):
        # Handle the food item when the snake eats it or not

        if self.eat():
            self.score += 1
            reward = 50
            self.food_spawn = False
        else:
            self.snake_body.pop()
            reward=0
            

        if not self.food_spawn:
            self.food_pos = self.spawn_food()

        self.food_spawn = True

        return reward

    def get_image_array_from_game(self):
        # Get the image array from the current game window surface

        img = array3d(self.game_window)
        img = np.swapaxes(img, 0, 1)
        return img

    def update_game_state(self):
        # Update the game state by redrawing the game window surface
        
        self.game_window.fill(GRAY)
        pygame.draw.rect(self.game_window, DARK_GRAY, pygame.Rect(0, 0, self.frame_size_x, self.cell_size))
        pygame.draw.rect(self.game_window, DARK_GRAY, pygame.Rect(0, self.frame_size_y - self.cell_size, self.frame_size_x, self.cell_size))
        pygame.draw.rect(self.game_window, DARK_GRAY, pygame.Rect(0, 0, self.cell_size, self.frame_size_y))
        pygame.draw.rect(self.game_window, DARK_GRAY, pygame.Rect(self.frame_size_x - self.cell_size, 0, self.cell_size, self.frame_size_y))

        for x in range(self.cell_size, self.frame_size_x, self.cell_size):
            pygame.draw.line(self.game_window, WHITE, (x, 0), (x, self.frame_size_y))

        for y in range(self.cell_size, self.frame_size_y, self.cell_size):
            pygame.draw.line(self.game_window, WHITE, (0, y), (self.frame_size_x, y))

        for pos in self.snake_body:
            if pos == self.snake_body[0]:
                pygame.draw.rect(self.game_window, LIGHT_BLUE, pygame.Rect(pos[0], pos[1], self.cell_size, self.cell_size))
            else:
                pygame.draw.rect(self.game_window, DARK_BLUE, pygame.Rect(pos[0], pos[1], self.cell_size, self.cell_size))
            pygame.draw.rect(self.game_window, GRAY, pygame.Rect(pos[0], pos[1], self.cell_size, self.cell_size), 1)

        # Drawing of food
        pygame.draw.rect(self.game_window, RED, pygame.Rect(self.food_pos[0], self.food_pos[1], self.cell_size, self.cell_size))
        pygame.draw.rect(self.game_window, GRAY, pygame.Rect(self.food_pos[0], self.food_pos[1], self.cell_size, self.cell_size), 1)

        # Displaying the score
        pygame.font.init()
        score_font = pygame.font.SysFont(None, 40)
        score_surface = score_font.render("Score: " + str(self.score), True, WHITE, BLACK)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.frame_size_x / 2, self.cell_size / 2)

        self.game_window.blit(score_surface, score_rect)



    def game_over(self, point, reward):
        # If touching the bounding box
        if (
            point[0] < self.cell_size or
            point[0] >= self.frame_size_x - self.cell_size or
            point[1] < self.cell_size or
            point[1] >= self.frame_size_y - self.cell_size
        ):
            if reward != None:
                return -50, True
            else:
                return True

        # If touching own body
        for block in self.snake_body[1:]:
            if (
                point[0] == block[0] and point[1] == block[1]
            ):
                if reward != None:
                    return -50, True
                else:
                    return True
                
        if self.steps >= self.STEP_LIMIT:
            if reward!=None:
                return 0, True
            else:
                return True
        
        if reward != None:
                return reward, False
        else:
            return False

    def render(self, mode="human"):
        if mode == "human":
            display.update()

    def close(self):
        pass



            
            
    

        