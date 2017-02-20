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

        Images.data['add'] = QPixmap(r'resources\icons\add.png')

    @staticmethod
    def get(item):
        return Images.data.get(item)


def update_style(widget):
    widget.style().unpolish(widget)
    widget.style().polish(widget)

class Label(QLabel):
    def __init__(self, parent, style, text=''):
        QLabel.__init__(self, text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setProperty('style', style)

class Button(QPushButton):
    def __init__(self, parent, style, text=''):
        QPushButton.__init__(self, text, parent)
        self.setProperty('style', style)
        self.setFixedWidth(100)


class InfoLabel(QLabel):
    def __init__(self, parent, style):
        QLabel.__init__(self, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(25, 25)
        self.setProperty('style', style)


class UnitWidget(QLabel):
    def __init__(self, parent, position, game):
        QLabel.__init__(self, parent)

        self.setAutoFillBackground(True)
        self.setMouseTracking(True)
        self.setAlignment(Qt.AlignCenter)
        self.installEventFilter(self)

        self.health_label = InfoLabel(self, 'health')
        self.damage_label = InfoLabel(self, 'damage')
        self.support_label = InfoLabel(self, 'support')
        self.reset()

        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(5, 5, 5, 5)
        self.hlay = QHBoxLayout()
        self.lay.addStretch(2)
        self.lay.addLayout(self.hlay)
        self.lay.addStretch(2)
        self.hlay.addStretch(2)
        self.hlay.addWidget(self.damage_label)
        self.hlay.addWidget(self.health_label)
        self.hlay.addWidget(self.support_label)
        self.hlay.addStretch(2)

        self.position = position
        self.game = game
        self.set_unit(None)
        self.mouse_out()

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
        if self.unit.name != BASE_UNIT:
            for _ in range(self.unit.direction):
                pixmap = pixmap.transformed(QTransform().rotate(90), Qt.SmoothTransformation)
        self.setPixmap(pixmap)

    def mouse_in(self):
        self.setProperty('style', 'hover')
        update_style(self)
        if self.unit is None:
            actions = self.game.get_actions(self.position)
            if Game.ADD in actions:
                pixmap = Images.get('add').scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.setPixmap(pixmap)
        else:
            self.health_label.setText(str(self.unit.health))
            self.health_label.setVisible(True)
            data = {}
            for pos, value in self.unit.damage:
                unit = self.game.field.get(pos + self.position)
                if unit and unit.clan == self.unit.clan: continue
                if pos not in data: data[pos] = [0, 0]
                data[pos][0] = value
            for pos, value in self.unit.redirect:
                unit = self.game.field.get(pos + self.position)
                if unit and unit.clan == self.unit.clan: continue
                if pos not in data: data[pos] = [0, 0]
                data[pos][0] += value
            for pos, value in self.unit.support:
                unit = self.game.field.get(pos + self.position)
                if unit and unit.clan != self.unit.clan: continue
                if pos not in data: data[pos] = [0, 0]
                data[pos][1] = value
            for pos, d in data.items():
                unit_widget = self.parent().get(pos + self.position)
                if unit_widget: unit_widget.display_data(d)

    def clicked(self):
        actions = self.game.get_actions(self.position)
        if Game.ADD in actions:
            unit = self.game.add(self.position)
            self.set_unit(unit)
            self.mouse_in()

    def display_data(self, data):
        if data[0]:
            self.damage_label.setText(str(data[0]))
            self.damage_label.setVisible(True)
        if data[1]:
            self.support_label.setText(str(data[1]))
            self.support_label.setVisible(True)

    def reset(self):
        self.health_label.setVisible(False)
        self.damage_label.setVisible(False)
        self.support_label.setVisible(False)

    def mouse_out(self):
        self.setProperty('style', 'default')
        update_style(self)
        if self.unit is None:
            self.clear()
        else:
            self.parent().reset_all()

    def eventFilter(self, widget, event):
        if event.type() == QEvent.Enter:
            self.mouse_in()
        elif event.type() == QEvent.Leave:
            self.mouse_out()
        elif event.type() == QEvent.MouseButtonPress:
            self.clicked()
        return QLabel.eventFilter(self, widget, event)


class FieldWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setFixedSize(600, 600)
        self.lay = QGridLayout(self)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.setMouseTracking(True)

    def set_game(self, game):
        self.game = game
        self.field = game.field
        self.field.remove_callback = self.remove_callback
        for x in range(self.field.width):
            for y in range(self.field.height):
                position = Position(x, y)
                unit_widget = UnitWidget(self, position, game)
                self.lay.addWidget(unit_widget, y, x)
                unit = self.field.get(position)
                if unit: unit_widget.set_unit(unit)

    def remove_callback(self, position):
        self.get(position).set_unit(None)

    def get(self, position):
        unit_item = self.lay.itemAtPosition(position.y, position.x)
        if unit_item: return unit_item.widget()

    def reset_all(self):
        for x in range(self.field.width):
            for y in range(self.field.height):
                self.get(Position(x, y)).reset()


class MainFrame(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(10, 10, 10, 10)

        self.top_lay = QHBoxLayout()

        self.turn_label = Label(self, 'data', 'BLUE')
        self.turn_label.setFixedWidth(70)
        self.turn_label.setProperty('color', 'blue')
        self.time_label = Label(self, 'data', '01:00')
        self.turn_button = Button(self, 'turn', 'Done')
        self.turn_button.clicked.connect(self.turn)
        self.battle_button = Button(self, 'battle', 'Battle')

        self.top_lay.addWidget(Label(self, 'title', 'Turn:'))
        self.top_lay.addWidget(self.turn_label)
        self.top_lay.addStretch(2)
        self.top_lay.addWidget(Label(self, 'title', 'Time:'))
        self.top_lay.addWidget(self.time_label)
        self.top_lay.addStretch(2)
        self.top_lay.addWidget(self.turn_button)
        self.top_lay.addWidget(self.battle_button)

        self.field_widget = FieldWidget(self)

        self.bottom_lay = QHBoxLayout()

        self.lay.addLayout(self.top_lay)
        self.lay.addWidget(self.field_widget)
        self.lay.addLayout(self.bottom_lay)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time)
        self.timer.start()
        self.time_left = 60
        self.game = Game()
        self.battle_button.clicked.connect(self.game.battle)
        self.field_widget.set_game(self.game)
        self.show()

    def update_time(self):
        self.time_left -= 1
        if self.time_left == 0: self.turn()
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        time = '{:02}:{:02}'.format(minutes, seconds)
        self.time_label.setText(time)

    def turn(self):
        self.time_left = 60
        self.time_label.setText('01:00')
        self.game.switch()
        turn = 'red' if self.game.turn else 'blue'
        self.turn_label.setProperty('color', turn)
        self.turn_label.setText(turn.upper())
        update_style(self.turn_label)

if __name__ == '__main__':
    app = QApplication(sys_argv)
    app.setStyleSheet(open(r'resources\style.css').read())
    Images.load()
    main_frame = MainFrame()
    app.exec()