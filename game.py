import game_classes as gc


class Game:
    def __init__(self, parent, sizex, sizey, current_player=gc.PLAYER1):
        self.sizex = sizex
        self.sizey = sizey
        self.battlefield = [[gc.NO_UNIT for i in range(self.sizex)] for j in range(self.sizey)]
        self.highlighted = (-1, -1)
        self.chosen = (-1, -1)
        self.current_player = current_player
        self.added = []
        pass
    
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
    
    def put_base_unit(self):
        if self.battlefield[self.chosen[1]][self.chosen[0]] != gc.NO_UNIT:
            return False
        new_unit = gc.Unit(self, self.chosen, self.current_player, 0)  # Please replace PLAYER1 to current_player
        self.battlefield[self.chosen[1]][self.chosen[0]] = new_unit
        self.added.append(('add', self.chosen))
        return True
    
    def remove_unit(self):
        if self.battlefield[self.chosen[1]][self.chosen[0]] == gc.NO_UNIT:
            return False
        if self.battlefield[self.chosen[1]][self.chosen[0]].side != self.current_player:
            return False
        if len(self.added) > 0 and self.chosen == self.added[1]:
            self.added = []
        unit = self.battlefield[self.chosen[1]][self.chosen[0]]
        self.battlefield[self.chosen[1]][self.chosen[0]] = gc.NO_UNIT
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
        if self.current_player == gc.PLAYER2:
            self.current_player = gc.PLAYER1
    
    def exit(self):
        del self.battlefield
        del self