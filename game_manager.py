import tkinter as tk
import game_classes as gc


class LeftMenuBar:
    def __init__(self, parent, x, y, width, height):
        self.parent = parent
        self.frame = tk.Frame(self.parent.root, width=width, height=height, bg='lightblue')
        self.frame.place(x=x, y=y)

class Field:
    def __init__(self, parent, x, y, width, height, sizex=9, sizey=8):
        self.parent = parent
        self.width = width
        self.height = height
        self.sizex = sizex
        self.sizey = sizey
        self.canvas = tk.Canvas(width=self.width, height=self.height, bg='pink')
        self.canvas.place(x=x, y=y)
        self.battlefield = [[gc.NO_UNIT for i in range(self.sizex)] for j in range(self.sizey)]
        for i in range(sizex + 1):
            lx = i * self.width // self.sizex + 1
            if lx == 1:
                lx += 1
            self.canvas.create_line(lx, 0, lx, self.height + 2)
        for i in range(sizey + 1):
            ly = i * self.height // self.sizey + 1
            if ly == 1:
                ly += 1
            self.canvas.create_line(0, ly, self.width + 2, ly)
        self.canvas.bind('<Button-1>', self.click)
        self.chosen = (-1, -1)
        self.highlight = None
    def click(self, event):
        sx = event.x * self.sizex // self.width
        sy = event.y * self.sizey // self.height
        #self.choose_square(sx, sy)
        self.put_base_unit(sx, sy)
    def choose_square(self, sx, sy):
        self.chosen = (sx, sy)
        self.parent.choose_square_menu()
    def put_base_unit(self):
        new_unit = gc.Unit(self.choice, gc.PLAYER1, (+1, 0))
        self.battlefield[sy][sx] = new_unit
    def upgrade_unit(self, choice):
        pass
    def delete_unit(self):
        pass
    def redraw(self):
        if self.highlight is not None:
            self.canvas.delete(self.highlight)
        for i in self.battlefield:
            for j in i:
                if j == gc.NO_UNIT:
                    continue
                j.redraw()

class TurnButton:
    def __init__(self, parent, x, y, max_height):
        self.parent = parent
        self.button = tk.Button(self.parent.root, text = 'Next turn', font = 'Arial 15',
                                bg='yellow', activebackground='#fffada')
        self.button['command'] = self.parent.next_turn
        self.button.place(x=x, y=y)
        self.parent.root.update()
        self.button.update()
        nx, ny = x - self.button.winfo_width() // 2, y - self.button.winfo_height() // 2
        if self.button.winfo_height() > max_height:
            self.button.place(x = nx, y = ny, height=max_height)
        else:
            self.button.place(x = nx, y = ny)

class GameManager:
    def __init__(self, parent):
        self.parent = parent
        self.root = self.parent.root
        self.w = self.root.winfo_width()
        self.h = self.root.winfo_height()
        pad_left = 45
        pad_right = 45
        self.left_menu_bar = LeftMenuBar(self, x = 0, y = 52, width = pad_left, height = self.h - 60)
        self.field = Field(self, x=pad_left, y=50, width = self.w - pad_left - pad_right, height = self.h - 60)
        self.turn_button = TurnButton(self, x=self.w//2, y=25, max_height=50)
    def next_turn(self):
        pass