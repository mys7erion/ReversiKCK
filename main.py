import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QMainWindow, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from collections import namedtuple
Point = namedtuple("point", ["x", "y"])


player1Color = "#FFFFFF"
player2Color = "#000000"

buttonClearText = "color: rgba(0,0,0,0); border-radius:38px"

bgInactive = "#268000"
bgActive = "#41de00"


class App(QMainWindow):

	def __init__(self):
		super().__init__()
		self.title = "reversi"
		self.left = 100
		self.top = 100
		self.width = 650
		self.height = 650

		self.player1 = "O"
		self.player1canMove = True
		self.player2 = "X"
		self.player2canMove = True
		self.empty = " "

		self.activePlayer = self.player1
		self.initUI()

	def activePlayerColor(self):
		if self.activePlayer == self.player1:
			return player1Color

		if self.activePlayer == self.player2:
			return player2Color
		
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setFixedSize(self.width, self.height)

		
		self.createGridLayout()

		self.setCentralWidget(self.GroupBox)

		#self.board[4][4].setText("wololo")
		self.resetBoard()
		
		self.show()
		
	def createGridLayout(self):
		self.GroupBox = QGroupBox("Grid")
		self.GroupBox.setStyleSheet("color: rgba(0, 0, 0, 1); background-color:"+bgInactive)

		self.GroupBox.setTitle("ACTIVE PLAYER : " + self.activePlayer)

		layout = QGridLayout()
		layout.setSpacing(0)
		#layout.setColumnStretch(1, 4)
		#layout.setColumnStretch(2, 4)

		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)

		self.board = []
		for y in range(8):
			temp = []
			for x in range(8):
				butt = QPushButton(str(x) +" "+ str(y))
				sizePolicy.setHeightForWidth(butt.sizePolicy().hasHeightForWidth())
				butt.setSizePolicy(sizePolicy)
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
				
		self.setPiece(4, 4, self.player2)
		self.setPiece(3, 3, self.player2)
		self.setPiece(3, 4, self.player1)
		self.setPiece(4, 3, self.player1)
		self.enablePossibleMoves()

	def setEmpty(self, x, y):
		self.board[x][y].setText(self.empty)
		self.board[x][y].setStyleSheet("background-color: "+bgInactive)
		#self.board[x][y].setEnabled(False)


	def setPiece(self, x, y, piece):
		self.board[x][y].setText(piece)
		self.board[x][y].setEnabled(False)
		if piece == self.player1:
			self.board[x][y].setStyleSheet(buttonClearText+";background-color: "+player1Color)
		if piece == self.player2:
			self.board[x][y].setStyleSheet(buttonClearText+";background-color: "+player2Color)

		#print(self.board)

	def reverse(self, piece):
		x = piece[0]
		y = piece[1]

		#print("reversing: " + str(x) + "," + str(y))

		if self.board[x][y].text() == self.player2:
			self.setPiece(x, y, self.player1)
		elif self.board[x][y].text() == self.player1:
			self.setPiece(x, y, self.player2)


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
						self.board[x][y].setStyleSheet("background-color: "+bgActive+"; border: 5px solid "+self.activePlayerColor())

						possibleMovesCounter += 1
					else:
						self.board[x][y].setEnabled(False)
						self.board[x][y].setStyleSheet("background-color: "+bgInactive)

						
				else:
					self.board[x][y].setEnabled(False)
		return possibleMovesCounter
	
	def changePlayer(self):
		if self.activePlayer == self.player1:
			self.activePlayer = self.player2
		else:
			self.activePlayer = self.player1



		if self.enablePossibleMoves() == 0:
			if self.activePlayer == self.player1:
				self.player1canMove = False
				if self.player2canMove :
					self.changePlayer()
					return
				else:
					print("game over")
					return
			if self.activePlayer == self.player2:
				self.player2canMove = False
				if self.player1canMove :
					self.changePlayer()
					return
				else:
					print("game over")
					return
		else:
			if self.activePlayer == self.player1:
				self.player1canMove = True
			if self.activePlayer == self.player2:
				self.player2canMove = True

		print("ACTIVE PLAYER : " + self.activePlayer)

		player1Score = self.countScore(self.player1)
		player2Score = self.countScore(self.player2)

		self.GroupBox.setTitle("ACTIVE PLAYER : " + self.activePlayer +"; SCORES: "+self.player1+"-"+str(player1Score)+"; "+self.player2+"-"+str(player2Score)+"")

		# player has no legit moves to do , change player again
		




	def buttonPressed(self, x, y):
		#print("button "+ str(x) + "_" + str(y) + " clicked!")
		
		toReverse = self.getPiecesToReverse(x, y, self.activePlayer)
		if toReverse.__len__() > 0:

			self.setPiece(x,y,self.activePlayer)

			for piece in toReverse:
				self.reverse(piece)
			
			self.changePlayer()



if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())