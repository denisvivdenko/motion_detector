from typing import Any, Dict
import cv2

from src.motion_detector import MotionDetector

class VideoMotionDetector:
    def __init__(self, input_video: str, parameters: Dict[str, Any]) -> None:
        """
            Model for tunning parameters.
            It takes as input video and list of parameters for MotionDetector class.
            Writes output video to the specified path.
        """
        self.motion_detector = MotionDetector(**parameters)
        self.video = cv2.VideoCapture(input_video)

    def skip_frames(self, video, amount: int):
        for _ in range(amount):
            video.read()
        return video

    def save_output(self, output_path: str) -> None:
        recieved, frame = self.video.read()
        previous_frame = self.motion_detector.process_frame(frame)
        frame_size = (previous_frame.shape[1], previous_frame.shape[0])
        output = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc('M','J','P','G'), 
                                    fps=12, frameSize=frame_size, isColor=False)
        while self.video.isOpened():
            self.video = self.skip_frames(self.video, 4)
            recieved, current_frame = self.video.read()
            
            if not recieved:
                self.video.release()
                break

            processed_current_frame = self.motion_detector.process_frame(current_frame)
            difference_frame = self.motion_detector.compute_difference_frame(previous_frame, processed_current_frame)
            output.write(difference_frame)
            previous_frame = processed_current_frame
        output.release()

