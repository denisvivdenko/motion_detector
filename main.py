import cv2
from src.object_highlighter import ObjectHighlighter
from src.screen import Screen
from src.motion_detector import MotionDetector
from src.alarm import Alarm
from datetime import datetime
import numpy as np
from src.utils import *

import time

if __name__ == "__main__":
    alarm = Alarm("src\\alarms\\Alarm-ringtone.mp3")
    motion_detector = MotionDetector(guassian_blur_parameters=(1, 1), 
                                        erosion_kernel_shape=(1, 1), 
                                        dilation_kernel_shape=(1, 1))
    screen = Screen()
    previous_frame = motion_detector.process_frame(screen.take_screenshot())
    index = 0
    while True:
        current_frame = screen.take_screenshot()
        processed_current_frame = motion_detector.process_frame(current_frame)
        difference_frame = motion_detector.compute_difference_frame(previous_frame, processed_current_frame)
        save_frame(difference_frame, index)
        index += 1
        if motion_detector.has_movement(difference_frame, area_threshold=10**4):
            alarm.turn_on(1)
            print(1)
        else:
            print(0)
        previous_frame = processed_current_frame
        time.sleep(0.1)

        
# moving_objects = motion_detector.detect_movement(previous_frame, processed_current_frame)
# object_highlighter = ObjectHighlighter(current_frame, moving_objects)
# print(object_highlighter.get_result())
# cv2.imwrite(f"{np.sum(object_highlighter.get_result())}.jpeg", object_highlighter.get_result())
# highlighted_frame = screen.draw_cirle(current_frame, (100, 100), 10)
# screen.save_frame(highlighted_frame)