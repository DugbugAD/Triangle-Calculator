import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from home import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Futura")
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
