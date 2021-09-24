from PIL import Image
from datetime import datetime, timedelta
import threading
import pyautogui
import time


class netflix_skipperino(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self._start_time = 0
        self._duration = 0
        self._total_episode = 0
        self._intro = False
        self._recap = False
        self._resolution = 0
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
    def resolution(self):
        return self._resolution
    
    @resolution.setter
    def resolution(self, dimension):
        self._resolution = dimension
    

    def setup_path(self):
        self._button_path["skip"] = "next_15.png"
        self._button_path["recap"] = "recap_15.png"


    def pause(self):
        self._halt.set()

    #Setup region for faster detection
    def setup_region(self, recap_region = (), skip_region = (), intro_region = ()):
        if recap_region:
            self._region_map["recap"] =  recap_region
        if skip_region:
            self._region_map["skip"] = skip_region



    def run(self):       
        try:
            print("Starting...")
            self.task()
        finally:
            print("Stopping skipper...")
    
    def task(self):
        count = self._total_episode
        x, y = None, None
        self.setup_path()
        while count > 0:
            if self._intro:          
                time_spent = self.begin_skipper()
                is_killed = self._halt.wait(self._start_time - time_spent)
            else:
                is_killed = self._halt.wait(self._start_time)
            if is_killed:
                break
            self.end_skipper()    
            count -= 1

    def begin_skipper(self):
        attempt, is_killed = 0, False

        start = datetime.now()
        x, y = None, None
        while attempt < 4 and not is_killed:
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
        return 0
    

    def end_skipper(self):
        x,y = None, None
        attempt, is_killed = 6, False
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
            is_killed = self._halt.wait(5)




# print(button7location)

    # im3 = pyautogui.screenshot(region=(780,946, width, height))
    # im3.show()
    # if (input("save:") == "y"):
    #     im3.save("next_button_half_tab.png")
    #     break
    # print(pyautogui.position())
    # time.sleep(5) 
# pyautogui.position()
# pos = imagesearch("edit.png")
# if pos[0] != -1:
#     print("position : ", pos[0], pos[1])
# else:
#     print(pos)
#     print("image not found")

# time.monotonic() ? in case time clock is changed