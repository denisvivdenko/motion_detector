import pyautogui
import cv2
import numpy as np

class Screen:
    def take_screenshot(self) -> np.ndarray:
        """
            Takes screen screenshot of your screen.
            Example:
                screen = Screen()
                image = screen.take_screenshot()

            Returns:
                image (np.ndarray)
        """
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


if __name__ == "__main__":
    screen = Screen()
    cv2.imwrite("screen.png", screen.take_screenshot())
