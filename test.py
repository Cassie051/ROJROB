import sys
import matplotlib
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from MainWindow import Ui_RojRob
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from Robot import Robot

matplotlib.use('Qt5Agg')


def plot_robot(sc, robot):
    rec = matplotlib.pyplot.Circle([robot.get_position()[0]+0.5, robot.get_position()[1]+0.5], 0.5)
    rec.set(color=robot.get_color())
    sc.axes.add_artist(rec)


def plot_path(sc, path, color='r-'):
    x = []
    y = []
    for point in path:
        x.append(point[0] + 0.5)
        y.append(point[1] + 0.5)
    sc.axes.plot(x, y, color)


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        # build ui
        self.ui = Ui_RojRob()
        self.ui.setupUi(self)
        self.sc = MplCanvas(self, width=10, height=10, dpi=100)
        self.robots = [Robot([1, 0], 'b'), Robot([0, 1], 'g')]
        sc = self.sc
        robot1 = self.robots[0]
        robot2 = self.robots[1]
        robot1.find_path([9, 8])
        robot2.find_path([8, 9])
        plot_robot(sc, robot1)
        plot_robot(sc, robot2)
        plot_path(sc, robot1.get_path(), robot1.get_color() + '-')
        plot_path(sc, robot2.get_path(), robot2.get_color() + '-')
        sc.axes.axis([0, 10, 0, 10])
        major_ticks = np.arange(0, 11, 1)
        sc.axes.set_xticks(major_ticks)
        sc.axes.set_yticks(major_ticks)
        sc.axes.grid('both')
        sc.axes.set_aspect('equal')
        self.setCentralWidget(sc)
        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        self.sc.axes.cla()  # Clear the canvas.
        for robot in self.robots:
            if len(robot.get_path()) > 1:
                plot_robot(self.sc, robot)
                robot.set_position(robot.get_path()[1])
                robot_path = robot.get_path()
                plot_path(self.sc, robot_path, robot.get_color() + '-')
                del robot_path[0]
                robot.set_path(robot_path)
            elif len(robot.get_path()) == 1:
                plot_robot(self.sc, robot)
                robot_path = robot.get_path()
                del robot_path[0]
                robot.set_path(robot_path)
            else:
                plot_robot(self.sc, robot)
        self.sc.axes.axis([0, 10, 0, 10])
        major_ticks = np.arange(0, 11, 1)
        self.sc.axes.set_xticks(major_ticks)
        self.sc.axes.set_yticks(major_ticks)
        self.sc.axes.grid('both')
        self.sc.axes.set_aspect('equal')
        # Trigger the canvas to update and redraw.
        self.sc.draw()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
