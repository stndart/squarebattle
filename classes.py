import tkinter as tk

class LeftMenuBar:
    def __init__(self, parent, x, y, width, height):
        self.parent = parent
        self.frame = tk.Frame(self.parent.root, width=width, height=height, bg='blue')
        self.frame.place(x=x, y=y)

class Field:
    def __init__(self, parent, x, y, width, height):
        self.parent = parent
        self.canvas = tk.Canvas(width=width, height=height, bg='red')
        self.canvas.place(x=x, y=y)

class TurnButton:
    def __init__(self, parent, x, y, max_height):
        self.parent = parent
        self.button = tk.Button(self.parent.root, text = 'Next turn', font = 'Arial 15', bg='yellow')
        self.button.place(x=x, y=y)
        self.parent.root.update()
        self.button.update()
        nx, ny = x - self.button.winfo_width() // 2, y - self.button.winfo_height() // 2
        if self.button.winfo_height() > max_height:
            self.button.place(x = nx, y = ny, height=max_height)
        else:
            self.button.place(x = nx, y = ny)

class Window():
    def __init__(self, root):
        self.root = root
        self.w = self.root.winfo_width()
        self.h = self.root.winfo_height()
        pad_left = 45
        pad_right = 45
        self.left_menu_bar = LeftMenuBar(self, x = 0, y = 52, width = pad_left, height = self.h - 60)
        self.field = Field(self, x=pad_left, y=50, width = self.w - pad_left - pad_right, height = self.h - 60)
        self.turn_button = TurnButton(self, x=self.w//2, y=25, max_height=50)
    def resize(self):
        pass
    def run(self):
        pass
    def next_turn(self):
        pass