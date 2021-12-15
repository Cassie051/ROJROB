import random

class Map:
    def __init__(self, x, y):
        self.grid = [[0] * x] * y
        self.x = x
        self.y = y
        self.obstycle_amont = 5

    def is_occupacy(self, x, y):
        if self.grid[x][y] == 0:
            return False
        else:
            return True

    def generate_map(self):
        i = 0
        x, y = 0, 0
        for i in range(self.x):
            x = random.randint(1, (self.x - 1))
            for j in range(self.y):
                y = random.randint(1, (self.y - 1))
                self.grid[x][y] = random.randint(0, 1)


    def print_map(self):
        for x in range(self.x):
            for y in range(self.y):
                print(self.grid[x][y], end = ' ')
            print()

if __name__ == "__main__":
    map = Map(20, 20)
    map.generate_map()
    map.print_map()
