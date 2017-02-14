# Game logic implementation

from .const import UNITS

# Position aka Point
class Position:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)


class Matrix:
    def __init__(self, data):
        self.data = data[:]
        self.direction = 0
        self.width, self.height = len(data[0]), len(data)
        self.find_center()

    def find_center(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.data[y][x] is None:
                    self.center = Position(x, y)
                    return

    def rotate(self, direction):
        turns = (direction - self.direction) % 4
        for _ in range(turns):
            self.data = list(zip(*self.data[::-1]))
        if turns % 2 == 1:
            self.width, self.height = self.height, self.width
        self.direction = direction
        self.find_center()

    def get(self, position):
        position = self.center + position
        return self.data[position.y][position.x]

    def set(self, position, data):
        position = self.center + position
        self.data[position.y][position.x] = data

    def __iter__(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.data[y][x]: yield Position(x, y), self.data[x][y]


class Unit:
    def __init__(self, field, name, position, clan):
        self.field = field
        self.name = name
        self.position = position
        self.direction = 0
        self.clan = clan
        self.reset()

    def reset(self):
        self.health = UNITS[self.name]['health']
        self.damage = Matrix(UNITS[self.name]['damage'])
        self.support = Matrix(UNITS[self.name]['support'])
        self.children = UNITS[self.name]['children']
        self.redirect = Matrix([[0] * self.damage.width for _ in range(self.damage.height)])
        self.rotate(self.direction)
        self.update()

    def update(self):
        self.redirect_damage = 0
        for pos, value in self.support:
            unit = self.field.get(self.position + pos)
            if unit and self.clan == unit.clan:
                alt_value = unit.support.get(self.position - unit.position) or 1
                self.redirect_damage += self.damage.get(pos) * min(value, alt_value)

        if sum(i for _, i in self.redirect) > self.redirect_damage:
            for pos, value in self.redirect:
                self.redirect.set(pos, 0)  # Maybe decrease proportional

    def rotate(self, direction):
        self.damage.rotate(direction)
        self.support.rotate(direction)
        self.redirect.rotate(direction)
        self.direction = direction
        self.update()

    def fight(self):
        for matrix in (self.damage, self.redirect):
            for pos, value in matrix:
                unit = self.field.get(self.position + pos)
                if unit and self.clan != unit.clan:
                    unit.health -= value


class Field:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.data = Matrix([[None] * width for _ in height])

    def get(self, position):
        if position.x < 0 or position.x > self.width: return None
        if position.y < 0 or position.y > self.height: return None
        return self.data.get(position)

    def update_near(self, position):
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x or y:
                    unit = self.get(position + Position(x, y))
                    if unit: unit.update()

    def add(self, name, position, clan):
        unit = Unit(self, name, position, clan)
        self.data.set(position, unit)
        self.update_near(position)
        return unit

    def remove(self, position):
        self.data.set(position, None)
        self.update_near(position)

    def upgrade(self, position, name):
        unit = self.data.get(position)
        unit.name = name
        unit.reset()
        self.update_near(position)

    def battle(self):
        for _, unit in self.data:
            unit.fight()
        for pos, unit in self.data:
            if unit.health <= 0: self.data.set(pos, None)
        for _, unit in self.data:
            unit.reset()

            # Win / lose handler
