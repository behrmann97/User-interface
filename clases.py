from PyQt5.QtCore import QTimer, Qt, QObject, QSize
from PyQt5.QtWidgets import QProgressBar, QWidget, QLabel, QPushButton, \
    QLineEdit, QGroupBox, QComboBox, QScrollArea
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon, QPixmap, QFont
import time
from constantes import SCREEN_HEIGHT, SCREEN_WIDTH, else_creator, if_creator,\
 set_creator, while_creator, first_next, adjust


newfont = QFont("Copperplate Gothic Light", adjust([7]))
bigfont = QFont("Copperplate Gothic Light", adjust([12]))

if_yeah = """
QPushButton{
    background-color: rgb(100,255,100,70%);
    border-width: 1px;
}
QPushButton::pressed {
    background-color: rgb(0, 0, 0,75%);

}"""

while_yeah = """
QPushButton{
    background-color: rgb(255,100,100,70%);
    border-width: 1px;
}
QPushButton::pressed {
    background-color: rgb(0, 0, 0,75%);

}"""

set_yeah = """
QPushButton{
    background-color: rgb(100,100,255,70%);
    border-width: 1px;
}
QPushButton::pressed {
    background-color: rgb(0, 0, 0,75%);

}"""

else_yeah = """
QPushButton{
    background-color: rgb(186,85,211,70%);
    border-width: 1px;
}
QPushButton::pressed {
    background-color: rgb(0, 0, 0,75%);

}"""


class DragButton(QPushButton):
    def __init__(self, parent, creador):
        QPushButton.__init__(self, parent)
        self.creador = creador
        self.parent = parent
        self.set = False
        self.using = None

    def mousePressEvent(self, event):
        if self.creador:
            a = self.__class__(self.parent, True)
            a.show()
            self.creador = False
        self.prev = (self.x(), self.y())
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        super(DragButton, self).mousePressEvent(event)
        self.parent.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.__mouseMovePos = globalPos

        super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()

        super(DragButton, self).mouseReleaseEvent(event)
        self.change_next(self.parent.check_put(self))
        self.click()

    def change_next(self, pos):
        if not pos:
            self.hide()
            if isinstance(self, IF):
                if self.extra:
                    self.extra.hide()
                    del self.extra
            del self
        else:
            if not isinstance(self, IF):
                self.move(pos[0], pos[1])
            else:
                self.move(*adjust(((pos[2] - 0.5 ) * 175 + first_next[0], pos[1])))
                if self.extra:
                    self.extra.move(*adjust(((pos[2] + 0.5 ) * 175 + first_next[0], pos[1])))
                else:
                    a = ELSE(self.parent)
                    a.move(*adjust(((pos[2] + 0.5 ) * 175 + first_next[0], pos[1])))
                    a.show()
                    a.click()
                    a.setEnabled(False)
                    self.extra = a
            self.set = True
            self.col = pos[2] if not isinstance(self, IF) else pos[2] - 0.5
            self.row = pos[3]


class IF(DragButton):

    def __init__(self, parent, creador=False):
        super().__init__(parent, creador)

        signos = ['<','>','==','!=','>=','<=']

        self.extra = None

        self.setStyleSheet(if_yeah)
        self.setGeometry(*adjust((if_creator[0], if_creator[1],150, 50)))

        self.layer = QGroupBox(self)
        self.layer.setGeometry(*adjust((0,0,150 , 50)))

        self.text = QLabel("If", self.layer)
        self.text.setFont(newfont)
        self.text.move(*adjust((5, 18)))

        self.edit1 = QLineEdit("X", self.layer)
        self.edit1.setFont(newfont)
        self.edit1.setGeometry(*adjust((20, 10, 35, 30)))

        self.signos = QComboBox(self.layer)
        for i in signos:
            self.signos.addItem(i)
        self.signos.setGeometry(*adjust((60, 10, 35, 30)))

        self.edit2 = QLineEdit("0", self.layer)
        self.edit2.setFont(newfont)
        self.edit2.setGeometry(*adjust((100, 10, 40, 30)))


