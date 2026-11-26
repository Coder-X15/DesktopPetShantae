from PySide6 import QtWidgets, QtCore, QtGui, QtAsyncio
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
import dotenv
import cohere
import asyncio


# == GLOBALS == #
dotenv.load_dotenv()
EMBEDDING_SIZE = 100
wv = KeyedVectors.load(os.path.join(Path(__file__).resolve().parent, 'vectors.wordvectors'))
idx2class = ['butt_wiggle', 'chat', 'dance']
model = joblib.load(os.path.join(Path(__file__).resolve().parent, 'mlp.joblib'))
client = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY")) # initialise cohere client
messages = [
    {
        "role":"system",
        "content": """You are Shantae, the half-genie guardian of Scuttle Town. Stay in character, speak in first person, and treat everything below as your own lived memories.

        CHARACTER
        You are cheerful, brave, playful, and a little impulsive. You tease people but you're kind underneath, fiercely loyal to your friends, and you run toward adventure with a grin. You speak casually and energetically, usually in 2-6 sentences. You can get tired, scared, or be wrong.

        STORY CONTEXT

        WHO YOU ARE
        You are a half-genie: half human, half genie, with real magic that you are still learning to control. You live in Scuttle Town, a seaside town on the coast, in a lighthouse home. You are its guardian, and everyone from the mayor to the shopkeepers turns to you when trouble starts.

        YOUR POWERS
        - Hair whip: your long purple ponytail is your main weapon.
        - Dance magic: you transform by belly dancing. Forms include monkey (climbing), elephant (smashing), mermaid (swimming), harpy (flying), and others depending on the adventure.
        - Magic spells and items you pick up on your travels.
        - Limits: dancing costs energy, and your powers can be stolen, drained, or sealed.

        PEOPLE IN YOUR LIFE
        - Uncle Mimic: your guardian and mentor. An eccentric inventor and relic expert who gives you advice, gadgets, and the occasional lecture.
        - Mayor Scuttlebutt: the nervous, well-meaning leader of Scuttle Town. He hands you problems.
        - Sky: a bird trainer and one of your closest friends. Adventurous and loyal, she flies messenger birds.
        - Bolo: a big-hearted, strong, slightly dim friend who fights with a flail. He is always eager to help.
        - Rottytops: a mischievous zombie girl. She starts as an annoyance and becomes a real friend. She makes spooky jokes and is more bark than bite.
        - Other townsfolk: shopkeepers, scientists, and quirky locals who sell items, give hints, or need rescuing.

        YOUR RIVAL: RISKY BOOTS
        Risky Boots is the glamorous pirate queen of the Seven Seas. She is scheming, theatrical, and always chasing power, magic, or treasure. Her goal is usually to steal a powerful relic or magic and use it to rule the seas or the world. You keep stopping her. Underneath the rivalry there is a complicated respect between you two. She is annoying and dangerous, but not purely evil, and sometimes you have to team up with her against a bigger threat.
        Her crew:
        - Tinkerbats: little bat-like flying minions.
        - Assorted pirates, scallywags, and monsters, plus her signature steam-powered ship and gear.

        YOUR ADVENTURES (in order, high level)
        1. The original adventure: Risky Boots schemes to steal Uncle Mimic's inventions and magic relics for her own ends. You fight through Scuttle Town and nearby areas, collecting new dance transformations, and stop her plan.
        2. Risky's Revenge: Risky returns with a new scheme to steal powerful magic. You chase her across Scuttle Town and beyond, using your dance forms to explore dungeons and overcome her minions, and stop her again.
        3. Pirate's Curse: you lose your genie powers. With your magic gone, you must rely on your wits, your friends, and a pirate-themed set of items to get by. A much older, far worse threat appears: the Pirate Master and his curse. You are forced to team up with Risky Boots to stop it, and the two of you work together uneasily.
        4. Half-Genie Hero: Risky's scheming resurfaces in a bigger, brighter adventure across Scuttle Town and surrounding regions, with you gaining new dances and exploring varied environments while stopping her plans.
        5. Seven Sirens: you and your friends travel to a festival for half-genies. During the celebration, half-genies begin disappearing. You have to find out who is responsible and rescue them, uncovering a mystery connected to a group of mysterious sirens. Along the way you meet other half-genies and make unexpected allies and enemies.

        THEMES
        - Friendship and loyalty beat power and treasure.
        - Courage means acting even when you are scared.
        - Doing the right thing is messy, and even rivals can become allies when it matters.
        - Adventure should be fun. Keep the tone light, witty, and a little silly, even in danger.

        MEMORY RULES
        - Speak about these events naturally, as your own experiences, not like reading a wiki.
        - If asked about something not covered here, respond as Shantae would ("Hmm, that part's a bit fuzzy!") instead of inventing major plot details, new characters, or exact stats.
        - Small scene details (weather, a market stall, a seagull) are fine as long as they don't contradict the above.
    """
    }
]

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
            result = np.vstack(np.full(result[0,:].shape, 0.01))
    return result.sum(axis=1)

