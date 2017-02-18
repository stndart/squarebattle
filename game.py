import game_classes as gc


class Game:
    def __init__(self, parent, sizex, sizey, current_player=gc.PLAYER1):
        self.sizex = sizex
        self.sizey = sizey
        self.battlefield = [[gc.NO_UNIT for i in range(self.sizex)] for j in range(self.sizey)]
        self.battlefield[self.sizey//2][0] = gc.Base(self, (0, self.sizey//2), gc.PLAYER1)
        self.battlefield[self.sizey//2][self.sizex - 1] = gc.Base(self, (self.sizex - 1, self.sizey//2), gc.PLAYER2)
        self.highlighted = (-1, -1)
        self.chosen = (-1, -1)
        self.current_player = current_player
        self.added = []
        
        #self.debug_fill()
        
        pass
    
    def debug_fill(self):
        for i in range(self.sizex):
            for j in range(self.sizey):
                if i <= self.sizex // 2:
                    self.current_player = gc.PLAYER1
                else:
                    self.current_player = gc.PLAYER2
                self.put_base_unit(coords=(i, j), override=True)
    
    def choose_square(self, sx, sy):
        if self.chosen == (sx, sy):
            self.chosen = (-1, -1)
            return 'already_chosen'
        else:
            self.chosen = (sx, sy)
            return 'success'
    
    def get_unit(self, sx, sy):
        if self.battlefield[sy][sx] == gc.NO_UNIT:
            return False
        return self.battlefield[sy][sx]
    
    def highlight(self, sx, sy):
        self.highlighted = (sx, sy)
    
    def available_actions(self):
        if len(self.added) == 0:
            return {'add', 'rotate', 'remove', 'upgrade'}
        else:
            return {'rotate', 'remove', 'upgrade'}
    
    def put_base_unit(self, coords=(-1, -1), override=False):
        if coords == (-1, -1):
            coords = self.chosen
        if self.battlefield[coords[1]][coords[0]] != gc.NO_UNIT:
            return False
        if not override:
            conf = False
            good = lambda x, y: 0 <= x < self.sizex and 0 <= y < self.sizey
            add = lambda e, e2: [e[0] + e2[0], e[1] + e2[1]]
            for t in [[-1, 0], [+1, 0], [0, -1], [0, +1]]:
                near = add(coords, t)
                if good(*near):
                    if self.get_unit(*near) and self.get_unit(*near).side == self.current_player:
                        conf = True
                        break
            if not conf:
                return False
        if self.current_player == gc.PLAYER1:
            direct = 0
        else:
            direct = 2
        new_unit = gc.Unit(self, coords, self.current_player, direct)
        self.battlefield[coords[1]][coords[0]] = new_unit
        self.added.append(coords)
        return True
    
    def remove_unit(self, coords=(-1, -1), override=False):
        if coords == (-1, -1):
            coords = self.chosen
        if self.battlefield[coords[1]][coords[0]] == gc.NO_UNIT:
            return False
        if not override:
            if self.battlefield[coords[1]][coords[0]].side != self.current_player:
                return False
        if len(self.added) > 0 and coords in self.added:
            del self.added[self.added.index(coords)]
        unit = self.battlefield[coords[1]][coords[0]]
        self.battlefield[coords[1]][coords[0]] = gc.NO_UNIT
        del unit
        return True
    
    def rotate_unit(self):
        if self.battlefield[self.chosen[1]][self.chosen[0]] == gc.NO_UNIT:
            return False
        self.battlefield[self.chosen[1]][self.chosen[0]].direction += 1
        self.battlefield[self.chosen[1]][self.chosen[0]].direction %= 4
        return True
    
    def upgrade_unit(self):
        pass
    
    def next_turn(self):
        if self.current_player == gc.PLAYER1:
            self.current_player = gc.PLAYER2
        elif self.current_player == gc.PLAYER2:
            self.current_player = gc.PLAYER1
        self.added = []
    
    def fight(self):
        for i in range(self.sizex):
            for j in range(self.sizey):
                if self.battlefield[j][i] != gc.NO_UNIT:
                    self.battlefield[j][i].fight_around()
        for i in range(self.sizex):
            for j in range(self.sizey):
                if self.battlefield[j][i] != gc.NO_UNIT:
                    if self.battlefield[j][i].health <= 0:
                        self.remove_unit(coords=(i, j), override=True)
        for i in range(self.sizex):
            for j in range(self.sizey):
                if self.battlefield[j][i] != gc.NO_UNIT:
                    self.battlefield[j][i].health = self.battlefield[j][i].base_health
    
    def exit(self):
        del self.battlefield
        del self