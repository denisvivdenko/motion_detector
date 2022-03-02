import json
from os import path
from src.video_motion_detector import VideoMotionDetector

if __name__ == "__main__":
    input_video = "src\\videos\\camera_1.mp4"
    with open("src\\parameters.json") as json_file:
        parameters = json.load(json_file)

    for model_parameters in parameters:    
        output_name = f"src\\videos\\outputs\\{str(model_parameters.items())}.avi"
        if path.isfile(output_name):
            continue

        video_motion_detector = VideoMotionDetector(input_video, model_parameters)
        video_motion_detector.save_output(output_name)
    