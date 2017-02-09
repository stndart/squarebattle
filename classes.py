import tkinter as tk

class LeftMenuBar:
    def __init__(self, parent, root, width, height):
        self.frame = Frame(root, )

class Window():
    def __init__(self, root):
        self.root = root
        self.w = self.root.winfo_width()
        self.h = self.root.winfo_height()
        self.left_menu_bar = LeftMenuBar(self, self.rootwidth=30, height = self.h)
        self.field = Field(self, x=30, y=50, width = self.w - 30 * 2, height = self.h - 60)
        self.turn_button = TurnButton(self, x=self.w//2, y=self.h//2, max_height=50)
    def resize(self):
        pass
    def run(self):
        pass
    def next_turn(self):
        pass