import skipper
import sys
from datetime import datetime, timedelta
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
import threading

Font_tuple = ("Comic Sans MS", 9, "bold")
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self._fields = 'Start frame','Duration','Num of episodes','Resolution' 
        self._check_boxes = 'Recap','Intro' 
        self.title("Netflix Skipperino")
        self.resizable(False,False)
        self.geometry("400x300")
        self['bg'] = 'black'

        self._thread = None
        self._ents, self._bxes = self.build_GUI(self._fields, self._check_boxes)
    
        self.style = ttk.Style(self)
        self.style.configure(
            'TLabel',
            background='black',
            foreground='red')


        self.bind('<Return>', (lambda event, e=self._ents, b = self._bxes: self.start_skipper(e,b)))   
        self._start_btn = tk.Button(
            self, 
            width = 5,
            relief = tk.RIDGE, 
            text='Start',
            command = lambda e=self._ents, b=self._bxes : self.start_skipper(e,b))

        self._stop_btn = tk.Button(
            self, 
            width = 5,
            relief = tk.RIDGE, 
            text='Stop', 
            command= self.pause)
        
        self._start_btn.pack()
        self._stop_btn.pack() 
        self._stop_btn.place(relx=0.60, rely=0.9, anchor=CENTER)
        self._start_btn.place(relx=0.42, rely=0.9, anchor=CENTER)

    def pause(self):
        if self._thread and self._thread.is_alive():
            self._thread.pause()
            self._thread.join()
        else:
            print("shit not working")

    def start_skipper(self, entries = [], boxes = []):
        self._thread = skipper.netflix_skipperino()
        for e in entries:
            if e[0] == "Num of episodes":
                self._thread.total_episode = int(e[1].get())
            if e[0] == "Start frame":
                self._thread.start_time = int(e[1].get())
            
        for b in boxes:
            if b[0] == "recap" and b[1].get():
                self._thread.recap = True
            if b[0] == "intro" and b[1].get():
                self._thread.intro = True
        
        self._thread.start()
              

    def build_GUI(self, fields, check_boxes):
        entries = []
        boxes = []
        for field in fields:
            frame = tk.Frame(self)
            lab = tk.Label(frame, width=15, fg='#E50914', text=field, font=Font_tuple, anchor=W)
            ent = tk.Entry(frame, fg='#E50914', textvariable = IntVar(), justify = 'c')
            frame.pack(side=tk.TOP, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT)
            entries.append((field, ent))
        
        for box in check_boxes:
            frame = tk.Frame(self)
            button = Checkbutton(frame, text=box, variable=BooleanVar(), width=5, anchor = W)
            frame.pack(side = tk.TOP, pady=5)
            button.pack()
            boxes.append((box, button))
        return entries, boxes


if __name__=="__main__":
    App().mainloop()