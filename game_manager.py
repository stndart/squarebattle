import tkinter as tk
import game_classes as gc
from PIL import Image, ImageTk


class LeftMenuBar:
    def __init__(self, parent, x, y, width, height):
        self.parent = parent
        self.frame = tk.Frame(self.parent.root, width=width, height=height, bg='lightblue')
        self.frame.place(x=x, y=y)
        self.buttons = []
        self.base_menu
    def new_button(self, image, x, y):
        self.buttons.append(tk.Button(master=self.frame, image=self.parent.icons[image],
                                   width=self.parent.icons[image].width(),
                                   height=self.parent.icons[image].height()))
        self.buttons[-1].place(x=x, y=y)
    def base_menu(self):
        for i in self.buttons:
            i.destroy()
        self.new_button(image='new', x=0, y=0)
        self.new_button(image='upgrade', x=0, y=40)
        self.new_button(image='delete', x=0, y=80)
    def choose_square_menu(self):
        pass

class Field:
    HIGHLIGHT_COLOUR = 'red'
    CHOSEN_COLOUR = 'orange'
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
        self.canvas.bind('<Motion>', self.mouse_move)
        self.chosen_square = None
        self.highlighted_square = None
        self.highlighted = (-1, -1)
        self.chosen = (-1, -1)
    def click(self, event):
        sx = event.x * self.sizex // self.width
        sy = event.y * self.sizey // self.height
        self.choose_square(sx, sy)
    def mouse_move(self, event):
        sx = event.x * self.sizex // self.width
        sy = event.y * self.sizey // self.height
        self.highlighted = (sx, sy)
        self.redraw()
    def choose_square(self, sx, sy):
        if self.chosen == (sx, sy):
            self.canvas.delete(self.chosen_square)
            self.chosen_square = None
            self.chosen = (-1, -1)
            self.parent.base_menu()
        else:
            self.chosen = (sx, sy)
            self.parent.choose_square_menu(self.battlefield[sy][sx])
        self.redraw()
    def put_base_unit(self):
        new_unit = gc.Unit(self.choice, gc.PLAYER1, (+1, 0))
        self.battlefield[sy][sx] = new_unit
    def upgrade_unit(self, choice):
        pass
    def delete_unit(self):
        pass
    def colour_square(self, mode):
        if mode == 'highlight':
            sq = self.highlighted_square
            sc = self.highlighted
        if mode == 'chosen':
            sq = self.chosen_square
            sc = self.chosen
        if sq is not None:
            self.canvas.delete(sq)
        if sc != (-1, -1):
            x1 = sc[0] * self.width // self.sizex
            y1 = sc[1] * self.height // self.sizey
            x2 = (sc[0] + 1) * self.width // self.sizex
            y2 = (sc[1] + 1) * self.height // self.sizey
            if mode == 'highlight':
                self.highlighted_square = self.canvas.create_rectangle(x1+2, y1+2, x2, y2, fill='orange', outline='orange')
            if mode == 'chosen':
                self.chosen_square = self.canvas.create_rectangle(x1+2, y1+2, x2, y2, fill='red', outline='red')
    def redraw(self):
        if self.highlighted != (-1, -1):
            self.colour_square('highlight')
        if self.chosen != (-1, -1):
            self.colour_square('chosen')
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
        if self.button.winfo_height() > max_height:
            self.button.place(x = x, y = y, height=max_height, anchot=tk.CENTER)
        else:
            self.button.place(x = x, y = y, anchor=tk.CENTER)

class GameManager:
    ICONS = {'new': 'textures/new_unit.png',
             'upgrade': 'textures/up_unit.png',
             'delete': 'textures/del_unit.png'}
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
        self.icons = dict()
        self.load_icons()
        self.base_menu()
    def load_icons(self):
        for name in GameManager.ICONS:
            self.icons[name] = ImageTk.PhotoImage(Image.open(GameManager.ICONS[name]))
            print(self.icons[name].height(), self.icons[name].width())
    def next_turn(self):
        pass
    def base_menu(self):
        self.left_menu_bar.base_menu()
    def choose_square_menu(self, item):
        self.left_menu_bar.choose_square_menu()