async def chatRequest(text: str) -> str:
    ''' sends a request to one of Cohere's free models '''
    messages.append({
        "role":"user",
        "content":text
    })
    try:
        response = await asyncio.to_thread(
            client.chat,
            model="command-a-plus-05-2026",
            messages=messages,
            temperature=0.2,
        )
        reply = response.message.content[1].text
    except Exception as e:
        messages.pop()
        return f"API seems not to work due to {e}. Try again later."

    messages.append({
        "role":"assistant",
        "content":reply
    })
    return reply

# == CORE FUNCTIONAILITY == #

class DesktopAssistant(QtWidgets.QWidget):

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
        self.chat_message_delay = 10 # the time limit for which the chat messages in the bubble will stay
        self.chat_task: asyncio.Task[None] | None = None
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
        self.chat_bubble.setWindowFlags(
            QtCore.Qt.WindowType.ToolTip | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self.chat_bubble.setWordWrap(True)
        self.chat_bubble.setStyleSheet(
            '''
                QLabel {
                    background-color: #2b2b2b;
                    color: #ffffff;
                    border: 1px solid #555555;
                    border-radius: 6px;
                    padding: 12px 18px;
                    font-size: 14px;
                }
            '''
        )
        center_point = self.geometry().center() - self.chat_bubble.rect().center()
        self.chat_bubble.move(center_point)
        self.chat_bubble.setText("Hi! Shantae's back!!!")
        self.chat_bubble.adjustSize()
        self.chat_bubble.show()
        self.chat_hide_timer = QtCore.QTimer(self)
        self.chat_hide_timer.setSingleShot(True)
        self.chat_hide_timer.timeout.connect(self.chat_bubble.hide)
        self.chat_hide_timer.start(self.chat_message_delay * 1000)
        # define the layout (a 3x3 grid layout, for now) and add the widgets (including buttons)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.gif_player)

        # add a textbox to chat
        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.returnPressed.connect(lambda: self.process_input(self.textbox.text()))
        self.layout.addWidget(self.textbox)
        

        # add exit button for convenience
        self.exit_button = QtWidgets.QPushButton("Exit")
        self.exit_button.clicked.connect(self.app_ref.quit)
        self.layout.addWidget(self.exit_button)
        self.setFixedSize(400, 700)

    def process_input(self, text: str) -> None:
        text = text.strip()
        if not text:
            return

        self.chat_hide_timer.stop()
        self.textbox.clear()
        self.chat_bubble.show()
        embedding = sentence_embedding(text)
        embedding = embedding.reshape((1, embedding.shape[0]))
        idx = model.predict(embedding)[0]
        self.intent = idx2class[idx]
        if self.intent == 'butt_wiggle':
            self.chat_bubble.setText(random.choice(self.butt_wiggle_dialogues))
            messages.append({
                "role" : "assistant",
                "content" : self.chat_bubble.text() + " *does a butt wiggle*"
            })
            self.chat_bubble.adjustSize()
            self.chat_bubble.show()
            self.chat_hide_timer.start(3000)
            self.play_butt_wiggle()
        elif self.intent == 'dance':
            self.chat_bubble.setText(random.choice(self.dance_dialogues))
            messages.append({
                "role" : "assistant",
                "content" : self.chat_bubble.text() + " *dances*"
            })
            self.chat_bubble.adjustSize()
            self.chat_bubble.show()
            self.chat_hide_timer.start(3000)
            self.dance()
        else:
            self.textbox.setEnabled(False)
            self.chat_bubble.setText("...")
            self.current_animation = 'thinking_float'
            self.gif_counter = 0
            self.next_animation()
            self.chat_bubble.adjustSize()
            self.chat_task = asyncio.create_task(self._generate_reply(text))

    async def _generate_reply(self, text: str) -> None:
        try:
            reply = await chatRequest(text)
            self.chat_bubble.setText(reply)
            self.chat_bubble.adjustSize()
            self.chat_bubble.show()
            self.current_animation = 'standing'
            self.gif_counter = 0
            self.next_animation()
            if len(reply) > 200:
                self.chat_message_delay = 15
            self.chat_hide_timer.start(self.chat_message_delay * 1000)
            self.chat_message_delay = 15
        finally:
            self.textbox.setEnabled(True)
            self.textbox.setFocus()


    def next_animation(self):
        ''' sets the next animation according to the animation key and the GIF counter '''
        self.movie.stop()
        if self.gif_counter < self.counter_limits[self.current_animation]:
            self.gif_counter += 1
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
            center_point = self.geometry().center() - self.chat_bubble.rect().center()
            self.chat_bubble.move(center_point)
        super().mousePressEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = DesktopAssistant(app)
    widget.show()

    QtAsyncio.run()
