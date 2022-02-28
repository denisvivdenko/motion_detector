from typing import Tuple
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
    
    def draw_cirle(self, frame: np.ndarray, center: Tuple[int, int], radius: int) -> np.ndarray:
        """
            Draws circle on given image.

            Parameters:
                frame (np.ndarray): image
                center (Tuple[int, int]): coordinates of circle
                radius (int): circle radius

            Returns:
                image (np.ndarray)
        """
        return cv2.circle(frame, center, radius, (0, 0, 255), 3)

    def save_frame(self, frame: np.ndarray,) -> None:
        cv2.imwrite(f"detected{np.sum(frame)}.png", frame)


if __name__ == "__main__":
    screen = Screen()
    cv2.imwrite("screen.png", screen.take_screenshot())
