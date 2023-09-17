import tkinter as tk
from tkinter import *
from tkterm import Terminal

root = tk.Tk()

terminal = Terminal(root)
terminal.pack(fill=BOTH, expand=True)

root.mainloop()