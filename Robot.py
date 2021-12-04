from Astar import Astar


class Robot:
    """Klasa modelujaca robota"""

    def __init__(self, position=None, color='b'):
        if position:
            self.position = position
        else:
            self.position = 0, 0
        self.status = "Free"
        self.path = []
        self.color = color

    def find_path(self, goal):
        self.path = Astar().solve(self.position, goal)

    def print_path(self):
        for point in self.path:
            print(point)

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_position(self):
        return self.position

    def set_position(self, pos):
        self.position = pos


if __name__ == "__main__":
    robot1 = Robot([1, 1])
    robot1.find_path([5, 5])
    robot1.print_path()
