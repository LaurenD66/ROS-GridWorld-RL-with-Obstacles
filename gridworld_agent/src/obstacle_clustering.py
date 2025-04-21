import random
import numpy as np

class ObstacleClusteringMixin:
    def _place_obstacles(self, cluster_count=5, cluster_size=3):
        attempts, placed = 0, 0
        while placed < cluster_count and attempts < cluster_count * 10:
            x = random.randint(1, self.grid_size - 2)
            y = random.randint(1, self.grid_size - 2)
            direction = random.choice([(0,1), (1,0), (1,1), (1,-1)])
            cluster = [(x+i*direction[0], y+i*direction[1]) for i in range(cluster_size)]
            if all(0 <= cx < self.grid_size and 0 <= cy < self.grid_size for cx, cy in cluster):
                if all((cx, cy) not in self.goal_cells and self.grid[cx, cy] == 0 for cx, cy in cluster):
                    severity = np.random.choice([1, 2, 3], p=[0.5, 0.3, 0.2])
                    for cx, cy in cluster:
                        self.grid[cx, cy] = severity
                    placed += 1
            attempts += 1

