import tkinter as tk
from tkinter import ttk
import sqlite3 as sql
import threading
import autofill as auto


class GUI:
    def __init__(self,root):
        self.root=root
        self.mf=ttk.Frame(self.root)
        pass


class Func:
    def __init__(self):
        pass


class App:
    def __init__(self, master):
        pass


def main():
    root = tk.Tk()
    root.title('MedInventory')
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
