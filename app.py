import skipper
import region_locator
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
import threading
import os.path

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

        self._btn_frame = tk.Frame(self)
        
        self._start_btn = tk.Button(
            self._btn_frame, 
            width = 5,
            relief = tk.RIDGE,
            # fg='#E50914',
            font = Font_tuple,
            text='Start',
            command = lambda e=self._ents, b=self._bxes : self.start_skipper(e,b))

        self._stop_btn = tk.Button(
            self._btn_frame, 
            width = 5,
            relief = tk.RIDGE,
            font = Font_tuple,
            # fg='#E50914', 
            text='Stop', 
            command= self.stop)
        
        self._locator_btn = tk.Button(
            self._btn_frame,
            width = 7,
            relief = tk.RIDGE,
            fg='#E50914',
            font = Font_tuple,
            text = 'Locator' 
        )
        
        self._locator_btn.bind("<Button>", lambda e: region_locator.region_locator_GUI(self))
        
        
        self._status_bar.pack(pady = 15, anchor=CENTER)
        self._start_btn.pack(side = LEFT, anchor=CENTER)
        self._locator_btn.pack(side = LEFT, anchor=CENTER)
        self._stop_btn.pack(side = LEFT, anchor=CENTER)
        self._btn_frame.pack()
        
    # #check if directory exist and if image for condition exist
    def validate_img_path(self, boxes):
        if os.path.isdir("resource"):
            if boxes[0][1].get() and not os.path.exists("resource/recap.png"):
                raise ValueError('Recap img not exist')

            if boxes[1][1].get() and not os.path.exists("resource/intro.png"):
                raise ValueError('Intro img not exist')

            if not os.path.isfile("resource/next.png"):
                raise ValueError('Skip img not exist')
        else:
            raise ValueError('Directory not exist')
            
    #Update status of tool
    def status_update(self):
        status = self._thread.status
        self._status_bar.config(text = status)
        self._status_bar.after(1000, self.status_update)


    def stop(self):
        if self._thread and self._thread.is_alive():
            self._thread.pause()
            self._thread.join()
        else:
            messagebox.showerror("Error", "Tool not running")


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
            bool_var = BooleanVar()
            frame = tk.Frame(self)
            button = Checkbutton(
                frame, 
                text=box, 
                relief = SUNKEN,
                font = Font_tuple, 
                variable=BooleanVar(), 
                width=5, 
                anchor = W)
            frame.pack(side=TOP, pady=5)
            button.pack()
            boxes.append((box, bool_var))
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
            messagebox.showerror("Invalid", "Input not exceptable")
            return

        for b in boxes:
            if b[0] == "recap" and b[1].get():
                self._thread.recap = True
            if b[0] == "intro" and b[1].get():
                self._thread.intro = True
        
        if self._thread.is_alive():
            self.stop() 
            
        try:
            self.validate_img_path(boxes)
            self._thread.start()
            self.status_update()
        except ValueError as err:
            messagebox.showerror("Error",err.args[0])

    
if __name__=="__main__":
    App().mainloop()
    