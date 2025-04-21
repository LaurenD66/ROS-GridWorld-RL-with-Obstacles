class MovingObstaclesMixin:
    def _update_moving_reds(self):
        new_reds = []
        for x, y in getattr(self, 'moving_reds', []):
            self.grid[x, y] = 0
            new_x = max(0, x - 1)
            new_x = self.grid_size - 2 if new_x == 0 else new_x
            if self.grid[new_x, y] == 0:
                self.grid[new_x, y] = 3
                new_reds.append((new_x, y))
            else:
                self.grid[x, y] = 3
                new_reds.append((x, y))
        self.moving_reds = new_reds

