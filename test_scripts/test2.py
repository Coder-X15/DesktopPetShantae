import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class DancingWidget(QtWidgets.QWidget):
    def __init__(self, app_ref: QtWidgets.QApplication) -> None:

        # initialise window
        super().__init__()

        # make the window background transparent
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # load GIF
        self.app_ref = app_ref
        self.image = QtGui.QMovie('./actions/dancing/02.gif')
        self.image_display = QtWidgets.QLabel("dancer")

        self.image_display.setMovie(self.image)
        self.image.finished.connect(self.image.start)
        self.image.start()

        # set window layout
        self.layout = QtWidgets.QVBoxLayout(self)

        # add an exit button
        self.button = QtWidgets.QPushButton('Exit')
        self.button.clicked.connect(self.app_ref.exit)


        self.layout.addWidget(self.image_display)
        self.layout.addWidget(self.button)

    def mousePressEvent(self, event):
        # to enable mouse movement, detect an LMB press, move the window alongside it
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.windowHandle().startSystemMove()
        super().mousePressEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = DancingWidget(app)
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())