# Shantae Desktop Pet + Assistant (WIP)
![Enjoy some shimies, won't you?](https://i.pinimg.com/originals/2d/b6/0d/2db60d8da1201d149f1c4709f849e462.gif)
> **NB**: Custom sprite addition has been affected to the recent addition of code. Kindly bear with us till it is resolved.

## Motivation
Well, why don't you let your desktop pet do a bit of a wiggle or whatever when you ask it to, apart from helping you with stuff?

## System Requirements
- I've only tested it on Ubuntu 24.04 LTS, so preferably this is where you should run it.

# Before Running:
Do this in the repo root:
```shell
$ echo "COHERE_API_KEY=<your api key>" >> .env
```
Replace `<your api key>` with your Cohere API key.

### OR

Paste your API key in `.env.local`. rename it to `.env` and there you go, you can use it.

## To Run This:
0. Make sure that you have your sprite's `actions` folder location copied before you run the following, in case you're using a custom sprite 
1. In your own Python environment (`which python3`) or in a `venv` (activate it beforehand), run `pip install -r requirements.txt`
2. If you're using the default Shantae sprites, you can directly run `python3 test5.py shantae`
3. If you're using custom sprites, generate the metadata using `python3 action_metadata_generator.py <actions_foler_path> <sprite_name>` and then run `python3 test5.py <sprite_name>`'

## Todo:
- [X] Add a chat backend (maybe using some enterprise API or my own shi)
- [X] Add an intent classifier to direct stuff properly
- [X] Look for collaborators who could do the Windows/Mac edition

## Intent Classification Workflow
- I initially thought of implementing a custom TF-IDF vectorizer with OOV tokens mapped to `<UNK>` but that would make the final input vectors sparse for a sentence with a lot of OOV tokens. Instead, I will rely on `gensim.models.FastText` since it can also deal with OOV tokens
- **Sentence embedding**: sum of all the word embeddings
- **Sentence processing**: lower-case all of them, remove punctuation, split around spaces


## Project References and Credits:
1. [PySide6 Documentation](https://doc.qt.io/qtforpython-6/gettingstarted.html#getting-started)
2. [Qt forum post for using animated GIFs](https://forum.qt.io/topic/132594/adding-many-gifs-to-pyside6-widget-or-another-implementation-of-chat-with-animated-emotes)
3. [Bugfix for `xbc`/`libxbc*`](https://forum.qt.io/topic/93247/qt-qpa-plugin-could-not-load-the-qt-platform-plugin-xcb-in-even-though-it-was-found/153)
4. [PySide6 Layouts - PythonGUIs](https://www.pythonguis.com/tutorials/pyside6-layouts/)
5. [Ezgif.com](https://ezgif.com)
6. [Pinterest](https://pinterest.com)
7. [The Spriters Resource](https://www.spriters-resource.com) (supplied the sprites)
8. [StackOverflow Thread on keeping a window stay on top](https://stackoverflow.com/questions/42614623/how-to-make-a-pyside-window-pop-up-above-all-other-windows)
9. WayForward, for their amazing game.
10. Claude, for making me the dataset my intent classifier runs on: https://claude.ai/share/9772e95b-9065-4cde-b22f-274d6b282c72
11. [`gensim` Word2Vec reference](https://radimrehurek.com/gensim/models/word2vec.html)
12. [Python `re` module reference on W3Schools](https://www.w3schools.com/python/python_regex.asp)
13. [StackOverflow thread on dealing with OOV tokens](https://stackoverflow.com/questions/65372032/deal-with-out-of-vocabulary-word-with-gensim-pretrained-glove)
14. [Cohere AI](https://github.com/cohere-ai) for their Python library and `command-a-plus-05-2026` model. Genuinely makes my Shantae pet talk!
15. [Google Deepmind's](https://github.com/google-deepmind) Gemini search integration on Google Chrome for telling me how to switch from static labels to tooltips for chat bubbles.
16. [GitHub's](https://github.com/github) Copilot for helping me fix the issues in my async code 
