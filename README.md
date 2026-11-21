# Shantae Desktop Pet + Assistant

## Motivation
Well, why don't you let your desktop pet do a bit of a wiggle or whatever when you ask it to, apart from helping you with stuff?

## System Requirements
- I've only tested it on Ubuntu 24.04 LTS, so preferably this is where you should run it.

## To Run This:
0. Make sure that you have your sprite's `actions` folder location copied before you run the following, in case you're using a custom sprite 
1. In your own Python environment (`which python3`) or in a `venv` (activate it beforehand), run `pip install -r requirements.txt`
2. If you're using the default Shantae sprites, you can directly run `python3 test5.py shantae`
3. If you're using custom sprites, generate the metadata using `python3 action_metadata_generator.py <crawl_dir> <sprite_name>` and then run `python3 test5.py <sprite_name>`


## Project References and Credits:
1. [PySide6 Documentation](https://doc.qt.io/qtforpython-6/gettingstarted.html#getting-started)
2. [Qt forum post for using animated GIFs](https://forum.qt.io/topic/132594/adding-many-gifs-to-pyside6-widget-or-another-implementation-of-chat-with-animated-emotes)
3. [Bugfix for `xbc`/`libxbc*`](https://forum.qt.io/topic/93247/qt-qpa-plugin-could-not-load-the-qt-platform-plugin-xcb-in-even-though-it-was-found/153)
4. [PySide6 Layouts - PythonGUIs](https://www.pythonguis.com/tutorials/pyside6-layouts/)
5. [Ezgif.com](https://ezgif.com)
6. [Pinterest](https://pinterest.com)
7. [The Spriters Resource](https://www.spriters-resource.com) (supplied the sprites)
8. Capcom, for their amazing game.