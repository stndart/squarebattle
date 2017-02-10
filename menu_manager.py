import tkinter as tk


class MainButton:
    def __init__(self, parent):
        self.parent = parent
        self.button = tk.Button(self.parent.root, font='Arial 40', text='Start',
                                background = 'lightgreen', activebackground = 'orange',
                                foreground='red', activeforeground='blue')
        self.button['command'] = self.parent.start_game
        self.button.place(x=self.parent.root.winfo_width()//2,
                          y=self.parent.root.winfo_height()//2,
                          anchor=tk.CENTER)

class MenuManager:
    def __init__(self, parent):
        self.parent = parent
        self.root = self.parent.root
        self.w = self.root.winfo_width()
        self.h = self.root.winfo_height()
        self.main_button = MainButton(self)
    def start_game(self):
        self.parent.start_game()