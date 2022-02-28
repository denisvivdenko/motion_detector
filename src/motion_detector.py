import time
from datetime import datetime

import cv2
import numpy as np
import pandas as pd

class MotionDetector:
    def __init__(self) -> None:
        """
            Detects motion between frames.
            
            Usage example:

                motion_detector = MotionDetector()
                frame_1 = motion_detector.process_frame(frame_1)
                frame_2 = motion_detector.process_frame(frame_2)
                motion = motion_detector.has_movement(frame_1, frame_2)
        """
        pass

    def has_movement(self, previous_frame: np.ndarray, current_frame: np.ndarray,
                            contour_threshold: int = 10**5) -> bool:
        """
            Checks if there is movements captured between two frames.

            Parameters:
                prevous_frame (np.ndarray): frame processed by process_frame() method.
                current_frame (np.ndarray): frame processed by process_frame() method.
                countour_threshold (int): threshold for contour which identifies movement in difference frame.

            Returns:
                True | False
        """
        difference = cv2.absdiff(previous_frame, current_frame)
        threshold_frame = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)[1]
        threshold_frame = cv2.dilate(threshold_frame, None, iterations=2)
        contours, _ = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return any([cv2.contourArea(contour)> contour_threshold for contour in contours])

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
            Process captured frame to compare them in has_movement() method.
            Convert to Black&White and apply Gaussian blur.

            Parameters:
                frame (np.ndarray): input frame

            Returns:
                frame (np.ndarray)
        """
        processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.GaussianBlur(processed_frame, (21, 21), 0)
   

