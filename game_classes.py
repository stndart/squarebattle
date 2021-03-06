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
        res = [[self.unit.strength[i][j] for j in range(len(self.unit.strength[i]))] for i in range(len(self.unit.strength))]
        zero = self.unit.strength_center
        zerox = zero[0]
        zeroy = zero[1]
        res[zeroy - 1][zerox] += self.support[0]
        res[zeroy][zerox - 1] += self.support[1]
        res[zeroy][zerox + 1] += self.support[2]
        res[zeroy + 1][zerox] += self.support[3]
        return res


class Unit:
    def __init__(self, parent, position, side, direction):
        self.parent = parent
        self.position = position
        self.direction = direction  # 0=e, 1=n, 2=w, 3=s
        self.side = side
        self.strength = [[1, 1, 1],
                         [1, 0, 1],
                         [1, 1, 1]]
        self.strength_center = (1, 1)  # for archers, when self.strength
        self.support = [[0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]]
        self.support_center = (1, 1)
        self.strength_orginizer = StrengthOrginizer(self)
        self.base_health = 3
        self.health = self.base_health
        self.rotatable = True
        self.removable = True
        self.upgradeable = True

    def reorginize(self, values):
        self.strength_orginizer.reorganize(values)
    
    def fight_around(self):
        strength = self.strength_orginizer.get_strength()
        for i in range(len(strength)):
            for j in range(len(strength[i])):
                dy1 = i - self.strength_center[0]
                dx1 = j - self.strength_center[1]
                direction = [dy1, dx1, -dy1, -dx1]
                dy2 = direction[(-self.direction) % 4]
                dx2 = direction[(1 - self.direction) % 4]
                nx = self.position[0] + dx2
                ny = self.position[1] + dy2
                sx = self.strength_center[0] + dx2
                sy = self.strength_center[1] + dy2
                if 0 <= sx < len(self.strength[i]) and 0 <= sy < len(self.strength):
                    if 0 <= ny < self.parent.sizey and 0 <= nx < self.parent.sizex:
                        if self.parent.battlefield[ny][nx] != NO_UNIT and self.parent.battlefield[ny][nx].side != self.side:
                            self.parent.battlefield[ny][nx].health -= self.strength[sy][sx]
    
    def get_support(self):
        support_n = 0
        for i in range(len(self.support)):
            for j in range(len(self.support[i])):
                dy1 = i - self.support_center[0]
                dx1 = j - self.support_center[1]
                direction = [dy1, dx1, -dy1, -dx1]
                dy2 = direction[(-self.direction) % 4]
                dx2 = direction[(1 - self.direction) % 4]
                nx = self.position[1] + dx2
                ny = self.position[0] + dy2
                if 0 <= ny < self.parent.sizey and 0 <= nx < self.parent.sizex:
                    neig = self.parent.battlefield[ny][nx]
                else:
                    continue
                if 0 <= self.support_center[1] + dx2 < len(self.support[i]):
                    if 0 <= self.support_center[0] + dy2 < len(self.support):
                        if 0 <= neig.support_center - dx2 < len(neig.support[i]):
                            if 0 <= neig.support_center - dy2 < len(neig.support):
                                support_n += min(
                                    self.support[self.support_center[0] + dy2][self.support_center[1] + dx2],
                                    neig.support[neig.support_center[0] - dy2][neig.support_center[1] - dx2])
        return support_n

class Base(Unit):
    def __init__(self, *args, **kwargs):
        kwargs['direction'] = 0
        Unit.__init__(self, *args, **kwargs)
        self.strength = [[1, 1, 1],
                         [1, 0, 1],
                         [1, 1, 1]]
        self.support = [[1, 1, 1],
                        [1, 0, 1],
                        [1, 1, 1]]
        self.base_health = 3
        self.health = self.base_health
        self.rotatable = False
        self.removable = False
        self.upgradeable = False


class Infantry(Unit):
    def __init__(self, *args, **kwargs):
        Unit.__init__(self, *args, **kwargs)
        self.strength = [[1, 2, 1],
                         [1, 0, 1],
                         [1, 1, 1]]
        self.support = [[0, 0, 0],
                        [0, 0, 0],
                        [0, 2, 0]]
        self.base_health = 4
        self.health = self.base_health


class Horseman(Unit):  # The only difference is strength and support
    def __init__(self, *args, **kwargs):
        Unit.__init__(*args, **kwargs)
        self.strength = [[2, 1, 2],
                         [1, 0, 1],
                         [1, 1, 1]]
        self.support = [[0, 0, 0],
                        [1, 0, 1],
                        [0, 0, 0]]
        self.base_health = 3
        self.health = self.base_health