class WHILE(DragButton):

    def __init__(self, parent, creador=False):
        super().__init__(parent, creador)

        signos = ['<','>','==','!=','>=','<=']

        self.setStyleSheet(while_yeah)
        self.setGeometry(*adjust((while_creator[0], while_creator[1],150, 50)))

        self.layer = QGroupBox(self)
        self.layer.setGeometry(*adjust((0,0, 150, 50)))

        self.text = QLabel("while", self.layer)
        self.text.setFont(newfont)
        self.text.move(*adjust((5, 18)))

        self.edit1 = QLineEdit("X", self.layer)
        self.edit1.setFont(newfont)
        self.edit1.setGeometry(*adjust((40, 10, 35, 30)))

        self.signos = QComboBox(self.layer)
        for i in signos:
            self.signos.addItem(i)
        self.signos.setGeometry(*adjust((75, 10, 35, 30)))

        self.edit2 = QLineEdit("0", self.layer)
        self.edit2.setFont(newfont)
        self.edit2.setGeometry(*adjust((110, 10, 35, 30)))


class ELSE(DragButton):

    def __init__(self, parent, creador=False):
        super().__init__(parent, creador)

        self.setStyleSheet(else_yeah)

        self.setGeometry(*adjust((else_creator[0], else_creator[1],150, 50)))

        self.layer = QGroupBox(self)
        self.layer.setGeometry(*adjust((0,0, 150, 50)))

        self.text = QLabel("Else", self.layer)
        self.text.setFont(newfont)
        self.text.move(*adjust((60, 18)))


class SET(DragButton):

    def __init__(self, parent, creador=False):
        super().__init__(parent, creador)

        self.setStyleSheet(set_yeah)

        self.setGeometry(*adjust((set_creator[0], set_creator[1],150, 50)))

        self.layer = QGroupBox(self)
        self.layer.setGeometry(*adjust((0,0, 150, 50)))

        self.text = QLabel("Set", self.layer)
        self.text.setFont(newfont)
        self.text.move(*adjust((5, 18)))

        self.edit1 = QLineEdit("X", self.layer)
        self.edit1.setFont(newfont)
        self.edit1.setGeometry(*adjust((30, 10, 40, 30)))

        self.text2 = QLabel("to",self)
        self.text2.setFont(newfont)
        self.text2.move(*adjust((75, 18)))

        self.edit2 = QLineEdit("0", self.layer)
        self.edit2.setFont(newfont)
        self.edit2.setGeometry(*adjust((100, 10, 40, 30)))


class Next(QPushButton):

    def __init__(self, parent, col = 2, row = 0):
        super().__init__(parent)
        self.setFixedSize( 150, 50)
        self.setText("drop here to add")
        self.setFont(newfont)
        self.setEnabled(False)
        self.col = col
        self.row = row
        self._used = False
        self.move(*adjust((first_next[0]+ 175 * col, first_next[1] + 65 * row)))

    def over(self, x, y):
        if x in range(self.x() - 15, self.x() +  165) and y in range(self.y() - 10, self.y() + 60):
            return True
        return False

    @property
    def used(self):
        return self._used

    @used.setter
    def used(self, value):
        if value:
            self.hide()
        else:
            self.show()
        self._used = value


