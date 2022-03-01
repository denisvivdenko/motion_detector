import cv2
from src.object_highlighter import ObjectHighlighter
from src.screen import Screen
from src.motion_detector import MotionDetector
from src.alarm import Alarm
from datetime import datetime
import numpy as np

from src.video_motion_detector import VideoMotionDetector

if __name__ == "__main__":
    input_video = "src\\videos\\camera_1.mp4"
    parameters = {
        "guassian_blur_parameters": (3, 3), 
        "threshold": 30,
        "erosion_kernel_shape": (1, 1), 
        "dilation_kernel_shape": (1, 1),
        "erosion_iterations": 3,
        "dilation_iterations": 3
    }

    video_motion_detector = VideoMotionDetector(input_video, parameters)
    video_motion_detector.save_output("src\\videos\\outputs\\test_1.avi")
    