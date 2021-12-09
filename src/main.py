import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from scene import Scene


def main():
    app = QtWidgets.QApplication(sys.argv)
    scene = Scene()
    scene.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
