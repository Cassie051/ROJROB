from asyncio import tasks
import random
import json
from robot.robot import Robot
from scene.map import Map
from system.task import Tasks


class Menager:
    def __init__(self):
        self.robot_number = 0
        self.map_dimentions = 0, 0
        self.robots = []
        self.start_possition = []
        self.is_tasks_finish = []
        self.load_params("./config/scenario_1.json")
        self.generate_robots()
        self.get_aims()
        self.init_robots()
        self.print_world_info()

    def load_params(self, file_name):
        f = open(file_name)
        data = json.load(f)
        self.robot_number = data["robot"]["number"]
        if not data["robot"]["rand"]:
            for tuple in data["robot"]["start_possition"]:
                self.start_possition.append([tuple["x"], tuple["y"]])
                self.is_tasks_finish.append(False)
        else:
            self.generate_start_possition()
        dimensions = data["map"]["dimensions"]
        self.map_dimentions = dimensions["x"], dimensions["y"]
        self.map = Map(self.map_dimentions[0], self.map_dimentions[1])
        if not data["map"]["rand"]:
            self.map.load_map(data["map"]["grid"])
        else:
            self.init_map()
        self.is_tasks_rand = data["tasks"]["rand"]
        if not self.is_tasks_rand:
            self.tasks = Tasks()
            for tuple in data["tasks"]["move_to"]:
                self.tasks.put([tuple["x"], tuple["y"]])
        self.is_loading_point = data["tasks"]["is_loading_point"]
        if self.is_loading_point:
            self.loading_possition = []
            for tuple in data["tasks"]["take_from"]:
                self.loading_possition.append([tuple["x"], tuple["y"]])

    def init_robots(self):
        i = 0
        colors = ["m", "y", "g", "r"]
        for robot in self.robots:
            if i < len(colors):
                robot.set_color(colors[i])
            robot.find_path(self.aims[i], self.map)
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

    def get_aims(self):
        self.aims = []
        i = 0
        while len(self.aims) < self.robot_number:
            if self.is_tasks_rand:
                rand_x = random.randint(0, self.map_dimentions[0] - 1)
                rand_y = random.randint(0, self.map_dimentions[1] - 1)
                if any(x == rand_x for (x, _) in self.start_possition) and any(
                    y == rand_y for (_, y) in self.start_possition
                ):
                    pass
                elif any(x == rand_x for (x, _) in self.aims) and any(
                    y == rand_y for (_, y) in self.aims
                ):
                    pass
                elif any(x == rand_x for (x, _) in self.map.occupated_points()) and any(
                    y == rand_y for (_, y) in self.map.occupated_points()
                ):
                    pass
                else:
                    self.aims.append([rand_x, rand_y])
            else:
                if self.is_loading_point and not self.is_tasks_finish[i]:
                    x, y = self.loading_possition[i]
                    self.aims.append([x, y])
                else:
                    self.aims.append(self.tasks.get())
            i += 1

    def get_single_aim(self, robot_number):
        if self.is_tasks_rand:
            rand_x = random.randint(0, self.map_dimentions[0] - 1)
            rand_y = random.randint(0, self.map_dimentions[1] - 1)
            self.aims[robot_number] = [rand_x, rand_y]
            return rand_x, rand_y
        else:
            if self.is_loading_point and not self.is_tasks_finish[robot_number]:
                x, y = self.loading_possition[robot_number]
                self.is_tasks_finish[robot_number] = True
            else:
                x, y = self.tasks.get()
                self.is_tasks_finish[robot_number] = False
            self.aims[robot_number] = [x, y]
            return x, y

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
                    return True, another_robot.get_color(), i
                i += 1
        return False, None, None

    def halt_robot(self, color):
        for robot in self.robots:
            if robot.get_color() == color:
                return robot.set_status("Halt")

    def check_collisions(self):
        for robot in self.robots:
            collision = self.check_if_robot_path_is_free(robot)
            if collision[0] and 0 < collision[2] < 3:
                if self.get_robot_status(collision[1]) != "Halt":
                    robot.set_status("Halt")
            else:
                if robot.get_status() == "Halt":
                    robot.set_status("Busy")

    def set_robot_status(self, robot_number, status):
        if status == "Busy":
            new_x, new_y = self.get_single_aim(robot_number)
            self.robots[robot_number].find_path((new_x, new_y), self.map)
            self.robots[robot_number].set_status(status)
            self.print_robot_status(robot_number)
            print("------------------------")
        else:
            self.robots[robot_number].set_status(status)
            self.print_robot_status(robot_number)

    def print_world_info(self):
        print("Map size: ", self.map_dimentions)
        print("Number of robots: ", self.robot_number)
        print("------------------------")
        i = 0
        for robot in self.robots:
            print("Robot", i + 1)
            print("Starting possition:", self.start_possition[i])
            print("Aim:", self.aims[i])
            print("Robot status:", robot.get_status())
            i += 1
        print("------------------------")

    def print_robot_status(self, i):
        print("Robot", i + 1)
        print("Aim:", self.aims[i])
        print("Robot status:", self.robots[i].get_status())
