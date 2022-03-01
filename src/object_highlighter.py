from typing import List
import numpy as np
import cv2
from src.motion_detector import DetectedObject

class ObjectHighlighter:
    def __init__(self, frame: np.ndarray, objects: List[DetectedObject]):
        """
            Draws red circle on given frame.

            Example:
                object_highlighter = ObjectHighlighter(current_frame, moving_objects)
                cv2.imwrite("img.jpeg", object_highlighter.get_result())

            Parameters:
                frame (np.ndarray): essential frame.
                objects (List[DetectedObject]: contains x and y coordinates, width and height)
        """
        self._highlighted_frame = self._highlight_objects(frame, objects)

    def _highlight_objects(self, frame: np.ndarray, objects: List[DetectedObject]) -> np.ndarray:
        highlighted_frame = frame.copy()
        for object in objects:
            center = (int(object.x + object.width / 2), int(object.y + object.height / 2))
            radius = int(min(object.width, object.height) / 2)
            highlighted_frame = cv2.circle(highlighted_frame, center, radius, (0, 0, 255), 3)
        return highlighted_frame

    def get_result(self) -> np.ndarray:
        return self._highlighted_frame