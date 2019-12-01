import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QMainWindow, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets, uic

class App(QMainWindow):

	def __init__(self):
		super().__init__()
		self.title = 'PyQt5'
		self.left = 10
		self.top = 10
		self.width = 320
		self.height = 100
		self.initUI()
		
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		
		self.createGridLayout()

		self.setCentralWidget(self.GroupBox)

		#self.board[4][4].setText("wololo")
		self.resetBoard()
		
		self.show()
		
	def createGridLayout(self):
		self.GroupBox = QGroupBox("Grid")
		layout = QGridLayout()
		#layout.setColumnStretch(1, 4)
		#layout.setColumnStretch(2, 4)
		self.board = []
		for y in range(8):
			temp = []
			for x in range(8):
				butt = QPushButton("x:"+str(x) +", y:"+ str(y))
				butt.clicked.connect(lambda: self.placePiece(x, y))
				temp.append(butt)
				layout.addWidget(butt,x,y)
			self.board.append(temp)
		
		self.GroupBox.setLayout(layout)

	def resetBoard(self):
		for y in range(len(self.board)):
			for x in range(len(self.board[y])):
				print("x:"+str(x) + ", y:" + str(y))
				#self.board[y][x].setEnabled(False)
				self.setEmpty(x, y)
				
		self.setBlack(4, 4)
		self.setBlack(3, 3)
		self.setWhite(3, 4)
		self.setWhite(4, 3)
			
	def setBlack(self, x, y):
		self.board[y][x].setText("X")

	def setWhite(self, x, y):
		self.board[y][x].setText("O")
	
	def setEmpty(self, x, y):
		self.board[y][x].setText(" ")

	def placePiece(self, x, y):
		self.setWhite(x, y)
		self.board[y][x].setEnabled(False)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())