from robot.astar import Astar


class Robot:
    """Klasa modelujaca robota"""

    def __init__(self, position=None, color='blue'):
        if position:
            self.position = position
        else:
            self.position = 0, 0
        self.status = "Free"
        self.path = []
        self.color = color

    def make_step(self):
        if len(self.path) > 1:
            self.position = self.path[1]
            del self.path[0]
        elif len(self.path) == 1:
            del self.path[0]

    def find_path(self, goal, occupancy_map):
        self.path = Astar().solve(self.position, goal, occupancy_map)

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

    def set_status(self, stat):
        self.status = stat

    def get_status(self):
        return self.status


if __name__ == "__main__":
    robot1 = Robot([1, 1])
