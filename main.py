from src.screen import Screen
from src.motion_detector import MotionDetector

if __name__ == "__main__":
    motion_detector = MotionDetector()
    screen = Screen()
    previous_frame = motion_detector.process_frame(screen.take_screenshot())
    while True:
        current_frame = motion_detector.process_frame(screen.take_screenshot())
        has_mootion = motion_detector.has_movement(previous_frame, current_frame)
        previous_frame = current_frame
