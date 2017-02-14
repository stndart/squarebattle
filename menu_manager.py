import tkinter as tk


class CenterFrame:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent.root)
        self.frame.place(x=self.parent.root.winfo_width() // 2,
                         y=self.parent.root.winfo_height() // 2,
                         anchor=tk.CENTER)
    def exit(self):
        self.frame.destroy()


class MainButton:
    def __init__(self, parent):
        self.parent = parent
        self.button = tk.Button(self.parent.center_frame.frame, font='Arial 40', text='Start',
                                background='lightgreen', activebackground='orange',
                                foreground='red', activeforeground='blue')
        self.button['command'] = self.parent.start_game
        #self.button.place(x=self.parent.root.winfo_width() // 2,
                          #y=self.parent.root.winfo_height() // 2,
                          #anchor=tk.CENTER)
        self.button.pack(anchor='w')
    
    def exit(self):
        self.button.destroy()
        del self


class ExitButton:
    def __init__(self, parent):
        self.parent = parent
        self.button = tk.Button(self.parent.center_frame.frame, font='Arial 40', text='Exit',
                                background='pink', activebackground='lightblue',
                                foreground='blue', activeforeground='red')
        self.button['command'] = self.parent.root.destroy
        self.button.pack(anchor='s')
    
    def exit(self):
        self.button.destroy()
        del self

class MenuManager:
    def __init__(self, parent):
        self.parent = parent
        self.root = self.parent.root
        self.w = self.root.winfo_width()
        self.h = self.root.winfo_height()
        self.center_frame = CenterFrame(self)
        self.main_button = MainButton(self)
        self.exit_button = ExitButton(self)

    def start_game(self):
        self.parent.start_game()
        self.exit()
    
    def exit(self):
        self.main_button.exit()