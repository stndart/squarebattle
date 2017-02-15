import tkinter as tk
from PIL import Image, ImageTk
import game


class LeftMenuBar:
    def __init__(self, parent, x, y, width, height):
        self.parent = parent
        self.frame = tk.Frame(self.parent.root, width=width, height=height, bg='lightblue')
        self.frame.place(x=x, y=y)
        self.buttons = []
        self.icons = dict()

    def new_button(self, image, x, y, meth):
        self.icons[image] = ImageTk.PhotoImage(self.parent.icons[image])
        self.buttons.append(tk.Button(master=self.frame, image=self.icons[image],
                                      bg='white', activebackground='white',
                                      width=self.icons[image].width(),
                                      height=self.icons[image].height(),
                                      command=meth))
        self.buttons[-1].place(x=x, y=y)

    def base_menu(self):
        for i in self.buttons:
            i.destroy()
        self.buttons = []
        self.new_button(image='new', x=0, y=0, meth=self.add_unit)
        self.new_button(image='upgrade', x=0, y=40, meth=self.upgrade_unit)
        self.new_button(image='delete', x=0, y=80, meth=self.remove_unit)
        self.new_button(image='rotate', x=0, y=120, meth=self.rotate_unit)
        self.new_button(image='exit', x=0, y=160, meth=lambda: self.exit(flag='inner'))
    
    def add_unit(self):
        if self.parent.field.game.chosen == (-1, -1):
            self.parent.field.highlight_add_unit()
        else:
            self.parent.field.put_base_unit()
    
    def remove_unit(self):
        if self.parent.field.game.chosen == (-1, -1):
            self.parent.field.highlight_remove_unit()
        else:
            self.parent.field.remove_unit()
    
    def rotate_unit(self):
        if self.parent.field.game.chosen == (-1, -1):
            self.parent.field.highlight_rotate_unit()
        else:
            self.parent.field.rotate_unit()
    
    def upgrade_unit(self):
        if self.parent.field.game.chosen == (-1, -1):
            self.parent.field.highlight_upgrade_unit()
        else:
            self.parent.field.upgrade_unit()

    def choose_square_menu(self, item):
        pass
    
    def exit(self, flag='outer'):
        for b in self.buttons:
            b.destroy()
        self.frame.destroy()
        if flag != 'outer':
            self.parent.exit()
        del self


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
        
        self.game = game.Game(self, sizex, sizey)
        self.chosen_square = None
        self.highlighted_square = None
        self.waitng_for_choice = 'nothing'
        
        self.load_textures()
    
    def load_textures(self):
        self.unit_icons = dict()
        for key in ['unit']:
            im = self.parent.icons[key].resize((self.width // self.sizex - 2, self.height // self.sizey - 2))
            self.unit_icons[key] = [None for i in range(4)]
            for i in range(4):
                self.unit_icons[key][i] = ImageTk.PhotoImage(im.rotate(i * 90))
    
    def resize(self):
        pass

    def click(self, event):
        sx = event.x * self.sizex // self.width
        sy = event.y * self.sizey // self.height
        self.choose_square(sx, sy)

    def mouse_move(self, event):
        sx = event.x * self.sizex // self.width
        sy = event.y * self.sizey // self.height
        self.game.highlight(sx, sy)
        self.redraw()
    
    def highlight_add_unit(self):
        self.waitng_for_choice = 'add_unit'
        pass
    
    def highlight_remove_unit(self):
        self.waitng_for_choice = 'remove_unit'
        pass
    
    def highlight_rotate_unit(self):
        self.waitng_for_choice = 'rotate_unit'
        pass
    
    def highlight_upgrade_unit(self):
        self.waitng_for_choice = 'upgrade_unit'
        pass
    
    def unchoose_square(self):
        self.canvas.delete(self.chosen_square)
        self.chosen_square = None
        self.game.chosen = (-1, -1)
        self.parent.base_menu()
        self.redraw()

    def choose_square(self, sx, sy):
        r = self.game.choose_square(sx, sy)
        if r == 'already_chosen':  # unchoose square
            self.unchoose_square()
        else:
            if self.waitng_for_choice == 'nothing':
                self.parent.choose_square_menu(self.game.get_unit(sx, sy))
                self.redraw()
            elif self.waitng_for_choice == 'add_unit':
                self.put_base_unit()
                self.waitng_for_choice = 'nothing'
            elif self.waitng_for_choice == 'upgrade_unit':
                self.upgrade_unit()
                self.waitng_for_choice = 'nothing'
            elif self.waitng_for_choice == 'remove_unit':
                self.remove_unit()
                self.waitng_for_choice = 'nothing'
            elif self.waitng_for_choice == 'rotate_unit':
                self.rotate_unit()
                self.waitng_for_choice = 'nothing'

    def put_base_unit(self):
        if 'add' not in self.game.available_actions():
            return False
        kek = self.game.put_base_unit()
        self.unchoose_square()
        return kek

    def upgrade_unit(self):
        kek = self.game.upgrade_unit()
        self.unchoose_square()
        return kek

    def remove_unit(self):
        kek = self.game.remove_unit()
        self.unchoose_square()
        return kek
    
    def rotate_unit(self):
        kek = self.game.rotate_unit()
        self.unchoose_square()
        return kek

    def colour_square(self, mode):
        if mode == 'highlight':
            sq = self.highlighted_square
            sc = self.game.highlighted
        if mode == 'chosen':
            sq = self.chosen_square
            sc = self.game.chosen
        if sq is not None:
            self.canvas.delete(sq)
        if sc != (-1, -1):
            x1 = sc[0] * self.width // self.sizex
            y1 = sc[1] * self.height // self.sizey
            x2 = (sc[0] + 1) * self.width // self.sizex
            y2 = (sc[1] + 1) * self.height // self.sizey
            if sc[0] == 0:
                x1 += 1
            if sc[1] == 0:
                y1 += 1
            if mode == 'highlight':
                self.highlighted_square = self.canvas.create_rectangle(x1 + 2, y1 + 2, x2, y2, fill='orange',
                                                                       outline='orange')
            if mode == 'chosen':
                self.chosen_square = self.canvas.create_rectangle(x1 + 2, y1 + 2, x2, y2, fill='red', outline='red')

    def redraw(self):
        self.canvas.delete('temp')
        if self.game.highlighted != (-1, -1):
            self.colour_square('highlight')
        if self.game.chosen != (-1, -1):
            self.colour_square('chosen')
        for i in range(self.sizex):
            for j in range(self.sizey):
                u = self.game.get_unit(i, j)
                if u:
                    x1 = i * self.width // self.sizex
                    y1 = j * self.height // self.sizey
                    x2 = (i + 1) * self.width // self.sizex
                    y2 = (j + 1) * self.height // self.sizey
                    if x1 == 0:
                        x1 += 1
                    if y1 == 0:
                        y1 += 1
                    if isinstance(u, game.gc.Unit):
                        self.canvas.create_image(x1+2, y1+2, anchor='nw', image=self.unit_icons['unit'][u.direction], tag='temp')
                    elif isinstance(u, game.gc.Infantry):
                        pass
                    elif isinstance(u, game.gc.Horeseman):
                        pass
    
    def exit(self):
        self.game.exit()
        self.canvas.destroy()
        del self


class TurnButton:
    def __init__(self, parent, x, y, max_height):
        self.parent = parent
        self.button = tk.Button(self.parent.root, text='Next turn', font='Arial 15',
                                bg='yellow', activebackground='#fffada')
        self.button['command'] = self.parent.next_turn
        if self.button.winfo_height() > max_height:
            self.button.place(x=x, y=y, height=max_height, anchot=tk.CENTER)
        else:
            self.button.place(x=x, y=y, anchor=tk.CENTER)
    
    def exit(self):
        self.button.destroy()
        del self


class GameManager:
    ICONS = {'exit':    'textures/back.png',
             'new':     'textures/new_unit.png',
             'upgrade': 'textures/up_unit.png',
             'delete':  'textures/del_unit.png',
             'rotate':  'textures/rotate_unit.png',
             'unit':    'textures/unit.png'}

    def __init__(self, parent):
        self.parent = parent
        self.root = self.parent.root
        self.w = self.root.winfo_width()
        self.h = self.root.winfo_height()
        pad_left = 45
        pad_right = 45
        self.icons = dict()
        self.load_icons()
        
        self.left_menu_bar = LeftMenuBar(self, x=0, y=52, width=pad_left, height=self.h - 60)
        self.field = Field(self, x=pad_left, y=50, width=self.w - pad_left - pad_right, height=self.h - 60)
        self.turn_button = TurnButton(self, x=self.w // 2, y=25, max_height=50)
        self.base_menu()

    def load_icons(self):
        for name in GameManager.ICONS:
            self.icons[name] = Image.open(GameManager.ICONS[name])

    def next_turn(self):
        self.field.unchoose_square()
        self.field.game.next_turn()
        pass

    def base_menu(self):
        self.left_menu_bar.base_menu()

    def choose_square_menu(self, unit):
        self.left_menu_bar.choose_square_menu(unit)
    
    def exit(self):
        self.left_menu_bar.exit()
        self.field.exit()
        self.turn_button.exit()
        self.parent.to_menu()