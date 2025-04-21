import gymnasium as gym
import numpy as np
import pygame
import random
import imageio
import yaml
from pyvirtualdisplay import Display

display = Display(visible=0, size=(600, 600))
display.start()

class GridWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 10}

    def __init__(self, grid_size=15, max_steps=100, render_mode="human"):
        super().__init__()
        self.grid_size = grid_size
        self.max_steps = max_steps
        self.render_mode = render_mode
        self.step_count = 0
        self.observation_space = gym.spaces.Box(0, 9, (grid_size, grid_size), dtype=np.uint8)
        self.action_space = gym.spaces.Discrete(8)
        self.agent_pos = [0, 0]
        self.goal_cells = [(grid_size - 1, 4), (grid_size - 1, 5)]
        self.grid = np.zeros((grid_size, grid_size), dtype=np.uint8)
        self.frames = []
        pygame.init()
        self.cell_size = 50
        self.window_size = grid_size * self.cell_size
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        self.clock = pygame.time.Clock()

    def reset(self, seed=None, options=None):
        self.grid.fill(0)
        self.step_count = 0
        self.agent_pos = [0, random.randint(0, self.grid_size - 1)]
        self._place_obstacles()
        self._update_grid()
        if self.render_mode == "human":
            self.render()
        return self.grid.copy(), {}

    def _place_obstacles(self, count=15):
        for _ in range(count):
            x, y = random.randint(1, self.grid_size - 2), random.randint(0, self.grid_size - 1)
            if (x, y) not in self.goal_cells:
                severity = np.random.choice([1, 2, 3], p=[0.5, 0.3, 0.2])
                self.grid[x, y] = severity

    def _update_grid(self):
        self.grid[self.grid == 8] = 0
        for gx, gy in self.goal_cells:
            self.grid[gx, gy] = 9
        self.grid[tuple(self.agent_pos)] = 8

    def _distance_to_closest_goal(self, x, y):
        return min(np.sqrt((gx - x)**2 + (gy - y)**2) for gx, gy in self.goal_cells)

    def _is_valid_move(self, nx, ny):
        if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
            target_cell = int(self.grid[nx, ny])
            return target_cell not in [2, 3]
        return False

    def step(self, action):
        self.step_count += 1
        x, y = self.agent_pos
        reward = -0.1
        done = False
        moved = False

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        attempted = set()

        while True:
            dx, dy = moves[action]
            nx, ny = x + dx, y + dy

            if self._is_valid_move(nx, ny):
                old_dist = self._distance_to_closest_goal(x, y)
                new_dist = self._distance_to_closest_goal(nx, ny)
                reward += 1 if new_dist < old_dist else -0.5
                if self.grid[nx, ny] == 1:
                    reward -= 1
                if (nx, ny) in self.goal_cells:
                    reward = 100
                    done = True
                self.agent_pos = [nx, ny]
                moved = True
                break
            else:
                reward -= 2
                attempted.add(action)
                if len(attempted) == self.action_space.n:
                    break
                action = random.choice(list(set(range(self.action_space.n)) - attempted))

        if self.step_count >= self.max_steps:
            done = True

        self._update_grid()
        if self.render_mode == "human":
            self.render()
        return self.grid.copy(), reward, done, False, {"moved": moved}

    def render(self):
        return
    if self.render_mode == "human":
        self.screen.fill((0, 0, 0))
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                color = {
                    1: (0, 0, 255),
                    2: (255, 255, 0),
                    3: (255, 0, 0),
                    8: (0, 255, 0),
                    9: (0, 0, 0)
                }.get(self.grid[i, j], (200, 200, 200))
                pygame.draw.rect(self.screen, color, pygame.Rect(j*self.cell_size, i*self.cell_size, self.cell_size, self.cell_size))
        pygame.display.flip()
        self.clock.tick(10)

 # Save frame as an image array
        frame = pygame.surfarray.array3d(pygame.display.get_surface())
        frame = frame.swapaxes(0, 1)  # Convert from (width, height) to (height, width)
        self.frames.append(frame)