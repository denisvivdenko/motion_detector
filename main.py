import cv2
from src.screen import Screen
from src.motion_detector import MotionDetector
from src.alarm import Alarm
from datetime import datetime

import time

if __name__ == "__main__":
    alarm = Alarm("src\\alarms\\Alarm-ringtone.mp3")
    motion_detector = MotionDetector(contour_threshold=10**3)
    screen = Screen()
    previous_frame = motion_detector.process_frame(screen.take_screenshot())
    while True:
        current_frame = screen.take_screenshot()
        processed_current_frame = motion_detector.process_frame(current_frame)
        if motion_detector.has_movement(previous_frame, processed_current_frame):
            alarm.turn_on(1)
            moving_objects = motion_detector.detect_movement(previous_frame, processed_current_frame)

            # highlighted_frame = screen.draw_cirle(current_frame, (100, 100), 10)
            # screen.save_frame(highlighted_frame)
        previous_frame = processed_current_frame
        # time.sleep(1)
