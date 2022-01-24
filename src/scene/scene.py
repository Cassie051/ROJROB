import sys
import matplotlib
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.main_window import UiRojRob
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from system.menager import Menager

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
        self.menager = Menager()
        self.robots = self.menager.robots
        self.map = self.menager.map
        self.sc = MplCanvas(self, width=self.map.x, height=self.map.y, dpi=100)
        self.timer = QtCore.QTimer()
        self.set_up_plot()
        self.plot()
        self.set_up_timer()

    def plot_robot(self, robot):
        rob = matplotlib.pyplot.Circle(
            [robot.get_position()[0] + 0.5, robot.get_position()[1] + 0.5], 0.3
        )
        status_circle = matplotlib.pyplot.Circle(
            [robot.get_position()[0] + 0.5, robot.get_position()[1] + 0.5], 0.5
        )
        color = robot.get_color()
        if robot.get_status() == "Free":
            color = 'g'
        elif robot.get_status() == "Busy":
            color = 'r'
        elif robot.get_status() == "Halt":
            color = 'k'
        rob.set(color=robot.get_color())
        status_circle.set(color=color)
        self.sc.axes.add_artist(status_circle)
        self.sc.axes.add_artist(rob)

    def plot_obstacles(self):
        obstacles_xy = self.map.occupated_points()
        for obstacle_xy in obstacles_xy:
            rec = matplotlib.pyplot.Rectangle(
                [obstacle_xy[0], obstacle_xy[1]], 1, 1
            )
            color = 'black'
            rec.set(color=color)
            rec.set(fill=True)
            self.sc.axes.add_artist(rec)

    def plot_path(self, path, color="r-"):
        x = []
        y = []
        for point in path:
            x.append(point[0] + 0.5)
            y.append(point[1] + 0.5)
        self.sc.axes.plot(x, y, color)

    def plot(self):
        self.plot_obstacles()
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

    def check_status(self):
        i = 0
        self.menager.check_collisions()
        for robot in self.robots:
            if robot.get_status() != "Halt":
                robot.make_step()
            robot_path = robot.get_path()
            if len(robot_path) > 1:
                self.plot_path(robot_path, robot.get_color() + "-")
            elif len(robot_path) < 2:
                self.menager.set_robot_status(i, "Free")
            self.plot_robot(robot)
            if robot.get_status() == "Free":
                if(not self.menager.tasks.empty()):
                    self.menager.set_robot_status(i, "Busy")
                else:
                    self.menager.set_robot_status(i, "Free")
            i += 1
        self.set_up_plot()

    def update_plot(self):
        self.sc.axes.cla()
        self.plot_obstacles()
        self.check_status()
        self.sc.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    scene = Scene()
    scene.show()
    sys.exit(app.exec_())
