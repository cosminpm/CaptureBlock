import webbrowser
import time
import pyautogui
import os    

if __name__ == '__main__':
    webbrowser.open("https://twitter.com/cosminpm/status/1374518048367861768")
    time.sleep(2)
    img = pyautogui.screenshot()
    img.save('patata.png')
    os.system("taskkill /im chrome.exe /f")
    region=(0,0, 300, 400)
    