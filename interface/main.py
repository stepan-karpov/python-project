from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys

# def handle_click():


def application():
  app = QApplication(sys.argv)
  window = QMainWindow()

  window.setWindowTitle("jopa!")
  window.setGeometry(500, 500, 300, 300)

  label = QtWidgets.QLabel(window)
  label.setText("Current counter is: ")
  label.move(100, 100)
  label.adjustSize()

  btn = QtWidgets.QPushButton(window)
  btn.move(70, 150)
  btn.setText("Press on me!")
  btn.setFixedWidth(200)

  window.show()
  sys.exit(app.exec_())

if __name__ == "__main__":

  application()