class Tab(QLabel):
    id = 0
    def __init__(self, parent, size):
        super().__init__(parent)
        self.setGeometry(*adjust((size * 105 + 250, 0, 100, 35)))
        self.setStyleSheet("background-color: rgba(0,0,0,20%)")
        self.name = "New tab"
        self.size = size
        self.setText("  " + self.name)
        self.setFont(newfont)
        self.show()
        self. id = Tab.id
        Tab.id += 1
        self._focused = True
        self.editando = False

    @property
    def focused(self):
        return self._focused

    @focused.setter
    def focused(self, value):
        if value:
            self.setStyleSheet("background-color: rgba(0,0,0,20%)")
        else:
            self.setStyleSheet('background-color: rgb(130,130,130)')
        self._focused  = value

    def mouseDoubleClickEvent(self, event):
        if not self.editando:
            self.editando = True
            self.edit = QLineEdit(self.name, self.parent())
            self.edit.setGeometry(*adjust((self.size * 105 + 250, 0, 100, 35)))
            self.edit.show()
            self.edit.setFocus(True)

    def enter(self):
        if self.editando:
            self.name = self.edit.text()
            self.edit.hide()
            self.setText("  " + self.name)
            self.editando = False

    def mousePressEvent(self, event):
        self.parent().cambio_tab(self)
        self.parent().mousePressEvent(event)
        self.focused = True


class Layout(QGroupBox):

    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(*adjust((0, 0, SCREEN_WIDTH , SCREEN_HEIGHT)))

        self.initial_next = Next(self)

        self.if_creator = IF(self, True)

        self.while_creator = WHILE(self, True)

        self.set_creator = SET(self, True)

        self.colrows = {(0,0): self.initial_next}

        self.local_var = {'i':0}

        self.execute_button = QPushButton('Execute code', self)
        self.execute_button.setFont(bigfont)
        self.execute_button.setGeometry(*adjust((SCREEN_WIDTH - 250, SCREEN_HEIGHT - 100, 150, 60)))
        self.execute_button.setStyleSheet('background-color: rgba(255, 255, 255, 80%)')

        self.see_global = QPushButton('GLOBAL VARIABLES', self)
        self.see_global.setFont(bigfont)
        self.see_global.move(*adjust((50, 350)))
        self.see_global.clicked.connect(self.see_global_variables)

        self.show()

    def see_global_variables(self):
        Window(self.parent().global_var, 'global', self)

    def change_variables(self,type,result):
        print(result)
        if type == 'global':
            self.parent().global_var = result
        else:
            self.local_var = result

    def keyPressEvent(self, event):
        self.parent().keyPressEvent(event)

    def check_put(self, obj):
        if obj.using:
            obj.using.used = False
            obj.using = None
        for i in self.colrows.values():
            if i.over(obj.x(), obj.y()):
                if i.used and i.used != obj:
                    i.used.hide()
                if (i.col, i.row+1) not in self.colrows.keys():
                    n = Next(self, i.col - 0.5 if isinstance(obj, IF) else i.col, i.row + 1)
                    self.colrows[(i.col, i.row + 1)] = n
                    n.show()
                i.used = obj
                obj.using = i
                return (i.x(), i.y(), i.col, i.row)
        return False


class Window(QWidget):

    def __init__(self, variables,type, parent = None):
        super().__init__(parent)
        self.layout = QScrollArea(self)
        self.layout.setGeometry(*adjust((0,0, 600, 600)))
        self.setGeometry(*adjust((350, 150, 600, 600)))
        self.variables = variables
        i = 0
        self.edits = []
        self.apply_button = QPushButton('Apply changes', self.layout)
        self.apply_button.setGeometry(*adjust((400,500, 100, 50)))
        self.apply_button.setFont(newfont)
        self.apply_button.clicked.connect(self.apply_changes)
        for var in variables.keys():
            a = QLabel(var, self.layout)
            a.move(*adjust((50, 30 + i * 50)))
            a.setFont(newfont)

            b = QLineEdit(str(variables[var]), self.layout)
            b.move(*adjust((140, 30 + i * 50)))
            b.setFont(newfont)
            i += 1
            self.edits.append(b)
            a.show()
            b.show()
        self.show()

    def apply_changes(self):
        result = {}
        for i in range(len(self.variables)):
            result[list(self.variables.keys())[i]] = self.edits[i].text()
        self.parent().change_variables(type, result)
