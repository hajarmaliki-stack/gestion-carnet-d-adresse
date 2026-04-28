from tkinter import *
from tkinter import ttk
import adresse_book

from matplotlib.pylab import number


class Contact_GUI:
    def __init__(self, root):
        root.title("Contact's Carnet")
        mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.name = StringVar()
        self.email = StringVar()
        self.number = StringVar()

        name_entry = ttk.Entry(mainframe, width=20, textvariable=self.name)
        name_entry.grid(column=2, row=1, sticky=(W, E))  

        email_entry = ttk.Entry(mainframe, width=20, textvariable=self.email)
        email_entry.grid(column=2, row=2, sticky=(W, E))

        number_entry = ttk.Entry(mainframe, width=20, textvariable=self.number)
        number_entry.grid(column=2, row=3, sticky=(W, E))

        #definir les labels
        ttk.Label(mainframe, text="Nom").grid(column=1, row=1, sticky=W)
        ttk.Label(mainframe, text="Email").grid(column=1, row=2, sticky=W)
        ttk.Label(mainframe, text="Numéro").grid(column=1, row=3, sticky=W)  

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(2, weight=1)  

        ttk.Button(mainframe, text="Réinitialiser").grid(column=1, row=4, sticky=W)


root = Tk()
Contact_GUI(root)
root.mainloop()
