import numpy as np


class Map:
    def __init__(self, x, y):
        self.grid = np.zeros(shape=(x, y))
        self.x = x
        self.y = y

    def is_occupacy(self, x, y):
        if self.grid[x][y] == 0:
            return False
        else:
            return True

    def occupated_points(self):
        obstacles_xy = []
        for i in range(self.x):
            for j in range(self.y):
                if self.grid[i][j] == 1:
                    obstacles_xy.append([i, j])
        return obstacles_xy

    def generate_map(self):
        for i in range(self.x):
            arr_01 = [0, 1]
            rand = np.random.choice(arr_01, self.y, p=[0.9, 0.1])
            self.grid[i] = rand

    def print_map(self):
        print(self.grid)


if __name__ == "__main__":
    map = Map(20, 20)
    map.generate_map()
    map.print_map()
