import tkinter as tk
from tkinter import ttk, Menu, messagebox
import sqlite3 as sql
import threading
import autofill as autoe
from PIL import Image, ImageTk


class GUI:
    def __init__(self, root, *args):
        # variables
        self.root = root
        self.loadicons()

        # Styles
        c0 = '#F0F4F5'
        c1 = '#8aa4ff'
        c1_5 = '#009ABB'
        c2 = '#5086c1'
        c2_5 = '#007C92'
        c3 = '#5076b0'
        c4 = '#49598c'
        c5 = '#3e476f'
        txt1 = '#ffffff'
        txt2 = '#333333'

        self.style = ttk.Style()
        self.style.configure('.', font=('Helvetica', 10), sticky='nw')
        self.style.configure('Main.TFrame', background=c0)
        self.style.configure('Details.TFrame', background=c1)
        self.style.configure('TLabel', background=c1, foreground=txt2)
        self.style.configure('Det.TLabel', background=c1, foreground=txt1)
        self.style.configure('Main.TLabel', background=c0, foreground=txt2)

        # Global Variables
        self.db = './data/db/medinv'
        self.lista = self.makeList()
        print(self.lista)

        # menubar
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.fmenu = Menu(self.menu)
        self.fmenu.add_command(label='Exit', command=self.destroy)
        self.menu.add_cascade(label='File', menu=self.fmenu)

        # mainframe
        self.mf = ttk.Frame(self.root, style='Main.TFrame')
        self.mf.grid(row=0, column=0)
        self.mf.rowconfigure(1, weight=1)
        self.mf.columnconfigure(1, weight=1)

        # details frame
        self.df = ttk.Frame(self.mf, padding='5 5 5 5', style='Details.TFrame', relief='groove')
        self.df.rowconfigure(1, weight=1)
        self.df.columnconfigure(1, weight=1)

        # Static labels
        ttk.Label(self.mf, text='Medicine Name', style='Main.TLabel').grid(row=0, column=0, sticky='nw', padx=1,
                                                                           pady=20)
        ttk.Label(self.df, text="Amount Available:").grid(row=0, column=0, sticky='nw', pady=5)
        ttk.Label(self.df, text="MMF:").grid(row=0, column=3, sticky='nw', pady=5)
        ttk.Label(self.df, text="Nearest Expiry:").grid(row=1, column=0, sticky='nw', pady=5)
        ttk.Label(self.df, text="Oldest Batch:").grid(row=1, column=3, sticky='nw', pady=5)

        # Active Labels
        self.avilLB = ttk.Label(self.df, text='0', style='Det.TLabel')
        self.expLB = ttk.Label(self.df, text='00/00/00', style='Det.TLabel')
        self.mmfLB = ttk.Label(self.df, text='600', style='Det.TLabel')
        self.oldbtchLB = ttk.Label(self.df, text='Batch-0', style='Det.TLabel')

        # Components
        self.pillEN = autoe.AutocompleteEntry(self.lista, self.mf)

        self.addBut = ttk.Button(self.mf, image=self.plusIco)
        self.subBut = ttk.Button(self.mf, image=self.minusIco)

        # Seperators
        ttk.Separator(self.df, orient='vertical').grid(row=0, column=2, rowspan=4, sticky='nse', padx=5)

        # Design Main Frame
        self.pillEN.grid(row=0, column=1, padx=1, pady=20, sticky='nw')
        self.df.grid(row=1, column=0, columnspan=8,rowspan=5, sticky='nw')
        self.addBut.grid(row=1, column=9, padx=2, sticky='nw')
        self.subBut.grid(row=2, column=9, padx=2, sticky='nw')

        # Design Details Frame
        self.avilLB.grid(row=0, column=1, padx=5, pady=5, sticky='nw')
        self.expLB.grid(row=1, column=1, padx=5, pady=5, sticky='nw')
        self.mmfLB.grid(row=0, column=4, padx=5, pady=5, sticky='nw')
        self.oldbtchLB.grid(row=1, column=4, padx=5, pady=5, sticky='nw')

        # Binds/Focus
        self.pillEN.focus()
        self.pillEN.bind("<Return><Return>", func=self.go)

        # Functions

    def destroy(self):
        self.root.destroy()

    def makeList(self):
        try:
            ls = []
            con = sql.connect(self.db)
            cur = con.cursor()
            cur.execute('select name from namelist')
            for dets in cur.fetchall():
                ls.append(dets[0])
            return ls
        except sql.OperationalError:
            messagebox.showinfo('Error', 'Database not found, using default data')
            return [1, 2, 3, 4]

    def go(self, *args):
        print('WENT!!', self.pillEN.get())

    def loadicons(self):
        self.original = Image.open('.//data//img//plus.png')
        resized = self.original.resize((25, 25), Image.ANTIALIAS)
        self.plusIco = ImageTk.PhotoImage(resized)

        self.original = Image.open('.//data//img//minus.png')
        resized = self.original.resize((25, 25), Image.ANTIALIAS)
        self.minusIco = ImageTk.PhotoImage(resized)


class Func:
    def __init__(self):
        pass


class App:
    def __init__(self, master):
        self.gui = GUI(master)
        pass


def main():
    root = tk.Tk()
    root.title('MedInventory')
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
