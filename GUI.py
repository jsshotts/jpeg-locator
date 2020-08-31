from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QLabel
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont
from time import sleep
from os.path import basename
from main import get_zip
from config import *

class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(800, 500)
 
    #when the mouse enters the list box
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    #when the mouse moves within the box
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    #when the drop is finally released
    def dropEvent(self, event):

        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file = url.toLocalFile()
                    self.addItem(f"{basename(file):.<40} {get_zip(file)}")
                    QApplication.processEvents()

        else:
            event.ignore()

 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 530)
        self.label = QLabel(UI_LABEL, self)
        self.label.setGeometry(300, 500, 200, 30)
        self.listBox = ListBoxWidget(self)
        self.listBox.setFont(QFont(FONT, FONT_SIZE))
        self.setWindowTitle(WINDOW_TITLE)