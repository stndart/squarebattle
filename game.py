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
        new_unit = gc.Unit(self, self.chosen, gc.PLAYER1, 1)  # Replace PLAYER1 to current_player
        self.battlefield[self.chosen[1]][self.chosen[0]] = new_unit
    
    def exit(self):
        del self.battlefield
        del self