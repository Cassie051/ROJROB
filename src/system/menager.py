import random
import json
from robot.robot import Robot
from scene.map import Map


class Menager:
    def __init__(self, robot_number):
        self.robot_number = 0
        self.map_dimentions = 0, 0
        self.load_params('../config/scenario_1.json')
        self.robots = []
        self.start_possition = []
        self.generate_start_possition()
        self.generate_aim()
        self.generate_robots()
        self.init_robots()
        self.print_world_info()

    def load_params(self, file_name):
        f = open(file_name)
        data = json.load(f)
        self.robot_number = data["robot"]["number"]
        dimensions = data["map"]["dimensions"]
        self.map_dimentions = dimensions["x"], dimensions["y"]
        self.map = Map(self.map_dimentions[0], self.map_dimentions[1])
        if(data["map"]["rand"]):
            self.map.load_map(data["map"]["grid"])
        else:
            self.init_map()

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
        self.aim = []
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

    def generate_single_aim(self, robot_number):
        rand_x = random.randint(0, self.map_dimentions[0] - 1)
        rand_y = random.randint(0, self.map_dimentions[1] - 1)
        self.aim[robot_number] = [rand_x, rand_y]
        return rand_x, rand_y

    def generate_robots(self):
        for i in range(self.robot_number):
            self.robots.append(Robot(self.start_possition[i], "b"))

    def set_robot_status(self, robot_number, status):
        if status == "Busy":
            new_x, new_y = self.generate_single_aim(robot_number)
            self.robots[robot_number].find_path((new_x, new_y), self.map)
            self.robots[robot_number].set_status(status)
            self.print_robot_status(robot_number)
            print('------------------------')
        else:
            self.robots[robot_number].set_status(status)
            self.print_robot_status(robot_number)

    def print_world_info(self):
        print('Map size: ', self.map_dimentions)
        print('Number of robots: ', self.robot_number)
        print('------------------------')
        i = 0
        for robot in self.robots:
            print('Robot', i+1)
            print('Starting possition:', self.start_possition[i])
            print('Aim:', self.aim[i])
            print('Robot status:', robot.get_status())
            i += 1
        print('------------------------')

    def print_robot_status(self, i):
        print('Robot', i+1)
        print('Aim:', self.aim[i])
        print('Robot status:', self.robots[i].get_status())
