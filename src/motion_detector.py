from collections import namedtuple
from typing import List, Tuple

import cv2
import numpy as np

DetectedObject = namedtuple("DetectedObject", ["x", "y", "height", "width"])

class MotionDetector:
    def __init__(self, guassian_blur_parameters: Tuple[int, int] = (1, 1),
                    threshold: int = 30,
                    erosion_kernel_shape: Tuple[int, int] = (1, 1),
                    dilation_kernel_shape: Tuple[int, int] = (1, 1),
                    erosion_iterations: int = 1,
                    dilation_iterations: int = 1
        ) -> None:
        """
            Detects motion between frames.
            
            Usage example:

      # TODO
            Parameters:
                contour_threshold (int): countour threshold length
        """
        self.guassian_blur_parameters = guassian_blur_parameters
        self.threshold = threshold
        self.erosion_kernel_shape = erosion_kernel_shape
        self.dilation_kernel_shape = dilation_kernel_shape
        self.erosion_iterations = erosion_iterations
        self.dilation_iterations = dilation_iterations

    def has_movement(self, difference_frame: np.ndarray, area_threshold: int) -> bool:
        """
            Checks if there is movements captured between two frames.

            Parameters:
                difference_frame (np.ndarray): difference betweem frame_1, frame_2

            Returns:
                True | False
        """
        return np.sum(difference_frame > 0) > area_threshold

    # TODO
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
        processed_frame = cv2.GaussianBlur(processed_frame, self.guassian_blur_parameters, 0)
        return processed_frame
    
    def remove_noise(self, frame: np.ndarray, threshold: int = 30) -> np.ndarray:
        """
            Removes noise from image.
            Apply threshold, erosion, dilation.

            Parameters:
                threshold (int): cv2.threshold method parameter.
                kernel_shape (Tuple[int, int]): consists of odd numbers (3, 5, 7), used for erode and dilate methods.
        """
        erosion_kernel = np.ones(self.erosion_kernel_shape, np.uint8)
        dilation_kernel = np.ones(self.dilation_kernel_shape, np.uint8)
        processed_frame = cv2.threshold(frame, threshold, 255, cv2.THRESH_BINARY)[1]
        processed_frame = cv2.erode(processed_frame, erosion_kernel, iterations=self.erosion_iterations)
        processed_frame = cv2.dilate(processed_frame, dilation_kernel, iterations=self.dilation_iterations)
        return processed_frame

    def compute_difference_frame(self, frame_1: np.ndarray, frame_2: np.ndarray) -> np.ndarray:
        """
            Computes difference between two frames and removes noise.
        """
        difference_frame = cv2.absdiff(frame_1, frame_2)
        difference_frame = self.remove_noise(difference_frame, threshold=self.threshold)
        return difference_frame

