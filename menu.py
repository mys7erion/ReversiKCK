from PyQt5 import QtCore, QtGui, QtWidgets
from game import GameApp

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.window = MainWindow

        MainWindow.setObjectName("Reversi")
        MainWindow.resize(316, 293)
        MainWindow.setStyleSheet("background-color: rgb(42, 42, 42);\n"
"color: rgb(222, 222, 222);\n"
"font: 25 14pt \"Calibri Light\";")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setToolTip("")
        self.lineEdit.setToolTipDuration(-1)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 1, 1, 3)
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout.addWidget(self.radioButton_2, 1, 3, 1, 1)
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout.addWidget(self.radioButton, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(3)
        self.label.setFont(font)
        self.label.setStyleSheet("font: 25 26pt \"Calibri Light\";\n"
"")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 3, QtCore.Qt.AlignHCenter)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setDefault(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 4, 1, 1, 3)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.setupActions()

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Reversi"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "write your nick here"))
        self.radioButton_2.setText(_translate("MainWindow", "Black"))
        self.radioButton.setText(_translate("MainWindow", "White"))
        self.label.setText(_translate("MainWindow", "Reversi"))
        self.pushButton_2.setText(_translate("MainWindow", "Play!"))

    def setupActions(self):
        self.pushButton_2.clicked.connect(lambda: self.start())

    def exit(self):
        self.window.close()
        

    def start(self):
        print("start")
        nick = self.lineEdit.text()

        if(self.radioButton.isChecked() == True):
            #start as white
            print("starting game as white, nick = " + nick)
            executeGame = GameApp("w", nick)

        if(self.radioButton_2.isChecked() == True):
            #start as black
            print("starting game as black, nick = " + nick)
            executeGame = GameApp("b", nick)

        self.exit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
