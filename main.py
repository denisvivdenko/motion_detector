from src.screen import Screen
from src.motion_detector import MotionDetector
from src.alarm import Alarm

import time

if __name__ == "__main__":
    alarm = Alarm("src\\alarms\\Alarm-ringtone.mp3")
    motion_detector = MotionDetector()
    screen = Screen()
    previous_frame = motion_detector.process_frame(screen.take_screenshot())
    while True:
        current_frame = motion_detector.process_frame(screen.take_screenshot())
        has_mootion = motion_detector.has_movement(previous_frame, current_frame)
        if has_mootion:
            alarm.turn_on(2)
        previous_frame = current_frame
        time.sleep(1)
