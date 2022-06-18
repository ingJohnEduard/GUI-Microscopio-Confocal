

from PySide6 import QtCore, QtGui, QtWidgets


class Ui_SplashScreen(object):
    def setupUi(self, SplashScreen):
        SplashScreen.setObjectName("SplashScreen")
        SplashScreen.setWindowIcon(QtGui.QIcon("/logo1.ico"))#C:/Users/John E/Documents/Microscopio_Confocal/Microscopio_Confocal_V1.0/
        SplashScreen.resize(300, 300)
        SplashScreen.setMinimumSize(QtCore.QSize(300, 300))
        SplashScreen.setMaximumSize(QtCore.QSize(300, 300))
        self.centralwidget = QtWidgets.QWidget(SplashScreen)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.container = QtWidgets.QFrame(self.centralwidget)
        self.container.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.container.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.container.setObjectName("container")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.container)
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.circle_bg = QtWidgets.QFrame(self.container)
        self.circle_bg.setStyleSheet("QFrame{\n"
"        background-color: #44475a;\n"
"        color: #f8f8f2;\n"
"        border-radius: 120px;\n"
"        font: 14pt \"Bahnschrift SemiBold;\";\n"
"}")
        self.circle_bg.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.circle_bg.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.circle_bg.setObjectName("circle_bg")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.circle_bg)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.text = QtWidgets.QFrame(self.circle_bg)
        self.text.setMaximumSize(QtCore.QSize(16777215, 160))
        self.text.setStyleSheet("background: none;")
        self.text.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.text.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.text.setObjectName("text")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.text)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.loading = QtWidgets.QLabel(self.text)
        self.loading.setMaximumSize(QtCore.QSize(16777215, 30))
        self.loading.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.loading.setObjectName("loading")
        self.loading.setStyleSheet("QFrame{\n"
"    color: #bd93f9;\n"
"}")
        self.gridLayout.addWidget(self.loading, 2, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.text)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.version = QtWidgets.QLabel(self.frame)
        self.version.setMinimumSize(QtCore.QSize(100, 24))
        self.version.setMaximumSize(QtCore.QSize(100, 24))
        self.version.setStyleSheet("QFrame{\n"
"    color: #bd93f9;\n"
"    background-color: #282a36;\n"
"    border-radius: 12px;\n"
"}")
        self.version.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.version.setObjectName("version")
        self.verticalLayout_5.addWidget(self.version, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.text)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 10))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.title = QtWidgets.QLabel(self.frame_2)
        self.title.setGeometry(QtCore.QRect(0, 0, 238, 45))
        self.title.setMinimumSize(QtCore.QSize(0, 30))
        self.title.setMaximumSize(QtCore.QSize(16777215, 70))
        self.title.setStyleSheet("QFrame{\n"
"    color: #bd93f9;\n"
"}")
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setObjectName("title")
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.verticalLayout_3.addWidget(self.text)
        self.verticalLayout_2.addWidget(self.circle_bg)
        self.verticalLayout.addWidget(self.container)
        SplashScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(SplashScreen)
        QtCore.QMetaObject.connectSlotsByName(SplashScreen)

    def retranslateUi(self, SplashScreen):
        _translate = QtCore.QCoreApplication.translate
        SplashScreen.setWindowTitle(_translate("SplashScreen", "Loading..."))
        self.loading.setText(_translate("SplashScreen", "Cargando..."))
        self.version.setText(_translate("SplashScreen", "v1.5.1"))
        self.title.setText(_translate("SplashScreen", "Microscopio Confocal"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SplashScreen = QtWidgets.QMainWindow()
    ui = Ui_SplashScreen()
    ui.setupUi(SplashScreen)
    SplashScreen.show()
    sys.exit(app.exec())
