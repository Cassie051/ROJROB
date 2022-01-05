from robot.robot import Robot
import random
from scene.map import Map


class Menager:
    def __init__(self, robot_number):
        self.robot_number = robot_number
        self.map_dimentions = 20, 20
        self.map = Map(self.map_dimentions[0], self.map_dimentions[1])
        self.init_map()
        self.robots = []
        self.start_possition = []
        self.aim = []
        self.generate_start_possition()
        self.generate_aim()
        self.generate_robots()
        self.init_robots()

    def init_robots(self):
        i = 0
        colors = ['m', 'y', 'g', 'r']
        for robot in self.robots:
            if i < len(colors):
                robot.set_color(colors[i])
            robot.find_path(self.aim[i], self.map)
            robot.set_status("Busy")
            i += 1

    def init_map(self):
        self.map.generate_map()

    def generate_start_possition(self):
        while len(self.start_possition) < self.robot_number:
            rand_x = random.randint(0, self.map_dimentions[0] - 1)
            rand_y = random.randint(0, self.map_dimentions[1] - 1)
            if any(x == rand_x for (x, _) in self.start_possition) and any(
                    y == rand_y for (_, y) in self.start_possition
            ):
                pass
            else:
                self.start_possition.append([rand_x, rand_y])

    def generate_aim(self):
        while len(self.aim) < self.robot_number:
            rand_x = random.randint(0, self.map_dimentions[0] - 1)
            rand_y = random.randint(0, self.map_dimentions[1] - 1)
            if any(x == rand_x for (x, _) in self.start_possition) and any(
                    y == rand_y for (_, y) in self.start_possition
            ):
                pass
            elif any(x == rand_x for (x, _) in self.aim) and any(
                    y == rand_y for (_, y) in self.aim
            ):
                pass
            elif any(x == rand_x for (x, _) in self.map.occupated_points()) and any(
                    y == rand_y for (_, y) in self.map.occupated_points()):
                pass
            else:
                self.aim.append([rand_x, rand_y])

    def generate_robots(self):
        for i in range(self.robot_number):
            self.robots.append(Robot(self.start_possition[i], "b"))
