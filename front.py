import tkinter as tk
from tkinter import ttk

root=tk.Tk()
mainframe=ttk.Frame(root,padding='10 10 10 10')
mainframe.grid(column=0,row=0,sticky='news')
mainframe.columnconfigure(0,weight=1)
mainframe.rowconfigure(0,weight=1)



root.mainloop()