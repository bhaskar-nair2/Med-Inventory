import tkinter as tk
from tkinter import ttk, Menu, messagebox, Text
import sqlite3 as sql
import threading
import autofill as autoe
from PIL import Image, ImageTk

import time


#database and tables
# database: medinv
# nameTable: nameList
# dataTable: medDetails
# Log Table: <pillname>_log
# test Tabel: testVals


class GUI:
    def __init__(self, root, **kwargs):
        # variables
        self.root = root
        self.loadicons()

        # Functions
        self.getVals = kwargs['DetailsFunc']

        # Styles
        c0_5 = '#F0F4F5'
        c0 = '#a1e0ff'
        c1_2 = '#8aa4ff'
        c1 = '#8bc3f6'
        c1_3 = '#51acff'
        c1_5 = '#009ABB'
        c2 = '#5086c1'
        c2_2 = '#2f86ff'
        c2_3 = '#0051ff'
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
        self.style.configure('Main.TLabel', background=c0)
        self.style.configure('TButton', foreground=c1, background=c1)

        # Global Variables
        self.db = './data/db/medinv'
        self.lista = self.makeList()

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

        # Low Quantity Frame
        self.lqf = ttk.Labelframe(self.root, text='Items low in Quantity', style='Main.TFrame', relief='groove')
        self.lqf.grid(row=0, column=1, rowspan=5)
        self.lqf.rowconfigure(1, weight=1)
        self.lqf.columnconfigure(1, weight=1)

        # About to expire frame
        self.expf = ttk.Labelframe(self.root, text='Items about to expire', style='Main.TFrame', relief='groove')
        self.expf.grid(row=0, column=3, rowspan=5)
        self.expf.rowconfigure(1, weight=1)
        self.expf.columnconfigure(1, weight=1)

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
        self.medIco = ttk.Label(self.mf, image=self.clockIco, style='Main.TLabel')

        # Components
        self.pillEN = autoe.AutocompleteEntry(self.lista, self.mf, width=40)
        self.addBut = ttk.Button(self.mf, image=self.plusIco)
        self.subBut = ttk.Button(self.mf, image=self.minusIco)
        self.log = Text(self.mf, width=47, height=20)
        # self.log.yview_pickplace("end")

        # Seperators
        ttk.Separator(self.df, orient='vertical').grid(row=0, column=2, rowspan=4, sticky='nse', padx=20)

        # Design Main Frame
        self.pillEN.grid(row=0, column=1, padx=1, pady=20, columnspan=2, sticky='nw')
        self.medIco.grid(row=0, column=2, sticky='w')
        self.df.grid(row=1, column=0, columnspan=8, rowspan=5, sticky='nw', padx=3, pady=2)
        self.addBut.grid(row=1, column=9, padx=2, sticky='nw')
        self.subBut.grid(row=2, column=9, padx=2, sticky='nw')
        self.log.grid(row=3, column=0, columnspan=12, rowspan=5, sticky='nw', pady=5, padx=2)

        # Design Details Frame
        self.avilLB.grid(row=0, column=1, padx=5, pady=5, sticky='nw')
        self.expLB.grid(row=1, column=1, padx=5, pady=5, sticky='nw')
        self.mmfLB.grid(row=0, column=4, padx=5, pady=5, sticky='nw')
        self.oldbtchLB.grid(row=1, column=4, padx=5, pady=5, sticky='nw')

        # Design, Low quantity frame

        # Binds/Focus
        self.pillEN.focus()
        self.pillEN.bind("<Return><Return>", func=self.go)
        self.pillEN.bind("<BackSpace>", func=self.reset)

        # Functions

    def reset(self, *args):
        self.medIco['image'] = self.clockIco
        self.avilLB['text'] = 0

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
        self.getVals(self.pillEN.get())
        print('WENT!!', self.pillEN.get())

    def loadicons(self):
        smallIco = (25, 25)
        vSmallIco = (15, 15)
        self.original = Image.open('.//data//img//plus.png')
        resized = self.original.resize(smallIco, Image.ANTIALIAS)
        self.plusIco = ImageTk.PhotoImage(resized)

        self.original = Image.open('.//data//img//minus.png')
        resized = self.original.resize(smallIco, Image.ANTIALIAS)
        self.minusIco = ImageTk.PhotoImage(resized)

        self.original = Image.open('.//data//img//cancel.png')
        resized = self.original.resize(vSmallIco, Image.ANTIALIAS)
        self.cancelIco = ImageTk.PhotoImage(resized)

        self.original = Image.open('.//data//img//checked.png')
        resized = self.original.resize(vSmallIco, Image.ANTIALIAS)
        self.checkedIco = ImageTk.PhotoImage(resized)

        self.original = Image.open('.//data//img//clock.png')
        resized = self.original.resize(vSmallIco, Image.ANTIALIAS)
        self.clockIco = ImageTk.PhotoImage(resized)


class Func:
    def __init__(self, gui, db):
        self.gui = gui
        self.db = db
        pass

    def getVal(self, val):
        con = sql.connect(self.db)
        cur = con.execute("select * from namelist where name like \"" + val + '"')
        values = cur.fetchall()
        if not values == []:
            #TODO: Add a try-except here!
            self.gui.medIco['image'] = self.gui.checkedIco
            self.gui.avilLB['text'] = values[0][1]
        else:
            self.gui.medIco['image'] = self.gui.cancelIco

class App:
    def __init__(self, master):
        self.gui = GUI(master, DetailsFunc=self.getDetails)
        self.funs = Func(self.gui, self.gui.db)

    def getDetails(self, val):
        self.thred = threading.Thread(target=self.funs.getVal, args=[val])
        self.thred.start()


def main():
    root = tk.Tk()
    root.iconbitmap(default='.//favicon.ico')
    root.title('MedInventory')
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
