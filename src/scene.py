import sys
import matplotlib
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.main_window import UiRojRob
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from robot import Robot
from map import Map
from random import randrange

matplotlib.use("Qt5Agg")


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Scene(QtWidgets.QMainWindow):
    def __init__(self):
        super(Scene, self).__init__()
        self.ui = UiRojRob()
        self.map = Map(20, 20)
        self.sc = MplCanvas(self, width=self.map.x, height=self.map.y, dpi=100)
        self.start_possition = [[1, 0], [0, 1]]
        self.robots = [
            Robot(self.start_possition[0], "b"),
            Robot(self.start_possition[1], "g"),
        ]
        self.aim = [[19, 6], [8, 19]]
        self.timer = QtCore.QTimer()
        self.init_robots()
        self.set_up_plot()
        self.plot()
        self.set_up_timer()

    def plot_robot(self, robot):
        rec = matplotlib.pyplot.Circle(
            [robot.get_position()[0] + 0.5, robot.get_position()[1] + 0.5], 0.5
        )
        color = robot.get_color()
        if robot.get_status() == "Free":
            color = 'g'
        elif robot.get_status() == "Busy":
            color = 'r'
        rec.set(color=color)
        self.sc.axes.add_artist(rec)

    def plot_path(self, path, color="r-"):
        x = []
        y = []
        for point in path:
            x.append(point[0] + 0.5)
            y.append(point[1] + 0.5)
        self.sc.axes.plot(x, y, color)

    def init_robots(self):
        i = 0
        for robot in self.robots:
            robot.find_path(self.aim[i])
            robot.set_status("Busy")
            i += 1

    def plot(self):
        for robot in self.robots:
            self.plot_robot(robot)
            if len(robot.get_path()) > 1:
                self.plot_path(robot.get_path(), robot.get_color() + "-")

    def set_up_plot(self):
        major_ticks = np.arange(0, self.map.x+1, 1)
        self.sc.axes.axis([0, self.map.x, 0, self.map.y])
        self.sc.axes.set_xticks(major_ticks)
        self.sc.axes.set_yticks(major_ticks)
        self.sc.axes.grid("both")
        self.sc.axes.set_aspect("equal")
        self.setCentralWidget(self.sc)

    def set_up_timer(self):
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        self.sc.axes.cla()  # Clear the canvas.
        for robot in self.robots:
            robot.make_step()
            robot_path = robot.get_path()
            if len(robot_path) > 1:
                self.plot_path(robot_path, robot.get_color() + "-")
            elif len(robot_path) < 2:
                robot.set_status("Free")
            self.plot_robot(robot)
            if robot.get_status() == "Free":
                new_x, new_y = randrange(20), randrange(20)
                robot.find_path((new_x, new_y))
                robot.set_status("Busy")
        self.set_up_plot()
        self.sc.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    scene = Scene()
    scene.show()
    sys.exit(app.exec_())
