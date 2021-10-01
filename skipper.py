from PIL import Image
from datetime import datetime, timedelta
import threading
import pyautogui
import time
import math
 




class netflix_skipperino(threading.Thread):
    
    def __init__(self, width, height, confidence = 0.7):
        threading.Thread.__init__(self, daemon=True)
        self._status = "Dead"
        self._start_time = 0
        self._duration = 0
        self._total_episode = 0
        self._intro = False
        self._recap = False
        self._button_path = {}
        self._region = (width//2, height//2, width//2, height//2)
        self._conf = confidence
        self._halt = threading.Event()

    @property
    def start_time(self):
        return self._start_time
    
    @start_time.setter
    def start_time(self, start):
        self._start_time = start

    @property
    def duration(self):
        return self._duration
    
    @duration.setter
    def duration(self, duration):
        self._duration = duration
    
    @property
    def total_episode(self):
        return self._total_episode
    
    @total_episode.setter
    def total_episode(self, total_episode):
        self._total_episode = total_episode

    @property
    def intro(self):
        return self._intro
    
    @intro.setter
    def intro(self, enable):
        self._intro = enable

    @property
    def recap(self):
        return self._recap
    
    @recap.setter
    def recap(self, enable):
        self._recap= enable

    
    @property
    def status(self):
        return self._status


    def setup_path(self):
        if self._intro:
            self._button_path["intro"] = "resource/intro.png"
        
        if self._recap:
            self._button_path["recap"] = "resource/recap.png"

        self._button_path["skip"] = "resource/next.png"

    def pause(self):
        self._halt.set()
        

    def run(self):       
        start = time.time()
        try:
            self._status="Alive"
            self.task()
        finally:
            print(time.time() - start)
            self._status="Dead"
            
    
    def task(self):
        count, is_killed = self._total_episode, False
        x, y = None, None
        self.setup_path()
        while count > 0 and not is_killed:
            if self._intro or self._recap:          
                time_spent = self.begin_skipper()
                is_killed = self._halt.wait(self._start_time - time_spent)
            else:
                is_killed = self._halt.wait(self._start_time)
            self.end_skipper()    
            count -= 1


    def begin_skipper(self):
        attempt = 10
        is_killed = False
        start = datetime.now()
        x, y = None, None
        while attempt > 0 and not is_killed:
            try:
                if self._intro:
                    button = pyautogui.locateOnScreen(self._button_path["recap"], confidence = self._conf, region = self._region)
                    x, y = pyautogui.center(button)
                    pyautogui.click(x,y)
                
                if self._recap:
                    button = pyautogui.locateOnScreen(self._button_path["recap"], confidence = self._conf, region = self._region)
                    x, y = pyautogui.center(button)
                    pyautogui.click(x,y)
            except:
                print("can not center button")
            attempt +=1
            is_killed = self._halt.wait(2)    

        return (10*2) # stop 10 times of 2 second
    

    def end_skipper(self):
        x,y = None, None
        sleep_interval = math.ceil((self._duration - self._start_time)/10)
        attempt = 10 
        is_killed = False
        while attempt > 0 and not is_killed:
            try:
                button = pyautogui.locateOnScreen(self._button_path["skip"], confidence = self._conf, region = self._region)
                x, y = pyautogui.center(button)
                pyautogui.click(x,y)
                return
            except:
                print("can not center skip button")
            attempt-= 1
            # print("tryin:", attempt)
            is_killed = self._halt.wait(sleep_interval)
