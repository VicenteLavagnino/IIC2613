import numpy as np
import pygame
import gymnasium as gym
from gymnasium import spaces

LIGHTBLU = (150, 150, 255)

class FlappyBidoofEnv(gym.Env):
    metadata = {"render_modes": ["ascii", "fancy"], "render_fps": 3}

    def __init__(self, n_columns: int=2,
                 pizza_value: float=5.0,
                 fire_value: float=-2.0):
        self.max_length = 100
        # Action space: 0 = ×, 1 = ↑, 2 = ↓
        self.n_columns = n_columns
        self.pizza_value = pizza_value
        self.fire_value = fire_value
        self.action_space = spaces.Discrete(3)
        self.action_graphics = {0: '×', 1: '↑', 2: '↓'}

        # Observation space: height, plat_low, plat_mid, plat_high
        self.observation_space = spaces.MultiDiscrete(
            [3] + [4] * 3*self.n_columns)
        self.start_position = [1] + [0] * 3 * self.n_columns
        self.reset()

    def reset(self):
        bidoof_position = 1  # Middle row (0: low, 1: mid, 2: high)
        next_platforms = np.random.randint(0, 4, size=3)
        next_next_platforms = np.random.randint(0, 4, size=3)
        while not np.any(next_platforms != 0):
            next_platforms = np.random.randint(0, 4, size=3)
        while not np.any(next_next_platforms != 0):
            next_next_platforms = np.random.randint(0, 4, size=3)
        self.state = np.concatenate(([bidoof_position],
            next_platforms, next_next_platforms))
        # Rendering only
        self.previous_position = 1
        self.previous_platforms = np.array([0, 1, 0])
        self.screen = False
        return self.state
    
    def step(self, action):
        bidoof_position = self.state[0]
        platforms_col1 = self.state[1:4]
        platforms_col2 = self.state[4:7]

        # Determine Bidoof's new position based on the action
        if action == 2:  # move down
            new_position = max(0, bidoof_position - 1)
        elif action == 1:  # move up
            new_position = min(2, bidoof_position + 1)
        else:  # hold position
            new_position = bidoof_position

        done = False
        # Check if there's a platform at Bidoof's new position
        if (platforms_col1[new_position] == 0): # Falling
            reward = 0
            done = True
        elif (platforms_col1[new_position] == 1): # Safe landing
            reward = 1
        elif (platforms_col1[new_position] == 2): # Pizza landing
            reward = self.pizza_value + 1
        elif (platforms_col1[new_position] == 3): # Fire landing
            reward = self.fire_value + 1 
        new_platforms = np.random.randint(0, 4, size=3)
        while not np.any(new_platforms != 0):
            new_platforms = np.random.randint(0, 4, size=3)
        self.state = np.concatenate(
            ([new_position], platforms_col2, new_platforms))
        self.previous_position = bidoof_position
        self.previous_platforms = platforms_col1
        
        return self.state, reward, done, False, {}
            
    def render(self, **kwargs):
        SCROLL_FRAMES = 10  # Number of frames to complete one scroll step
        try:
            window_size = kwargs['window_size']
        except KeyError:
            window_size = 800, 600 # Default size
        PLATFORM_WIDTH = window_size[0] // 2.5 # Width of each column
        if 'done' in kwargs:
            terminated = kwargs['done']
        else:
            terminated = False
                    
        # Set up Pygame screen if not initialized
        if (not hasattr(self, 'screen')) or (self.screen == False):
            pygame.init()
            self.screen = pygame.display.set_mode(window_size)
            pygame.display.set_caption("Flappy Bidoof")
            self.img_player = pygame.image.load('Assets/minibidoof.png')
            self.img_player = pygame.transform.scale(
                self.img_player, (window_size[0]/9, window_size[1]/10))
            self.img_floor = pygame.image.load('Assets/platform.png')
            self.img_pizza = pygame.image.load('Assets/Pizza.png')
            self.img_fire = pygame.image.load('Assets/Fire.png')
            self.clock = pygame.time.Clock()
        
        bidoof_position = 2 - self.state[0] # From up to down
        present_platforms = self.previous_platforms
        future_platforms1 = self.state[1:4]
        future_platforms2 = self.state[4:7]
        old_position = 2 - self.previous_position
        
        offset = self.screen.get_width() / (3.5 * SCROLL_FRAMES)
        for i in range(SCROLL_FRAMES):
            self.screen.fill(LIGHTBLU)
            
            # Falling of Bidoof :c
            if terminated:
                original_width, original_height = self.img_player.get_size()
                new_width = int(original_width * 0.9)
                new_height = int(original_height * 0.9)
                self.img_player = pygame.transform.scale(
                    self.img_player, (new_width, new_height))
            # Draw Bidoof at his current position
            bidoof_x = self.screen.get_width()/8
            displacement_factor = min(3*(i+1), SCROLL_FRAMES-1)
            true_position = old_position + \
                displacement_factor / (SCROLL_FRAMES-1) * \
                (bidoof_position - old_position)
            bidoof_y = self.screen.get_height()/6 + \
                       true_position * self.screen.get_height()/4
            self.screen.blit(self.img_player, (bidoof_x, bidoof_y))

            player_rect = self.img_player.get_rect(
                topleft=(bidoof_x, bidoof_y))

            # Draw platforms
            for col in range(3):
                x_position = self.screen.get_width()/8 + \
                             col * PLATFORM_WIDTH - i*offset
                if col == 0:
                    platforms = present_platforms
                elif col == 1:
                    platforms = future_platforms1
                else:
                    platforms = future_platforms2

                # Draw platforms in each row of the column
                for row, platform in enumerate(platforms):
                    y_position = 130 + (2-row) * 150
                    pos = (x_position, y_position)
                    pizzapos = (x_position + 20, y_position - 37)
                    firepos = (x_position - 4, y_position - 37)
                    if platform == 1:
                        self.screen.blit(self.img_floor, pos)
                    elif platform == 2:
                        self.screen.blit(self.img_floor, pos)
                        pizza_rect = self.img_pizza.get_rect(topleft=pizzapos)
                        if not (player_rect.colliderect(pizza_rect)) and \
                           not ((i > 4) and (col == 0)):
                            self.screen.blit(self.img_pizza, pizzapos)
                    elif platform == 3:
                        self.screen.blit(self.img_floor, pos)
                        self.screen.blit(self.img_fire, firepos)          
            # Redraw player on top
            self.screen.blit(self.img_player, (bidoof_x, bidoof_y))
            # Update display
            pygame.display.flip()
            pygame.event.pump()
            self.clock.tick(self.metadata["render_fps"])