import sys
from PyQt5.QtWidgets import QApplication

from game import GameApp

player = ""

def main():
    app = QApplication(sys.argv)
    ex = GameApp("b")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()