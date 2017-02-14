# Game logic implementation

# Position aka Point
class Position(tuple):
    # (-1, -1) + (2, 3) = (1, 2)
    def __add__(self):
        pass

# Class for storing any masks (damage, support...)
class Mask:
    # Data - any rectangle (maybe square?) array with None (?) in center
    def __init__(self, data):
        pass
    
    # Don't return anything, just change self
    def rotate(self, direction):
        pass
    
    # Return element with specified position
    def get(self, position):
        pass
    
    # Iterator of non-zero elements
    def __iter__(self):
        pass
        # for x in range(self.width):
        #    for y in range(self.height):
        #        if self.data[x][y]: yield self.data[x][y]
        
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
        
UNITS = {'unit': {'damage': Mask(), 'support': Mask(), 'childs': ['infantry', 'horseman']} # And so on
