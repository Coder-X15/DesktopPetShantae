from PySide6 import QtWidgets, QtCore, QtGui 
import json
import sys
import random
import pathlib
import os
import joblib
from utils import preprocess
import numpy as np
from gensim.models import KeyedVectors
from pathlib import Path
import time

# == GLOBALS == #
EMBEDDING_SIZE = 100
wv = KeyedVectors.load(os.path.join(Path(__file__).resolve().parent, 'vectors.wordvectors'))
idx2class = ['butt_wiggle', 'chat', 'dance']
model = joblib.load(os.path.join(Path(__file__).resolve().parent, 'mlp.joblib'))


# == COMMON UTILS == #

def load_meta(path : str) -> dict[str, list]:
    ''' loads metadata fom json '''
    data = None
    with open(path, mode = 'r', encoding = 'utf-8') as fp:
        data = json.load(fp)
    return data

def sentence_embedding(sentence : str) -> np.ndarray:
    ''' generates sentence embeddings '''
    tokens = preprocess(sentence)
    result = np.zeros((EMBEDDING_SIZE,))
    for token in tokens:
        try:
            result = np.vstack(wv[token])
        except:
            result = np.vstack(np.zeros(result[0,:].shape))
    return result.sum(axis=1)

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
        self.intent = 'chat' # the initial intent
        self.chat_message_delay = 30 # the time limit for which the chat messages in the bubble will stay
        self.last_checked = time.time()
        self.butt_wiggle_dialogues = [
            "Bruhhhh!",
            "Eww, pervert! But I'll do this just for your happiness! >:(",
            "You couldv'e told me to dancee!!! Ughhhh never mind."
        ] # these dialogues will be rendered in the chat bubble before the butt-wiggle starts

        self.dance_dialogues = [
            "Yess I will!! Dance is what I was born for and what I will do!! :)",
            "Hehe why not? Enjoy my mesmerising shimmies and undulations!",
            "Of course! Here you go, hehe!! ;)",
        ] # these dialogues will be rendered in the chat bubble while dancing

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

        # construct the chat bubble widget
        self.chat_bubble = QtWidgets.QLabel(self)
        self.chat_bubble.setWordWrap(True)
        self.chat_bubble.setStyleSheet(
            '''
                QLabel {
                    background-color: #ffffff;
                    color: #222222;
                    border: 2px solid #333333;
                    border-radius: 12px;
                    padding: 8px 12px;
                    font-family: "Segoe UI", Arial, sans-serif;
                    font-size: 13px;
                    font-weight: 500;
                }
            '''
        )
        self.chat_bubble.setText("Hi! Shantae's back!!!")
        # define the layout (a 3x3 grid layout, for now) and add the widgets (including buttons)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.chat_bubble)
        self.layout.addWidget(self.gif_player)

        # add a textbox to chat
        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.returnPressed.connect(lambda : self.process_input(self.textbox.text()))
        self.layout.addWidget(self.textbox)
        

        # add exit button for convenience
        self.exit_button = QtWidgets.QPushButton("Exit")
        self.exit_button.clicked.connect(self.app_ref.exit)
        self.layout.addWidget(self.exit_button)
        self.setFixedSize(400, 450)

    def process_input(self, text: str):
        self.last_checked = time.time()
        self.textbox.clear()
        self.chat_bubble.show()
        embedding = sentence_embedding(text)
        embedding = embedding.reshape((1, embedding.shape[0]))
        idx = model.predict(embedding)[0]
        self.intent = idx2class[idx]
        if self.intent == 'butt_wiggle':
            self.chat_bubble.setText(random.choice(self.butt_wiggle_dialogues))
            self.play_butt_wiggle()
        elif self.intent == 'dance':
            self.chat_bubble.setText(random.choice(self.dance_dialogues))
            self.dance()
        else:
            self.chat_bubble.setText("Chat API hasnt been enabled as of now, dummy!")


    def next_animation(self):
        ''' sets the next animation according to the animation key and the GIF counter '''
        self.movie.stop()
        if self.gif_counter < self.counter_limits[self.current_animation]:
            self.gif_counter += 1
            if self.intent == 'chat' and (time.time()-self.last_checked) > 30:
                self.chat_bubble.hide()
            elif (time.time()-self.last_checked) > 3:
                self.chat_bubble.hide()
            if self.gif_counter >= self.counter_limits[self.current_animation]:
                self.gif_counter = 0
                self.current_animation = self.idle_animation_key
                self.intent = 'chat'
        self.movie.setFileName(self.gif_map[self.current_animation][self.gif_counter])
        self.movie.start()

    def play_butt_wiggle(self):
        self.movie.stop()
        self.gif_counter = 0
        self.current_animation = 'butt_wiggle'
        self.movie.setFileName(self.gif_map[self.current_animation][self.gif_counter])
        self.movie.start()

    def dance(self):
            self.movie.stop()
            self.gif_counter = 0
            self.current_animation = 'dancing'
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