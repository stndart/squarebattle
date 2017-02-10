NO_UNIT = -1

class StrengthOrginizer:
    def __init__(self, unit):
        self.unit = unit
        self.ability_buff = [0, 0, 0, 0]
    def reorganize(self, values):
        self.ability_buff = values
    def get_strength(self):
        res = [[self.unit.strength[i][j] for j in range(3)] for i in range(3)]
        res[0][1] += self.ability_buff[0]
        res[1][0] += self.ability_buff[1]
        res[1][2] += self.ability_buff[2]
        res[2][1] += self.ability_buff[3]
        return res

class Unit:
    def __init__(self, position, side, direction):
        self.position = position
        self.direction = direction
        self.side = side
        self.strength = [[1, 1, 1],
                         [1, 0, 1],
                         [1, 1, 1]]
        self.ability = [0, 0, 0, 0]  # n, w, s, e
        self.strength_orginizer = StrengthOrginizer(self)
    def reorginize(self, values):
        self.strength_orginizer.reorginize(values)
    def get_strength(self, direction):
        return self.strength_orginizer.get_strength(direction)
    def get_ability(self, direction):
        return self.ability

class Infantry(Unit):
    def __init__(self, *args, **kwargs):
        self.Unit.__init__(*args, **kwargs)
        self.strength = None  # !!!
        self.ability = None   # !!!

class Horeseman(Unit):  # The only difference is strength and ability
    def __init__(self, *args, **kwargs):
        self.Unit.__init__(*args, **kwargs)
        self.strength = None  # !!!
        self.ability = None   # !!!