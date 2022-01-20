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

    def get_robot_status(self, color):
        for robot in self.robots:
            if robot.get_color() == color:
                return robot.get_status()

    def check_if_robot_path_is_free(self, robot):
        rest_of_robots = self.robots.copy()
        rest_of_robots.remove(robot)
        for another_robot in rest_of_robots:
            robot_path = robot.get_path()
            another_robot_path = another_robot.get_path()
            i = 0
            for point in robot_path:
                if point in another_robot_path:
                    j = 0
                    for second_point in another_robot_path:
                        if second_point  in robot_path:
                            break
                        j += 1
                    # print("Collision with ", another_robot.get_color(), " in ", i, "steps!", " Point: ", point)
                    # print(another_robot.get_color(), "has ", j ,"steps to collision!")
                    return True, another_robot.get_color(), i, j
                i += 1
        # print(robot.get_color(), " is free to go")
        return False, None, None

    def halt_robot(self, color):
        for robot in self.robots:
            if robot.get_color() == color:
                return robot.set_status("Halt")

    def check_collisions(self):
        # print("\n--------------------------------")
        for robot in self.robots:
            collision = self.check_if_robot_path_is_free(robot)
            if collision[0] and 0 < collision[2] < 3:
                if self.get_robot_status(collision[1]) != "Halt":
                    if collision[3] > collision[2]:
                        self.halt_robot(collision[1])
                    else:
                        robot.set_status("Halt")
            else:
                if robot.get_status() == "Halt":
                    robot.set_status("Busy")
