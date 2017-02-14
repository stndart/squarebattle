import game_classes as gc


class Game:
    def __init__(self, parent, sizex, sizey):
        self.sizex = sizex
        self.sizey = sizey
        self.battlefield = [[gc.NO_UNIT for i in range(self.sizex)] for j in range(self.sizey)]
        self.highlighted = (-1, -1)
        self.chosen = (-1, -1)
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
    
    def put_base_unit(self):
        if self.battlefield[self.chosen[1]][self.chosen[0]] != gc.NO_UNIT:
            return False
        new_unit = gc.Unit(self, self.chosen, gc.PLAYER1, 0)  # Please replace PLAYER1 to current_player
        self.battlefield[self.chosen[1]][self.chosen[0]] = new_unit
        return True
    
    def remove_unit(self):
        if self.battlefield[self.chosen[1]][self.chosen[0]] == gc.NO_UNIT:
            return False
        unit = self.battlefield[self.chosen[1]][self.chosen[0]]
        self.battlefield[self.chosen[1]][self.chosen[0]] = gc.NO_UNIT
        del unit
        return True
    
    def rotate_unit(self):
        if self.battlefield[self.chosen[1]][self.chosen[0]] == gc.NO_UNIT:
            return False
        self.battlefield[self.chosen[1]][self.chosen[0]].direction += 1
        self.battlefield[self.chosen[1]][self.chosen[0]].direction %= 4
        print(self.battlefield[self.chosen[1]][self.chosen[0]].direction)
        return True
    
    def upgrade_unit(self):
        pass
    
    def exit(self):
        del self.battlefield
        del self