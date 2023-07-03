import pygame
import sys
import time
import random
from pygame.surfarray import array3d


#Setting game colors:

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(225, 230, 230)
RED = pygame.Color(255, 0, 0)
LIGHT_GREEN = pygame.Color(144, 238, 144)
DARK_GREEN = pygame.Color(0, 100, 0)
GRAY = pygame.Color(209, 209, 209)
DARK_GRAY = pygame.Color(174, 176, 176)



class SnakeEnv():
    def __init__(self, frame_size_x, frame_size_y,cell_size):
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.cell_size = cell_size
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))
        
        # Reset the game:
        self.reset()

    def reset(self):
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

        self.score = 0
        self.steps = 0
        print("GAME RESET")

    def change_direction(self, action, direction):
        
        if action =="UP" and direction!="DOWN":
            direction = "UP"

        if action =="DOWN" and direction!="UP":
            direction = "DOWN"

        if action =="RIGHT" and direction!="LEFT":
            direction = "RIGHT"

        if action =="LEFT" and direction!="RIGHT":
            direction = "LEFT"

        return direction
    
    def move(self, direction, snake_pos):

        if direction=="UP":
            snake_pos[1] -= self.cell_size

        if direction=="DOWN":
            snake_pos[1] += self.cell_size

        if direction=="LEFT":
            snake_pos[0] -= self.cell_size

        if direction=="RIGHT":
            snake_pos[0] += self.cell_size

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
        #check if the position of snake and food is the same
        return self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]

    def human_step(self, event):
        
        action = None

        if event.type ==pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                
                action = "UP"
            if event.key == pygame.K_LEFT:
                
                action = "LEFT"
            if event.key == pygame.K_DOWN:
                
                action = "DOWN"
            if event.key == pygame.K_RIGHT:
                
                action = "RIGHT"

            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

        return action
    
    def display_score(self, color, font, size):
        
        score_font = pygame.font.SysFont(None, 40)
        score_surface = score_font.render("Score: " + str(self.score), True, WHITE, BLACK)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.frame_size_x / 2, self.cell_size / 2)
        
        self.game_window.blit(score_surface,score_rect)

    def game_over(self):

        #if touching the bounding box
        over = False

        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x-2*self.cell_size:
            over = True

        
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y-2*self.cell_size:
            over = True

        #if touch own body
        
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                over = True
        return over
    
    
        
    
    def end_game(self):

        message = pygame.font.SysFont("arial",25)
        message_surface = message.render("GAME HAS ENDED", True, RED)
        message_rect = message_surface.get_rect()
        message_rect.midtop = (self.frame_size_x/2, self.frame_size_y/2)

        self.game_window.fill(BLACK)
        self.game_window.blit(message_surface, message_rect)
        self.display_score(RED, "times", 20)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()
    
            
            
    

        