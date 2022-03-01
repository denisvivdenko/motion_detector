import cv2
from src.object_highlighter import ObjectHighlighter
from src.screen import Screen
from src.motion_detector import MotionDetector
from src.alarm import Alarm
from datetime import datetime
import numpy as np


def skip_frames(video, amount: int):
    for _ in range(amount):
        video.read()
    return video

if __name__ == "__main__":
    video = cv2.VideoCapture("src\\videos\\camera_1.mp4")
    alarm = Alarm("src\\alarms\\Alarm-ringtone.mp3")
    motion_detector = MotionDetector(guassian_blur_parameters=(3, 3), 
                                        threshold=30,
                                        erosion_kernel_shape=(1, 1), 
                                        dilation_kernel_shape=(1, 1),
                                        erosion_iterations=3,
                                        dilation_iterations=3)
    screen = Screen()
    ret, frame = video.read()
    previous_frame = motion_detector.process_frame(frame)
    index = 0
    print(previous_frame.shape)
    output = cv2.VideoWriter('test_1.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 12, (previous_frame.shape[1], previous_frame.shape[0]), 0)
    while video.isOpened():
        skip_frames(video, 4)
        recieved, current_frame = video.read()
        if not recieved:
            video.release()
            break

        processed_current_frame = motion_detector.process_frame(current_frame)
        difference_frame = motion_detector.compute_difference_frame(previous_frame, processed_current_frame)

        output.write(difference_frame)

        if motion_detector.has_movement(difference_frame, area_threshold=10**4):
            alarm.turn_on(1)

        previous_frame = processed_current_frame
    output.release()
        
# moving_objects = motion_detector.detect_movement(previous_frame, processed_current_frame)
# object_highlighter = ObjectHighlighter(current_frame, moving_objects)
# print(object_highlighter.get_result())
# cv2.imwrite(f"{np.sum(object_highlighter.get_result())}.jpeg", object_highlighter.get_result())
# highlighted_frame = screen.draw_cirle(current_frame, (100, 100), 10)
# screen.save_frame(highlighted_frame)