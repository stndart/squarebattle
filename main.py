import tkinter
import classes

if __name__ == '__main__':
    root = tkinter.Tk()
    root.geometry('700x600')
    root.resizable(False, False)  # Until we have classes.Windon.resize method
    root.bind('Alt-<F4>', lambda e: root.destroy())
    root.bind('<Escape>', lambda e: root.destroy())
    root.update()
    w1 = classes.Window(root)
    root.after(100, w1.run)
    root.mainloop()