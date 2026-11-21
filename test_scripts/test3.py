import sys
from PySide6.QtGui import QMovie
import PySide6.QtCore as Qt
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)

label = QLabel()
movie = QMovie("./actions/dancing/02.gif")
movie.finished.connect(movie.start)
label.setMovie(movie)
label.resize(500, 500)
label.setStyleSheet("background-color: rgba(255, 255, 255, 0.1);")
label.setWindowFlags(label.windowFlags() | Qt.Qt.WindowType.FramelessWindowHint)
label.setAttribute(Qt.Qt.WA_TranslucentBackground)
label.show()

movie.start()
sys.exit(app.exec())
