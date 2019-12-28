import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QMainWindow, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from collections import namedtuple
Point = namedtuple("point", ["x", "y"])


class App(QMainWindow):

	def __init__(self):
		super().__init__()
		self.title = "reversi"
		self.left = 100
		self.top = 100
		self.width = 320
		self.height = 100

		self.player1 = "O"
		self.player2 = "X"
		self.empty = " "

		self.activePlayer = self.player1
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

		self.GroupBox.setTitle("ACTIVE PLAYER : " + self.activePlayer)

		layout = QGridLayout()
		#layout.setColumnStretch(1, 4)
		#layout.setColumnStretch(2, 4)
		self.board = []
		for y in range(8):
			temp = []
			for x in range(8):
				butt = QPushButton(str(x) +" "+ str(y))
				butt.clicked.connect(lambda B=butt,Y=y,X=x: self.buttonPressed(Y,X))
				temp.append(butt)
				layout.addWidget(butt,x,y)
			self.board.append(temp)
		
		self.GroupBox.setLayout(layout)

	def countScore(self, player):
		score = 0
		for y in range(8):
			for x in range(8):
				if self.board[x][y].text() == player:
					score += 1
		return score

	def resetBoard(self):
		for y in range(len(self.board)):
			for x in range(len(self.board[y])):
				#self.board[x][y].setText("x:"+str(x) + ", y:" + str(y))
				#self.board[y][x].setEnabled(False)
				self.setEmpty(x, y)
				
		self.setPlayer2(4, 4)
		self.setPlayer2(3, 3)
		self.setPlayer1(3, 4)
		self.setPlayer1(4, 3)
		self.enablePossibleMoves()
			
	def setPlayer2(self, x, y):
		self.board[x][y].setText(self.player2)
		self.board[x][y].setEnabled(False)

	def setPlayer1(self, x, y):
		self.board[x][y].setText(self.player1)
		self.board[x][y].setEnabled(False)
	
	def setEmpty(self, x, y):
		self.board[x][y].setText(self.empty)
		self.board[x][y].setEnabled(True)

	def setPiece(self, x, y, piece):
		self.board[x][y].setText(piece)
		self.board[x][y].setEnabled(False)
		#print(self.board)

	def reverse(self, piece):
		x = piece[0]
		y = piece[1]

		#print("reversing: " + str(x) + "," + str(y))

		if self.board[x][y].text() == self.player2:
			self.board[x][y].setText(self.player1)
		elif self.board[x][y].text() == self.player1:
			self.board[x][y].setText(self.player2)


	def checkPiece(self, x, y):
		return self.board[x][y].text()

	def checkPiece(self, piece):
		return self.board[piece[0]][piece[1]].text()

	def checkIfValidPieceCoordinates(self, piece):
		if piece[0] >= 0 and piece[0] <= 7 and piece[1] >= 0 and piece[1] <= 7 :
			return True
		else:
			return False

	def getPiecesToReverse(self, x, y, player):
		#d - directions where to check for possible pieces to reverse (8 directions)
		
		directions = [(0,-1), (-1,-1), (-1,0), (-1,1), (0,1), (1, 1), (1, 0), (1, -1)]
		#list of pieces to reverse
		toReverse = []
		#starting point (placed piece)
		start = (x, y)

		for d in directions :
			tempToReverse = []
			piece = list(start)
		
			#while checked piece is in board
			while True:
				piece[0] += d[0]
				piece[1] += d[1]
				if self.checkIfValidPieceCoordinates(piece) == False:
					break

				checkedPiece = self.checkPiece(piece)

				#print("checking piece: " + str(piece[0]) +","+ str(piece[1]) + " : " + str(checkedPiece))
				# if next piece in direction is empty, break and continue to check next dirextion
				if checkedPiece == self.empty:
					#print("break")
					break
				#opponent piece, add to list to be reversed
				elif checkedPiece != player :
					#print("append")
					tempToReverse.append(list(piece))
					continue
				#player piece, break loop
				elif checkedPiece == player : 
					#print("end checking")
					for p in tempToReverse:
						#print("appending to reverse: " + str(p))
						toReverse.append(p)
					break


		return toReverse
		
		#for piece in toReverse:
		#	self.reverse(piece)

	def enablePossibleMoves(self):
		possibleMovesCounter = 0
		for y in range(8):
			for x in range(8):
				if self.board[x][y].text() == self.empty:
					if len(self.getPiecesToReverse(x, y, self.activePlayer)) > 0:
						self.board[x][y].setEnabled(True)
						possibleMovesCounter += 1
					else:
						self.board[x][y].setEnabled(False)
				else:
					self.board[x][y].setEnabled(False)
				
	
		


	def buttonPressed(self, x, y):
		#print("button "+ str(x) + "_" + str(y) + " clicked!")
		
		toReverse = self.getPiecesToReverse(x, y, self.activePlayer)
		if toReverse.__len__() > 0:

			self.setPiece(x,y,self.activePlayer)

			for piece in toReverse:
				self.reverse(piece)

			if self.activePlayer == self.player1:
				self.activePlayer = self.player2
			else:
				self.activePlayer = self.player1

			#print("ACTIVE PLAYER : " + self.activePlayer)

			player1Score = self.countScore(self.player1)
			player2Score = self.countScore(self.player2)

			self.GroupBox.setTitle("ACTIVE PLAYER : " + self.activePlayer +"; SCORES: "+self.player1+"-"+str(player1Score)+"; "+self.player2+"-"+str(player2Score)+"")

			self.enablePossibleMoves()
				
			
		


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())