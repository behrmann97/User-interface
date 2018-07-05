from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, \
    QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread, \
    QCoreApplication
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, \
    QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QProgressBar, QGroupBox
from PyQt5.Qt import QTest, QTransform, QSound
from clases import IF, WHILE, ELSE, SET, Next, Tab, Layout
from constantes import SCREEN_HEIGHT, SCREEN_WIDTH, first_next, adjust


class Editor(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setGeometry(0, 30, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.label = QLabel(self)
        self.label.setGeometry(*adjust((250, 35, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 35)))
        self.label.setStyleSheet("background-color: rgba(0,0,0,20%)")

        self.current_window = 0
        self.current_size = 0

        self.layout = Layout(self)

        a = Tab(self, self.current_size)
        self.tabs = {0:a}

        self.windows = {0:self.layout}

        self.boton_addTab = QPushButton('+', self)
        self.boton_addTab.setGeometry(*adjust((350,0, 35,35)))
        self.boton_addTab.clicked.connect(self.new_tab)

        self.global_var = {'X': 0, 'Y': 100, 'Z':5, 'speed': 3000, 'hp':150}

        self.show()

    def new_tab(self):
        self.windows[self.current_window].hide()
        self.layout = Layout(self)
        self.tabs[self.current_window].focused = False
        self.current_size += 1
        self.current_window = self.current_size
        a = Tab(self, self.current_size)
        self.tabs[self.current_size] = a
        self.windows[self.current_window] = self.layout

        self.mousePressEvent("")

        self.boton_addTab.move(*adjust((350 + 105 * self.current_size, 0)))

        for i in self.tabs.values():
            i.raise_()
        self.boton_addTab.raise_()

    def cambio_tab(self, tab):
        for i in self.tabs.values():
            i.focused = False
        self.layout.hide()
        self.layout = self.windows[tab.id]
        self.layout.show()


    def mousePressEvent(self, event):
        for i in self.tabs.values():
            i.enter()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            for i in self.tabs.values():
                i.enter()





if __name__ == "__main__":
    app = QApplication([])
    editor = Editor()
    app.exec_()
