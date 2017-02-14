# Game logic implementation

# Position aka Point
class Position:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)


# Class for storing any masks (damage, support...)
class Mask:
    def __init__(self, data):
        self.data = data
        self.direction = 0
        self.width, self.height = len(data[0]), len(data)
        for x in range(self.width):
            for y in range(self.height):
                if self.data[y][x] is None:
                    self.center = Position(x, y)
                    break

    def rotate(self, direction):
        turns = (direction - self.direction) % 4
        for _ in range(turns):
            self.data = list(zip(*self.data[::-1]))
        if turns % 2 == 1:
            self.width, self.height = self.height, self.width
        self.direction = direction

    def get(self, position):
        position = self.center + position
        return self.data[position.y][position.x]

    def __iter__(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.data[y][x]: yield (x, y), self.data[x][y]


class Unit:
    def __init__(self, position):
        pass

    def rotate(self, direction):
        pass

    # Redirect additional damage from support (not sure about method name)
    def redirect(self, data):
        pass

    def fight(self):
        pass


# Please fill
UNITS = {
    'unit': {
        'damage': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]),
        'support': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]),
        'children': ['infantry', 'horseman']
    },
    'infantry': {
        'damage': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]),
        'support': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]),
        'children': ['pikeman', 'archer', 'warrior']
    },
    'horseman': {
        'damage': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]),
        'support': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]),
        'children': ['dragoon', 'knight', 'hobbler']
    },
    'pikeman': {
        'damage': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]),
        'support': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
    },
    'archer': {
        'damage': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]),
        'support': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
    },
    'warrior': {
        'damage': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]),
        'support': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
    },
    'dragoon': {
        'damage': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]),
        'support': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
    },
    'knight': {
        'damage': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]),
        'support': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
    },
    'hobbler': {
        'damage': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]),
        'support': Mask([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
    }
}
