import socket
import struct
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QMainWindow, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import time
from multiprocessing.pool import ThreadPool
from collections import namedtuple

player1Color = "#FFFFFF"
player2Color = "#000000"

buttonClearText = "color: rgba(0,0,0,0); border-radius:38px"

bgInactive = "#268000"
bgActive = "#41de00"

player1port = 55555
player2port = 55556

cantMoveMsg = (8,8)

class App(QMainWindow):

    def __init__(self, player):
        super().__init__()
        self.title = "reversi"
        self.left = 100
        self.top = 100
        self.width = 650
        self.height = 650

        self.player1 = "w"
        self.player2 = "b"
        self.empty = " "

        self.selectedPlayer = player
        self.opponentPlayer = ""
        self.myPort = 0
        self.opponentPort = 0

        if(self.selectedPlayer == self.player1):
            self.opponentPlayer = self.player2
            self.myPort = player1port
            self.opponentPort = player2port
        else:
            self.opponentPlayer = self.player1
            self.myPort = player2port
            self.opponentPort = player1port

        self.iCanMove = True
        self.opponentCanMove = True
        
        self.initUI()

    def activePlayerColor(self):
        if self.selectedPlayer == self.player1:
            return player1Color

        if self.selectedPlayer == self.player2:
            return player2Color

    def getPlayerColor(self, player):
        if player == self.player1:
            return player1Color

        if player == self.player2:
            return player2Color
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.createGridLayout()
        self.setCentralWidget(self.GroupBox)
        self.resetBoard()
        self.show()
        self.firstMove()
        
    def createGridLayout(self):
        self.GroupBox = QGroupBox("Grid")
        self.GroupBox.setStyleSheet("color: rgba(0, 0, 0, 1); background-color:"+bgInactive)

        layout = QGridLayout()
        layout.setSpacing(0)

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
                self.setEmpty(x, y)
                
        self.setPiece(4, 4, self.player2)
        self.setPiece(3, 3, self.player2)
        self.setPiece(3, 4, self.player1)
        self.setPiece(4, 3, self.player1)


        ## to tylko do testow   
        for y in range(len(self.board)-1):
            for x in range(len(self.board[y])):
                if x % 2 == 0:
                    self.setPiece(x, y, self.player2)
                else:
                    self.setPiece(x, y, self.player1)

        

    def firstMove(self):
        if(self.selectedPlayer == self.player1):
            self.enablePossibleMoves(self.selectedPlayer)
        else:
            self.repaint()
            r = self.getMove()
            print("received move" + str(r))
            self.opponentsMove(r[0], r[1])
            self.enablePossibleMoves(self.selectedPlayer)

    def setEmpty(self, x, y):
        self.board[x][y].setText(self.empty)
        self.board[x][y].setStyleSheet("background-color: "+bgInactive)

    def setPiece(self, x, y, piece):
        self.board[x][y].setText(piece)
        self.board[x][y].setEnabled(False)

        self.board[x][y].setStyleSheet(buttonClearText+";background-color: " + self.getPlayerColor(piece))

    def reverse(self, piece):
        x = piece[0]
        y = piece[1]

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

    def enablePossibleMoves(self, player):
        possibleMovesCounter = 0
        #with self._key_lock:
        for y in range(8):
            for x in range(8):
                if self.board[x][y].text() == self.empty:
                    if len(self.getPiecesToReverse(x, y, player)) > 0:
                        self.board[x][y].setEnabled(True)
                        #print(40)
                        self.board[x][y].setStyleSheet("background-color: "+bgActive+"; border: 5px solid "+self.activePlayerColor())

                        possibleMovesCounter += 1
                    else:
                        self.board[x][y].setEnabled(False)
                        #print(50)
                        self.board[x][y].setStyleSheet("background-color: "+bgInactive)

                        
                else: 
                    self.board[x][y].setEnabled(False)

        return possibleMovesCounter

    def disableBoard(self):
        #with self._key_lock:
        for y in range(8):
            for x in range(8):
                if self.board[x][y].text() == self.empty:
                    self.board[x][y].setEnabled(False)
                    #print(60)
                    self.board[x][y].setStyleSheet("background-color: "+bgInactive)
                     

    def getScore(self):
        return "YOUR SCORE:" + str(self.countScore(self.selectedPlayer)) + " OPPONENT SCORE:" + str(self.countScore(self.opponentPlayer))

    def buttonPressed(self, x, y):
        possibleMoves = 0
        toReverse = self.getPiecesToReverse(x, y, self.selectedPlayer)
        
        if len(toReverse) > 0:
            self.setPiece(x, y, self.selectedPlayer)
            for piece in toReverse:
                self.reverse(piece)

            self.repaint()

            print("Sending your move to opponent..." + str(x) + "," + str(y))
            pos = struct.pack('ii', x, y)
            
            self.disableBoard()
            self.sendSocket(pos)
            print("Waiting for oponent's move...")
            self.GroupBox.setTitle(self.getScore() + " (Waiting for oponent's move)")
            self.repaint()
            r = self.getMove()
            print("received move" + str(r))
            self.opponentsMove(r[0], r[1])
            possibleMoves = self.enablePossibleMoves(self.selectedPlayer)
            self.repaint()
        
        while(possibleMoves == 0):
            #i cant move
            print(" ... i cant move, send msg ... ")
            print("Sending your move to opponent..." + str(cantMoveMsg[0]) + "," + str(cantMoveMsg[1]))
            pos = struct.pack('ii', cantMoveMsg[0], cantMoveMsg[1])
            #self.disableBoard()
            self.sendSocket(pos)

            if(self.opponentCanMove):
                print("Waiting for oponent's move...")
                self.GroupBox.setTitle(self.getScore() + " (Waiting for oponent's move)")
                self.repaint()
                r = self.getMove()
                print("received move" + str(r))

            if((r[0] == cantMoveMsg[0] and r[1] == cantMoveMsg[1] ) or not self.opponentCanMove) :
                #opponent also cant move, game over
                print("game over")
                self.GroupBox.setTitle("GAME OVER! - " + self.getScore())
                self.disableBoard()
                return
            else:
                self.opponentsMove(r[0], r[1])
                self.repaint()
                possibleMoves = self.enablePossibleMoves(self.selectedPlayer)
                self.repaint()
        
        print("Waiting for your move ...")
        self.GroupBox.setTitle(self.getScore() + " (Waiting for your move)")
            

        
            
    #odpowiednik buttonPressed ale dla przeciwnika
    def opponentsMove(self, x, y):
        toReverse = self.getPiecesToReverse(x, y, self.opponentPlayer)
        if toReverse.__len__() > 0:
            self.setPiece(x, y, self.opponentPlayer)
            for piece in toReverse:
                self.reverse(piece)
        else:
            print("received invalid move from opponent")



    def sendSocket(self, pos):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #print("Sending your move to opponent..." + str(pos[0]) + "," + str(pos[1]))

        while True:
            try:
                s.connect((socket.gethostname(), self.opponentPort))
                break
            except Exception as e:
                print(e.__cause__)
                pass
        
        
        s.send(pos)

        s.close()

    def getMove(self):
        print("Receiving opponent's move...")
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(self.receiveSocket)
        r = async_result.get()  
        if(r[0] == cantMoveMsg[0] and r[1] == cantMoveMsg[1] ):
            self.opponentCanMove = False
        else:
            self.opponentCanMove = True

        return r

    def receiveSocket(self):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind((socket.gethostname(), self.myPort))
        self.listener.listen()
        clientsocket, address = self.listener.accept()
        print(f"Connection {address} has been established.")

        new_pos = clientsocket.recv(1024)
        

        x, y = struct.unpack('ii', new_pos)
        print(str(x) + " " + str(y)) 

        clientsocket.close()
        return x, y

        #self.opponentsMove(x, y)