from PyQt4.QtGui import *
from PyQt4.QtCore import *
from game import *
from const import *
from sys import argv as sys_argv


class Images:  # Kind of singleton
    data = {}

    @staticmethod
    def load():
        Images.data['king_blue'] = QPixmap(r'resources\images\king_blue.png')
        Images.data['king_red'] = QPixmap(r'resources\images\king_red.png')
        Images.data['unit_blue'] = QPixmap(r'resources\images\unit_blue.png')
        Images.data['unit_red'] = QPixmap(r'resources\images\unit_red.png')

    @staticmethod
    def get(item):
        return Images.data.get(item)

class UnitWidget(QLabel):
    def __init__(self, parent, position):
        QLabel.__init__(self, parent)
        self.setAutoFillBackground(True)

        self.position = position
        self.set_unit(None)

    def set_unit(self, unit):
        self.unit = unit
        if self.unit is not None:
            self.unit.update_callback = self.update_callback
            self.update_callback()
        else:
            self.clear()

    def update_callback(self):
        image = self.unit.name + '_' + ('red' if self.unit.clan else 'blue')
        pixmap = Images.get(image).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        for _ in range(self.unit.direction):
            pixmap = pixmap.transformed(QTransform().rotate(90), Qt.SmoothTransformation)
        self.setPixmap(pixmap)

class FieldWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.lay = QGridLayout(self)

    def render_field(self, field):
        for x in range(field.width):
            self.lay.setColumnMinimumWidth(x, 70)
            for y in range(field.height):
                self.lay.setRowMinimumHeight(y, 70)
                position = Position(x, y)
                unit_widget = UnitWidget(self, position)
                self.lay.addWidget(unit_widget, y, x)
                unit = field.get(position)
                if unit: unit_widget.set_unit(unit)

    def get(self, position):
        return self.lay.itemAtPosition(position.y, position.x).widget()

class MainFrame(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.lay = QHBoxLayout(self)
        self.field_widget = FieldWidget(self)
        self.lay.addWidget(self.field_widget)
        self.game = Game()
        self.field_widget.render_field(self.game.field)
        self.test_btn = QPushButton('Test', self)
        self.test_btn.clicked.connect(self.test)
        self.lay.addWidget(self.test_btn)
        self.show()

    def test(self):
        self.game.field.kings[0].rotate(2)
        unit = self.game.add(Position(1, 3))
        self.field_widget.get(Position(1, 3)).set_unit(unit)
        self.game.switch()
        unit = self.game.add(Position(5, 3))
        self.field_widget.get(Position(5, 3)).set_unit(unit)

if __name__ == '__main__':
    app = QApplication(sys_argv)
    app.setStyleSheet(open(r'resources\style.css').read())
    Images.load()
    main_frame = MainFrame()
    app.exec()