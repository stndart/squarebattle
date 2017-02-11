NO_UNIT = -1
PLAYER1 = 1
PLAYER2 = 2


class StrengthOrginizer:  # Maybe include in Unit class?
    def __init__(self, unit):
        self.unit = unit
        self.support = [0, 0, 0, 0]

    def reorganize(self, values):
        self.support = values

    def get_strength(self):
        res = [[self.unit.strength[i][j] for j in range(3)] for i in range(3)]
        res[0][1] += self.support[0]
        res[1][0] += self.support[1]
        res[1][2] += self.support[2]
        res[2][1] += self.support[3]
        return res


class Unit:
    def __init__(self, position, side, direction):
        self.position = position
        self.direction = direction
        self.side = side
        self.strength = [[1, 1, 1],
                         [1, 0, 1],
                         [1, 1, 1]]
        self.support = [0, 0, 0, 0]  # n, w, s, e
        self.strength_orginizer = StrengthOrginizer(self)

    def reorginize(self, values):
        self.strength_orginizer.reorginize(values)

    def get_strength(self, direction):
        return self.strength_orginizer.get_strength(direction)

    def get_support(self, direction):
        return self.support
    
    def redraw(self):
        pass


class Infantry(Unit):
    def __init__(self, *args, **kwargs):
        Unit.__init__(*args, **kwargs)
        self.strength = [[1, 2, 1],
                         [1, 0, 1],
                         [1, 1, 1]]
        self.support = [0, 0, 2, 0]  # n, w, s, e


class Horeseman(Unit):  # The only difference is strength and support
    def __init__(self, *args, **kwargs):
        Unit.__init__(*args, **kwargs)
        self.strength = [[2, 1, 2],
                         [1, 0, 1],
                         [1, 1, 1]]
        self.support = [0, 1, 0, 1]  # n, w, s, e