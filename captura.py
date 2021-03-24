import pyautogui

if __name__ == '__main__':
    image = pyautogui.screenshot()
    image.save("patata.png")