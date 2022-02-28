from doctest import script_from_examples
from turtle import screensize
import pyautogui
import cv2
import numpy as np

class Screen:
    def take_screenshot(self) -> np.array:
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


if __name__ == "__main__":
    screen = Screen()
    screen.take_screenshot()
    # cv2.imshow(screen.take_scenshot())