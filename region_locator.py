import threading
import pyautogui
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox




class region_locator_GUI(Toplevel):
    def __init__(self, master = None):
        super().__init__(master = master)
        self._fields = "x","y","Width","Height"
        self.title('Region Locator')
        self.resizable(0, 0)
        self.geometry('340x320')
        self['bg'] = 'black'

        # change the background color to black
        self._style = ttk.Style(self)
        self._style.configure(
            'TLabel',
            background='black',
            foreground='red')
        
        # label
        self._ents = self.generate_field(["x","y","width","height"])
         
        self._label = ttk.Label(
            self,
            text='x:y',
            font=('Digital-7', 40))

        self._label.pack(expand=True)
        self._label.after(1000, self.update)
        

        self.bind('<Return>', (lambda event, e=self._ents : self.screen_shot(e))) 
        self._button = ttk.Button(
            self, 
            text='Screenshot',
            command=lambda e=self._ents: self.screen_shot(e))
        self._button.pack(expand=True, ipadx=10, ipady=2)

    
    
    def generate_field(self, fields):
        entries = []
        for field in fields:
            frame = tk.Frame(self)
            lab = tk.Label(frame, width=8, text=field, font=('Helvetica', 10), anchor='c')
            ent = tk.Entry(frame, width=5, textvariable = IntVar(), justify='c')
            frame.pack(side=tk.TOP, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT)
            entries.append((field, ent))
        return entries

    def screen_shot(self, ents):
        x, y , wid, hgt = ents[0][1].get(), ents[1][1].get(), ents[2][1].get(), ents[3][1].get()
        try:
            im = pyautogui.screenshot(region=(x,y,wid, hgt))
            im.show()
        except:
            messagebox.showwarning("Invalid input", "Dimension is not valid!")

    def locator(self):
        x, y = pyautogui.position()
        return "{0}:{1}".format(x,y)

    def update(self):
        self.label.configure(text = self.locator())
        self.label.after(100, self.update)


    