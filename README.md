# Netflix xkipper


Netflix xkipper is a python GUI tool, a crucial aid that helps the bingers
who just want to sit back, relax, and enjoy their favourite shows hand-free!  


## Guides
1. Use locator to spawn a locator tool to calibrate the dimension - **x, y, width, height** - of the button image - **intro, recap, skip** - with the following formula:
    - x = x_top_left
    - y = y_top_left
    - width = x_bottom_right - x_top_left
    - height = y_bottom_right - y_top_right  

2. Use screenshot button of locator tool to take a snap shot of the button and save it in the resouce folder under recap.png for recap, intro.png for intro, and skip.png for skip.

3. Go back to the xkipper tool
    1. Enter the estimate time of an epsiode and round up to closet minute i.e 23:30 -> 24 minutes. 
    2. Enter the approximate time where the episode end before the outro under the same rule.  
    3. Enter the total episodes to binge
    4. Click start and enjoy the marathon!

4. Warning! If you stop midway, you will need to stop the tool and redo the math for **Start frame** and **Duration**

## Library

Netflix xkipper utilizes the advantage of python's massive open source library to envelop itself:
- [Tkinter] - An interface for python's GUI tk toolkit
- [threading] - A thread interface that built on top of _thread module to spawn the xkipper
- [pyautogui] - An interface to automate mouse and keyboard interactions with image detection

    
## Installation

Netflix xkipper require [Python 3] and above to run.

1. Go to [release](https://github.com/Thisausername99/netflix_skipper/releases) and download the dist zip file (use latest version)

2. Unpack the zip file and run **app.exe**


## License

- MIT

- <div>Icons made by <a href="https://www.flaticon.com/authors/bqlqn" title="bqlqn">bqlqn</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

