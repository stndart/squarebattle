# Game logic implementation

from .const import FIELD_SIZE, KINGS, UNITS


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
        self.update_callback = lambda: None
        self.reset()

    def reset(self):
        self.health = UNITS[self.name]['health']
        self.damage = Matrix(UNITS[self.name]['damage'])
        self.support = Matrix(UNITS[self.name]['support'])
        self.children = UNITS[self.name].get('children')
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
                self.redirect.set(pos, 0)
        self.field.update_near(self.position)
        self.update_callback()

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
    def __init__(self):
        self.width, self.height = FIELD_SIZE
        self.data = Matrix([[None] * width for _ in range(height)])
        self.kings = []
        for i, pos in enumerate(KINGS):
            direction = 3 if i else 1
            king = self.add('king', Position(pos), i, direction)
            self.kings.append(king)

    def get(self, position):
        if position.x < 0 or position.x >= self.width: return False
        if position.y < 0 or position.y >= self.height: return False
        return self.data.get(position)

    def get_near(self, position):
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x or y:
                    unit = self.get(position + Position(x, y))
                    if unit: yield unit

    def update_near(self, position):
        for unit in self.get_near(position): unit.update()

    def add(self, name, position, clan, direction):
        unit = Unit(self, name, position, clan)
        self.data.set(position, unit)
        unit.rotate(direction)
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
            if unit.name == 'king': continue
            unit.reset()


class Game:
    ADD, REMOVE, ROTATE, UPGRADE, REDIRECT = range(5)

    def __init__(self):
        self.field = Field()
        self.turn = 0
        self.turn_done = False
        self.battle_mode = False
        self.finished = False

    def switch(self):
        self.turn = not self.turn
        self.turn_done = False
        if self.battle_mode:
            self.field.battle()
            return self.check_victory()
        return False

    def check_victory(self):
        dead_kings = [(i, x) for i, x in enumerate(self.field.kings) if x.health <= 0]
        if dead_kings:
            self.finished = True
            return -1 if len(dead_kings) == 2 else not dead_kings[0][0]
        return None

    def get_actions(self, position):
        unit = self.field.get(position)
        if unit is None:
            if self.can_add(position): return [self.ADD]
        elif self.can_modify(position):
            ret = [self.ROTATE]
            if unit.redirect_damage: ret.append(self.REDIRECT)
            if not self.turn_done:
                ret.append(self.REMOVE)
                if unit.children: ret.append(self.UPGRADE)
            return ret
        return []

    def can_modify(self, position):
        if self.finished: return False
        unit = self.field.get(position)
        if not unit: return False
        if unit.name == 'king': return False
        if unit.clan != self.turn: return False
        return True

    def can_add(self, position):
        if self.field.get(position) is not None: return False
        near_units = filter(lambda x: x.clan == self.turn, self.field.get_near(position))
        if not any(near_units): return False
        return True

    def add(self, position):
        if self.turn_done: return False
        if not self.can_add(position): return False
        self.turn_done = True
        direction = 3 if self.turn else 1
        unit = self.field.add('unit', position, self.turn, direction)
        return unit

    def remove(self, position):
        if self.turn_done: return False
        if not self.can_modify(position): return False
        self.turn_done = True
        self.field.remove(position)
        return True

    def rotate(self, position, direction):
        if not self.can_modify(position): return False
        self.field.get(position).rotate(direction)
        return True

    def upgrade(self, position, name):
        if self.turn_done: return False
        if not self.can_modify(position): return False
        unit = self.field.get(position)
        if not unit.children or name not in unit.children: return False
        self.turn_done = True
        self.field.upgrade(position, name)
        return True

    def redirect(self, position, matrix):
        if not self.can_modify(position): return False
        unit = self.field.get(position)
        redirect = dict(matrix)
        if sum(redirect.items()) > unit.redirect_damage: return False
        valid_places = [i[0] for i in unit.damage]
        if not all(i in valid_places for i in redirect.keys()): return False
        for pos, value in redirect: unit.redirect.set(pos, value)
        return True