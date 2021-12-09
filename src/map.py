class Map:
    def __init__(self, x, y):
        self.grid = [[0]*x, [0]*y]
        self.x = x
        self.y = y

    def is_occupacy(self, x, y):
        if self.grid[x][y] == 0:
            return False
        else:
            return True
