from PyQt5 import QtCore, QtGui, QtWidgets

class UiRojRob(object):
    def setupUi(self, RojRob):
        RojRob.setObjectName("RojRob")
        RojRob.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(RojRob)
        self.centralwidget.setObjectName("centralwidget")
        RojRob.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RojRob)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        RojRob.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RojRob)
        self.statusbar.setObjectName("statusbar")
        RojRob.setStatusBar(self.statusbar)

        self.retranslateUi(RojRob)
        QtCore.QMetaObject.connectSlotsByName(RojRob)

    def retranslateUi(self, RojRob):
        _translate = QtCore.QCoreApplication.translate
        RojRob.setWindowTitle(_translate("RojRob", "MainWindow"))