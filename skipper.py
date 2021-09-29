from PIL import Image
from datetime import datetime, timedelta
import threading
import pyautogui
import time
import math
 




class netflix_skipperino(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self._status = "Dead"
        self._start_time = 0
        self._duration = 0
        self._total_episode = 0
        self._intro = False
        self._recap = False
        self._button_path = {}
        self._region_map = {}
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
            self._button_path["recap"] = "resource/recap_15.png"

        self._button_path["skip"] = "resource/next_15.png"

    def pause(self):
        self._halt.set()

    #Setup region for faster detection
    def setup_region(self, recap_region = (), skip_region = (), intro_region = ()):
        if recap_region:
            self._region_map["recap"] =  recap_region
        if skip_region:
            self._region_map["skip"] = skip_region



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
            if self._intro:          
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
            if self.region_map["recap"]:
                button_location = pyautogui.locateOnScreen(self._button_path["recap"], confidence = 0.9, region = self.region_map["recap"])
                x,y = pyautogui.center(button_location)

            else:
                x, y = pyautogui.locateCenterOnScreen(self._button_path["recap"])

            if x and y:
                pyautogui.click(x,y)
                diff = datetime.now() - start
                return diff.total_seconds() 

            attempt +=1
            is_killed = self._halt.wait(2)

        return (10*2) # stop 10 times of 2 second
    

    def end_skipper(self):
        x,y = None, None
        sleep_interval = math.ceil((self._duration - self._start_time)/10)
        # print("snooze:",sleep_interval)
        attempt = 10 
        is_killed = False
        while attempt > 0 and not is_killed:
            if "skip" in self._region_map:
                x, y = pyautogui.locateCenterOnScreen(self._button_path["skip"], confidence=0.9, region = self.region_map["skip"])
            
            else:
                button = pyautogui.locateOnScreen(self._button_path["skip"], confidence = 0.6)
                if button:
                    try:
                        x, y = pyautogui.center(button)
                    except:
                        print("can not center skip button")
            
            if x and y:
                pyautogui.click(x,y)
                print("Skipped!")
                return

            attempt-= 1
            is_killed = self._halt.wait(sleep_interval)
