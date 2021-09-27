import skipper
import time
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
import threading

Font_tuple = ('Digital-7', 9, 'bold')
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self._fields = 'Start frame','Duration','# of episodes' 
        self._check_boxes = 'Recap','Intro' 
        self._thread = None

        self.title("Netflix Skipperino")
        self.resizable(False,False)
        self.geometry("400x340")
        self['bg'] = '#0F0503'
        self._title = ttk.Label(
            self,
            borderwidth	 = 5,
            text = 'XKIPPER',
            font = ('Digital-7', 15, 'bold')
        )
        self._title.pack(padx=5, anchor = CENTER)
        
        #Generate fields for GUI
        self._ents, self._bxes = self.build_GUI(self._fields, self._check_boxes)

        self.style = ttk.Style(self)
        self.style.configure(
            'TLabel',
            background='black',
            foreground='red')

        
        #Define button binding
        self.bind('<Return>', (lambda event, e=self._ents, b = self._bxes: self.start_skipper(e,b)))   
        
        self._status_bar = ttk.Label(
            self,
            font = Font_tuple,
            foreground = '#E50914')

        self._start_btn = tk.Button(
            self, 
            width = 5,
            relief = tk.RIDGE,
            fg='#E50914',
            font = Font_tuple,
            text='Start',
            command = lambda e=self._ents, b=self._bxes : self.start_skipper(e,b))

        self._stop_btn = tk.Button(
            self, 
            width = 5,
            relief = tk.RIDGE,
            font = Font_tuple, 
            text='Stop', 
            command= self.stop)
        
        self._status_bar.pack(pady = 15, anchor=CENTER)
        self._start_btn.pack()
        self._stop_btn.pack() 
        self._stop_btn.place(relx=0.58, rely=0.85, anchor=CENTER)
        self._start_btn.place(relx=0.43, rely=0.85, anchor=CENTER)


    #Update status of tool
    def status_update(self):
        status = self._thread.status
        self._status_bar.config(text = status)
        self._status_bar.after(1000, self.status_update)


    def stop(self):
        print("active threads", threading.active_count())
        if self._thread and self._thread.is_alive():
            self._thread.pause()
            self._thread.join()
        else:
            messagebox.showerror("Error", "Tool is not running")


    def build_GUI(self, fields, check_boxes):
        entries = []
        boxes = []
        for field in fields:
            frame = tk.Frame(self)
            lab = tk.Label(frame, width=15, fg='#E50914', text=field, font=Font_tuple, anchor=W)
            ent = tk.Entry(frame, width=5, bg = '#EDDBD7', fg='#0F0302', font=Font_tuple, textvariable = IntVar(), justify = 'c')
            frame.pack(side=TOP, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT)
            entries.append((field, ent))
        
        for box in check_boxes:
            frame = tk.Frame(self)
            button = Checkbutton(
                frame, 
                text=box, 
                relief = SUNKEN,
                font = Font_tuple, 
                fg='#E50914',
                variable=BooleanVar(), 
                width=5, 
                anchor = W)
            frame.pack(side=TOP, pady=5)
            button.pack()
            boxes.append((box, button))
        return entries, boxes



    def start_skipper(self, entries = [], boxes = []):
        self._thread = skipper.netflix_skipperino()
        try:
            for e in entries:
                if e[0] == "# of episodes" and isinstance(int(e[1].get()), int):
                    self._thread.total_episode = int(e[1].get())

                if e[0] == "Start frame" and isinstance(int(e[1].get()), int):
                    self._thread.start_time = int(e[1].get()) * 60

                if e[0] == "Duration" and isinstance(int(e[1].get()), int):
                    self._thread.duration = int(e[1].get()) * 60

        except:
            messagebox.showerror("Invalid", "Inputs not exceptable")
            return

        for b in boxes:
            if b[0] == "recap" and b[1].get():
                self._thread.recap = True
            if b[0] == "intro" and b[1].get():
                self._thread.intro = True
        
        if self._thread.is_alive():
            self.stop() 
        
        self._thread.start()
        self.status_update()
        

    
if __name__=="__main__":
    App().mainloop()