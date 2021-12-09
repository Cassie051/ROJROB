import sys
import matplotlib
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.main_window import UiRojRob
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from robot import Robot

matplotlib.use("Qt5Agg")


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.timer = QtCore.QTimer()


class Scene(QtWidgets.QMainWindow):
    def __init__(self):
        self.ui = UiRojRob()
        self.sc = MplCanvas(self, width=10, height=10, dpi=100)
        self.robots = [Robot([1, 0], "b"), Robot([0, 1], "g")]
        self.aim = [[9, 8], [8, 9]]

    def plot_robot(self, robot):
        rec = matplotlib.pyplot.Circle(
            [robot.get_position()[0] + 0.5, robot.get_position()[1] + 0.5], 0.5
        )
        rec.set(color=robot.get_color())
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
            i += 1

    def plot(self, robot):
        self.plot_robot(robot)
        self.plot_path(robot.get_path(), robot.get_color() + "-")

    def set_up_plot(self):
        major_ticks = np.arange(0, 11, 1)
        self.sc.axes.axis([0, 10, 0, 10])
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
            if len(robot.get_path()) > 1:
                self.plot_robot(self.sc, robot)
                robot.set_position(robot.get_path()[1])
                robot_path = robot.get_path()
                self.plot_path(self.sc, robot_path, robot.get_color() + "-")
                del robot_path[0]
                robot.set_path(robot_path)
            elif len(robot.get_path()) == 1:
                self.plot_robot(self.sc, robot)
                robot_path = robot.get_path()
                del robot_path[0]
                robot.set_path(robot_path)
            else:
                self.plot_robot(self.sc, robot)
        self.set_up_plot()
        self.sc.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Scene()
    main.show()
    sys.exit(app.exec_())
