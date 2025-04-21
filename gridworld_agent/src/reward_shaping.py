import numpy as np

class RewardShapingMixin:
    def _distance_to_closest_goal(self, x, y):
        return min(np.sqrt((gx - x)**2 + (gy - y)**2) for gx, gy in self.goal_cells)

    def _nearby_red_penalty(self, x, y):
        penalty = 0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and self.grid[nx, ny] == 3:
                    dist = abs(dx) + abs(dy)
                    if dist <= 2:
                        penalty += 5 / (dist + 1)
        return -penalty

