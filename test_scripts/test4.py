import sys
import os
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

        # load butt wiggle animations
        # print([file for file in os.walk('./actions/butt_wiggle/')])
        paths = []
        for root, dir, files in os.walk('./actions/butt_wiggle'):
            for file in files:
                paths.append(os.path.join(root, file))
        self.animation = sorted(paths)

        self.idle_animation = './actions/friendly_dialogue/01.gif'
        self.image = QtGui.QMovie(self.idle_animation)
        self.image_display = QtWidgets.QLabel("dancer")
        self.image_display.setMovie(self.image)
        self.image_display.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignBottom
        )
        self.image.finished.connect(self.playback_loop)
        self.image.start()
        self.animation_counter = 0

        # set window layout
        self.layout = QtWidgets.QGridLayout(self)

        # add an exit button
        self.button = QtWidgets.QPushButton('Exit')
        self.butt_wiggle = QtWidgets.QPushButton('Butt Wiggle')
        self.button.clicked.connect(self.app_ref.exit)
        self.butt_wiggle.clicked.connect(self.butt_wiggle_action)


        self.layout.addWidget(self.image_display, 0, 0, 0, 1)
        self.layout.addWidget(self.button, 1, 1)
        self.layout.addWidget(self.butt_wiggle, 1, 0)

    def mousePressEvent(self, event):
        # to enable mouse movement, detect an LMB press, move the window alongside it
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.windowHandle().startSystemMove()
        super().mousePressEvent(event)

    def playback_loop(self):
        self.image.stop()
        if self.animation_counter == 0:
            self.image.setFileName(self.idle_animation)
        elif self.animation_counter < len(self.animation):
            if self.animation_counter == 1:
                self.image_display.setAlignment(
                        QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignBottom
                    )
            self.image.setFileName(self.animation[self.animation_counter])
            self.animation_counter += 1
        else:
            self.animation_counter = 0
            self.image.setFileName(self.idle_animation)
        self.image.start()

    def butt_wiggle_action(self):
        self.image.stop()
        self.animation_counter = 1
        self.image.setFileName(self.animation[0])
        self.image.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = DancingWidget(app)
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())