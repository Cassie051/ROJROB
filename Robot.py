from Astar import Astar


class Robot:
    """Klasa modelujaca robota"""

    def __init__(self, position=None):
        if position:
            self.position = position
        else:
            self.position = 0, 0
        self.status = "Free"
        self.path = []

    def find_path(self, goal):
        self.path = Astar().solve(self.position, goal)

    def print_path(self):
        for point in self.path:
            print(point)

    def get_path(self):
        return self.path

    def get_position(self):
        return self.position


if __name__ == "__main__":
    robot1 = Robot([1, 1])
    robot1.find_path([5, 5])
    robot1.print_path()
