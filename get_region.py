from PIL import Image
import pyautogui
import time
import sys



while True:
    print(pyautogui.position())
    if input("found:") == "y":
        q = "n"
        while q != "y":
            x = input("x:")
            y = input("y:")
            wid = input("width:")
            hght = input("height:")
            im = pyautogui.screenshot("recap_15.png",region = (x,y, wid, hght)) 
            im.show()
            q = input("finished ?")
            im.close()
    else:
        time.sleep(4)


    

