from PySide6 import QtWidgets, QtCore, QtGui 
import json
import sys
import random
import pathlib
import os

# == COMMON UTILS == #

def load_meta(path : str) -> dict[str, list]:
    ''' loads metadata fom json '''
    data = None
    with open(path, mode = 'r', encoding = 'utf-8') as fp:
        data = json.load(fp)
    return data

# == CORE FUNCTIONAILITY == #

class ButtonControlledAssistant(QtWidgets.QWidget):

    ''' derived class for our pet widget '''
    def __init__(self,
                 app_ref : QtWidgets.QApplication,
                 metadata_path : str = f"{sys.argv[1]}.json", 
                 idle_animation_name : str = 'standing') -> None:
        ''' constructor '''
        super().__init__()

        # set transparent background settings
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.app_ref =  app_ref

        # set some internal variables for use
        self.idle_animation_key = idle_animation_name # the default animation to play
        self.gif_counter = 0 # counter to control animation choice
        self.current_animation = 'loading' # current animation pointer

        #loading the gifs using the metadata
        self.gif_map = load_meta(os.path.join(pathlib.Path(__file__).resolve().parent, metadata_path))
        self.animation_keys = list(self.gif_map.keys())

        # creating counter limits for each GIF
        self.counter_limits = {key : len(self.gif_map[key]) for key in self.gif_map}

        # construct a common label widget to place all GIFs at
        self.gif_player = QtWidgets.QLabel("player")
        self.gif_player.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignBottom)
        self.movie = QtGui.QMovie(self.gif_map[self.current_animation][0])

        # blit the idle animation onto the GIF player widget
        self.gif_player.setMovie(self.movie)
        self.movie.finished.connect(self.next_animation)
        self.movie.start()

        # define the layout (a 3x3 grid layout, for now) and add the widgets (including buttons)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.gif_player)

        # add a textbox for fun
        self.textbox = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.textbox)

        # add buttons
        self.animate_button = QtWidgets.QPushButton("Random animation")
        self.animate_button.clicked.connect(self.button_press_event)
        self.layout.addWidget(self.animate_button)

        self.exit_button = QtWidgets.QPushButton("Exit")
        self.exit_button.clicked.connect(self.app_ref.exit)
        self.layout.addWidget(self.exit_button)
        self.setFixedSize(400, 600)

    def next_animation(self):
        ''' sets the next animation according to the animation key and the GIF counter '''
        self.movie.stop()
        if self.gif_counter < self.counter_limits[self.current_animation]:
            self.gif_counter += 1
            if self.gif_counter >= self.counter_limits[self.current_animation]:
                self.gif_counter = 0
                self.current_animation = self.idle_animation_key
        self.movie.setFileName(self.gif_map[self.current_animation][self.gif_counter])
        self.movie.start()

    # @QtCore.Slot()
    def button_press_event(self) -> None:
        self.movie.stop()
        self.gif_counter = 0
        self.current_animation = random.choice(self.animation_keys)
        self.movie.setFileName(self.gif_map[self.current_animation][self.gif_counter])
        self.movie.start()


    def mousePressEvent(self, event) -> None:
        ''' enables dragging '''
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.windowHandle().startSystemMove()
        super().mousePressEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = ButtonControlledAssistant(app)
    widget.show()

    sys.exit(app.exec())