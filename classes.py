import tkinter as tk
import game_classes as gc
from game_manager import GameManager
from menu_manager import MenuManager

class Window():
    WAITING = 'waiting'
    MENU =  'menu'
    GAME = 'single game'
    def __init__(self, root):
        self.root = root
        self.state = Window.WAITING
    def resize(self):
        pass
    def run(self):
        if self.state != Window.WAITING:
            pass  # error handler?
        self.state = Window.GAME
        self.menu_manager = MenuManager(self)
    def start_game(self):
        if self.state != Window.MENU:
            pass  # error handler?
        del self.menu_manager
        self.state = Window.GAME
        self.menu_manager = GameManager(self)