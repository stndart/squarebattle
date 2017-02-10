import tkinter
import classes

root = tkinter.Tk()
root.geometry('700x600')
root.bind('Alt-<F4>', lambda e: root.destroy())
root.bind('<Escape>', lambda e: root.destroy())
root.update()
w1 = classes.Window(root)
root.after(100, w1.run)
root.mainloop()