from collections import namedtuple
import time
from datetime import datetime
from typing import List, Tuple

import cv2
import numpy as np
import pandas as pd

DetectedObject = namedtuple("DetectedObject", ["x", "y", "height", "width"])

class MotionDetector:
    def __init__(self, contour_threshold: int) -> None:
        """
            Detects motion between frames.
            
            Usage example:

                motion_detector = MotionDetector()
                frame_1 = motion_detector.process_frame(frame_1)
                frame_2 = motion_detector.process_frame(frame_2)
                motion = motion_detector.has_movement(frame_1, frame_2)

            Parameters:
                contour_threshold (int): countour threshold length
        """
        self.contour_threshold = contour_threshold

    def has_movement(self, previous_frame: np.ndarray, current_frame: np.ndarray) -> bool:
        """
            Checks if there is movements captured between two frames.

            Parameters:
                prevous_frame (np.ndarray): frame processed by process_frame() method.
                current_frame (np.ndarray): frame processed by process_frame() method.

            Returns:
                True | False
        """
        contours = self._detect_difference_contours(previous_frame, current_frame)
        return any([cv2.contourArea(contour)> self.contour_threshold for contour in contours])

    def detect_movement(self, previous_frame: np.ndarray, current_frame: np.ndarray) -> List[DetectedObject]:
        """
            Detects moving objects coordinates.

            Parameters:
                prevous_frame (np.ndarray): frame processed by process_frame() method.
                current_frame (np.ndarray): frame processed by process_frame() method.

            Returns:
                List of DetectedObjects(x, y, height, width)
        """
        contours = self._detect_difference_contours(previous_frame, current_frame)
        detected_objects = []
        for contour in contours:
            if cv2.contourArea(contour) > self.contour_threshold:
                detected_objects.append(DetectedObject(*cv2.boundingRect(contour)))
        return detected_objects
    
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
   
    def _detect_difference_contours(self, frame_1: np.ndarray, frame_2: np.ndarray) -> List:
        """
            Detects contours between two processed frames.
        """
        difference = cv2.absdiff(frame_1, frame_2)
        threshold_frame = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)[1]
        threshold_frame = cv2.dilate(threshold_frame, None, iterations=2)
        contours, _ = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours
