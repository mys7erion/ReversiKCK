import sys
from PyQt5.QtWidgets import QApplication

from game import App

player = ""

def main():
    app = QApplication(sys.argv)
    ex = App("w")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()