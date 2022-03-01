from collections import namedtuple
import time
from datetime import date, datetime
from typing import List, Tuple

import cv2
import numpy as np
import pandas as pd

DetectedObject = namedtuple("DetectedObject", ["x", "y", "height", "width"])

class MotionDetector:
    def __init__(self, guassian_blur_parameters: Tuple[int, int] = (3, 3)) -> None:
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
        self.guassian_blur_parameters = guassian_blur_parameters

    def has_movement(self, previous_frame: np.ndarray, current_frame: np.ndarray, area_threshold: int) -> bool:
        """
            Checks if there is movements captured between two frames.

            Parameters:
                prevous_frame (np.ndarray): frame processed by process_frame() method.
                current_frame (np.ndarray): frame processed by process_frame() method.

            Returns:
                True | False
        """
        difference_frame = self.compute_difference_frame(previous_frame, current_frame)
        return np.sum(difference_frame > 0) > area_threshold

    def detect_movement(self, previous_frame: np.ndarray, current_frame: np.ndarray) -> List[DetectedObject]: # TODO
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
        processed_frame = cv2.GaussianBlur(processed_frame, self.guassian_blur_parameters, 0)
        return processed_frame
    
    def remove_noise(self, frame: np.ndarray, threshold: int = 30, kernel_shape: Tuple[int, int] = (3, 3)) -> np.ndarray:
        """
            Removes noise from image.
            Apply threshold, erosion, dilation.

            Parameters:
                threshold (int): cv2.threshold method parameter.
                kernel_shape (Tuple[int, int]): consists of odd numbers (3, 5, 7), used for erode and dilate methods.
        """
        kernel = np.ones(kernel_shape, np.uint8)
        processed_frame = cv2.threshold(frame, threshold, 255, cv2.THRESH_BINARY)[1]
        processed_frame = cv2.erode(processed_frame, kernel, iterations=2)
        processed_frame = cv2.dilate(processed_frame, kernel, iterations=2)
        return processed_frame

    def compute_difference_frame(self, frame_1: np.ndarray, frame_2: np.ndarray) -> np.ndarray:
        """
            Computes difference between two frames and removes noise.
        """
        difference_frame = cv2.absdiff(frame_1, frame_2)
        return self.remove_noise(difference_frame)

