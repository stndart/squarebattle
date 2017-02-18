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
    
    def key_bind(self, key, meth):
        self.parent.root.bind(key, lambda e: meth())

    def base_menu(self):
        for i in self.buttons:
            i.destroy()
        self.buttons = []
        self.new_button(image='new', x=0, y=0, meth=self.add_unit)
        self.key_bind(key='a', meth=self.add_unit)
        self.new_button(image='upgrade', x=0, y=40, meth=self.upgrade_unit)
        self.new_button(image='delete', x=0, y=80, meth=self.remove_unit)
        self.new_button(image='rotate', x=0, y=120, meth=self.rotate_unit)
        self.new_button(image='exit', x=0, y=160, meth=lambda: self.exit(flag='inner'))
    
    def add_unit(self):
        if 'add' in self.parent.field.game.available_actions():
            if self.parent.field.game.chosen == (-1, -1):
                self.parent.field.highlight_add_unit()
            else:
                self.parent.field.put_base_unit()
    
    def remove_unit(self):
        if 'remove' in self.parent.field.game.available_actions():
            if self.parent.field.game.chosen == (-1, -1):
                self.parent.field.highlight_remove_unit()
            else:
                self.parent.field.remove_unit()
    
    def rotate_unit(self):
        if 'rotate' in self.parent.field.game.available_actions():
            if self.parent.field.game.chosen == (-1, -1):
                self.parent.field.highlight_rotate_unit()
            else:
                self.parent.field.rotate_unit()
    
    def upgrade_unit(self):
        if 'upgrade' in self.parent.field.game.available_actions():
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


class TurnButton:
    def __init__(self, parent, max_height, side=tk.BOTTOM):
        self.parent = parent
        self.button = tk.Button(self.parent.frame, text='Next turn', font='Arial 15',
                                bg='yellow', activebackground='#fffada')
        self.button['command'] = self.parent.parent.next_turn
        self.button.pack(side=side)
        self.parent.parent.root.bind('t', lambda e: self.parent.parent.next_turn())
    
    def exit(self):
        self.button.destroy()
        self.parent.exit()

class FightButton:
    def __init__(self, parent, max_height, side=tk.BOTTOM):
        self.parent = parent
        self.button = tk.Button(self.parent.frame, text='Fight!', font='Arial 15',
                                bg='red', activebackground='#f47980')
        self.button['command'] = self.parent.parent.field.fight
        self.button.pack(side=side)
        self.parent.parent.root.bind('f', lambda e: self.parent.parent.field.fight())
    
    def exit(self):
        self.button.destroy()
        self.parent.exit()


class TopMenuBar:
    def __init__(self, parent, x, y, max_height):
        self.parent = parent
        self.frame = tk.Frame(self.parent.root, height=max_height, width=self.parent.root.winfo_width(), bg='red')
        self.frame.place(x=x, y=y, anchor=tk.CENTER)
        self.turn_button = TurnButton(self, max_height, side=tk.LEFT)
        self.fight_button = FightButton(self, max_height, side=tk.RIGHT)
    
    def exit(self):
        del self.turn_button
        self.frame.destroy()
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
        self.cursor_on_square = None
        self.waitng_for_choice = 'nothing'
        self.highlighted_add_unit = set()
        self.highlighted_remove_unit = set()
        self.highlighted_rotate_unit = set()
        self.highlighted_upgrade_unit = set()
        
        self.unit_icons = dict()
        self.textures = dict()
        self.load_textures()
        self.redraw()
    
    def load_textures(self):
        self.unit_icons = dict()
        for key in ['unit', 'base_1', 'base_2']:
            im = self.parent.icons[key].resize((self.width // self.sizex - 2, self.height // self.sizey - 2))
            self.unit_icons[key] = [None for i in range(4)]
            if key.startswith('base'):
                self.unit_icons[key] = ImageTk.PhotoImage(im)
            else:
                for i in range(4):
                    self.unit_icons[key][i] = ImageTk.PhotoImage(im.rotate(i * 90))
        self.textures = dict()
        for key in ['highlight_add', 'highlight_upgrade', 'highlight_remove', 'highlight_rotate']:
            im = self.parent.icons[key].resize((self.width // self.sizex - 2, self.height // self.sizey - 2))
            self.textures[key] = ImageTk.PhotoImage(im)
    
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
        if self.highlighted_add_unit:
            self.unhighlight()
            return
        self.unhighlight()
        self.waitng_for_choice = 'add_unit'
        for i in range(self.sizex):
            for j in range(self.sizey):
                if self.game.get_unit(i, j) and self.game.get_unit(i, j).side == self.game.current_player:
                    good = lambda x, y: 0 <= x < self.sizex and 0 <= y < self.sizey
                    for arg in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                        if good(*arg):
                            self.highlighted_add_unit.add(arg)
        self.redraw()
    
    def highlight_remove_unit(self):
        if self.highlighted_remove_unit:
            self.unhighlight()
            return
        self.unhighlight()
        self.waitng_for_choice = 'remove_unit'
        for i in range(self.sizex):
            for j in range(self.sizey):
                if self.game.get_unit(i, j) and self.game.get_unit(i, j).side == self.game.current_player:
                    if self.game.get_unit(i, j).removable:
                        self.highlighted_remove_unit.add((i, j))
        self.redraw()
    
    def highlight_rotate_unit(self):
        if self.highlighted_rotate_unit:
            self.unhighlight()
            return
        self.unhighlight()
        self.waitng_for_choice = 'rotate_unit'
        for i in range(self.sizex):
            for j in range(self.sizey):
                if self.game.get_unit(i, j) and self.game.get_unit(i, j).side == self.game.current_player:
                    if self.game.get_unit(i, j).rotatable:
                        self.highlighted_rotate_unit.add((i, j))
        self.redraw()
    
    def highlight_upgrade_unit(self):
        if self.highlighted_upgrade_unit:
            self.unhighlight()
            return
        self.unhighlight()
        self.waitng_for_choice = 'upgrade_unit'
        for i in range(self.sizex):
            for j in range(self.sizey):
                if self.game.get_unit(i, j) and self.game.get_unit(i, j).side == self.game.current_player:
                    if self.game.get_unit(i, j).upgradeable:
                        self.highlighted_upgrade_unit.add((i, j))
        self.redraw()
    
    def unhighlight(self):
        self.highlighted_add_unit = set()
        self.highlighted_remove_unit = set()
        self.highlighted_rotate_unit = set()
        self.highlighted_upgrade_unit = set()
        self.waitng_for_choice = 'nothing'
        self.canvas.delete('temp2')
        pass
    
    def unchoose_square(self):
        self.unhighlight()
        
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
        if self.waitng_for_choice == 'nothing':
            self.unhighlight()

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
    
    def fight(self):
        self.game.fight()
        self.unchoose_square()
        self.unhighlight()
        self.redraw()

    def colour_square(self, mode):
        if mode == 'cursor':
            sq = self.cursor_on_square
            sc = self.game.highlighted
            if self.game.current_player == game.gc.PLAYER1:
                hc = 'red'
            else:
                hc = 'blue'
        if mode == 'chosen':
            sq = self.chosen_square
            sc = self.game.chosen
            hc2 = 'green'
        
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
            if mode == 'cursor':
                self.cursor_on_square = self.canvas.create_rectangle(x1 + 2, y1 + 2, x2, y2,
                                                                     fill=hc, outline=hc)
            if mode == 'chosen':
                self.chosen_square = self.canvas.create_rectangle(x1 + 2, y1 + 2, x2, y2,
                                                                  fill=hc2, outline=hc2)

    def redraw(self):
        self.canvas.delete('temp')
        self.canvas.delete('temp2')
        if self.game.highlighted != (-1, -1):
            self.colour_square('cursor')
        if self.game.chosen != (-1, -1):
            self.colour_square('chosen')
        for i in range(self.sizex):
            for j in range(self.sizey):
                x1 = i * self.width // self.sizex
                y1 = j * self.height // self.sizey
                x2 = (i + 1) * self.width // self.sizex
                y2 = (j + 1) * self.height // self.sizey
                if x1 == 0:
                    x1 += 1
                if y1 == 0:
                    y1 += 1
                if (i, j) in self.highlighted_remove_unit:
                    self.canvas.create_image(x1+2, y1+2, anchor='nw', image=self.textures['highlight_remove'], tag='temp2')
                if (i, j) in self.highlighted_rotate_unit:
                    self.canvas.create_image(x1+2, y1+2, anchor='nw', image=self.textures['highlight_rotate'], tag='temp2')
                if (i, j) in self.highlighted_upgrade_unit:
                    self.canvas.create_image(x1+2, y1+2, anchor='nw', image=self.textures['highlight_upgrade'], tag='temp2')
                
                u = self.game.get_unit(i, j)
                if u:
                    if u.__class__ is game.gc.Unit:
                        self.canvas.create_image(x1+2, y1+2, anchor='nw', image=self.unit_icons['unit'][u.direction], tag='temp')
                    elif u.__class__ is game.gc.Infantry:
                        pass
                    elif u.__class__ is game.gc.Horseman:
                        pass
                    elif u.__class__ is game.gc.Base:
                        if u.side == game.gc.PLAYER1:
                            self.canvas.create_image(x1+2, y1+2, anchor='nw', image=self.unit_icons['base_1'], tag='base')
                        else:
                            self.canvas.create_image(x1+2, y1+2, anchor='nw', image=self.unit_icons['base_2'], tag='base')
                else:
                    if (i, j) in self.highlighted_add_unit:
                        self.canvas.create_image(x1+2, y1+2, anchor='nw', image=self.textures['highlight_add'], tag='temp2')
    
    def exit(self):
        self.game.exit()
        self.canvas.destroy()
        del self


class GameManager:
    ICONS = {'exit':    'textures/back.png',
             'new':     'textures/new_unit.png',
             'upgrade': 'textures/up_unit.png',
             'delete':  'textures/del_unit.png',
             'rotate':  'textures/rotate_unit.png',
             'unit':    'textures/unit.png',
             'base_1':    'textures/base_1.png',
             'base_2':    'textures/base_2.png',
             'highlight_add':     'textures/new_available.png',
             'highlight_rotate':  'textures/rotate_available.png',
             'highlight_remove':  'textures/remove_available.png',
             'highlight_upgrade': 'textures/upgrade_available.png'}

    def __init__(self, parent):
        self.parent = parent
        self.root = self.parent.root
        self.w = self.root.winfo_width()
        self.h = self.root.winfo_height()
        pad_left = 45
        pad_right = 45
        self.icons = dict()
        self.load_icons()
        
        self.field = Field(self, x=pad_left, y=50, width=self.w - pad_left - pad_right, height=self.h - 60)
        self.left_menu_bar = LeftMenuBar(self, x=0, y=52, width=pad_left, height=self.h - 60)
        self.top_menu_bar = TopMenuBar(self, x=self.w//2, y=25, max_height=50)
        self.base_menu()

    def load_icons(self):
        for name in GameManager.ICONS:
            self.icons[name] = Image.open(GameManager.ICONS[name])

    def next_turn(self):
        self.field.unchoose_square()
        self.field.game.next_turn()
        self.field.redraw()
        pass

    def base_menu(self):
        self.left_menu_bar.base_menu()

    def choose_square_menu(self, unit):
        self.left_menu_bar.choose_square_menu(unit)
    
    def exit(self):
        self.left_menu_bar.exit()
        self.top_menu_bar.exit()
        self.field.exit()
        self.parent.to_menu()